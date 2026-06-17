from datetime import date
from decimal import Decimal
from modules.alquileres.models import Alquiler
from modules.cobros.models import DetalleCobroMensual
from modules.cobros import service as cobros_service
from modules.egresos.models import EgresoCasa
from modules.reportes import service as reportes_service
from modules.servicios_mensuales import service as sm_service
from modules.servicios_mensuales.models import DistribucionServicioMensual
from modules.servicios_mensuales.schemas import ServicioMensualCreate
from tests.test_servicios_mensuales_rules import seed


def make_sm(p, servicio, casa, cuarto, monto):
    return ServicioMensualCreate(id_periodo=p, id_servicio=servicio, id_casa=casa, id_cuarto=cuarto, monto=Decimal(str(monto)), responsable_pago="inquilino")


def test_alquiler_mensual_no_prorratea_y_servicio_10_dias(db):
    x=seed(db); a=x['a3']; a.fecha_inicio=date(2026,1,1); a.fecha_fin=date(2026,1,10); a.modalidad_alquiler="mensual"; db.commit()
    sm=sm_service.create_item(db, make_sm(x['p'].id_periodo,x['luz'].id_servicio,x['casa'].id_casa,x['c3'].id_cuarto,300), x['u'].id_usuario)
    r=cobros_service.generar_periodo(db,x['p'].id_periodo,x['u'].id_usuario)
    assert r['errores']==[]
    cobro=[c for c in a.cobros if c.id_periodo==x['p'].id_periodo][0]
    assert cobro.monto_alquiler == Decimal('120.00')
    assert cobro.monto_servicios == Decimal('96.77')
    dist=db.query(DistribucionServicioMensual).filter_by(id_servicio_mensual=sm.id_servicio_mensual,id_alquiler=a.id_alquiler).one()
    assert dist.dias_ocupados == 10
    assert dist.tipo_calculo == 'proporcional'


def test_alquiler_mensual_15_dias_servicio_completo(db):
    x=seed(db); a=x['a3']; a.fecha_inicio=date(2026,1,1); a.fecha_fin=date(2026,1,15); a.modalidad_alquiler="mensual"; db.commit()
    sm_service.create_item(db, make_sm(x['p'].id_periodo,x['luz'].id_servicio,x['casa'].id_casa,x['c3'].id_cuarto,300), x['u'].id_usuario)
    cobros_service.generar_periodo(db,x['p'].id_periodo,x['u'].id_usuario)
    cobro=[c for c in a.cobros if c.id_periodo==x['p'].id_periodo][0]
    assert cobro.monto_alquiler == Decimal('120.00')
    assert cobro.monto_servicios == Decimal('300.00')


def test_alquiler_diario_no_recibe_servicios(db):
    x=seed(db); a=x['a3']; a.modalidad_alquiler="diario"; a.fecha_inicio=date(2026,1,1); a.fecha_fin=date(2026,1,4); a.precio_diario=150; a.total_alquiler_diario=600; a.monto_alquiler=600; db.commit()
    sm_service.create_item(db, make_sm(x['p'].id_periodo,x['luz'].id_servicio,x['casa'].id_casa,x['c3'].id_cuarto,300), x['u'].id_usuario)
    r=cobros_service.generar_periodo(db,x['p'].id_periodo,x['u'].id_usuario)
    assert r['errores']==[]
    cobro=[c for c in a.cobros if c.id_periodo==x['p'].id_periodo][0]
    assert cobro.monto_alquiler == Decimal('600.00')
    assert cobro.monto_servicios == Decimal('0.00')
    assert db.query(DetalleCobroMensual).filter_by(id_cobro=cobro.id_cobro,tipo_concepto='servicio').count() == 0


def test_dos_mensuales_menores_15_y_vacio_suman_factura(db):
    x=seed(db); a=x['a3']; a.fecha_inicio=date(2026,1,1); a.fecha_fin=date(2026,1,10); a.modalidad_alquiler='mensual'
    b=Alquiler(id_inquilino=x['i1'].id_inquilino,id_cuarto=x['c3'].id_cuarto,fecha_inicio=date(2026,1,21),fecha_fin=date(2026,1,30),monto_alquiler=100,monto_mensual=100,modalidad_alquiler='mensual',estado='finalizado')
    db.add(b); db.commit()
    sm=sm_service.create_item(db, make_sm(x['p'].id_periodo,x['luz'].id_servicio,x['casa'].id_casa,x['c3'].id_cuarto,310), x['u'].id_usuario)
    dists=db.query(DistribucionServicioMensual).filter_by(id_servicio_mensual=sm.id_servicio_mensual).all()
    assert sum(Decimal(d.monto_asignado) for d in dists) == Decimal('310.00')
    assert [d.tipo_calculo for d in dists if d.id_alquiler] == ['proporcional','proporcional']


def test_conflicto_mensual_15_y_otro_exige_manual(db):
    x=seed(db); a=x['a3']; a.fecha_inicio=date(2026,1,1); a.fecha_fin=date(2026,1,15); a.modalidad_alquiler='mensual'
    b=Alquiler(id_inquilino=x['i1'].id_inquilino,id_cuarto=x['c3'].id_cuarto,fecha_inicio=date(2026,1,16),fecha_fin=date(2026,1,20),monto_alquiler=100,monto_mensual=100,modalidad_alquiler='mensual',estado='finalizado')
    db.add(b); db.commit()
    sm_service.create_item(db, make_sm(x['p'].id_periodo,x['luz'].id_servicio,x['casa'].id_casa,x['c3'].id_cuarto,300), x['u'].id_usuario)
    r=cobros_service.generar_periodo(db,x['p'].id_periodo,x['u'].id_usuario)
    assert r['errores']
    assert db.query(DetalleCobroMensual).filter_by(tipo_concepto='servicio').count() == 0


def test_reporte_egreso_bruto_recuperado_y_neto(db):
    x=seed(db)
    eg=EgresoCasa(id_casa=x['casa'].id_casa,id_periodo=x['p'].id_periodo,id_cuarto=x['c3'].id_cuarto,concepto='Luz',categoria='servicio',monto=300,registrado_por=x['u'].id_usuario,estado='activo')
    db.add(eg); db.commit()
    sm_service.create_item(db, make_sm(x['p'].id_periodo,x['luz'].id_servicio,x['casa'].id_casa,x['c3'].id_cuarto,300), x['u'].id_usuario)
    cobros_service.generar_periodo(db,x['p'].id_periodo,x['u'].id_usuario)
    rep=reportes_service.resumen_periodo(db,x['p'].id_periodo)
    assert rep['total_egresos'] == 300.0
    assert rep['monto_recuperado_inquilinos'] == 300.0
    assert rep['costo_neto_propietario'] == 0.0
