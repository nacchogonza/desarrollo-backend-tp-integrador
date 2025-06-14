from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api.core.schemas import (
    SucursalCreateRequest,
)
from api.core.models import Sucursal

async def obtener_sucursales(db: AsyncSession):
    result = await db.execute(select(Sucursal).options(selectinload(Sucursal.ciudad)))
    return result.scalars().all()


async def crear_sucursal(db: AsyncSession, sucursal: SucursalCreateRequest):
    nueva_sucursal = Sucursal(**sucursal.dict())
    db.add(nueva_sucursal)
    await db.commit()
    await db.refresh(nueva_sucursal)
    result = await db.execute(
        select(Sucursal).options(selectinload(Sucursal.ciudad)).where(Sucursal.id == nueva_sucursal.id)
    )
    sucursal_con_relacion = result.scalar_one()
    return sucursal_con_relacion