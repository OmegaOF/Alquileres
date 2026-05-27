from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from modules.auth.dependencies import get_current_user
from modules.reportes import service

router = APIRouter(prefix="/api/reportes", tags=["reportes"])

@router.get('/resumen-periodo/{id_periodo}')
def resumen_periodo(id_periodo:int, db:Session=Depends(get_db), _=Depends(get_current_user)):
    return service.resumen_periodo(db,id_periodo)

@router.get('/casa/{id_casa}/periodo/{id_periodo}')
def casa_periodo(id_casa:int,id_periodo:int, db:Session=Depends(get_db), _=Depends(get_current_user)):
    return service.reporte_casa_periodo(db,id_casa,id_periodo)
