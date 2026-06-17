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
from modules.periodos.validators import require_periodo_abierto
from modules.servicios_mensuales.models import ServicioMensual
from modules.servicios_mensuales.service import recrear_distribuciones_servicio


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
    require_periodo_abierto(db, d["id_periodo"])
    i = CobroMensual(**d)
    i.total_a_pagar = Decimal(i.monto_alquiler) + Decimal(i.monto_servicios) + Decimal(i.deuda_anterior) + Decimal(i.recargos) - Decimal(i.descuentos)
    i.total_pagado = Decimal("0"); i.saldo_pendiente = i.total_a_pagar; i.estado = "pendiente"
    db.add(i); db.commit(); db.refresh(i); return i

def update_item(db: Session, item, payload):
    require_periodo_abierto(db, item.id_periodo)
    for k,v in payload.model_dump(exclude_unset=True).items(): setattr(item,k,v)
    item.total_a_pagar = Decimal(item.monto_alquiler)+Decimal(item.monto_servicios)+Decimal(item.deuda_anterior)+Decimal(item.recargos)-Decimal(item.descuentos)
    db.commit(); recalcular_cobro(db,item.id_cobro); db.refresh(item); return item

def delete_item(db: Session, item): require_periodo_abierto(db, item.id_periodo); item.estado="anulado"; db.commit()

def generar_periodo(db: Session, id_periodo: int, registrado_por: int):
    periodo = require_periodo_abierto(db, id_periodo)
    r={"id_periodo":id_periodo,"cobros_creados":0,"cobros_omitidos":0,"egresos_creados":0,"errores":[]}
    activos = db.query(Alquiler).filter(Alquiler.fecha_inicio<=periodo.fecha_fin, ((Alquiler.fecha_fin.is_(None)) | (Alquiler.fecha_fin>=periodo.fecha_inicio)), Alquiler.estado!="anulado").all()
    try:
      for a in activos:
        modalidad=a.modalidad_alquiler or "mensual"
        if modalidad=="diario" and not (periodo.fecha_inicio<=a.fecha_inicio<=periodo.fecha_fin):
          r["cobros_omitidos"]+=1; continue
        if db.query(CobroMensual).filter(CobroMensual.id_alquiler==a.id_alquiler).first() if modalidad=="diario" else db.query(CobroMensual).filter(CobroMensual.id_periodo==id_periodo,CobroMensual.id_alquiler==a.id_alquiler).first(): r["cobros_omitidos"]+=1; continue
        cuarto=db.get(Cuarto,a.id_cuarto); inq=db.get(Inquilino,a.id_inquilino)
        if not cuarto or not inq: r["errores"].append(f"alquiler {a.id_alquiler} sin cuarto/inquilino"); continue
        deuda=sum(Decimal(c.saldo_pendiente) for c in db.query(CobroMensual).filter(CobroMensual.id_alquiler==a.id_alquiler,CobroMensual.saldo_pendiente>0,CobroMensual.id_periodo!=id_periodo).all())
        dia=min(max(a.dia_pago,1),28); limite=date(periodo.anio,periodo.mes,dia)
        monto_alquiler=Decimal(a.total_alquiler_diario or a.monto_alquiler) if modalidad=="diario" else Decimal(a.monto_mensual or a.monto_alquiler)
        detalles=[DetalleCobroMensual(tipo_concepto="alquiler_diario" if modalidad=="diario" else "alquiler",concepto="Alquiler diario" if modalidad=="diario" else "Alquiler mensual",monto=monto_alquiler,descripcion="Servicios básicos incluidos" if modalidad=="diario" else "Renta mensual completa")]
        monto_serv=Decimal('0.00')
        if modalidad=="mensual":
          sm=db.query(ServicioMensual).filter(ServicioMensual.id_periodo==id_periodo,ServicioMensual.id_cuarto==a.id_cuarto,ServicioMensual.responsable_pago=="inquilino",ServicioMensual.estado=="activo").all()
          for s in sm:
            recrear_distribuciones_servicio(db,s); db.flush()
            if any(d.tipo_calculo=="manual_requerido" for d in s.distribuciones):
              r["errores"].append(f"Servicio {s.id_servicio_mensual} requiere distribución manual por cambio de inquilino en el periodo")
              continue
            for dist in [d for d in s.distribuciones if d.id_alquiler==a.id_alquiler and Decimal(d.monto_asignado)>0]:
              monto_serv+=Decimal(dist.monto_asignado)
              detalles.append(DetalleCobroMensual(tipo_concepto="servicio",concepto=(s.servicio.nombre_servicio if s.servicio else f"Servicio {s.id_servicio}"),monto=dist.monto_asignado,id_servicio_mensual=s.id_servicio_mensual,id_distribucion_servicio=dist.id_distribucion_servicio,descripcion=f"{dist.tipo_calculo}; días considerados: {dist.dias_ocupados}"))
        total=monto_alquiler+monto_serv+deuda
        cobro=CobroMensual(id_periodo=id_periodo,id_alquiler=a.id_alquiler,id_casa=cuarto.id_casa,id_cuarto=cuarto.id_cuarto,id_inquilino=inq.id_inquilino,monto_alquiler=monto_alquiler,monto_servicios=monto_serv,deuda_anterior=deuda,descuentos=0,recargos=0,total_a_pagar=total,total_pagado=0,saldo_pendiente=total,fecha_limite_pago=limite,estado="pendiente")
        db.add(cobro); db.flush()
        for det in detalles: det.id_cobro=cobro.id_cobro; db.add(det)
        r["cobros_creados"]+=1
      if r["errores"]:
        db.rollback(); return r
      servicios=db.query(ServicioMensual).filter(ServicioMensual.id_periodo==id_periodo,ServicioMensual.estado=="activo",ServicioMensual.pagador_factura=="propietario").all()
      for s in servicios:
        if db.query(EgresoCasa).filter(EgresoCasa.id_servicio_mensual==s.id_servicio_mensual).first(): continue
        db.add(EgresoCasa(id_casa=s.id_casa,id_periodo=s.id_periodo,id_cuarto=s.id_cuarto,id_servicio_mensual=s.id_servicio_mensual,concepto=(s.servicio.nombre_servicio if s.servicio else f"Servicio {s.id_servicio}"),categoria="servicio",monto=s.monto,registrado_por=registrado_por,metodo_pago=s.metodo_pago,numero_comprobante=s.numero_comprobante,observacion=s.observacion))
        r["egresos_creados"]+=1
      db.commit(); return r
    except Exception:
      db.rollback(); raise

def get_detalles(db: Session, item):
    return [d for d in item.detalles if d.tipo_concepto != "servicio" or (d.servicio_mensual and d.servicio_mensual.estado == "activo" and d.servicio_mensual.responsable_pago == "inquilino")]
