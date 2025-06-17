from fastapi import FastAPI

import api.resources.cliente.endpoint
import api.resources.location.endpoint
import api.resources.stock.endpoint
import api.resources.producto.endpoint
import api.resources.proveedor.endpoint
from .resources.remito_devolucion.endpoints import router as remito_devolucion_router
from .resources.remito_compra.endpoints import router as remito_compra_router
from .resources.remito_transferencia import router as remito_transferencia_router
from .resources.remito_venta import router as remito_venta_router

from api.core.config import settings
from api.core import models
from api.core.database import engine, Base

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para la gestion de stocks",
    version="0.0.1"
)

"""
async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    print("Iniciando creación/verificación de tablas de base de datos...")
    await create_db_tables()
    print("Tablas de base de datos creadas (o verificadas) correctamente.")

 import api.deposito.endpoint """

prefix_base = "/api/v1"
app.include_router(api.resources.cliente.endpoint.router, prefix=f"{prefix_base}/cliente")
app.include_router(api.resources.location.endpoint.router, prefix=f"{prefix_base}/location")
app.include_router(api.resources.stock.endpoint.router, prefix=f"{prefix_base}/stock")
app.include_router(api.resources.producto.endpoint.router, prefix=f"{prefix_base}/producto")
app.include_router(api.resources.proveedor.endpoint.router, prefix=f"{prefix_base}/proveedor")
app.include_router(remito_devolucion_router, prefix=f"{prefix_base}/remito_devolucion")
app.include_router(remito_compra_router, prefix=f"{prefix_base}/remito_compra")
app.include_router(remito_transferencia_router, prefix=f"{prefix_base}/remito_transferencia")
app.include_router(remito_venta_router, prefix=f"{prefix_base}/remito_venta")

