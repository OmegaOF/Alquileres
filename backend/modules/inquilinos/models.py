from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base
class Inquilino(Base):
    __tablename__ = "inquilinos"
    id_inquilino: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    ci: Mapped[str | None] = mapped_column(String(30))
    telefono: Mapped[str | None] = mapped_column(String(30))
    correo: Mapped[str | None] = mapped_column(String(150))
    direccion_referencia: Mapped[str | None] = mapped_column(String(255))
    contacto_emergencia: Mapped[str | None] = mapped_column(String(120))
    telefono_emergencia: Mapped[str | None] = mapped_column(String(30))
    estado: Mapped[str] = mapped_column(String(20), default="activo")
    observacion: Mapped[str | None] = mapped_column(Text)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    fecha_actualizacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    alquileres = relationship("Alquiler", back_populates="inquilino")
    cobros = relationship("CobroMensual", back_populates="inquilino")
    pagos = relationship("Pago", back_populates="inquilino")
