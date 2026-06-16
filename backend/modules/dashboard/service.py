from sqlalchemy import func
from sqlalchemy.orm import Session
from modules.casas.models import Casa
from modules.cuartos.models import Cuarto
from modules.alquileres.models import Alquiler
from modules.periodos.models import PeriodoMensual
from modules.cobros.models import CobroMensual
from modules.egresos.models import EgresoCasa

def _sum(v): return float(v or 0)
def resumen(db:Session):
 props={"total_casas":db.query(Casa).count(),"total_cuartos":db.query(Cuarto).count(),"cuartos_libres":db.query(Cuarto).filter(Cuarto.estado=="libre").count(),"cuartos_ocupados":db.query(Cuarto).filter(Cuarto.estado=="ocupado").count(),"alquileres_activos":db.query(Alquiler).filter(Alquiler.estado=="activo").count()}
 periodo=db.query(PeriodoMensual).filter(PeriodoMensual.estado=="abierto").order_by(PeriodoMensual.anio.desc(),PeriodoMensual.mes.desc(),PeriodoMensual.id_periodo.desc()).first()
 fin={"total_facturado":0,"total_pagado":0,"saldo_pendiente":0,"total_egresos":0,"resultado_actual":0}; cob={"pendientes":0,"parciales":0,"pagados":0,"atrasados":0}
 per=None
 if periodo:
  per={"id_periodo":periodo.id_periodo,"anio":periodo.anio,"mes":periodo.mes,"estado":periodo.estado}
  q=db.query(CobroMensual).filter(CobroMensual.id_periodo==periodo.id_periodo)
  fin["total_facturado"]=_sum(q.with_entities(func.sum(CobroMensual.total_a_pagar)).scalar()); fin["total_pagado"]=_sum(q.with_entities(func.sum(CobroMensual.total_pagado)).scalar()); fin["saldo_pendiente"]=_sum(q.with_entities(func.sum(CobroMensual.saldo_pendiente)).scalar()); fin["total_egresos"]=_sum(db.query(func.sum(EgresoCasa.monto)).filter(EgresoCasa.id_periodo==periodo.id_periodo).scalar()); fin["resultado_actual"]=fin["total_pagado"]-fin["total_egresos"]
  for estado,key in [("pendiente","pendientes"),("parcial","parciales"),("pagado","pagados"),("atrasado","atrasados")]: cob[key]=q.filter(CobroMensual.estado==estado).count()
 return {"periodo":per,"propiedades":props,"finanzas":fin,"cobros":cob}
