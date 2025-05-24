from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api.cliente.schemas import ClienteCreateRequest
from api.cliente.models import Cliente
from api import location

async def obtener_clientes(db: AsyncSession):
    result = await db.execute(select(Cliente).options(selectinload(Cliente.ciudad)))
    return result.scalars().all()

async def crear_cliente(db: AsyncSession, cliente: ClienteCreateRequest):
    nuevo_cliente = cliente.models.Cliente(**cliente)
    db.add(nuevo_cliente)
    await db.commit()
    await db.refresh(nuevo_cliente)
    return nuevo_cliente

