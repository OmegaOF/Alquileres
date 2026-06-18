from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.pagos.models import Pago
from modules.cobros.models import CobroMensual, DetalleCobroMensual
from modules.cobros.service import recalcular_cobro
from modules.inquilinos.models import Inquilino
from modules.usuarios.models import Usuario
def list_items(db:Session): return db.query(Pago).all()
def get_item(db:Session,item_id:int): return db.get(Pago,item_id)
def _val(db,d):
 cobro=db.get(CobroMensual,d["id_cobro"])
 if not cobro: raise HTTPException(400,"Cobro no existe")
 if cobro.estado=="anulado": raise HTTPException(400,"Cobro anulado")
 if d.get("id_inquilino") != cobro.id_inquilino: raise HTTPException(400,"El inquilino del pago debe coincidir con el cobro")
 if not db.get(Inquilino,d["id_inquilino"]): raise HTTPException(400,"Inquilino no existe")
 if not db.get(Usuario,d["registrado_por"]): raise HTTPException(400,"Usuario registrador no existe")
 if d.get("id_detalle_cobro"):
  det=db.get(DetalleCobroMensual,d["id_detalle_cobro"])
  if not det or det.id_cobro!=d["id_cobro"]: raise HTTPException(400,"Detalle no pertenece al cobro")
def create_item(db:Session,payload,registrado_por:int):
 d=payload.model_dump(exclude_unset=True)
 cobro=db.get(CobroMensual,d["id_cobro"])
 if not cobro: raise HTTPException(400,"Cobro no existe")
 d["id_inquilino"]=cobro.id_inquilino
 d["registrado_por"]=registrado_por
 _val(db,d); i=Pago(**d); db.add(i); db.commit(); db.refresh(i); recalcular_cobro(db,i.id_cobro); return i
def update_item(db:Session,item,payload): d=payload.model_dump(exclude_unset=True); chk={"id_cobro":item.id_cobro,"id_inquilino":d.get("id_inquilino",item.id_inquilino),"registrado_por":d.get("registrado_por",item.registrado_por),"id_detalle_cobro":d.get("id_detalle_cobro",item.id_detalle_cobro)}; _val(db,chk); [setattr(item,k,v) for k,v in d.items()]; db.commit(); db.refresh(item); recalcular_cobro(db,item.id_cobro); return item
def anular_pago(db:Session,item): item.estado="anulado"; db.commit(); db.refresh(item); recalcular_cobro(db,item.id_cobro); return item
def delete_item(db:Session,item): anular_pago(db,item)
