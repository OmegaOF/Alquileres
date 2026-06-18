from decimal import Decimal
import pytest
from fastapi import HTTPException

from modules.cobros.models import CobroMensual
from modules.egresos import service as egresos_service
from modules.egresos.schemas import EgresoCasaCreate
from modules.pagos import service as pagos_service
from modules.pagos.schemas import PagoCreate
from modules.servicios_mensuales import service as sm_service
from modules.servicios_mensuales.schemas import DistribucionManualUpdate, DistribucionManualItem, ServicioMensualCreate
from tests.test_servicios_mensuales_rules import seed


def test_pago_deriva_inquilino_y_usuario_desde_cobro_y_auth(db):
    x = seed(db)
    cobro = CobroMensual(
        id_periodo=x["p"].id_periodo,
        id_alquiler=x["a1"].id_alquiler,
        id_casa=x["casa"].id_casa,
        id_cuarto=x["c1"].id_cuarto,
        id_inquilino=x["i1"].id_inquilino,
        monto_alquiler=Decimal("100.00"),
        total_a_pagar=Decimal("100.00"),
        saldo_pendiente=Decimal("100.00"),
    )
    db.add(cobro)
    db.commit()

    payload = PagoCreate(
        id_cobro=cobro.id_cobro,
        id_inquilino=x["i3"].id_inquilino,
        registrado_por=999,
        monto_pagado=Decimal("10.00"),
    )
    pago = pagos_service.create_item(db, payload, x["u"].id_usuario)

    assert pago.id_inquilino == cobro.id_inquilino
    assert pago.registrado_por == x["u"].id_usuario


def test_pago_update_rechaza_inquilino_manipulado(db):
    x = seed(db)
    cobro = CobroMensual(
        id_periodo=x["p"].id_periodo,
        id_alquiler=x["a1"].id_alquiler,
        id_casa=x["casa"].id_casa,
        id_cuarto=x["c1"].id_cuarto,
        id_inquilino=x["i1"].id_inquilino,
        monto_alquiler=Decimal("100.00"),
        total_a_pagar=Decimal("100.00"),
        saldo_pendiente=Decimal("100.00"),
    )
    db.add(cobro)
    db.commit()
    payload = PagoCreate(id_cobro=cobro.id_cobro, id_inquilino=x["i1"].id_inquilino, registrado_por=x["u"].id_usuario, monto_pagado=Decimal("10.00"))
    pago = pagos_service.create_item(db, payload, x["u"].id_usuario)

    from modules.pagos.schemas import PagoUpdate
    with pytest.raises(HTTPException):
        pagos_service.update_item(db, pago, PagoUpdate(id_inquilino=x["i3"].id_inquilino))


def test_egreso_manual_no_permite_servicio_mensual_arbitrario(db):
    x = seed(db)
    sm = sm_service.create_item(db, ServicioMensualCreate(id_periodo=x["p"].id_periodo, id_servicio=x["luz"].id_servicio, id_casa=x["casa"].id_casa, id_cuarto=None, monto=Decimal("30.00"), responsable_pago="propietario"), x["u"].id_usuario)

    payload = EgresoCasaCreate(
        id_casa=x["casa"].id_casa,
        id_periodo=x["p"].id_periodo,
        id_servicio_mensual=sm.id_servicio_mensual,
        concepto="Manual manipulado",
        monto=Decimal("5.00"),
    )
    with pytest.raises(HTTPException):
        egresos_service.create_item(db, payload, x["u"].id_usuario)


def test_distribucion_manual_rechaza_alquiler_fuera_de_la_distribucion_calculada(db):
    x = seed(db)
    sm = sm_service.create_item(db, ServicioMensualCreate(id_periodo=x["p"].id_periodo, id_servicio=x["luz"].id_servicio, id_casa=x["casa"].id_casa, id_cuarto=x["c3"].id_cuarto, monto=Decimal("30.00"), responsable_pago="inquilino"), x["u"].id_usuario)

    payload = DistribucionManualUpdate(distribuciones=[
        DistribucionManualItem(id_alquiler=x["a1"].id_alquiler, monto_asignado=Decimal("30.00"))
    ])
    with pytest.raises(HTTPException):
        sm_service.guardar_distribuciones(db, sm.id_servicio_mensual, payload, x["u"].id_usuario)
