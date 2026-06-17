from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.egresos.models import EgresoCasa
from modules.casas.models import Casa
from modules.periodos.utils import require_periodo_abierto
from modules.cuartos.models import Cuarto
from modules.usuarios.models import Usuario


def list_items(db:Session): return db.query(EgresoCasa).all()
def get_item(db:Session,item_id:int): return db.get(EgresoCasa,item_id)

def _val(db,d,item=None):
 id_periodo=d.get("id_periodo", item.id_periodo if item else None)
 if id_periodo: require_periodo_abierto(db,id_periodo)
 id_casa=d.get("id_casa", item.id_casa if item else None)
 if id_casa and not db.get(Casa,id_casa): raise HTTPException(400,"Casa no existe")
 id_cuarto=d.get("id_cuarto", item.id_cuarto if item else None)
 if id_cuarto:
  c=db.get(Cuarto,id_cuarto)
  if not c: raise HTTPException(400,"Cuarto no existe")
  if id_casa and c.id_casa!=id_casa: raise HTTPException(400,"Cuarto no pertenece a casa")
 registrado=d.get("registrado_por", item.registrado_por if item else None)
 if registrado and not db.get(Usuario,registrado): raise HTTPException(400,"Usuario registrador no existe")

def create_item(db:Session,payload,registrado_por:int|None=None):
 d=payload.model_dump(exclude_unset=True); _val(db,d)
 if registrado_por is not None: d["registrado_por"]=registrado_por
 i=EgresoCasa(**d); db.add(i); db.commit(); db.refresh(i); return i

def update_item(db:Session,item,payload):
 d=payload.model_dump(exclude_unset=True); _val(db,d,item); [setattr(item,k,v) for k,v in d.items()]; db.commit(); db.refresh(item); return item

def anular_item(db:Session,item):
 require_periodo_abierto(db,item.id_periodo); item.estado="anulado"; item.fecha_anulacion=datetime.utcnow(); db.commit(); db.refresh(item); return item

def delete_item(db:Session,item): return anular_item(db,item)
