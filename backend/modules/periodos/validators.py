from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.periodos.models import PeriodoMensual


def require_periodo_abierto(db: Session, id_periodo: int) -> PeriodoMensual:
    periodo = db.get(PeriodoMensual, id_periodo)
    if not periodo:
        raise HTTPException(400, "Periodo no existe")
    if periodo.estado == "cerrado":
        raise HTTPException(400, "Periodo cerrado")
    return periodo
