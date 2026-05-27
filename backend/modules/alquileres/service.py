from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.alquileres.models import Alquiler
from modules.cuartos.models import Cuarto
from modules.inquilinos.models import Inquilino
def list_items(db:Session): return db.query(Alquiler).all()
def get_item(db:Session,item_id:int): return db.get(Alquiler,item_id)
def _val(db,d,item=None):
 if "id_inquilino" in d and not db.get(Inquilino,d["id_inquilino"]): raise HTTPException(400,"Inquilino no existe")
 if "id_cuarto" in d and not db.get(Cuarto,d["id_cuarto"]): raise HTTPException(400,"Cuarto no existe")
 cuarto_id=d.get("id_cuarto", item.id_cuarto if item else None); estado=d.get("estado", item.estado if item else "activo")
 if cuarto_id and estado=="activo":
  q=db.query(Alquiler).filter(Alquiler.id_cuarto==cuarto_id,Alquiler.estado=="activo")
  if item: q=q.filter(Alquiler.id_alquiler!=item.id_alquiler)
  if q.first(): raise HTTPException(400,"El cuarto ya tiene alquiler activo")

def create_item(db:Session,payload):
 d=payload.model_dump(exclude_unset=True); _val(db,d)
 i=Alquiler(**d); db.add(i);
 if i.estado=="activo": db.get(Cuarto,i.id_cuarto).estado="ocupado"
 db.commit(); db.refresh(i); return i
def update_item(db:Session,item,payload):
 d=payload.model_dump(exclude_unset=True); _val(db,d,item)
 for k,v in d.items(): setattr(item,k,v)
 cuarto=db.get(Cuarto,item.id_cuarto)
 if item.estado=="activo": cuarto.estado="ocupado"
 elif item.estado in ("finalizado","cancelado"): cuarto.estado="libre"
 db.commit(); db.refresh(item); return item
def finalizar_alquiler(db:Session,item):
 item.estado="finalizado"
 if not item.fecha_fin: item.fecha_fin=date.today()
 db.get(Cuarto,item.id_cuarto).estado="libre"
 db.commit(); db.refresh(item); return item
def delete_item(db:Session,item): db.delete(item); db.commit()
