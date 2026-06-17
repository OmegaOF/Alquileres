from sqlalchemy.orm import Session
from modules.alquileres.models import Alquiler
from modules.periodos.models import PeriodoMensual


def alquiler_del_cuarto_en_periodo(db: Session, id_cuarto: int, periodo: PeriodoMensual) -> Alquiler | None:
    """Return the rental whose dates overlap the monthly period for a room.

    Overlap rule: rental starts on/before period end and has no end date or ends on/after
    period start. This supports historical periods better than checking estado == activo.
    If multiple records overlap because of inconsistent data, the most recent start wins.
    """
    return (
        db.query(Alquiler)
        .filter(
            Alquiler.id_cuarto == id_cuarto,
            Alquiler.fecha_inicio <= periodo.fecha_fin,
            (Alquiler.fecha_fin.is_(None)) | (Alquiler.fecha_fin >= periodo.fecha_inicio),
            Alquiler.estado != "cancelado",
        )
        .order_by(Alquiler.fecha_inicio.desc(), Alquiler.id_alquiler.desc())
        .first()
    )
