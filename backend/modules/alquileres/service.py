from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.alquileres.models import Alquiler
from modules.cuartos.models import Cuarto
from modules.inquilinos.models import Inquilino

CENT = Decimal("0.01")
def money(v): return Decimal(v or 0).quantize(CENT, rounding=ROUND_HALF_UP)
def list_items(db:Session): return db.query(Alquiler).all()
def get_item(db:Session,item_id:int): return db.get(Alquiler,item_id)

def _dias_inclusivos(inicio:date, fin:date):
 return (fin-inicio).days+1

def _normalizar(d, item=None):
 modalidad=d.get("modalidad_alquiler", getattr(item,"modalidad_alquiler",None) or "mensual")
 inicio=d.get("fecha_inicio", getattr(item,"fecha_inicio",None)); fin=d.get("fecha_fin", getattr(item,"fecha_fin",None))
 if fin and inicio and fin < inicio: raise HTTPException(400,"Fecha de salida no puede ser anterior a fecha de entrada")
 if modalidad=="mensual":
  monto=d.get("monto_mensual", d.get("monto_alquiler", getattr(item,"monto_mensual",None) or getattr(item,"monto_alquiler",None)))
  if monto is None: raise HTTPException(400,"El alquiler mensual requiere monto mensual")
  d["monto_mensual"]=money(monto); d["monto_alquiler"]=money(monto); d["precio_diario"]=None; d["total_alquiler_diario"]=None
 else:
  precio=d.get("precio_diario", getattr(item,"precio_diario",None))
  if precio is None: raise HTTPException(400,"El alquiler por día requiere precio diario")
  if not inicio or not fin: raise HTTPException(400,"El alquiler por día requiere fecha de entrada y salida")
  total=money(precio)*Decimal(_dias_inclusivos(inicio,fin))
  d["precio_diario"]=money(precio); d["total_alquiler_diario"]=money(total); d["monto_alquiler"]=money(total); d["monto_mensual"]=None
 return d

def _val(db,d,item=None):
 if not item and not d.get("id_inquilino"): raise HTTPException(400,"El inquilino es obligatorio")
 if "id_inquilino" in d and (not d["id_inquilino"] or not db.get(Inquilino,d["id_inquilino"])): raise HTTPException(400,"Inquilino no existe")
 if "id_cuarto" in d and (not d["id_cuarto"] or not db.get(Cuarto,d["id_cuarto"])): raise HTTPException(400,"Cuarto no existe")
 cuarto_id=d.get("id_cuarto", item.id_cuarto if item else None); estado=d.get("estado", item.estado if item else "activo")
 if cuarto_id and estado=="activo":
  q=db.query(Alquiler).filter(Alquiler.id_cuarto==cuarto_id,Alquiler.estado=="activo")
  if item: q=q.filter(Alquiler.id_alquiler!=item.id_alquiler)
  if q.first(): raise HTTPException(400,"El cuarto ya tiene alquiler activo")

def create_item(db:Session,payload):
 d=_normalizar(payload.model_dump(exclude_unset=True)); _val(db,d)
 i=Alquiler(**d); db.add(i);
 if i.estado=="activo": db.get(Cuarto,i.id_cuarto).estado="ocupado"
 db.commit(); db.refresh(i); return i

def update_item(db:Session,item,payload):
 d=_normalizar(payload.model_dump(exclude_unset=True), item); _val(db,d,item)
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
