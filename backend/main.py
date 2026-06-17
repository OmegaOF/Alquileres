from fastapi import FastAPI
from db import Base, engine
from modules.auth.router import router as auth_router
from modules.usuarios.router import router as usuarios_router
from modules.casas.router import router as casas_router
from modules.cuartos.router import router as cuartos_router
from modules.inquilinos.router import router as inquilinos_router
from modules.alquileres.router import router as alquileres_router
from modules.periodos.router import router as periodos_router
from modules.servicios.router import router as servicios_router
from modules.servicios_mensuales.router import router as servicios_mensuales_router
from modules.cobros.router import router as cobros_router
from modules.pagos.router import router as pagos_router
from modules.egresos.router import router as egresos_router
from modules.reportes.router import router as reportes_router
from modules.dashboard.router import router as dashboard_router
from schema_migrations import ensure_runtime_schema

from modules.usuarios import models as _u
from modules.casas import models as _c
from modules.cuartos import models as _cu
from modules.inquilinos import models as _i
from modules.alquileres import models as _a
from modules.periodos import models as _p
from modules.servicios import models as _s
from modules.servicios_mensuales import models as _sm
from modules.cobros import models as _co
from modules.pagos import models as _pa
from modules.egresos import models as _e

app = FastAPI(title="Sistema Alquileres")
Base.metadata.create_all(bind=engine)
ensure_runtime_schema(engine)

@app.get('/api/health')
def health(): return {"ok": True}

for r in [auth_router,usuarios_router,casas_router,cuartos_router,inquilinos_router,alquileres_router,periodos_router,servicios_router,servicios_mensuales_router,cobros_router,pagos_router,egresos_router,reportes_router,dashboard_router]:
    app.include_router(r)
