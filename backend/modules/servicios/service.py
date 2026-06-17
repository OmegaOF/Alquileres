from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.servicios.models import Servicio
def list_items(db:Session): return db.query(Servicio).all()
def get_item(db:Session,item_id:int): return db.get(Servicio,item_id)
def create_item(db:Session,payload):
 d=payload.model_dump(exclude_unset=True)
 if db.query(Servicio).filter(Servicio.nombre_servicio==d["nombre_servicio"]).first(): raise HTTPException(400,"Servicio duplicado")
 i=Servicio(**d); db.add(i); db.commit(); db.refresh(i); return i
def update_item(db:Session,item,payload):
 d=payload.model_dump(exclude_unset=True)
 if "nombre_servicio" in d:
  dup=db.query(Servicio).filter(Servicio.nombre_servicio==d["nombre_servicio"],Servicio.id_servicio!=item.id_servicio).first()
  if dup: raise HTTPException(400,"Servicio duplicado")
 for k,v in d.items(): setattr(item,k,v)
 db.commit(); db.refresh(item); return item
def delete_item(db:Session,item):
 from modules.servicios_mensuales.models import ServicioMensual
 if db.query(ServicioMensual).filter(ServicioMensual.id_servicio==item.id_servicio).first():
  item.estado="inactivo"; db.commit(); db.refresh(item); return item
 db.delete(item); db.commit(); return None
