from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.resource.proveedor import dal
from api.core import database
from api.resource.proveedor.schemas import (
    ProveedorResponse, 
    ProveedorCreateRequest, 
)

router = APIRouter()


async def get_db():
    async with database.AsyncSessionLocal() as session:
        yield session

@router.get("/", response_model= list[ProveedorResponse])
async def listar(db: AsyncSession = Depends(get_db)):
    return await dal.obtener_proveedor(db)

@router.post("/", response_model= ProveedorResponse)
async def crear_proveedor(proveedor: ProveedorCreateRequest, db: AsyncSession = Depends(get_db)):
    return await dal.crear_proveedor(db, proveedor)