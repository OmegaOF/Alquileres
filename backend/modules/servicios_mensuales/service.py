from datetime import datetime, date
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session
from modules.servicios_mensuales.models import ServicioMensual, DistribucionServicioMensual
from modules.periodos.models import PeriodoMensual
from modules.periodos.validators import require_periodo_abierto
from modules.servicios.models import Servicio
from modules.casas.models import Casa
from modules.cuartos.models import Cuarto
from modules.alquileres.models import Alquiler
from modules.cobros.models import CobroMensual, DetalleCobroMensual
from modules.egresos.models import EgresoCasa
from modules.pagos.models import Pago

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

def _alquiler_activo(db,id_periodo,id_cuarto):
 p=db.get(PeriodoMensual,id_periodo)
 if not p: raise HTTPException(400,"Periodo no existe")
 return db.query(Alquiler).filter(
  Alquiler.id_cuarto==id_cuarto,
  Alquiler.fecha_inicio<=p.fecha_fin,
  ((Alquiler.fecha_fin.is_(None)) | (Alquiler.fecha_fin>=p.fecha_inicio)),
  Alquiler.estado!="anulado",
  ((Alquiler.modalidad_alquiler.is_(None)) | (Alquiler.modalidad_alquiler=="mensual")),
 ).order_by(Alquiler.fecha_inicio.desc(),Alquiler.id_alquiler.desc()).first()

def _validar(db,d,item=None):
 _periodo_abierto(db,d["id_periodo"]); servicio=_servicio_activo(db,d["id_servicio"])
 if not db.get(Casa,d["id_casa"]): raise HTTPException(400,"Casa no existe")
 id_cuarto=d.get("id_cuarto")
 if id_cuarto:
  c=db.get(Cuarto,id_cuarto)
  if not c: raise HTTPException(400,"Cuarto no existe")
  if c.id_casa!=d["id_casa"]: raise HTTPException(400,"Cuarto no pertenece a casa")
 d.setdefault("pagador_factura", "propietario" if d.get("responsable_pago")=="propietario" else "inquilino_directo")
 if d["responsable_pago"]=="inquilino":
  if not id_cuarto: raise HTTPException(400,MSG_DIST)
  if not _alquiler_activo(db,d["id_periodo"],id_cuarto): raise HTTPException(400,MSG_VACIO)
 q=db.query(ServicioMensual).filter(ServicioMensual.id_periodo==d["id_periodo"],ServicioMensual.id_servicio==d["id_servicio"],ServicioMensual.id_casa==d["id_casa"],ServicioMensual.responsable_pago==d["responsable_pago"],ServicioMensual.estado=="activo")
 q=q.filter(ServicioMensual.id_cuarto==id_cuarto) if id_cuarto else q.filter(ServicioMensual.id_cuarto.is_(None))
 if item: q=q.filter(ServicioMensual.id_servicio_mensual!=item.id_servicio_mensual)
 if q.first(): raise HTTPException(400,"Ya existe un servicio mensual activo con el mismo periodo, servicio, casa, alcance, cuarto y responsable")
 return servicio

def _recalc(db,cobro):
 total_serv=sum(Decimal(x.monto) for x in db.query(DetalleCobroMensual).filter(DetalleCobroMensual.id_cobro==cobro.id_cobro,DetalleCobroMensual.tipo_concepto=="servicio").all() if x.servicio_mensual and x.servicio_mensual.estado=="activo" and x.servicio_mensual.responsable_pago=="inquilino")
 total_pag=sum(Decimal(x.monto_pagado) for x in db.query(Pago).filter(Pago.id_cobro==cobro.id_cobro,Pago.estado=="valido").all())
 total=Decimal(cobro.monto_alquiler)+total_serv+Decimal(cobro.deuda_anterior)+Decimal(cobro.recargos)-Decimal(cobro.descuentos)
 if total < total_pag: raise HTTPException(400,"Existen pagos registrados que impiden reducir el total del cobro por debajo de lo pagado")
 cobro.monto_servicios=total_serv; cobro.total_a_pagar=total; cobro.total_pagado=total_pag; cobro.saldo_pendiente=total-total_pag
 cobro.estado="pagado" if cobro.saldo_pendiente<=0 else ("parcial" if total_pag>0 else ("atrasado" if cobro.fecha_limite_pago and cobro.fecha_limite_pago<date.today() else "pendiente"))

def _sync_detalle(db,s):
 if s.estado!="activo" or s.responsable_pago!="inquilino":
  for old in db.query(DetalleCobroMensual).filter(DetalleCobroMensual.id_servicio_mensual==s.id_servicio_mensual).all():
   cobro=old.cobro; db.delete(old); db.flush(); _recalc(db,cobro)
  return
 dists=[d for d in s.distribuciones if d.id_alquiler and d.tipo_calculo!="manual_requerido" and Decimal(d.monto_asignado)>0]
 if not dists: return
 nombre=s.servicio.nombre_servicio if s.servicio else f"Servicio {s.id_servicio}"
 valid_ids={d.id_distribucion_servicio for d in dists}
 for stale in db.query(DetalleCobroMensual).filter(DetalleCobroMensual.id_servicio_mensual==s.id_servicio_mensual).all():
  if stale.id_distribucion_servicio not in valid_ids:
   cobro=stale.cobro; db.delete(stale); db.flush(); _recalc(db,cobro)
 for dist in dists:
  cobro=db.query(CobroMensual).filter(CobroMensual.id_periodo==s.id_periodo,CobroMensual.id_alquiler==dist.id_alquiler).first()
  if not cobro: continue
  exists=db.query(DetalleCobroMensual).filter(DetalleCobroMensual.id_cobro==cobro.id_cobro,DetalleCobroMensual.id_servicio_mensual==s.id_servicio_mensual,DetalleCobroMensual.id_distribucion_servicio==dist.id_distribucion_servicio).first()
  if not exists:
   db.add(DetalleCobroMensual(id_cobro=cobro.id_cobro,tipo_concepto="servicio",concepto=nombre,monto=dist.monto_asignado,id_servicio_mensual=s.id_servicio_mensual,id_distribucion_servicio=dist.id_distribucion_servicio,descripcion=f"{dist.tipo_calculo}; días considerados: {dist.dias_ocupados}"))
  else:
   exists.concepto=nombre; exists.monto=dist.monto_asignado; exists.id_distribucion_servicio=dist.id_distribucion_servicio; exists.descripcion=f"{dist.tipo_calculo}; días considerados: {dist.dias_ocupados}"
  db.flush(); _recalc(db,cobro)

def _sync_egreso(db,s,registrado_por:int):
 eg=db.query(EgresoCasa).filter(EgresoCasa.id_servicio_mensual==s.id_servicio_mensual).first()
 if s.estado!="activo" or s.pagador_factura!="propietario":
  if eg: eg.estado="anulado"; eg.fecha_anulacion=datetime.utcnow()
  return
 nombre=s.servicio.nombre_servicio if s.servicio else f"Servicio {s.id_servicio}"
 if not eg:
  eg=EgresoCasa(id_casa=s.id_casa,id_periodo=s.id_periodo,id_cuarto=s.id_cuarto,id_servicio_mensual=s.id_servicio_mensual,concepto=nombre,categoria="servicio",monto=s.monto,fecha_egreso=s.fecha_pago or datetime.utcnow(),metodo_pago=s.metodo_pago,numero_comprobante=s.numero_comprobante,observacion=s.observacion,registrado_por=registrado_por,estado="activo"); db.add(eg)
 else:
  eg.id_casa=s.id_casa; eg.id_periodo=s.id_periodo; eg.id_cuarto=s.id_cuarto; eg.concepto=nombre; eg.monto=s.monto; eg.fecha_egreso=s.fecha_pago or eg.fecha_egreso; eg.metodo_pago=s.metodo_pago; eg.numero_comprobante=s.numero_comprobante; eg.observacion=s.observacion; eg.estado="activo"; eg.fecha_anulacion=None

def _sync(db,s,registrado_por:int): _sync_detalle(db,s); _sync_egreso(db,s,registrado_por)

def create_item(db:Session,payload,registrado_por:int):
 d=payload.model_dump(exclude_unset=True); d.setdefault("estado","activo"); _validar(db,d); i=ServicioMensual(**d); db.add(i); db.flush(); recrear_distribuciones_servicio(db,i); _sync(db,i,registrado_por); db.commit(); db.refresh(i); return i

def update_item(db:Session,item,payload,registrado_por:int):
 old_cobros=[d.cobro for d in db.query(DetalleCobroMensual).filter(DetalleCobroMensual.id_servicio_mensual==item.id_servicio_mensual).all()]
 d=payload.model_dump(exclude_unset=True); chk={"id_periodo":d.get("id_periodo",item.id_periodo),"id_servicio":d.get("id_servicio",item.id_servicio),"id_casa":d.get("id_casa",item.id_casa),"id_cuarto":d.get("id_cuarto",item.id_cuarto),"responsable_pago":d.get("responsable_pago",item.responsable_pago),"monto":d.get("monto",item.monto)}; _validar(db,chk,item)
 for k,v in d.items(): setattr(item,k,v)
 db.flush(); recrear_distribuciones_servicio(db,item); _sync(db,item,registrado_por);
 for old_cobro in old_cobros:
  if old_cobro: _recalc(db,old_cobro)
 db.commit(); db.refresh(item); return item

def anular_item(db:Session,item,motivo:str|None=None,registrado_por:int|None=None):
 _periodo_abierto(db,item.id_periodo); item.estado="anulado"; item.fecha_anulacion=datetime.utcnow(); item.motivo_anulacion=motivo; db.flush(); _sync(db,item,registrado_por or 1); db.commit(); db.refresh(item); return item

def delete_item(db:Session,item,registrado_por:int|None=None): return anular_item(db,item,registrado_por=registrado_por)

# Reglas definitivas: fechas inclusivas; solo alquileres mensuales reciben servicios.
def dias_ocupados_en_periodo(alquiler, periodo):
 inicio=max(alquiler.fecha_inicio, periodo.fecha_inicio)
 fin=min(alquiler.fecha_fin or periodo.fecha_fin, periodo.fecha_fin)
 return max(0,(fin-inicio).days+1)

def calcular_distribuciones_servicio(db:Session, s:ServicioMensual):
 p=db.get(PeriodoMensual,s.id_periodo)
 if not p or not s.id_cuarto or s.responsable_pago!="inquilino" or s.estado!="activo": return []
 dias_periodo=(p.fecha_fin-p.fecha_inicio).days+1
 monto=Decimal(s.monto).quantize(Decimal('0.01'))
 alquileres=db.query(Alquiler).filter(Alquiler.id_cuarto==s.id_cuarto, Alquiler.fecha_inicio<=p.fecha_fin, ((Alquiler.fecha_fin.is_(None)) | (Alquiler.fecha_fin>=p.fecha_inicio)), Alquiler.estado!="anulado", ((Alquiler.modalidad_alquiler.is_(None)) | (Alquiler.modalidad_alquiler=="mensual"))).order_by(Alquiler.fecha_inicio,Alquiler.id_alquiler).all()
 candidatos=[(a,dias_ocupados_en_periodo(a,p)) for a in alquileres]
 candidatos=[x for x in candidatos if x[1]>0]
 if not candidatos: return []
 full=[x for x in candidatos if x[1]>=15]
 if len(candidatos)>1 and full:
  sugeridos=[]; usado=Decimal('0.00')
  for a,dias in candidatos:
   prop=(monto/Decimal(dias_periodo)*Decimal(dias)).quantize(Decimal('0.01'))
   usado+=prop; sugeridos.append({"alquiler":a,"dias":dias,"monto":prop,"tipo":"manual_requerido"})
  return sugeridos + [{"alquiler":None,"dias":dias_periodo-sum(d for _,d in candidatos),"monto":monto-usado,"tipo":"propietario"}]
 if len(candidatos)==1:
  a,dias=candidatos[0]
  if dias>=15: return [{"alquiler":a,"dias":dias,"monto":monto,"tipo":"completo"},{"alquiler":None,"dias":dias_periodo-dias,"monto":Decimal('0.00'),"tipo":"propietario"}]
 # varios menores a 15, o un único menor
 res=[]; usado=Decimal('0.00')
 for a,dias in candidatos:
  val=(monto/Decimal(dias_periodo)*Decimal(dias)).quantize(Decimal('0.01'))
  usado+=val; res.append({"alquiler":a,"dias":dias,"monto":val,"tipo":"proporcional"})
 res.append({"alquiler":None,"dias":dias_periodo-sum(d for _,d in candidatos),"monto":monto-usado,"tipo":"propietario"})
 return res

def recrear_distribuciones_servicio(db:Session, s:ServicioMensual):
 db.query(DistribucionServicioMensual).filter(DistribucionServicioMensual.id_servicio_mensual==s.id_servicio_mensual).delete()
 for x in calcular_distribuciones_servicio(db,s):
  db.add(DistribucionServicioMensual(id_servicio_mensual=s.id_servicio_mensual,id_alquiler=x["alquiler"].id_alquiler if x["alquiler"] else None,dias_ocupados=x["dias"],monto_asignado=x["monto"],parte_propietario=x["monto"] if not x["alquiler"] else 0,tipo_calculo=x["tipo"],manual_confirmada="si" if x["tipo"]!="manual_requerido" else "no"))


def obtener_distribuciones(db:Session, item_id:int):
 s=get_item(db,item_id)
 if not s: raise HTTPException(404,"No encontrado")
 p=db.get(PeriodoMensual,s.id_periodo); total=Decimal(s.monto).quantize(Decimal('0.01'))
 dists=s.distribuciones or []
 asignado=sum(Decimal(d.monto_asignado) for d in dists if d.estado=="vigente")
 return {"servicio":{"id_servicio_mensual":s.id_servicio_mensual,"id_periodo":s.id_periodo,"id_servicio":s.id_servicio,"id_casa":s.id_casa,"id_cuarto":s.id_cuarto,"monto":float(total),"estado":s.estado,"manual_requerido":any(d.tipo_calculo=="manual_requerido" for d in dists)},"monto_total":float(total),"distribuciones":[{"id_distribucion_servicio":d.id_distribucion_servicio,"id_alquiler":d.id_alquiler,"inquilino":getattr(getattr(d.alquiler,'inquilino',None),'nombre_completo',None),"fecha_inicio":str(d.alquiler.fecha_inicio) if d.alquiler else None,"fecha_fin":str(d.alquiler.fecha_fin) if d.alquiler and d.alquiler.fecha_fin else None,"dias_ocupados":d.dias_ocupados,"monto_sugerido":float(d.monto_asignado),"monto_asignado":float(d.monto_asignado),"parte_propietario":float(d.parte_propietario),"tipo_calculo":d.tipo_calculo,"manual_confirmada":d.manual_confirmada} for d in dists],"resuelto":asignado==total and not any(d.tipo_calculo=="manual_requerido" for d in dists),"diferencia_pendiente":float(total-asignado)}

def guardar_distribuciones(db:Session, item_id:int, payload, registrado_por:int):
 s=get_item(db,item_id)
 if not s: raise HTTPException(404,"No encontrado")
 _periodo_abierto(db,s.id_periodo)
 if s.estado!="activo": raise HTTPException(400,"El servicio no está activo")
 p=db.get(PeriodoMensual,s.id_periodo); total=Decimal(s.monto).quantize(Decimal('0.01'))
 entradas=payload.distribuciones
 suma=sum(Decimal(str(x.monto_asignado)).quantize(Decimal('0.01')) for x in entradas)
 if suma!=total:
  diff=total-suma; raise HTTPException(400,f"La distribución debe sumar exactamente {total} Bs. Actualmente suma {suma} Bs; {'faltan distribuir' if diff>0 else 'sobran'} {abs(diff)} Bs.")
 old_cobros=[d.cobro for d in db.query(DetalleCobroMensual).filter(DetalleCobroMensual.id_servicio_mensual==s.id_servicio_mensual).all()]
 db.query(DistribucionServicioMensual).filter(DistribucionServicioMensual.id_servicio_mensual==s.id_servicio_mensual).delete()
 for x in entradas:
  aid=x.id_alquiler
  if aid is not None:
   a=db.get(Alquiler,aid)
   if not a or a.id_cuarto!=s.id_cuarto or a.estado=="anulado" or (a.modalidad_alquiler and a.modalidad_alquiler!="mensual") or a.fecha_inicio>p.fecha_fin or (a.fecha_fin and a.fecha_fin<p.fecha_inicio): raise HTTPException(400,"Alquiler inválido para esta distribución")
   dias=dias_ocupados_en_periodo(a,p); parte=Decimal('0.00'); tipo="manual"
  else:
   dias=0; parte=Decimal(str(x.monto_asignado)).quantize(Decimal('0.01')); tipo="propietario_manual"
  db.add(DistribucionServicioMensual(id_servicio_mensual=s.id_servicio_mensual,id_alquiler=aid,dias_ocupados=dias,monto_asignado=Decimal(str(x.monto_asignado)).quantize(Decimal('0.01')),parte_propietario=parte,tipo_calculo=tipo,manual_confirmada="si"))
 db.flush(); _sync(db,s,registrado_por)
 for c in old_cobros:
  if c: _recalc(db,c)
 db.commit(); return obtener_distribuciones(db,item_id)
