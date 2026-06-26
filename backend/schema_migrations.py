from sqlalchemy import inspect, text


def ensure_runtime_schema(engine):
    """Conservative create_all companion for SQLite/dev DBs; only adds missing nullable/default columns."""
    insp = inspect(engine)
    with engine.begin() as conn:
        if "alquileres" in insp.get_table_names():
            cols = {c["name"] for c in insp.get_columns("alquileres")}
            if "modalidad_alquiler" not in cols:
                conn.execute(text("ALTER TABLE alquileres ADD COLUMN modalidad_alquiler VARCHAR(20) DEFAULT 'mensual' NOT NULL"))
            if "monto_mensual" not in cols:
                conn.execute(text("ALTER TABLE alquileres ADD COLUMN monto_mensual NUMERIC(10,2)"))
                conn.execute(text("UPDATE alquileres SET monto_mensual = monto_alquiler WHERE monto_mensual IS NULL"))
            if "precio_diario" not in cols:
                conn.execute(text("ALTER TABLE alquileres ADD COLUMN precio_diario NUMERIC(10,2)"))
            if "total_alquiler_diario" not in cols:
                conn.execute(text("ALTER TABLE alquileres ADD COLUMN total_alquiler_diario NUMERIC(10,2)"))
        if "distribuciones_servicios_mensuales" not in insp.get_table_names():
            conn.execute(text("CREATE TABLE distribuciones_servicios_mensuales (id_distribucion_servicio INTEGER PRIMARY KEY, id_servicio_mensual INTEGER NOT NULL, id_alquiler INTEGER, dias_ocupados INTEGER DEFAULT 0, monto_asignado NUMERIC(10,2) DEFAULT 0, parte_propietario NUMERIC(10,2) DEFAULT 0, tipo_calculo VARCHAR(30) DEFAULT 'proporcional', estado VARCHAR(20) DEFAULT 'vigente', observacion TEXT, manual_confirmada VARCHAR(2) DEFAULT 'no', fecha_creacion DATETIME, FOREIGN KEY(id_servicio_mensual) REFERENCES servicios_mensuales(id_servicio_mensual), FOREIGN KEY(id_alquiler) REFERENCES alquileres(id_alquiler))"))

        if "cobros_mensuales" in insp.get_table_names():
            cols = {c["name"] for c in insp.get_columns("cobros_mensuales")}
            if "estado_recordatorio" not in cols:
                conn.execute(text("ALTER TABLE cobros_mensuales ADD COLUMN estado_recordatorio VARCHAR(30) DEFAULT 'no_preparado'"))
            if "fecha_ultimo_contacto" not in cols:
                conn.execute(text("ALTER TABLE cobros_mensuales ADD COLUMN fecha_ultimo_contacto DATETIME"))
            if "observacion_recordatorio" not in cols:
                conn.execute(text("ALTER TABLE cobros_mensuales ADD COLUMN observacion_recordatorio TEXT"))
        if "servicios_mensuales" in insp.get_table_names():
            cols = {c["name"] for c in insp.get_columns("servicios_mensuales")}
            if "estado" not in cols:
                conn.execute(text("ALTER TABLE servicios_mensuales ADD COLUMN estado VARCHAR(20) DEFAULT 'activo'"))
            if "fecha_anulacion" not in cols:
                conn.execute(text("ALTER TABLE servicios_mensuales ADD COLUMN fecha_anulacion DATETIME"))
            if "motivo_anulacion" not in cols:
                conn.execute(text("ALTER TABLE servicios_mensuales ADD COLUMN motivo_anulacion TEXT"))
            if "pagador_factura" not in cols:
                conn.execute(text("ALTER TABLE servicios_mensuales ADD COLUMN pagador_factura VARCHAR(30) DEFAULT 'propietario'"))
                conn.execute(text("UPDATE servicios_mensuales SET pagador_factura = CASE WHEN responsable_pago = 'propietario' THEN 'propietario' ELSE 'inquilino_directo' END WHERE pagador_factura IS NULL"))

            if "estado_recordatorio" not in cols:
                conn.execute(text("ALTER TABLE servicios_mensuales ADD COLUMN estado_recordatorio VARCHAR(30) DEFAULT 'no_preparado'"))
            if "fecha_ultimo_contacto" not in cols:
                conn.execute(text("ALTER TABLE servicios_mensuales ADD COLUMN fecha_ultimo_contacto DATETIME"))
            if "observacion_recordatorio" not in cols:
                conn.execute(text("ALTER TABLE servicios_mensuales ADD COLUMN observacion_recordatorio TEXT"))
        if "detalle_cobro_mensual" in insp.get_table_names():
            cols = {c["name"] for c in insp.get_columns("detalle_cobro_mensual")}
            if "id_distribucion_servicio" not in cols:
                conn.execute(text("ALTER TABLE detalle_cobro_mensual ADD COLUMN id_distribucion_servicio INTEGER"))
        if "distribuciones_servicios_mensuales" in insp.get_table_names():
            cols = {c["name"] for c in insp.get_columns("distribuciones_servicios_mensuales")}
            if "manual_confirmada" not in cols:
                conn.execute(text("ALTER TABLE distribuciones_servicios_mensuales ADD COLUMN manual_confirmada VARCHAR(2) DEFAULT 'no'"))
        if "egresos_casa" in insp.get_table_names():
            cols = {c["name"] for c in insp.get_columns("egresos_casa")}
            if "estado" not in cols:
                conn.execute(text("ALTER TABLE egresos_casa ADD COLUMN estado VARCHAR(20) DEFAULT 'activo'"))
            if "fecha_anulacion" not in cols:
                conn.execute(text("ALTER TABLE egresos_casa ADD COLUMN fecha_anulacion DATETIME"))

        if "servicios_activos_inmueble" not in insp.get_table_names():
            conn.execute(text("CREATE TABLE servicios_activos_inmueble (id_servicio_activo INTEGER PRIMARY KEY, id_servicio INTEGER NOT NULL, id_casa INTEGER NOT NULL, id_cuarto INTEGER, alcance VARCHAR(20) DEFAULT 'casa', responsable_pago VARCHAR(20) DEFAULT 'inquilino', pagador_factura VARCHAR(30) DEFAULT 'propietario', monto_base NUMERIC(10,2), estado VARCHAR(20) DEFAULT 'activo', observacion TEXT, fecha_creacion DATETIME, FOREIGN KEY(id_servicio) REFERENCES servicios(id_servicio), FOREIGN KEY(id_casa) REFERENCES casas(id_casa), FOREIGN KEY(id_cuarto) REFERENCES cuartos(id_cuarto))"))
