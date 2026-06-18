from datetime import date
from decimal import Decimal
import warnings

from sqlalchemy import create_engine
from sqlalchemy.exc import SAWarning
from sqlalchemy.orm import configure_mappers, sessionmaker
from sqlalchemy.orm.collections import InstrumentedList

from db import Base

# Import every mapped model so configure_mappers validates the full ORM graph.
from modules.alquileres.models import Alquiler
from modules.casas.models import Casa
from modules.cobros.models import CobroMensual, DetalleCobroMensual
from modules.cuartos.models import Cuarto
from modules.egresos.models import EgresoCasa  # noqa: F401
from modules.inquilinos.models import Inquilino
from modules.pagos.models import Pago
from modules.periodos.models import PeriodoMensual
from modules.servicios.models import Servicio
from modules.servicios_mensuales.models import ServicioMensual, DistribucionServicioMensual  # noqa: F401
from modules.usuarios.models import Usuario


def test_configure_mappers_without_detalle_cobro_alias_warning():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", SAWarning)
        configure_mappers()

    messages = [str(w.message) for w in caught]
    assert not any(
        "ServicioMensual.detalles_cobro" in msg and "detalle_cobro" in msg
        for msg in messages
    ), messages


def test_servicio_mensual_detalles_cobro_collection_and_pago_detalle_scalar():
    engine = create_engine("sqlite:///:memory:", future=True, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, future=True)

    with Session() as db:
        usuario = Usuario(nombre="Admin", correo="admin@example.com", password_hash="x")
        casa = Casa(nombre_casa="Casa A", direccion="Dir", usuario_responsable=usuario)
        cuarto = Cuarto(casa=casa, numero_cuarto="1", precio_alquiler=Decimal("100.00"))
        inquilino = Inquilino(nombre="Ana")
        alquiler = Alquiler(
            inquilino=inquilino,
            cuarto=cuarto,
            fecha_inicio=date(2026, 1, 1),
            monto_alquiler=Decimal("100.00"),
            dia_pago=5,
        )
        periodo = PeriodoMensual(
            anio=2026,
            mes=1,
            nombre_periodo="Enero 2026",
            fecha_inicio=date(2026, 1, 1),
            fecha_fin=date(2026, 1, 31),
            estado="abierto",
        )
        servicio = Servicio(nombre_servicio="Luz", estado="activo")
        servicio_mensual = ServicioMensual(
            periodo=periodo,
            servicio=servicio,
            casa=casa,
            cuarto=cuarto,
            monto=Decimal("30.00"),
            responsable_pago="inquilino",
            pagador_factura="propietario",
        )
        cobro = CobroMensual(
            periodo=periodo,
            alquiler=alquiler,
            casa=casa,
            cuarto=cuarto,
            inquilino=inquilino,
            monto_alquiler=Decimal("100.00"),
            monto_servicios=Decimal("30.00"),
            total_a_pagar=Decimal("130.00"),
            saldo_pendiente=Decimal("130.00"),
        )
        detalle = DetalleCobroMensual(
            cobro=cobro,
            tipo_concepto="servicio",
            concepto="Luz",
            monto=Decimal("30.00"),
            servicio_mensual=servicio_mensual,
        )
        pago = Pago(
            cobro=cobro,
            detalle_cobro=detalle,
            inquilino=inquilino,
            monto_pagado=Decimal("10.00"),
            registrado_por=1,
        )
        db.add_all([usuario, casa, cuarto, inquilino, alquiler, periodo, servicio, servicio_mensual, cobro, detalle, pago])
        db.commit()

        loaded_servicio_mensual = db.get(ServicioMensual, servicio_mensual.id_servicio_mensual)
        loaded_detalle = db.get(DetalleCobroMensual, detalle.id_detalle_cobro)
        loaded_pago = db.get(Pago, pago.id_pago)

        assert isinstance(loaded_servicio_mensual.detalles_cobro, InstrumentedList)
        assert loaded_servicio_mensual.detalles_cobro == [loaded_detalle]
        assert not hasattr(loaded_servicio_mensual, "detalle_cobro")
        assert loaded_detalle.servicio_mensual is loaded_servicio_mensual
        assert loaded_pago.detalle_cobro is loaded_detalle
