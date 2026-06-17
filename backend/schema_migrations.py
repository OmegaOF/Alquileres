from sqlalchemy import inspect, text


def ensure_runtime_schema(engine):
    """Conservative create_all companion for SQLite/dev DBs; only adds missing nullable/default columns."""
    insp = inspect(engine)
    with engine.begin() as conn:
        if "servicios_mensuales" in insp.get_table_names():
            cols = {c["name"] for c in insp.get_columns("servicios_mensuales")}
            if "estado" not in cols:
                conn.execute(text("ALTER TABLE servicios_mensuales ADD COLUMN estado VARCHAR(20) DEFAULT 'activo'"))
            if "fecha_anulacion" not in cols:
                conn.execute(text("ALTER TABLE servicios_mensuales ADD COLUMN fecha_anulacion DATETIME"))
            if "motivo_anulacion" not in cols:
                conn.execute(text("ALTER TABLE servicios_mensuales ADD COLUMN motivo_anulacion TEXT"))
        if "egresos_casa" in insp.get_table_names():
            cols = {c["name"] for c in insp.get_columns("egresos_casa")}
            if "estado" not in cols:
                conn.execute(text("ALTER TABLE egresos_casa ADD COLUMN estado VARCHAR(20) DEFAULT 'activo'"))
            if "fecha_anulacion" not in cols:
                conn.execute(text("ALTER TABLE egresos_casa ADD COLUMN fecha_anulacion DATETIME"))
