from datetime import date, datetime
from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base
class Alquiler(Base):
    __tablename__ = "alquileres"
    id_alquiler: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_inquilino: Mapped[int] = mapped_column(ForeignKey("inquilinos.id_inquilino"), nullable=False)
    id_cuarto: Mapped[int] = mapped_column(ForeignKey("cuartos.id_cuarto"), nullable=False)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[date | None] = mapped_column(Date)
    monto_alquiler: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    modalidad_alquiler: Mapped[str] = mapped_column(String(20), default="mensual", nullable=False)
    monto_mensual: Mapped[float | None] = mapped_column(Numeric(10,2))
    precio_diario: Mapped[float | None] = mapped_column(Numeric(10,2))
    total_alquiler_diario: Mapped[float | None] = mapped_column(Numeric(10,2))
    dia_pago: Mapped[int] = mapped_column(Integer, default=1)
    garantia: Mapped[float | None] = mapped_column(Numeric(10,2))
    estado: Mapped[str] = mapped_column(String(20), default="activo")
    observacion: Mapped[str | None] = mapped_column(Text)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    fecha_actualizacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inquilino = relationship("Inquilino", back_populates="alquileres")
    cuarto = relationship("Cuarto", back_populates="alquileres")
    cobros = relationship("CobroMensual", back_populates="alquiler")
