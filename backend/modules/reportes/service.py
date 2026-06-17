from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.cobros.models import CobroMensual
from modules.egresos.models import EgresoCasa
from modules.periodos.models import PeriodoMensual
from modules.casas.models import Casa


def resumen_periodo(db: Session, id_periodo: int):
    if not db.get(PeriodoMensual, id_periodo): raise HTTPException(404, "Periodo no existe")
    cobros = db.query(CobroMensual).filter(CobroMensual.id_periodo == id_periodo, CobroMensual.estado != "anulado").all()
    egresos = db.query(EgresoCasa).filter(EgresoCasa.id_periodo == id_periodo, EgresoCasa.estado == "activo").all()
    return {
        "id_periodo": id_periodo,
        "total_a_cobrar": float(sum(Decimal(c.total_a_pagar) for c in cobros)),
        "total_pagado": float(sum(Decimal(c.total_pagado) for c in cobros)),
        "total_pendiente": float(sum(Decimal(c.saldo_pendiente) for c in cobros)),
        "total_egresos": float(sum(Decimal(e.monto) for e in egresos)),
        "cantidad_cobros": len(cobros),
        "cantidad_pagados": len([c for c in cobros if c.estado == "pagado"]),
        "cantidad_pendientes": len([c for c in cobros if c.estado == "pendiente"]),
        "cantidad_parciales": len([c for c in cobros if c.estado == "parcial"]),
        "cantidad_atrasados": len([c for c in cobros if c.estado == "atrasado"]),
    }


def reporte_casa_periodo(db: Session, id_casa: int, id_periodo: int):
    if not db.get(Casa, id_casa): raise HTTPException(404, "Casa no existe")
    if not db.get(PeriodoMensual, id_periodo): raise HTTPException(404, "Periodo no existe")
    cobros = db.query(CobroMensual).filter(CobroMensual.id_periodo == id_periodo, CobroMensual.id_casa == id_casa, CobroMensual.estado != "anulado").all()
    egresos = db.query(EgresoCasa).filter(EgresoCasa.id_periodo == id_periodo, EgresoCasa.id_casa == id_casa, EgresoCasa.estado == "activo").all()
    return {
        "id_casa": id_casa,
        "id_periodo": id_periodo,
        "total_a_cobrar": float(sum(Decimal(c.total_a_pagar) for c in cobros)),
        "total_pagado": float(sum(Decimal(c.total_pagado) for c in cobros)),
        "total_pendiente": float(sum(Decimal(c.saldo_pendiente) for c in cobros)),
        "total_egresos": float(sum(Decimal(e.monto) for e in egresos)),
        "cobros": len(cobros),
        "egresos": len(egresos),
    }
