from datetime import date
from decimal import Decimal

from modules.alquileres.models import Alquiler
from modules.cobros.models import CobroMensual
from modules.cobros import service as cobros_service
from tests.test_servicios_mensuales_rules import seed


def _add_cobro(db, periodo, alquiler, casa, cuarto, inquilino, estado="pendiente"):
    cobro = CobroMensual(
        id_periodo=periodo.id_periodo,
        id_alquiler=alquiler.id_alquiler,
        id_casa=casa.id_casa,
        id_cuarto=cuarto.id_cuarto,
        id_inquilino=inquilino,
        monto_alquiler=Decimal("100.00"),
        monto_servicios=Decimal("0.00"),
        deuda_anterior=Decimal("0.00"),
        descuentos=Decimal("0.00"),
        recargos=Decimal("0.00"),
        total_a_pagar=Decimal("100.00"),
        total_pagado=Decimal("0.00"),
        saldo_pendiente=Decimal("100.00"),
        fecha_limite_pago=date(2026, 1, 5),
        estado=estado,
    )
    db.add(cobro)
    db.commit()
    return cobro


def test_cobranza_periodo_solo_muestra_ocupados_activos_con_nombre(db):
    x = seed(db)
    x["c1"].estado = "ocupado"
    x["c2"].estado = "libre"
    x["c3"].estado = "ocupado"
    activo = Alquiler(
        id_inquilino=x["i1"].id_inquilino,
        id_cuarto=x["c1"].id_cuarto,
        fecha_inicio=date(2026, 1, 1),
        monto_alquiler=100,
        monto_mensual=100,
        modalidad_alquiler="mensual",
        estado="activo",
    )
    libre = Alquiler(
        id_inquilino=x["i3"].id_inquilino,
        id_cuarto=x["c2"].id_cuarto,
        fecha_inicio=date(2026, 1, 1),
        monto_alquiler=100,
        monto_mensual=100,
        modalidad_alquiler="mensual",
        estado="activo",
    )
    finalizado = Alquiler(
        id_inquilino=x["i3"].id_inquilino,
        id_cuarto=x["c3"].id_cuarto,
        fecha_inicio=date(2026, 1, 1),
        monto_alquiler=100,
        monto_mensual=100,
        modalidad_alquiler="mensual",
        estado="finalizado",
    )
    db.add_all([activo, libre, finalizado])
    db.commit()

    _add_cobro(db, x["p"], activo, x["casa"], x["c1"], x["i1"].id_inquilino)
    _add_cobro(db, x["p"], libre, x["casa"], x["c2"], x["i3"].id_inquilino)
    _add_cobro(db, x["p"], finalizado, x["casa"], x["c3"], x["i3"].id_inquilino)

    rows = cobros_service.cobranza_periodo(db, x["p"].id_periodo)["items"]

    assert [row["id_alquiler"] for row in rows] == [activo.id_alquiler]
    assert rows[0]["nombre_inquilino"] == "Ana"
    assert rows[0]["inquilino"] == "Ana"
    assert rows[0]["nombre_casa"] == "Casa A"
    assert rows[0]["numero_cuarto"] == "1"
    assert rows[0]["estado_alquiler"] == "activo"
    assert rows[0]["estado_cuarto"] == "ocupado"


def test_cobranza_periodo_excluye_inquilino_inexistente_y_anulados(db):
    x = seed(db)
    x["c1"].estado = "ocupado"
    activo = Alquiler(
        id_inquilino=9999,
        id_cuarto=x["c1"].id_cuarto,
        fecha_inicio=date(2026, 1, 1),
        monto_alquiler=100,
        monto_mensual=100,
        modalidad_alquiler="mensual",
        estado="activo",
    )
    db.add(activo)
    db.commit()
    _add_cobro(db, x["p"], activo, x["casa"], x["c1"], 9999)

    rows = cobros_service.cobranza_periodo(db, x["p"].id_periodo)["items"]

    assert rows == []
