from datetime import datetime, date
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.servicios_mensuales.models import ServicioMensual
from modules.periodos.models import PeriodoMensual
from modules.servicios.models import Servicio
from modules.casas.models import Casa
from modules.cuartos.models import Cuarto
from modules.cobros.models import CobroMensual, DetalleCobroMensual
from modules.egresos.models import EgresoCasa
from modules.pagos.models import Pago
from modules.periodos.utils import require_periodo_abierto
from modules.alquileres.utils import alquiler_del_cuarto_en_periodo

MSG_DIST = "Todavía no está habilitada la distribución de servicios generales entre varios inquilinos. Seleccione un cuarto específico o cambie el responsable a propietario."
MSG_VACIO = "El cuarto seleccionado no tiene un alquiler activo. Seleccione responsable propietario o elija un cuarto ocupado."

def list_items(db:Session, id_periodo:int|None=None):
 q=db.query(ServicioMensual)
 if id_periodo is not None: q=q.filter(ServicioMensual.id_periodo==id_periodo)
 return q.all()

def get_item(db:Session,item_id:int): return db.get(ServicioMensual,item_id)

def _periodo_abierto(db,id_periodo):
 return require_periodo_abierto(db,id_periodo)

def _servicio_activo(db,id_servicio):
 s=db.get(Servicio,id_servicio)
 if not s: raise HTTPException(400,"Servicio no existe")
 if s.estado!="activo": raise HTTPException(400,"El servicio está inactivo y no puede usarse en nuevos registros")
 return s

def _alquiler_periodo(db,id_periodo,id_cuarto):
 periodo=db.get(PeriodoMensual,id_periodo)
 if not periodo: raise HTTPException(400,"Periodo no existe")
 return alquiler_del_cuarto_en_periodo(db,id_cuarto,periodo)

def _validar(db,d,item=None):
 _periodo_abierto(db,d["id_periodo"]); servicio=_servicio_activo(db,d["id_servicio"])
 if not db.get(Casa,d["id_casa"]): raise HTTPException(400,"Casa no existe")
 id_cuarto=d.get("id_cuarto")
 if id_cuarto:
  c=db.get(Cuarto,id_cuarto)
  if not c: raise HTTPException(400,"Cuarto no existe")
  if c.id_casa!=d["id_casa"]: raise HTTPException(400,"Cuarto no pertenece a casa")
 if d["responsable_pago"]=="inquilino":
  if not id_cuarto: raise HTTPException(400,MSG_DIST)
  if not _alquiler_periodo(db,d["id_periodo"],id_cuarto): raise HTTPException(400,MSG_VACIO)
 q=db.query(ServicioMensual).filter(ServicioMensual.id_periodo==d["id_periodo"],ServicioMensual.id_servicio==d["id_servicio"],ServicioMensual.id_casa==d["id_casa"],ServicioMensual.responsable_pago==d["responsable_pago"],ServicioMensual.estado=="activo")
 q=q.filter(ServicioMensual.id_cuarto==id_cuarto) if id_cuarto else q.filter(ServicioMensual.id_cuarto.is_(None))
 if item: q=q.filter(ServicioMensual.id_servicio_mensual!=item.id_servicio_mensual)
 if q.first(): raise HTTPException(400,"Ya existe un servicio mensual activo con el mismo periodo, servicio, casa, alcance, cuarto y responsable")
 return servicio

def _recalc(db,cobro):
 total_serv=sum(Decimal(x.monto) for x in db.query(DetalleCobroMensual).filter(DetalleCobroMensual.id_cobro==cobro.id_cobro,DetalleCobroMensual.tipo_concepto=="servicio").all())
 total_pag=sum(Decimal(x.monto_pagado) for x in db.query(Pago).filter(Pago.id_cobro==cobro.id_cobro,Pago.estado=="valido").all())
 total=Decimal(cobro.monto_alquiler)+total_serv+Decimal(cobro.deuda_anterior)+Decimal(cobro.recargos)-Decimal(cobro.descuentos)
 if total < total_pag: raise HTTPException(400,"Existen pagos registrados que impiden reducir el total del cobro por debajo de lo pagado")
 cobro.monto_servicios=total_serv; cobro.total_a_pagar=total; cobro.total_pagado=total_pag; cobro.saldo_pendiente=total-total_pag
 cobro.estado="pagado" if cobro.saldo_pendiente<=0 else ("parcial" if total_pag>0 else ("atrasado" if cobro.fecha_limite_pago and cobro.fecha_limite_pago<date.today() else "pendiente"))

def _sync_detalle(db,s):
 det=db.query(DetalleCobroMensual).filter(DetalleCobroMensual.id_servicio_mensual==s.id_servicio_mensual).first()
 if s.estado!="activo" or s.responsable_pago!="inquilino":
  if det:
   cobro=det.cobro; db.delete(det); db.flush(); _recalc(db,cobro)
  return
 a=_alquiler_periodo(db,s.id_periodo,s.id_cuarto)
 if not a: raise HTTPException(400,MSG_VACIO)
 cobro=db.query(CobroMensual).filter(CobroMensual.id_periodo==s.id_periodo,CobroMensual.id_alquiler==a.id_alquiler).first()
 if not cobro: return
 nombre=s.servicio.nombre_servicio if s.servicio else f"Servicio {s.id_servicio}"
 if det and det.id_cobro!=cobro.id_cobro:
  old=det.cobro; db.delete(det); db.flush(); _recalc(db,old); det=None
 if not det:
  det=DetalleCobroMensual(id_cobro=cobro.id_cobro,tipo_concepto="servicio",concepto=nombre,monto=s.monto,id_servicio_mensual=s.id_servicio_mensual,descripcion=s.observacion); db.add(det)
 else:
  det.concepto=nombre; det.monto=s.monto; det.descripcion=s.observacion
 db.flush(); _recalc(db,cobro)

def _sync_egreso(db,s,registrado_por:int):
 eg=db.query(EgresoCasa).filter(EgresoCasa.id_servicio_mensual==s.id_servicio_mensual).first()
 if s.estado!="activo" or s.responsable_pago!="propietario":
  if eg: eg.estado="anulado"; eg.fecha_anulacion=datetime.utcnow()
  return
 nombre=s.servicio.nombre_servicio if s.servicio else f"Servicio {s.id_servicio}"
 if not eg:
  eg=EgresoCasa(id_casa=s.id_casa,id_periodo=s.id_periodo,id_cuarto=s.id_cuarto,id_servicio_mensual=s.id_servicio_mensual,concepto=nombre,categoria="servicio",monto=s.monto,fecha_egreso=s.fecha_pago or datetime.utcnow(),metodo_pago=s.metodo_pago,numero_comprobante=s.numero_comprobante,observacion=s.observacion,registrado_por=registrado_por,estado="activo"); db.add(eg)
 else:
  eg.id_casa=s.id_casa; eg.id_periodo=s.id_periodo; eg.id_cuarto=s.id_cuarto; eg.concepto=nombre; eg.monto=s.monto; eg.fecha_egreso=s.fecha_pago or eg.fecha_egreso; eg.metodo_pago=s.metodo_pago; eg.numero_comprobante=s.numero_comprobante; eg.observacion=s.observacion; eg.estado="activo"; eg.fecha_anulacion=None

def _sync(db,s,registrado_por:int): _sync_detalle(db,s); _sync_egreso(db,s,registrado_por)

def create_item(db:Session,payload,registrado_por:int):
 try:
  d=payload.model_dump(exclude_unset=True); d.setdefault("estado","activo"); _validar(db,d); i=ServicioMensual(**d); db.add(i); db.flush(); _sync(db,i,registrado_por); db.commit(); db.refresh(i); return i
 except Exception:
  db.rollback(); raise

def update_item(db:Session,item,payload,registrado_por:int):
 try:
  old_det=db.query(DetalleCobroMensual).filter(DetalleCobroMensual.id_servicio_mensual==item.id_servicio_mensual).first(); old_cobro=old_det.cobro if old_det else None
  d=payload.model_dump(exclude_unset=True); chk={"id_periodo":d.get("id_periodo",item.id_periodo),"id_servicio":d.get("id_servicio",item.id_servicio),"id_casa":d.get("id_casa",item.id_casa),"id_cuarto":d.get("id_cuarto",item.id_cuarto),"responsable_pago":d.get("responsable_pago",item.responsable_pago),"monto":d.get("monto",item.monto)}; _validar(db,chk,item)
  for k,v in d.items(): setattr(item,k,v)
  db.flush(); _sync(db,item,registrado_por)
  if old_cobro: _recalc(db,old_cobro)
  db.commit(); db.refresh(item); return item
 except Exception:
  db.rollback(); raise

def anular_item(db:Session,item,motivo:str|None=None,registrado_por:int|None=None):
 try:
  _periodo_abierto(db,item.id_periodo); item.estado="anulado"; item.fecha_anulacion=datetime.utcnow(); item.motivo_anulacion=motivo; db.flush(); _sync(db,item,registrado_por or 0); db.commit(); db.refresh(item); return item
 except Exception:
  db.rollback(); raise

def delete_item(db:Session,item,registrado_por:int|None=None): return anular_item(db,item,registrado_por=registrado_por)
