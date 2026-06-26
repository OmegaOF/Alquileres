from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base
class ServicioMensual(Base):
    __tablename__ = "servicios_mensuales"
    id_servicio_mensual: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_periodo: Mapped[int] = mapped_column(ForeignKey("periodos_mensuales.id_periodo"), nullable=False)
    id_servicio: Mapped[int] = mapped_column(ForeignKey("servicios.id_servicio"), nullable=False)
    id_casa: Mapped[int] = mapped_column(ForeignKey("casas.id_casa"), nullable=False)
    id_cuarto: Mapped[int | None] = mapped_column(ForeignKey("cuartos.id_cuarto"))
    monto: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    responsable_pago: Mapped[str] = mapped_column(String(20), default="inquilino")
    # pagador_factura: quien hizo el desembolso real (propietario o inquilino_directo).
    # responsable_pago queda como compatibilidad histórica y representa el destino de cobro inicial.
    pagador_factura: Mapped[str] = mapped_column(String(30), default="propietario")
    estado_pago: Mapped[str] = mapped_column(String(20), default="pendiente")
    metodo_pago: Mapped[str | None] = mapped_column(String(40))
    fecha_pago: Mapped[datetime | None] = mapped_column(DateTime)
    numero_comprobante: Mapped[str | None] = mapped_column(String(80))
    observacion: Mapped[str | None] = mapped_column(Text)
    estado_recordatorio: Mapped[str] = mapped_column(String(30), default="no_preparado")
    fecha_ultimo_contacto: Mapped[datetime | None] = mapped_column(DateTime)
    observacion_recordatorio: Mapped[str | None] = mapped_column(Text)
    estado: Mapped[str] = mapped_column(String(20), default="activo")
    fecha_anulacion: Mapped[datetime | None] = mapped_column(DateTime)
    motivo_anulacion: Mapped[str | None] = mapped_column(Text)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    periodo = relationship("PeriodoMensual", back_populates="servicios_mensuales")
    servicio = relationship("Servicio", back_populates="servicios_mensuales")
    casa = relationship("Casa", back_populates="servicios_mensuales")
    cuarto = relationship("Cuarto", back_populates="servicios_mensuales")
    detalles_cobro = relationship("DetalleCobroMensual", back_populates="servicio_mensual")
    egreso = relationship("EgresoCasa", back_populates="servicio_mensual", uselist=False)
    distribuciones = relationship("DistribucionServicioMensual", back_populates="servicio_mensual")

class DistribucionServicioMensual(Base):
    __tablename__ = "distribuciones_servicios_mensuales"
    id_distribucion_servicio: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_servicio_mensual: Mapped[int] = mapped_column(ForeignKey("servicios_mensuales.id_servicio_mensual"), nullable=False)
    id_alquiler: Mapped[int | None] = mapped_column(ForeignKey("alquileres.id_alquiler"))
    dias_ocupados: Mapped[int] = mapped_column(Integer, default=0)
    monto_asignado: Mapped[float] = mapped_column(Numeric(10,2), default=0)
    parte_propietario: Mapped[float] = mapped_column(Numeric(10,2), default=0)
    tipo_calculo: Mapped[str] = mapped_column(String(30), default="proporcional")
    manual_confirmada: Mapped[str] = mapped_column(String(2), default="no")
    estado: Mapped[str] = mapped_column(String(20), default="vigente")
    observacion: Mapped[str | None] = mapped_column(Text)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    servicio_mensual = relationship("ServicioMensual", back_populates="distribuciones")
    alquiler = relationship("Alquiler")


class ServicioActivoInmueble(Base):
    __tablename__ = "servicios_activos_inmueble"
    __table_args__ = (UniqueConstraint("id_servicio", "id_casa", "id_cuarto", "alcance", name="uq_servicio_activo_inmueble"),)
    id_servicio_activo: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_servicio: Mapped[int] = mapped_column(ForeignKey("servicios.id_servicio"), nullable=False)
    id_casa: Mapped[int] = mapped_column(ForeignKey("casas.id_casa"), nullable=False)
    id_cuarto: Mapped[int | None] = mapped_column(ForeignKey("cuartos.id_cuarto"))
    alcance: Mapped[str] = mapped_column(String(20), default="casa")
    responsable_pago: Mapped[str] = mapped_column(String(20), default="inquilino")
    pagador_factura: Mapped[str] = mapped_column(String(30), default="propietario")
    monto_base: Mapped[float | None] = mapped_column(Numeric(10,2))
    estado: Mapped[str] = mapped_column(String(20), default="activo")
    observacion: Mapped[str | None] = mapped_column(Text)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    servicio = relationship("Servicio")
    casa = relationship("Casa")
    cuarto = relationship("Cuarto")
