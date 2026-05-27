from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.cuartos.models import Cuarto
from modules.casas.models import Casa

def list_items(db:Session): return db.query(Cuarto).all()
def get_item(db:Session,item_id:int): return db.get(Cuarto,item_id)
def create_item(db:Session,payload):
 d=payload.model_dump(exclude_unset=True)
 if not db.get(Casa,d["id_casa"]): raise HTTPException(400,"Casa no existe")
 i=Cuarto(**d); db.add(i); db.commit(); db.refresh(i); return i
def update_item(db:Session,item,payload):
 d=payload.model_dump(exclude_unset=True)
 if "id_casa" in d and not db.get(Casa,d["id_casa"]): raise HTTPException(400,"Casa no existe")
 for k,v in d.items(): setattr(item,k,v)
 db.commit(); db.refresh(item); return item
def delete_item(db:Session,item): db.delete(item); db.commit()
