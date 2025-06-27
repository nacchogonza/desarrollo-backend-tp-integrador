from fastapi import FastAPI

import api.resources.cliente.endpoint
import api.resources.location.endpoint
import api.resources.stock.endpoint
import api.resources.producto.endpoint
import api.resources.proveedor.endpoint

from .resources.remito_compra import router as remito_compra_router
from .resources.remito_devolucion import router as remito_devolucion_router
from .resources.remito_transferencia import router as remito_transferencia_router
from .resources.remito_venta import router as remito_venta_router
from .resources.deposito import router as deposito_router
from .resources.sucursal import router as sucursal_router

from api.core.config import settings
from api.core import models
from api.core.database import engine, Base

from .reports import routes as reports_routes

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para la gestion de stocks",
    version="0.0.1"
)
""""

async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    print("Iniciando creación/verificación de tablas de base de datos...")
    await create_db_tables()
    print("Tablas de base de datos creadas (o verificadas) correctamente.")
"""
 

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
app.include_router(deposito_router, prefix=f"{prefix_base}/deposito")
app.include_router(sucursal_router, prefix=f"{prefix_base}/sucursal")
app.include_router(reports_routes.router)
