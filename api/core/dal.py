from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.cliente import models, schemas

async def crear_cliente(db: AsyncSession, cliente: schemas.ClienteCreateRequest):
    nuevo_cliente = models.Cliente(**cliente)
    db.add(nuevo_cliente)
    await db.commit()
    await db.refresh(nuevo_cliente)
    return nuevo_cliente


async def obtener_clientes(db: AsyncSession):
    result = await db.execute(select(models.Cliente))
    return result.scalars().all()