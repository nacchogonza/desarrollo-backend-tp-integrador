from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api.core.schemas import (
    DepositoCreateRequest
)
from api.core.models import Deposito

async def obtener_deposito(db: AsyncSession):
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