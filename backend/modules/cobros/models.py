from datetime import date, datetime
from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base
class CobroMensual(Base):
    __tablename__ = "cobros_mensuales"
    __table_args__ = (UniqueConstraint("id_periodo", "id_alquiler", name="uq_cobro_periodo_alquiler"),)
    id_cobro: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_periodo: Mapped[int] = mapped_column(ForeignKey("periodos_mensuales.id_periodo"), nullable=False)
    id_alquiler: Mapped[int] = mapped_column(ForeignKey("alquileres.id_alquiler"), nullable=False)
    id_casa: Mapped[int] = mapped_column(ForeignKey("casas.id_casa"), nullable=False)
    id_cuarto: Mapped[int] = mapped_column(ForeignKey("cuartos.id_cuarto"), nullable=False)
    id_inquilino: Mapped[int] = mapped_column(ForeignKey("inquilinos.id_inquilino"), nullable=False)
    monto_alquiler: Mapped[float] = mapped_column(Numeric(10,2), default=0)
    monto_servicios: Mapped[float] = mapped_column(Numeric(10,2), default=0)
    deuda_anterior: Mapped[float] = mapped_column(Numeric(10,2), default=0)
    descuentos: Mapped[float] = mapped_column(Numeric(10,2), default=0)
    recargos: Mapped[float] = mapped_column(Numeric(10,2), default=0)
    total_a_pagar: Mapped[float] = mapped_column(Numeric(10,2), default=0)
    total_pagado: Mapped[float] = mapped_column(Numeric(10,2), default=0)
    saldo_pendiente: Mapped[float] = mapped_column(Numeric(10,2), default=0)
    fecha_limite_pago: Mapped[date | None] = mapped_column(Date)
    estado: Mapped[str] = mapped_column(String(20), default="pendiente")
    fecha_generacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    observacion: Mapped[str | None] = mapped_column(Text)
    estado_recordatorio: Mapped[str] = mapped_column(String(30), default="no_preparado")
    fecha_ultimo_contacto: Mapped[datetime | None] = mapped_column(DateTime)
    observacion_recordatorio: Mapped[str | None] = mapped_column(Text)
    periodo = relationship("PeriodoMensual", back_populates="cobros")
    alquiler = relationship("Alquiler", back_populates="cobros")
    casa = relationship("Casa", back_populates="cobros")
    cuarto = relationship("Cuarto", back_populates="cobros")
    inquilino = relationship("Inquilino", back_populates="cobros")
    detalles = relationship("DetalleCobroMensual", back_populates="cobro")
    pagos = relationship("Pago", back_populates="cobro")

class DetalleCobroMensual(Base):
    __tablename__ = "detalle_cobro_mensual"
    id_detalle_cobro: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_cobro: Mapped[int] = mapped_column(ForeignKey("cobros_mensuales.id_cobro"), nullable=False)
    tipo_concepto: Mapped[str] = mapped_column(String(30), nullable=False)
    concepto: Mapped[str] = mapped_column(String(120), nullable=False)
    monto: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    id_servicio_mensual: Mapped[int | None] = mapped_column(ForeignKey("servicios_mensuales.id_servicio_mensual"))
    id_distribucion_servicio: Mapped[int | None] = mapped_column(ForeignKey("distribuciones_servicios_mensuales.id_distribucion_servicio"))
    descripcion: Mapped[str | None] = mapped_column(Text)
    cobro = relationship("CobroMensual", back_populates="detalles")
    pagos = relationship("Pago", back_populates="detalle_cobro")
    servicio_mensual = relationship("ServicioMensual", back_populates="detalles_cobro")
    distribucion_servicio = relationship("DistribucionServicioMensual")

    # Alias histórico de solo lectura; el nombre canónico es id_detalle_cobro.
    @property
    def id_detalle(self):
        return self.id_detalle_cobro
