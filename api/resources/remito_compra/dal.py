from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from .schemas import (
    RemitoCompraCreateRequest,
    RemitoCompraResponse,
)
from ...proveedor.schemas import ProveedorResponse
from ...producto.schemas import ProductoResponse
from ...deposito.schemas import DepositoResponse
from api.core.models import Cliente, Ciudad, Provincia, Pais, Stock, Sucursal, Deposito, Producto, Proveedor, RemitoCompra, RemitoVenta, RemitoDevolucion, RemitoTransferencia

async def create_remito_compra(db: AsyncSession, remito_data: RemitoCompraCreateRequest):
    
    db_remito = RemitoCompra(
        fecha=remito_data.fecha,
        cantidad=remito_data.cantidad,
        id_proveedor=remito_data.id_proveedor,
        id_producto=remito_data.id_producto,
        id_deposito=remito_data.id_deposito
    )
    
    db.add(db_remito)
    await db.commit()
    await db.refresh(db_remito)
    return db_remito

async def get_remito_compra_by_id(db: AsyncSession, remito_id: int):
   
    stmt = select(RemitoCompra).where(RemitoCompra.id == remito_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none() 

async def get_all_remitos_compra(db: AsyncSession, skip: int = 0, limit: int = 100):
    
    stmt = select(RemitoCompra).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all() 

async def update_remito_compra(db: AsyncSession, remito_id: int, remito_update: RemitoCompraCreateRequest):
    
    stmt = select(RemitoCompra).where(RemitoCompra.id == remito_id)
    result = await db.execute(stmt)
    db_remito = result.scalar_one_or_none()
    
    if db_remito:
        
        for key, value in remito_update.model_dump(exclude_unset=True).items():
            setattr(db_remito, key, value)
        await db.commit()
        await db.refresh(db_remito)
        return db_remito
    return None

async def delete_remito_compra(db: AsyncSession, remito_id: int):
    
    stmt = select(RemitoCompra).where(RemitoCompra.id == remito_id)
    result = await db.execute(stmt)
    db_remito = result.scalar_one_or_none()
    
    if db_remito:
        await db.delete(db_remito)
        await db.commit()
        return True
    return False