from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from modules.auth.dependencies import get_current_user
from modules.periodos import schemas, service

router = APIRouter(prefix="/api/periodos", tags=["periodos"])

@router.get("", response_model=list[schemas.PeriodoMensualResponse])
def list_items(db: Session = Depends(get_db), _=Depends(get_current_user)): return service.list_items(db)
@router.post("", response_model=schemas.PeriodoMensualResponse)
def create_item(payload: schemas.PeriodoMensualCreate, db: Session = Depends(get_db), _=Depends(get_current_user)): return service.create_item(db,payload)
@router.get("/actual", response_model=schemas.PeriodoMensualResponse)
def periodo_actual(db: Session = Depends(get_db), _=Depends(get_current_user)):
 return service.obtener_o_crear_actual(db)

@router.get("/{item_id}", response_model=schemas.PeriodoMensualResponse)
def get_item(item_id:int, db: Session = Depends(get_db), _=Depends(get_current_user)):
 item=service.get_item(db,item_id)
 if not item: raise HTTPException(404,"No encontrado")
 return item
@router.put("/{item_id}", response_model=schemas.PeriodoMensualResponse)
def update_item(item_id:int, payload: schemas.PeriodoMensualUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
 item=service.get_item(db,item_id)
 if not item: raise HTTPException(404,"No encontrado")
 return service.update_item(db,item,payload)
@router.delete("/{item_id}")
def delete_item(item_id:int, db: Session = Depends(get_db), _=Depends(get_current_user)):
 item=service.get_item(db,item_id)
 if not item: raise HTTPException(404,"No encontrado")
 service.delete_item(db,item)
 return {"ok":True}

@router.post("/{item_id}/cerrar", response_model=schemas.PeriodoMensualResponse)
def cerrar(item_id:int, db:Session=Depends(get_db), _=Depends(get_current_user)):
 item=service.get_item(db,item_id)
 if not item: raise HTTPException(404,"No encontrado")
 return service.cerrar_periodo(db,item)

@router.get("/{item_id}/cobros")
def cobros_periodo(item_id:int, db:Session=Depends(get_db), _=Depends(get_current_user)):
 from modules.cobros.models import CobroMensual
 return db.query(CobroMensual).filter(CobroMensual.id_periodo==item_id).all()
