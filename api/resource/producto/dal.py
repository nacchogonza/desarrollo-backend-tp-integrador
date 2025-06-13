from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api.resource.producto.schemas import (
   ProductoCreateRequest
)
from api.core.models import Producto

async def obtener_productos(db: AsyncSession):
	result = await db.execute(select(Producto))
	return result.scalars().all()

async def crear_producto(db: AsyncSession, producto: ProductoCreateRequest):
	nuevo_producto = Producto(**producto.dict())
	db.add(nuevo_producto)
	await db.commit()
	await db.refresh(nuevo_producto)
	return nuevo_producto