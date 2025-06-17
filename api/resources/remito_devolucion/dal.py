from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from .schemas import (
    RemitoDevolucionCreateRequest,
    RemitoDevolucionResponse,
)
from ...cliente.schemas import ClienteResponse
from ...producto.schemas import ProductoResponse
from ...sucursal.schemas import SucursalResponse
from api.core.models import RemitoDevolucion

async def create_remito_devolucion(db: AsyncSession, remito_data: RemitoDevolucionCreateRequest):
    
    db_remito = RemitoDevolucion(
        fecha=remito_data.fecha,
        cantidad=remito_data.cantidad,
        id_cliente=remito_data.id_cliente,
        id_producto=remito_data.id_producto,
        id_sucursal=remito_data.id_sucursal
    )
    db.add(db_remito)
    await db.commit()
    await db.refresh(db_remito)
    return db_remito

async def get_remito_devolucion_by_id(db: AsyncSession, remito_id: int):
    
    stmt = select(RemitoDevolucion).where(RemitoDevolucion.id == remito_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none() # Obtiene un único resultado o None

async def get_all_remitos_devolucion(db: AsyncSession, skip: int = 0, limit: int = 100):
    
    stmt = select(RemitoDevolucion).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def update_remito_devolucion(db: AsyncSession, remito_id: int, remito_update: RemitoDevolucionCreateRequest):
   
    stmt = select(RemitoDevolucion).where(RemitoDevolucion.id == remito_id)
    result = await db.execute(stmt)
    db_remito = result.scalar_one_or_none()
    
    if db_remito:
        
        for key, value in remito_update.model_dump(exclude_unset=True).items():
            setattr(db_remito, key, value)
        await db.commit()
        await db.refresh(db_remito)
        return db_remito
    return None

async def delete_remito_devolucion(db: AsyncSession, remito_id: int):
    
    stmt = select(RemitoDevolucion).where(RemitoDevolucion.id == remito_id)
    result = await db.execute(stmt)
    db_remito = result.scalar_one_or_none()
    
    if db_remito:
        await db.delete(db_remito)
        await db.commit()
        return True
    return False