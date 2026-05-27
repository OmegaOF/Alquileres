from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base
class Pago(Base):
    __tablename__ = "pagos"
    id_pago: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_cobro: Mapped[int] = mapped_column(ForeignKey("cobros_mensuales.id_cobro"), nullable=False)
    id_detalle_cobro: Mapped[int | None] = mapped_column(ForeignKey("detalle_cobro_mensual.id_detalle_cobro"))
    id_inquilino: Mapped[int] = mapped_column(ForeignKey("inquilinos.id_inquilino"), nullable=False)
    monto_pagado: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    fecha_pago: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    metodo_pago: Mapped[str | None] = mapped_column(String(40))
    numero_comprobante: Mapped[str | None] = mapped_column(String(80))
    imagen_comprobante: Mapped[str | None] = mapped_column(String(255))
    registrado_por: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"), nullable=False)
    observacion: Mapped[str | None] = mapped_column(Text)
    estado: Mapped[str] = mapped_column(String(20), default="valido")
    cobro = relationship("CobroMensual", back_populates="pagos")
    detalle_cobro = relationship("DetalleCobroMensual", back_populates="pagos")
    inquilino = relationship("Inquilino", back_populates="pagos")
    usuario_registrador = relationship("Usuario", back_populates="pagos_registrados")
