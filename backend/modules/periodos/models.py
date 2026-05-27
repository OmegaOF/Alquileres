from datetime import date, datetime
from sqlalchemy import Date, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base
class PeriodoMensual(Base):
    __tablename__ = "periodos_mensuales"
    __table_args__ = (UniqueConstraint("anio", "mes", name="uq_periodo_anio_mes"),)
    id_periodo: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    anio: Mapped[int] = mapped_column(Integer, nullable=False)
    mes: Mapped[int] = mapped_column(Integer, nullable=False)
    nombre_periodo: Mapped[str] = mapped_column(String(20), nullable=False)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="abierto")
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    servicios_mensuales = relationship("ServicioMensual", back_populates="periodo")
    cobros = relationship("CobroMensual", back_populates="periodo")
    egresos = relationship("EgresoCasa", back_populates="periodo")
