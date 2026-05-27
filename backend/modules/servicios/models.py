from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base
class Servicio(Base):
    __tablename__ = "servicios"
    id_servicio: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_servicio: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text)
    estado: Mapped[str] = mapped_column(String(20), default="activo")
    servicios_mensuales = relationship("ServicioMensual", back_populates="servicio")
