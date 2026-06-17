from datetime import date
from decimal import Decimal
import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base
from modules.usuarios.models import Usuario
from modules.casas.models import Casa
from modules.cuartos.models import Cuarto
from modules.inquilinos.models import Inquilino
from modules.alquileres.models import Alquiler
from modules.periodos.models import PeriodoMensual
from modules.servicios.models import Servicio
from modules.cobros.models import CobroMensual, DetalleCobroMensual
from modules.egresos.models import EgresoCasa
from modules.pagos.models import Pago
from modules.servicios_mensuales.schemas import ServicioMensualCreate, ServicioMensualUpdate
from modules.servicios_mensuales import service as sm_service
from modules.cobros import service as cobros_service
from modules.reportes import service as reportes_service

@pytest.fixture()
def db():
    engine = create_engine("sqlite:///:memory:", future=True, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, future=True)
    s = Session()
    yield s
    s.close()

def seed(db):
    u=Usuario(nombre="Admin", correo="a@test.com", password_hash="x"); db.add(u); db.flush()
    casa=Casa(nombre_casa="Casa A", direccion="Dir", id_usuario_responsable=u.id_usuario); db.add(casa); db.flush()
    c1=Cuarto(id_casa=casa.id_casa, numero_cuarto="1", precio_alquiler=100)
    c2=Cuarto(id_casa=casa.id_casa, numero_cuarto="2", precio_alquiler=100)
    c3=Cuarto(id_casa=casa.id_casa, numero_cuarto="3", precio_alquiler=100); db.add_all([c1,c2,c3]); db.flush()
    i1=Inquilino(nombre="Ana"); i3=Inquilino(nombre="Leo"); db.add_all([i1,i3]); db.flush()
    p=PeriodoMensual(anio=2026, mes=1, nombre_periodo="Enero 2026", fecha_inicio=date(2026,1,1), fecha_fin=date(2026,1,31), estado="abierto")
    ph=PeriodoMensual(anio=2025, mes=12, nombre_periodo="Diciembre 2025", fecha_inicio=date(2025,12,1), fecha_fin=date(2025,12,31), estado="abierto")
    db.add_all([p,ph]); db.flush()
    a1=Alquiler(id_inquilino=i1.id_inquilino,id_cuarto=c1.id_cuarto,fecha_inicio=date(2025,12,15),monto_alquiler=100,dia_pago=5,estado="finalizado")
    a3=Alquiler(id_inquilino=i3.id_inquilino,id_cuarto=c3.id_cuarto,fecha_inicio=date(2026,1,10),fecha_fin=date(2026,1,20),monto_alquiler=120,dia_pago=5,estado="finalizado")
    old=Alquiler(id_inquilino=i1.id_inquilino,id_cuarto=c3.id_cuarto,fecha_inicio=date(2025,11,1),fecha_fin=date(2025,11,30),monto_alquiler=90,dia_pago=5,estado="finalizado")
    db.add_all([a1,a3,old]); db.flush()
    internet=Servicio(nombre_servicio="Internet", estado="activo"); luz=Servicio(nombre_servicio="Luz", estado="activo"); off=Servicio(nombre_servicio="Gas", estado="inactivo"); db.add_all([internet,luz,off]); db.commit()
    return locals()

def make(periodo, servicio, casa, cuarto, monto, resp):
    return ServicioMensualCreate(id_periodo=periodo, id_servicio=servicio, id_casa=casa, id_cuarto=cuarto, monto=Decimal(str(monto)), responsable_pago=resp)

def test_monthly_service_rules_and_sync(db):
    x=seed(db); uid=x['u'].id_usuario; p=x['p']; casa=x['casa']; c1=x['c1']; c2=x['c2']; c3=x['c3']; internet=x['internet']; luz=x['luz']
    s1=sm_service.create_item(db, make(p.id_periodo,internet.id_servicio,casa.id_casa,c1.id_cuarto,10,"inquilino"), uid)
    s3=sm_service.create_item(db, make(p.id_periodo,internet.id_servicio,casa.id_casa,c3.id_cuarto,25,"inquilino"), uid)
    assert {s.id_cuarto for s in sm_service.list_items(db,p.id_periodo) if s.id_servicio==internet.id_servicio} == {c1.id_cuarto,c3.id_cuarto}
    with pytest.raises(HTTPException): sm_service.create_item(db, make(p.id_periodo,internet.id_servicio,casa.id_casa,None,50,"inquilino"), uid)
    with pytest.raises(HTTPException): sm_service.create_item(db, make(p.id_periodo,internet.id_servicio,casa.id_casa,c2.id_cuarto,10,"inquilino"), uid)
    with pytest.raises(HTTPException): sm_service.create_item(db, make(p.id_periodo,x['off'].id_servicio,casa.id_casa,c1.id_cuarto,10,"inquilino"), uid)
    with pytest.raises(HTTPException): sm_service.create_item(db, make(p.id_periodo,internet.id_servicio,casa.id_casa,c1.id_cuarto,10,"inquilino"), uid)
    owner=sm_service.create_item(db, make(p.id_periodo,luz.id_servicio,casa.id_casa,None,30,"propietario"), uid)
    assert db.query(EgresoCasa).filter_by(id_servicio_mensual=owner.id_servicio_mensual).count()==1
    cobros_service.generar_periodo(db,p.id_periodo,uid)
    c1c=db.query(CobroMensual).filter_by(id_cuarto=c1.id_cuarto).one(); c3c=db.query(CobroMensual).filter_by(id_cuarto=c3.id_cuarto).one()
    assert c1c.monto_servicios == Decimal("10.00") and c3c.monto_servicios == Decimal("25.00")
    assert db.query(DetalleCobroMensual).filter_by(id_servicio_mensual=s1.id_servicio_mensual).count()==1
    sm_service.update_item(db,s1,ServicioMensualUpdate(monto=Decimal("15")),uid)
    assert db.get(CobroMensual,c1c.id_cobro).monto_servicios == Decimal("15.00")
    sm_service.update_item(db,s1,ServicioMensualUpdate(id_cuarto=c3.id_cuarto),uid)
    assert db.query(DetalleCobroMensual).filter_by(id_servicio_mensual=s1.id_servicio_mensual).count()==1
    sm_service.update_item(db,s1,ServicioMensualUpdate(responsable_pago="propietario"),uid)
    assert db.query(EgresoCasa).filter_by(id_servicio_mensual=s1.id_servicio_mensual).count()==1
    sm_service.update_item(db,s1,ServicioMensualUpdate(responsable_pago="inquilino"),uid)
    assert db.query(EgresoCasa).filter_by(id_servicio_mensual=s1.id_servicio_mensual).one().estado == "anulado"
    sm_service.anular_item(db,s1,registrado_por=uid)
    assert db.query(DetalleCobroMensual).filter_by(id_servicio_mensual=s1.id_servicio_mensual).count()==0
    eg=db.query(EgresoCasa).filter_by(id_servicio_mensual=owner.id_servicio_mensual).one(); eg.estado="anulado"; db.commit()
    assert reportes_service.resumen_periodo(db,p.id_periodo)["total_egresos"] == 0.0
    p.estado="cerrado"; db.commit()
    with pytest.raises(HTTPException): sm_service.create_item(db, make(p.id_periodo,luz.id_servicio,casa.id_casa,None,30,"propietario"), uid)
    pago=Pago(id_cobro=c1c.id_cobro,id_inquilino=x['i1'].id_inquilino,monto_pagado=5,registrado_por=uid,estado="valido"); db.add(pago); db.commit(); cobros_service.recalcular_cobro(db,c1c.id_cobro)
    assert db.get(CobroMensual,c1c.id_cobro).total_pagado == Decimal("5.00")

def test_report_ignores_cancelled_egress(db):
    x=seed(db); eg=EgresoCasa(id_casa=x['casa'].id_casa,id_periodo=x['p'].id_periodo,concepto="X",monto=50,registrado_por=x['u'].id_usuario,estado="anulado"); db.add(eg); db.commit()
    assert reportes_service.resumen_periodo(db,x['p'].id_periodo)["total_egresos"] == 0.0
