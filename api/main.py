from fastapi import FastAPI
import api.cliente.endpoint
import api.deposito.endpoint
import api.core
import api.core.endpoint


from api.core.config import settings
from api.core import models
from api.core.database import engine, Base

app = FastAPI(title=settings.PROJECT_NAME)

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
