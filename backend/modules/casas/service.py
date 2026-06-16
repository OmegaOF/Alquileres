from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from modules.casas.models import Casa
from modules.usuarios.models import Usuario
from modules.cuartos.models import Cuarto
from modules.alquileres.models import Alquiler
from modules.inquilinos.models import Inquilino
from modules.cobros.models import CobroMensual

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

def list_resumen(db:Session):
 casas = db.query(Casa).all(); out=[]
 for c in casas:
  cuartos = db.query(Cuarto).filter(Cuarto.id_casa==c.id_casa).all()
  out.append({"id_casa":c.id_casa,"nombre_casa":c.nombre_casa,"direccion":c.direccion,"zona":c.zona,"ciudad":c.ciudad,"estado":c.estado,"total_cuartos":len(cuartos),"cuartos_libres":sum(1 for x in cuartos if str(x.estado).lower()=="libre"),"cuartos_ocupados":sum(1 for x in cuartos if str(x.estado).lower()=="ocupado")})
 return out

def cuartos_resumen(db:Session, id_casa:int):
 if not db.get(Casa,id_casa): raise HTTPException(404,"Casa no encontrada")
 cuartos=db.query(Cuarto).filter(Cuarto.id_casa==id_casa).all(); out=[]
 for cuarto in cuartos:
  alquiler=db.query(Alquiler).filter(Alquiler.id_cuarto==cuarto.id_cuarto, Alquiler.estado=="activo").order_by(Alquiler.fecha_inicio.desc(), Alquiler.id_alquiler.desc()).first()
  saldo=None; inq=None
  if alquiler:
   inq=db.get(Inquilino, alquiler.id_inquilino)
   saldo=db.query(func.coalesce(func.sum(CobroMensual.saldo_pendiente),0)).filter(CobroMensual.id_alquiler==alquiler.id_alquiler, CobroMensual.estado!="anulado").scalar()
  out.append({"id_cuarto":cuarto.id_cuarto,"id_casa":cuarto.id_casa,"numero_cuarto":cuarto.numero_cuarto,"descripcion":cuarto.descripcion,"estado":cuarto.estado,"precio_alquiler":float(cuarto.precio_alquiler or 0),"id_alquiler_activo":alquiler.id_alquiler if alquiler else None,"monto_alquiler_activo":float(alquiler.monto_alquiler) if alquiler else None,"id_inquilino_actual":inq.id_inquilino if inq else None,"nombre_inquilino_actual":inq.nombre if inq else None,"telefono_inquilino_actual":inq.telefono if inq else None,"fecha_inicio_alquiler_activo":alquiler.fecha_inicio.isoformat() if alquiler else None,"saldo_pendiente_alquiler_activo":float(saldo) if alquiler else None})
 return out
