from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base

class Casa(Base):
    __tablename__ = "casas"
    id_casa: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_casa: Mapped[str] = mapped_column(String(120), nullable=False)
    direccion: Mapped[str] = mapped_column(String(255), nullable=False)
    zona: Mapped[str | None] = mapped_column(String(100))
    ciudad: Mapped[str | None] = mapped_column(String(100))
    descripcion: Mapped[str | None] = mapped_column(Text)
    estado: Mapped[str] = mapped_column(String(30), default="activa")
    id_usuario_responsable: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    fecha_actualizacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario_responsable = relationship("Usuario", back_populates="casas")
    cuartos = relationship("Cuarto", back_populates="casa")
    servicios_mensuales = relationship("ServicioMensual", back_populates="casa")
    cobros = relationship("CobroMensual", back_populates="casa")
    egresos = relationship("EgresoCasa", back_populates="casa")
