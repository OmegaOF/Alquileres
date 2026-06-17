from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.cobros.models import CobroMensual
from modules.egresos.models import EgresoCasa
from modules.periodos.models import PeriodoMensual
from modules.casas.models import Casa


def _cobros_validos(db: Session, id_periodo: int, id_casa: int | None = None):
    q = db.query(CobroMensual).filter(CobroMensual.id_periodo == id_periodo, CobroMensual.estado != "anulado")
    if id_casa is not None: q = q.filter(CobroMensual.id_casa == id_casa)
    return q.all()


def _egresos_validos(db: Session, id_periodo: int, id_casa: int | None = None):
    q = db.query(EgresoCasa).filter(EgresoCasa.id_periodo == id_periodo, EgresoCasa.estado != "anulado")
    if id_casa is not None: q = q.filter(EgresoCasa.id_casa == id_casa)
    return q.all()


def _resumen(cobros, egresos, extra):
    total_pagado = sum(Decimal(c.total_pagado) for c in cobros)
    total_egresos = sum(Decimal(e.monto) for e in egresos)
    return {
        **extra,
        "total_a_cobrar": float(sum(Decimal(c.total_a_pagar) for c in cobros)),
        "total_pagado": float(total_pagado),
        "total_pendiente": float(sum(Decimal(c.saldo_pendiente) for c in cobros)),
        "total_egresos": float(total_egresos),
        "resultado_periodo": float(total_pagado - total_egresos),
        "cantidad_cobros": len(cobros),
        "cantidad_pagados": len([c for c in cobros if c.estado == "pagado"]),
        "cantidad_pendientes": len([c for c in cobros if c.estado == "pendiente"]),
        "cantidad_parciales": len([c for c in cobros if c.estado == "parcial"]),
        "cantidad_atrasados": len([c for c in cobros if c.estado == "atrasado"]),
    }


def resumen_periodo(db: Session, id_periodo: int):
    if not db.get(PeriodoMensual, id_periodo): raise HTTPException(404, "Periodo no existe")
    return _resumen(_cobros_validos(db,id_periodo), _egresos_validos(db,id_periodo), {"id_periodo": id_periodo})


def reporte_casa_periodo(db: Session, id_casa: int, id_periodo: int):
    if not db.get(Casa, id_casa): raise HTTPException(404, "Casa no existe")
    if not db.get(PeriodoMensual, id_periodo): raise HTTPException(404, "Periodo no existe")
    cobros = _cobros_validos(db,id_periodo,id_casa); egresos = _egresos_validos(db,id_periodo,id_casa)
    data = _resumen(cobros, egresos, {"id_casa": id_casa, "id_periodo": id_periodo})
    data["cobros"] = len(cobros); data["egresos"] = len(egresos)
    return data
