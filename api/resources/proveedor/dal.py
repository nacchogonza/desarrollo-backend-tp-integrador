from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api.resources.proveedor.schemas import (
   ProveedorCreateRequest
)
from api.core.models import Proveedor

async def obtener_proveedor(db: AsyncSession):
	result = await db.execute(select(Proveedor))
	return result.scalars().all()

async def crear_proveedor(db: AsyncSession, proveedor: ProveedorCreateRequest):
	nuevo_proveedor = Proveedor(**proveedor.dict())
	db.add(nuevo_proveedor)
	await db.commit()
	await db.refresh(nuevo_proveedor)
	return nuevo_proveedor