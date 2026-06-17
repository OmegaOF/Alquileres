from datetime import date
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.alquileres.models import Alquiler
from modules.alquileres.utils import alquiler_del_cuarto_en_periodo
from modules.cobros.models import CobroMensual, DetalleCobroMensual
from modules.cuartos.models import Cuarto
from modules.egresos.models import EgresoCasa
from modules.inquilinos.models import Inquilino
from modules.periodos.models import PeriodoMensual
from modules.periodos.utils import require_periodo_abierto
from modules.servicios_mensuales.models import ServicioMensual


def list_items(db: Session): return db.query(CobroMensual).all()
def get_item(db: Session, item_id: int): return db.get(CobroMensual, item_id)

def detalles_cobro(db: Session, id_cobro: int):
    cobro = db.get(CobroMensual, id_cobro)
    if not cobro: raise HTTPException(404, "Cobro no existe")
    return db.query(DetalleCobroMensual).filter(DetalleCobroMensual.id_cobro == id_cobro).all()

def recalcular_cobro(db: Session, id_cobro: int):
    from modules.pagos.models import Pago
    cobro = db.get(CobroMensual, id_cobro)
    if not cobro: return
    detalles = db.query(DetalleCobroMensual).filter(DetalleCobroMensual.id_cobro == id_cobro).all()
    cobro.monto_servicios = sum(Decimal(d.monto) for d in detalles if d.tipo_concepto == "servicio")
    cobro.total_a_pagar = Decimal(cobro.monto_alquiler) + Decimal(cobro.monto_servicios) + Decimal(cobro.deuda_anterior) + Decimal(cobro.recargos) - Decimal(cobro.descuentos)
    total_pagado = sum(Decimal(p.monto_pagado) for p in db.query(Pago).filter(Pago.id_cobro == id_cobro, Pago.estado == "valido").all())
    if Decimal(cobro.total_a_pagar) < total_pagado:
        raise HTTPException(400, "Existen pagos registrados que impiden reducir el total del cobro por debajo de lo pagado")
    cobro.total_pagado = total_pagado
    cobro.saldo_pendiente = Decimal(cobro.total_a_pagar) - total_pagado
    if cobro.saldo_pendiente <= 0: cobro.estado = "pagado"
    elif total_pagado > 0: cobro.estado = "parcial"
    elif cobro.fecha_limite_pago and cobro.fecha_limite_pago < date.today(): cobro.estado = "atrasado"
    else: cobro.estado = "pendiente"
    db.commit(); db.refresh(cobro)

def create_item(db: Session, payload):
    d = payload.model_dump(exclude_unset=True)
    require_periodo_abierto(db, d["id_periodo"])
    i = CobroMensual(**d)
    i.total_a_pagar = Decimal(i.monto_alquiler) + Decimal(i.monto_servicios) + Decimal(i.deuda_anterior) + Decimal(i.recargos) - Decimal(i.descuentos)
    i.total_pagado = Decimal("0"); i.saldo_pendiente = i.total_a_pagar; i.estado = "pendiente"
    db.add(i); db.commit(); db.refresh(i); return i

def update_item(db: Session, item, payload):
    require_periodo_abierto(db, item.id_periodo)
    try:
        for k,v in payload.model_dump(exclude_unset=True).items(): setattr(item,k,v)
        item.total_a_pagar = Decimal(item.monto_alquiler)+Decimal(item.monto_servicios)+Decimal(item.deuda_anterior)+Decimal(item.recargos)-Decimal(item.descuentos)
        db.flush(); recalcular_cobro(db,item.id_cobro); db.refresh(item); return item
    except Exception:
        db.rollback(); raise

def delete_item(db: Session, item):
    require_periodo_abierto(db, item.id_periodo)
    item.estado = "anulado"; db.commit()

def _servicios_inquilino_para_alquiler(db: Session, periodo: PeriodoMensual, alquiler: Alquiler):
    return db.query(ServicioMensual).filter(
        ServicioMensual.id_periodo == periodo.id_periodo,
        ServicioMensual.id_cuarto == alquiler.id_cuarto,
        ServicioMensual.responsable_pago == "inquilino",
        ServicioMensual.estado == "activo",
    ).all()

def generar_periodo(db: Session, id_periodo: int, registrado_por: int):
    periodo = require_periodo_abierto(db, id_periodo)
    r={"id_periodo":id_periodo,"cobros_creados":0,"cobros_omitidos":0,"egresos_creados":0,"errores":[]}
    alquileres = db.query(Alquiler).filter(Alquiler.fecha_inicio <= periodo.fecha_fin, (Alquiler.fecha_fin.is_(None)) | (Alquiler.fecha_fin >= periodo.fecha_inicio), Alquiler.estado != "cancelado").all()
    for a in alquileres:
        if db.query(CobroMensual).filter(CobroMensual.id_periodo==id_periodo,CobroMensual.id_alquiler==a.id_alquiler).first(): r["cobros_omitidos"]+=1; continue
        cuarto=db.get(Cuarto,a.id_cuarto); inq=db.get(Inquilino,a.id_inquilino)
        if not cuarto or not inq: r["errores"].append(f"alquiler {a.id_alquiler} sin cuarto/inquilino"); continue
        # protect against overlapping inconsistent rentals selecting a different occupant for the room
        if alquiler_del_cuarto_en_periodo(db, cuarto.id_cuarto, periodo).id_alquiler != a.id_alquiler:
            continue
        deuda=sum(Decimal(c.saldo_pendiente) for c in db.query(CobroMensual).filter(CobroMensual.id_alquiler==a.id_alquiler,CobroMensual.saldo_pendiente>0,CobroMensual.id_periodo!=id_periodo,CobroMensual.estado!="anulado").all())
        sm=_servicios_inquilino_para_alquiler(db, periodo, a)
        monto_serv=sum(Decimal(x.monto) for x in sm)
        dia=min(max(a.dia_pago,1),28)
        limite=date(periodo.anio,periodo.mes,dia)
        cobro=CobroMensual(id_periodo=id_periodo,id_alquiler=a.id_alquiler,id_casa=cuarto.id_casa,id_cuarto=cuarto.id_cuarto,id_inquilino=inq.id_inquilino,monto_alquiler=a.monto_alquiler,monto_servicios=monto_serv,deuda_anterior=deuda,descuentos=0,recargos=0,total_a_pagar=Decimal(a.monto_alquiler)+monto_serv+deuda,total_pagado=0,saldo_pendiente=Decimal(a.monto_alquiler)+monto_serv+deuda,fecha_limite_pago=limite,estado="pendiente")
        db.add(cobro); db.flush()
        db.add(DetalleCobroMensual(id_cobro=cobro.id_cobro,tipo_concepto="alquiler",concepto="Alquiler mensual",monto=a.monto_alquiler,descripcion="Renta"))
        for s in sm:
            nombre=s.servicio.nombre_servicio if s.servicio else f"Servicio {s.id_servicio}"
            if not db.query(DetalleCobroMensual).filter(DetalleCobroMensual.id_servicio_mensual==s.id_servicio_mensual).first():
                db.add(DetalleCobroMensual(id_cobro=cobro.id_cobro,tipo_concepto="servicio",concepto=nombre,monto=s.monto,id_servicio_mensual=s.id_servicio_mensual,descripcion=s.observacion))
        r["cobros_creados"]+=1
    servicios=db.query(ServicioMensual).filter(ServicioMensual.id_periodo==id_periodo,ServicioMensual.estado=="activo",ServicioMensual.responsable_pago=="propietario").all()
    for s in servicios:
        eg=db.query(EgresoCasa).filter(EgresoCasa.id_servicio_mensual==s.id_servicio_mensual).first()
        nombre=s.servicio.nombre_servicio if s.servicio else f"Servicio {s.id_servicio}"
        if eg:
            if eg.estado == "anulado": eg.estado="activo"
            eg.id_casa=s.id_casa; eg.id_periodo=s.id_periodo; eg.id_cuarto=s.id_cuarto; eg.concepto=nombre; eg.monto=s.monto; eg.metodo_pago=s.metodo_pago; eg.numero_comprobante=s.numero_comprobante; eg.observacion=s.observacion
            continue
        db.add(EgresoCasa(id_casa=s.id_casa,id_periodo=s.id_periodo,id_cuarto=s.id_cuarto,id_servicio_mensual=s.id_servicio_mensual,concepto=nombre,categoria="servicio",monto=s.monto,registrado_por=registrado_por,metodo_pago=s.metodo_pago,numero_comprobante=s.numero_comprobante,observacion=s.observacion,estado="activo"))
        r["egresos_creados"]+=1
    db.commit(); return r
