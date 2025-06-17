from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api.core.schemas import (
    SucursalCreateRequest,
    DepositoCreateRequest
)

from api.core.models import  Sucursal, Deposito
  
# SUCURSAL  
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

# DEPOSITO 
async def obtener_depositos(db: AsyncSession):
    result = await db.execute(select(Deposito).options(selectinload(Deposito.ciudad)))
    return result.scalars().all()


async def crear_deposito(db: AsyncSession, deposito: DepositoCreateRequest):
    nuevo_deposito = Deposito(**deposito.dict())
    db.add(nuevo_deposito)
    await db.commit()
    await db.refresh(nuevo_deposito)
    result = await db.execute(
        select(Deposito).options(selectinload(Deposito.ciudad)).where(Deposito.id == nuevo_deposito.id)
    )
    deposito_con_relacion = result.scalar_one()
    return deposito_con_relacion
