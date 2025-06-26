from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from .schemas import (
    SucursalCreateRequest,
)
from api.core.models import Sucursal, Ciudad, Provincia


async def obtener_sucursales(db: AsyncSession):
    result = await db.execute(
        select(Sucursal).options(
            selectinload(Sucursal.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
    )
    return result.scalars().all()


async def crear_sucursal(db: AsyncSession, sucursal: SucursalCreateRequest):
    nueva_sucursal = Sucursal(**sucursal.dict())
    db.add(nueva_sucursal)
    await db.commit()
    await db.refresh(nueva_sucursal)
    result = await db.execute(
        select(Sucursal)
        .options(
            selectinload(Sucursal.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .where(Sucursal.id == nueva_sucursal.id)
    )
    sucursal_con_relacion = result.scalar_one()
    return sucursal_con_relacion
