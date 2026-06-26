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

from datetime import date
import calendar

MESES_ES = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

def obtener_o_crear_actual(db: Session):
    hoy = date.today()
    item = db.query(PeriodoMensual).filter(PeriodoMensual.anio == hoy.year, PeriodoMensual.mes == hoy.month).first()
    if item:
        return item
    ultimo = calendar.monthrange(hoy.year, hoy.month)[1]
    item = PeriodoMensual(anio=hoy.year, mes=hoy.month, nombre_periodo=f"{MESES_ES[hoy.month]} {hoy.year}", fecha_inicio=date(hoy.year, hoy.month, 1), fecha_fin=date(hoy.year, hoy.month, ultimo), estado="abierto")
    db.add(item); db.commit(); db.refresh(item); return item
