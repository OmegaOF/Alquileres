from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.periodos.models import PeriodoMensual
def list_items(db:Session): return db.query(PeriodoMensual).all()
def get_item(db:Session,item_id:int): return db.get(PeriodoMensual,item_id)
def create_item(db:Session,payload):
 d=payload.model_dump(exclude_unset=True)
 if db.query(PeriodoMensual).filter(PeriodoMensual.anio==d["anio"],PeriodoMensual.mes==d["mes"]).first(): raise HTTPException(400,"Periodo duplicado")
 i=PeriodoMensual(**d); db.add(i); db.commit(); db.refresh(i); return i
def update_item(db:Session,item,payload):
 d=payload.model_dump(exclude_unset=True)
 anio=d.get("anio",item.anio); mes=d.get("mes",item.mes)
 dup=db.query(PeriodoMensual).filter(PeriodoMensual.anio==anio,PeriodoMensual.mes==mes,PeriodoMensual.id_periodo!=item.id_periodo).first()
 if dup: raise HTTPException(400,"Periodo duplicado")
 for k,v in d.items(): setattr(item,k,v)
 db.commit(); db.refresh(item); return item
def cerrar_periodo(db:Session,item): item.estado="cerrado"; db.commit(); db.refresh(item); return item
def delete_item(db:Session,item): db.delete(item); db.commit()
