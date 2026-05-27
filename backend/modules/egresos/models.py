from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base
class EgresoCasa(Base):
    __tablename__ = "egresos_casa"
    id_egreso: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_casa: Mapped[int] = mapped_column(ForeignKey("casas.id_casa"), nullable=False)
    id_periodo: Mapped[int] = mapped_column(ForeignKey("periodos_mensuales.id_periodo"), nullable=False)
    id_cuarto: Mapped[int | None] = mapped_column(ForeignKey("cuartos.id_cuarto"))
    id_servicio_mensual: Mapped[int | None] = mapped_column(ForeignKey("servicios_mensuales.id_servicio_mensual"))
    concepto: Mapped[str] = mapped_column(String(120), nullable=False)
    categoria: Mapped[str] = mapped_column(String(30), default="otro")
    monto: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    fecha_egreso: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    metodo_pago: Mapped[str | None] = mapped_column(String(40))
    numero_comprobante: Mapped[str | None] = mapped_column(String(80))
    comprobante: Mapped[str | None] = mapped_column(String(255))
    observacion: Mapped[str | None] = mapped_column(Text)
    registrado_por: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    casa = relationship("Casa", back_populates="egresos")
    periodo = relationship("PeriodoMensual", back_populates="egresos")
    cuarto = relationship("Cuarto", back_populates="egresos")
    servicio_mensual = relationship("ServicioMensual", back_populates="egreso")
    usuario_registrador = relationship("Usuario", back_populates="egresos_registrados")
