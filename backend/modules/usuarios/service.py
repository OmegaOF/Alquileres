from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.auth.service import hash_password
from modules.usuarios.models import Usuario


def list_items(db: Session): return db.query(Usuario).all()

def get_item(db: Session, item_id: int): return db.get(Usuario, item_id)

def create_item(db: Session, payload):
    if db.query(Usuario).filter(Usuario.correo == payload.correo).first():
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    data = payload.model_dump(exclude_unset=True)
    data["password_hash"] = hash_password(data.pop("password"))
    item = Usuario(**data); db.add(item); db.commit(); db.refresh(item); return item

def update_item(db: Session, item, payload):
    data = payload.model_dump(exclude_unset=True)
    if "correo" in data:
        dup = db.query(Usuario).filter(Usuario.correo == data["correo"], Usuario.id_usuario != item.id_usuario).first()
        if dup: raise HTTPException(status_code=400, detail="Correo ya registrado")
    if "password" in data: item.password_hash = hash_password(data.pop("password"))
    for k,v in data.items(): setattr(item,k,v)
    db.commit(); db.refresh(item); return item

def delete_item(db: Session, item): db.delete(item); db.commit()
