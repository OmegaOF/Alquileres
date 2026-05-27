from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.casas.models import Casa
from modules.usuarios.models import Usuario

def list_items(db:Session): return db.query(Casa).all()
def get_item(db:Session,item_id:int): return db.get(Casa,item_id)
def create_item(db:Session,payload):
 d=payload.model_dump(exclude_unset=True)
 if not db.get(Usuario,d["id_usuario_responsable"]): raise HTTPException(400,"Usuario responsable no existe")
 i=Casa(**d); db.add(i); db.commit(); db.refresh(i); return i
def update_item(db:Session,item,payload):
 d=payload.model_dump(exclude_unset=True)
 if "id_usuario_responsable" in d and not db.get(Usuario,d["id_usuario_responsable"]): raise HTTPException(400,"Usuario responsable no existe")
 for k,v in d.items(): setattr(item,k,v)
 db.commit(); db.refresh(item); return item
def delete_item(db:Session,item): db.delete(item); db.commit()
