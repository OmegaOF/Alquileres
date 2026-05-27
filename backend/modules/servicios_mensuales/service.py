from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.servicios_mensuales.models import ServicioMensual
from modules.periodos.models import PeriodoMensual
from modules.servicios.models import Servicio
from modules.casas.models import Casa
from modules.cuartos.models import Cuarto
def list_items(db:Session): return db.query(ServicioMensual).all()
def get_item(db:Session,item_id:int): return db.get(ServicioMensual,item_id)
def _val(db,d):
 if "id_periodo" in d and not db.get(PeriodoMensual,d["id_periodo"]): raise HTTPException(400,"Periodo no existe")
 if "id_servicio" in d and not db.get(Servicio,d["id_servicio"]): raise HTTPException(400,"Servicio no existe")
 if "id_casa" in d and not db.get(Casa,d["id_casa"]): raise HTTPException(400,"Casa no existe")
 if d.get("id_cuarto"):
  c=db.get(Cuarto,d["id_cuarto"])
  if not c: raise HTTPException(400,"Cuarto no existe")
  if c.id_casa!=d.get("id_casa",c.id_casa): raise HTTPException(400,"Cuarto no pertenece a casa")
def create_item(db:Session,payload): d=payload.model_dump(exclude_unset=True); _val(db,d); i=ServicioMensual(**d); db.add(i); db.commit(); db.refresh(i); return i
def update_item(db:Session,item,payload): d=payload.model_dump(exclude_unset=True); chk={"id_periodo":d.get("id_periodo",item.id_periodo),"id_servicio":d.get("id_servicio",item.id_servicio),"id_casa":d.get("id_casa",item.id_casa),"id_cuarto":d.get("id_cuarto",item.id_cuarto)}; _val(db,chk); [setattr(item,k,v) for k,v in d.items()]; db.commit(); db.refresh(item); return item
def delete_item(db:Session,item): db.delete(item); db.commit()
