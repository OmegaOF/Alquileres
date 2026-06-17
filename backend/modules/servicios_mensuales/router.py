from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db import get_db
from modules.auth.dependencies import get_current_user
from modules.servicios_mensuales import schemas, service

router = APIRouter(prefix="/api/servicios-mensuales", tags=["servicios_mensuales"])

@router.get("", response_model=list[schemas.ServicioMensualResponse])
def list_items(id_periodo:int|None=Query(default=None), db: Session = Depends(get_db), _=Depends(get_current_user)): return service.list_items(db,id_periodo)
@router.post("", response_model=schemas.ServicioMensualResponse)
def create_item(payload: schemas.ServicioMensualCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)): return service.create_item(db,payload,current_user.id_usuario)
@router.get("/{item_id}/distribuciones")
def get_distribuciones(item_id:int, db: Session = Depends(get_db), _=Depends(get_current_user)):
 return service.obtener_distribuciones(db,item_id)
@router.put("/{item_id}/distribuciones")
def put_distribuciones(item_id:int, payload: schemas.DistribucionManualUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
 return service.guardar_distribuciones(db,item_id,payload,current_user.id_usuario)
@router.get("/{item_id}", response_model=schemas.ServicioMensualResponse)
def get_item(item_id:int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
 item=service.get_item(db,item_id)
 if not item: raise HTTPException(404,"No encontrado")
 return item
@router.put("/{item_id}", response_model=schemas.ServicioMensualResponse)
def update_item(item_id:int, payload: schemas.ServicioMensualUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
 item=service.get_item(db,item_id)
 if not item: raise HTTPException(404,"No encontrado")
 return service.update_item(db,item,payload,current_user.id_usuario)
@router.post("/{item_id}/anular", response_model=schemas.ServicioMensualResponse)
def anular_item(item_id:int, motivo: str | None = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
 item=service.get_item(db,item_id)
 if not item: raise HTTPException(404,"No encontrado")
 return service.anular_item(db,item,motivo,current_user.id_usuario)
@router.delete("/{item_id}")
def delete_item(item_id:int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
 item=service.get_item(db,item_id)
 if not item: raise HTTPException(404,"No encontrado")
 service.delete_item(db,item,current_user.id_usuario)
 return {"ok":True}
