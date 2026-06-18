from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from modules.auth.dependencies import get_current_user
from modules.pagos import schemas, service

router = APIRouter(prefix="/api/pagos", tags=["pagos"])

@router.get("", response_model=list[schemas.PagoResponse])
def list_items(db: Session = Depends(get_db), _=Depends(get_current_user)): return service.list_items(db)
@router.post("", response_model=schemas.PagoResponse)
def create_item(payload: schemas.PagoCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)): return service.create_item(db,payload,current_user.id_usuario)
@router.get("/{item_id}", response_model=schemas.PagoResponse)
def get_item(item_id:int, db: Session = Depends(get_db), _=Depends(get_current_user)):
 item=service.get_item(db,item_id)
 if not item: raise HTTPException(404,"No encontrado")
 return item
@router.put("/{item_id}", response_model=schemas.PagoResponse)
def update_item(item_id:int, payload: schemas.PagoUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
 item=service.get_item(db,item_id)
 if not item: raise HTTPException(404,"No encontrado")
 return service.update_item(db,item,payload)
@router.post("/{item_id}/anular", response_model=schemas.PagoResponse)
def anular(item_id:int, db:Session=Depends(get_db), _=Depends(get_current_user)):
 item=service.get_item(db,item_id)
 if not item: raise HTTPException(404,"No encontrado")
 return service.anular_pago(db,item)

@router.delete("/{item_id}")
def delete_item(item_id:int, db: Session = Depends(get_db), _=Depends(get_current_user)):
 item=service.get_item(db,item_id)
 if not item: raise HTTPException(404,"No encontrado")
 service.anular_pago(db,item)
 return {"ok":True,"detalle":"Pago anulado"}
