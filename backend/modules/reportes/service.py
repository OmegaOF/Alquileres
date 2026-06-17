from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.cobros.models import CobroMensual
from modules.egresos.models import EgresoCasa
from modules.periodos.models import PeriodoMensual
from modules.casas.models import Casa
from modules.pagos.models import Pago
from modules.servicios_mensuales.models import DistribucionServicioMensual


def _servicios(cobros):
    detalles=[d for c in cobros for d in c.detalles if d.tipo_concepto=="servicio" and d.servicio_mensual and d.servicio_mensual.estado=="activo"]
    fact=sum(Decimal(d.monto) for d in detalles)
    ids={d.id_detalle_cobro for d in detalles}
    pag=sum(Decimal(p.monto_pagado) for c in cobros for p in c.pagos if p.estado=="valido" and p.id_detalle_cobro in ids)
    return fact,pag

def _resumen(db,id_periodo,id_casa=None):
    q=db.query(CobroMensual).filter(CobroMensual.id_periodo==id_periodo,CobroMensual.estado!="anulado")
    if id_casa: q=q.filter(CobroMensual.id_casa==id_casa)
    cobros=q.all()
    qe=db.query(EgresoCasa).filter(EgresoCasa.id_periodo==id_periodo,EgresoCasa.estado=="activo",EgresoCasa.categoria=="servicio")
    if id_casa: qe=qe.filter(EgresoCasa.id_casa==id_casa)
    egresos=qe.all(); total_egresos=sum(Decimal(e.monto) for e in egresos)
    fact,pag=_servicios(cobros)
    qd=db.query(DistribucionServicioMensual).join(DistribucionServicioMensual.servicio_mensual).filter(DistribucionServicioMensual.id_alquiler.is_(None),DistribucionServicioMensual.estado=="vigente")
    parte=sum(Decimal(d.parte_propietario or 0) for d in qd.all() if d.servicio_mensual.id_periodo==id_periodo and d.servicio_mensual.estado=="activo" and (not id_casa or d.servicio_mensual.id_casa==id_casa))
    return {"total_a_cobrar":float(sum(Decimal(c.total_a_pagar) for c in cobros)),"total_pagado":float(sum(Decimal(c.total_pagado) for c in cobros)),"total_pendiente":float(sum(Decimal(c.saldo_pendiente) for c in cobros)),"total_egresos":float(total_egresos),"total_egresos_servicios":float(total_egresos),"monto_servicios_facturado_inquilinos":float(fact),"monto_servicios_pagado_inquilinos":float(pag),"monto_servicios_pendiente_inquilinos":float(fact-pag),"parte_servicios_propietario":float(parte),"costo_neto_caja_propietario":float(total_egresos-pag),"monto_recuperado_inquilinos":float(pag),"costo_neto_propietario":float(total_egresos-pag)}

def resumen_periodo(db: Session, id_periodo: int):
    if not db.get(PeriodoMensual, id_periodo): raise HTTPException(404,"Periodo no existe")
    cobros=db.query(CobroMensual).filter(CobroMensual.id_periodo==id_periodo,CobroMensual.estado!="anulado").all()
    r={"id_periodo":id_periodo,**_resumen(db,id_periodo),"cantidad_cobros":len(cobros),"cantidad_pagados":len([c for c in cobros if c.estado=="pagado"]),"cantidad_pendientes":len([c for c in cobros if c.estado=="pendiente"]),"cantidad_parciales":len([c for c in cobros if c.estado=="parcial"]),"cantidad_atrasados":len([c for c in cobros if c.estado=="atrasado"])}
    return r

def reporte_casa_periodo(db: Session, id_casa: int, id_periodo: int):
    if not db.get(Casa,id_casa): raise HTTPException(404,"Casa no existe")
    if not db.get(PeriodoMensual,id_periodo): raise HTTPException(404,"Periodo no existe")
    cobros=db.query(CobroMensual).filter(CobroMensual.id_periodo==id_periodo,CobroMensual.id_casa==id_casa,CobroMensual.estado!="anulado").all()
    egresos=db.query(EgresoCasa).filter(EgresoCasa.id_periodo==id_periodo,EgresoCasa.id_casa==id_casa,EgresoCasa.estado=="activo").all()
    return {"id_casa":id_casa,"id_periodo":id_periodo,**_resumen(db,id_periodo,id_casa),"cobros":len(cobros),"egresos":len(egresos)}
