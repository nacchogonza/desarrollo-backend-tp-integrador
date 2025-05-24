from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api import cliente
from api import location

async def obtener_clientes(db: AsyncSession):
    result = await db.execute(select(cliente.models.Cliente).options(selectinload(cliente.models.Cliente.ciudad)))
    return result.scalars().all()

async def crear_cliente(db: AsyncSession, cliente: cliente.schemas.ClienteCreateRequest):
    nuevo_cliente = cliente.models.Cliente(**cliente)
    db.add(nuevo_cliente)
    await db.commit()
    await db.refresh(nuevo_cliente)
    return nuevo_cliente

