from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.egresos.models import EgresoCasa
from modules.casas.models import Casa
from modules.periodos.models import PeriodoMensual
from modules.cuartos.models import Cuarto
from modules.usuarios.models import Usuario
def list_items(db:Session): return db.query(EgresoCasa).all()
def get_item(db:Session,item_id:int): return db.get(EgresoCasa,item_id)
def _val(db,d):
 if "id_casa" in d and not db.get(Casa,d["id_casa"]): raise HTTPException(400,"Casa no existe")
 if "id_periodo" in d:
  p=db.get(PeriodoMensual,d["id_periodo"])
  if not p: raise HTTPException(400,"Periodo no existe")
  if p.estado=="cerrado": raise HTTPException(400,"Periodo cerrado")
 if d.get("id_cuarto"):
  c=db.get(Cuarto,d["id_cuarto"])
  if not c: raise HTTPException(400,"Cuarto no existe")
  if c.id_casa!=d.get("id_casa",c.id_casa): raise HTTPException(400,"Cuarto no pertenece a casa")
 if "registrado_por" in d and not db.get(Usuario,d["registrado_por"]): raise HTTPException(400,"Usuario registrador no existe")
def create_item(db:Session,payload): d=payload.model_dump(exclude_unset=True); _val(db,d); i=EgresoCasa(**d); db.add(i); db.commit(); db.refresh(i); return i
def update_item(db:Session,item,payload): d=payload.model_dump(exclude_unset=True); chk={"id_casa":d.get("id_casa",item.id_casa),"id_periodo":d.get("id_periodo",item.id_periodo),"id_cuarto":d.get("id_cuarto",item.id_cuarto),"registrado_por":d.get("registrado_por",item.registrado_por)}; _val(db,chk); [setattr(item,k,v) for k,v in d.items()]; db.commit(); db.refresh(item); return item
def delete_item(db:Session,item): item.estado="anulado"; db.commit(); db.refresh(item); return item
