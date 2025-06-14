from fastapi import FastAPI
import api.cliente.endpoint
import api.deposito.endpoint
import api.core
import api.core.endpoint


from api.core.config import settings
from api.core import models
from api.core.database import engine, Base

from .resource.remito_devolucion.endpionts import router as remito_devolucion_router
from .resource.remito_compra.endpoints import router as remito_compra_router
from .resource.remito_transferencia import router as remito_transferencia_router
from . resource.remito_venta import router as remito_venta_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para la gestion de stocks",
    version="0.0.1")

app.include_router(remito_devolucion_router)
app.include_router(remito_compra_router)
app.include_router(remito_transferencia_router)
app.include_router(remito_venta_router)


async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    print("Iniciando creación/verificación de tablas de base de datos...")
    await create_db_tables()
    print("Tablas de base de datos creadas (o verificadas) correctamente.")

""" import api.deposito.endpoint """

prefix_base = "/api/v1"
app.include_router(api.cliente.endpoint.router, prefix=f"{prefix_base}/cliente")
app.include_router(api.core.endpoint.router, prefix=f"{prefix_base}/core")
app.include_router(api.deposito.endpoint.router, prefix=f"{prefix_base}/deposito")
