from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api.resources.cliente.schemas import (
    ClienteCreateRequest,
)
from api.core.models import Cliente, Ciudad, Provincia

# CLIENTE
async def obtener_clientes(db: AsyncSession):
    result = await db.execute(
        select(Cliente).options(
            selectinload(Cliente.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
    )
    return result.scalars().all()


async def crear_cliente(db: AsyncSession, cliente: ClienteCreateRequest):
    nuevo_cliente = Cliente(**cliente.dict())
    db.add(nuevo_cliente)
    await db.commit()
    await db.refresh(nuevo_cliente)

    result = await db.execute(
        select(Cliente)
        .options(
            selectinload(Cliente.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .where(Cliente.id == nuevo_cliente.id)
    )
    cliente_con_relacion = result.scalar_one()
    return cliente_con_relacion


