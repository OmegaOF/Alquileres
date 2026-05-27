from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from modules.auth.dependencies import get_current_user
from modules.casas import schemas, service

router = APIRouter(prefix="/api/casas", tags=["casas"])

@router.get("", response_model=list[schemas.CasaResponse])
def list_items(db: Session = Depends(get_db), _=Depends(get_current_user)): return service.list_items(db)
@router.post("", response_model=schemas.CasaResponse)
def create_item(payload: schemas.CasaCreate, db: Session = Depends(get_db), _=Depends(get_current_user)): return service.create_item(db,payload)
@router.get("/{item_id}", response_model=schemas.CasaResponse)
def get_item(item_id:int, db: Session = Depends(get_db), _=Depends(get_current_user)):
 item=service.get_item(db,item_id)
 if not item: raise HTTPException(404,"No encontrado")
 return item
@router.put("/{item_id}", response_model=schemas.CasaResponse)
def update_item(item_id:int, payload: schemas.CasaUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
 item=service.get_item(db,item_id)
 if not item: raise HTTPException(404,"No encontrado")
 return service.update_item(db,item,payload)
@router.delete("/{item_id}")
def delete_item(item_id:int, db: Session = Depends(get_db), _=Depends(get_current_user)):
 item=service.get_item(db,item_id)
 if not item: raise HTTPException(404,"No encontrado")
 service.delete_item(db,item)
 return {"ok":True}

@router.get("/{item_id}/cuartos")
def cuartos_casa(item_id:int, db:Session=Depends(get_db), _=Depends(get_current_user)):
 from modules.cuartos.models import Cuarto
 return db.query(Cuarto).filter(Cuarto.id_casa==item_id).all()
