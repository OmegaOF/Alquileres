from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from modules.auth.dependencies import get_current_user
from modules.dashboard.schemas import DashboardResumen
from modules.dashboard.service import resumen
router=APIRouter(prefix="/api/dashboard", tags=["dashboard"])
@router.get("/resumen", response_model=DashboardResumen)
def get_resumen(db:Session=Depends(get_db), _=Depends(get_current_user)):
    return resumen(db)
