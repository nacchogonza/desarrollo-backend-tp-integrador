from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from api.core.database import get_db
from api.resource.producto import dal
from api.resource.producto.schemas import (
    ProductoResponse, 
    ProductoCreateRequest,
    )

router = APIRouter()


@router.get("/", response_model= list[ProductoResponse])
async def listar(db: AsyncSession = Depends(get_db)):
    return await dal.obtener_productos(db)

@router.post("/", response_model= ProductoResponse)
async def crear_producto(producto: ProductoCreateRequest, db: AsyncSession = Depends(get_db)):
    return await dal.crear_producto(db, producto)