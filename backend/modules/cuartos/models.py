from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base
class Cuarto(Base):
    __tablename__ = "cuartos"
    id_cuarto: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_casa: Mapped[int] = mapped_column(ForeignKey("casas.id_casa"), nullable=False)
    numero_cuarto: Mapped[str] = mapped_column(String(40), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text)
    precio_alquiler: Mapped[float] = mapped_column(Numeric(10,2), default=0)
    estado: Mapped[str] = mapped_column(String(30), default="libre")
    observacion: Mapped[str | None] = mapped_column(Text)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    fecha_actualizacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    casa = relationship("Casa", back_populates="cuartos")
    alquileres = relationship("Alquiler", back_populates="cuarto")
    servicios_mensuales = relationship("ServicioMensual", back_populates="cuarto")
    cobros = relationship("CobroMensual", back_populates="cuarto")
    egresos = relationship("EgresoCasa", back_populates="cuarto")
