from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
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
    estado_pago: Mapped[str] = mapped_column(String(20), default="pendiente")
    metodo_pago: Mapped[str | None] = mapped_column(String(40))
    fecha_pago: Mapped[datetime | None] = mapped_column(DateTime)
    numero_comprobante: Mapped[str | None] = mapped_column(String(80))
    observacion: Mapped[str | None] = mapped_column(Text)
    estado: Mapped[str] = mapped_column(String(20), default="activo")
    fecha_anulacion: Mapped[datetime | None] = mapped_column(DateTime)
    motivo_anulacion: Mapped[str | None] = mapped_column(Text)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    periodo = relationship("PeriodoMensual", back_populates="servicios_mensuales")
    servicio = relationship("Servicio", back_populates="servicios_mensuales")
    casa = relationship("Casa", back_populates="servicios_mensuales")
    cuarto = relationship("Cuarto", back_populates="servicios_mensuales")
    detalle_cobro = relationship("DetalleCobroMensual", back_populates="servicio_mensual", uselist=False)
    egreso = relationship("EgresoCasa", back_populates="servicio_mensual", uselist=False)
