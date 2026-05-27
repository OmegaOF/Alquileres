from datetime import date
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.alquileres.models import Alquiler
from modules.cobros.models import CobroMensual, DetalleCobroMensual
from modules.cuartos.models import Cuarto
from modules.egresos.models import EgresoCasa
from modules.inquilinos.models import Inquilino
from modules.periodos.models import PeriodoMensual
from modules.servicios_mensuales.models import ServicioMensual


def list_items(db: Session): return db.query(CobroMensual).all()
def get_item(db: Session, item_id: int): return db.get(CobroMensual, item_id)

def recalcular_cobro(db: Session, id_cobro: int):
    from modules.pagos.models import Pago
    cobro = db.get(CobroMensual, id_cobro)
    if not cobro: return
    total_pagado = sum(Decimal(p.monto_pagado) for p in db.query(Pago).filter(Pago.id_cobro == id_cobro, Pago.estado == "valido").all())
    cobro.total_pagado = total_pagado
    cobro.saldo_pendiente = Decimal(cobro.total_a_pagar) - total_pagado
    if cobro.saldo_pendiente <= 0: cobro.estado = "pagado"
    elif total_pagado > 0: cobro.estado = "parcial"
    elif cobro.fecha_limite_pago and cobro.fecha_limite_pago < date.today(): cobro.estado = "atrasado"
    else: cobro.estado = "pendiente"
    db.commit(); db.refresh(cobro)

def create_item(db: Session, payload):
    d = payload.model_dump(exclude_unset=True)
    i = CobroMensual(**d)
    i.total_a_pagar = Decimal(i.monto_alquiler) + Decimal(i.monto_servicios) + Decimal(i.deuda_anterior) + Decimal(i.recargos) - Decimal(i.descuentos)
    i.total_pagado = Decimal("0"); i.saldo_pendiente = i.total_a_pagar; i.estado = "pendiente"
    db.add(i); db.commit(); db.refresh(i); return i

def update_item(db: Session, item, payload):
    for k,v in payload.model_dump(exclude_unset=True).items(): setattr(item,k,v)
    item.total_a_pagar = Decimal(item.monto_alquiler)+Decimal(item.monto_servicios)+Decimal(item.deuda_anterior)+Decimal(item.recargos)-Decimal(item.descuentos)
    db.commit(); recalcular_cobro(db,item.id_cobro); db.refresh(item); return item

def delete_item(db: Session, item): db.delete(item); db.commit()

def generar_periodo(db: Session, id_periodo: int, registrado_por: int):
    periodo = db.get(PeriodoMensual, id_periodo)
    if not periodo: raise HTTPException(404, "Periodo no existe")
    if periodo.estado == "cerrado": raise HTTPException(400, "Periodo cerrado")
    r={"id_periodo":id_periodo,"cobros_creados":0,"cobros_omitidos":0,"egresos_creados":0,"errores":[]}
    activos = db.query(Alquiler).filter(Alquiler.estado=="activo").all()
    for a in activos:
        if db.query(CobroMensual).filter(CobroMensual.id_periodo==id_periodo,CobroMensual.id_alquiler==a.id_alquiler).first(): r["cobros_omitidos"]+=1; continue
        cuarto=db.get(Cuarto,a.id_cuarto); inq=db.get(Inquilino,a.id_inquilino)
        if not cuarto or not inq: r["errores"].append(f"alquiler {a.id_alquiler} sin cuarto/inquilino"); continue
        deuda=sum(Decimal(c.saldo_pendiente) for c in db.query(CobroMensual).filter(CobroMensual.id_alquiler==a.id_alquiler,CobroMensual.saldo_pendiente>0,CobroMensual.id_periodo!=id_periodo).all())
        sm=db.query(ServicioMensual).filter(ServicioMensual.id_periodo==id_periodo,ServicioMensual.id_cuarto==a.id_cuarto,ServicioMensual.responsable_pago=="inquilino").all()
        monto_serv=sum(Decimal(x.monto) for x in sm)
        dia=min(max(a.dia_pago,1),28)
        limite=date(periodo.anio,periodo.mes,dia)
        cobro=CobroMensual(id_periodo=id_periodo,id_alquiler=a.id_alquiler,id_casa=cuarto.id_casa,id_cuarto=cuarto.id_cuarto,id_inquilino=inq.id_inquilino,monto_alquiler=a.monto_alquiler,monto_servicios=monto_serv,deuda_anterior=deuda,descuentos=0,recargos=0,total_a_pagar=Decimal(a.monto_alquiler)+monto_serv+deuda,total_pagado=0,saldo_pendiente=Decimal(a.monto_alquiler)+monto_serv+deuda,fecha_limite_pago=limite,estado="pendiente")
        db.add(cobro); db.flush()
        db.add(DetalleCobroMensual(id_cobro=cobro.id_cobro,tipo_concepto="alquiler",concepto="Alquiler mensual",monto=a.monto_alquiler,descripcion="Renta"))
        for s in sm: db.add(DetalleCobroMensual(id_cobro=cobro.id_cobro,tipo_concepto="servicio",concepto=f"Servicio {s.id_servicio}",monto=s.monto,id_servicio_mensual=s.id_servicio_mensual,descripcion=s.observacion))
        r["cobros_creados"]+=1
    # egresos desde servicios propietario o cuarto libre/sin alquiler activo
    servicios=db.query(ServicioMensual).filter(ServicioMensual.id_periodo==id_periodo).all()
    for s in servicios:
        if s.responsable_pago!="propietario":
            if s.id_cuarto and not db.query(Alquiler).filter(Alquiler.id_cuarto==s.id_cuarto,Alquiler.estado=="activo").first():
                pass
            else:
                continue
        if db.query(EgresoCasa).filter(EgresoCasa.id_servicio_mensual==s.id_servicio_mensual).first():
            continue
        db.add(EgresoCasa(id_casa=s.id_casa,id_periodo=s.id_periodo,id_cuarto=s.id_cuarto,id_servicio_mensual=s.id_servicio_mensual,concepto=f"Servicio mensual {s.id_servicio}",categoria="servicio",monto=s.monto,registrado_por=registrado_por))
        r["egresos_creados"]+=1
    db.commit(); return r
