from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from ...core.database import get_db


from .schemas import RemitoTransferenciaCreateRequest, RemitoTransferenciaResponse


from . import dal as remito_transferencia_dal


router = APIRouter(
    prefix="/remitos-transferencia",
    tags=["Remitos Transferencia"],
    responses={404: {"description": "Remito de transferencia no encontrado"}},
)

@router.post("/", response_model=RemitoTransferenciaResponse, status_code=status.HTTP_201_CREATED)
async def create_remito_transferencia_endpoint(
    remito_data: RemitoTransferenciaCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    
    db_remito = await remito_transferencia_dal.create_remito_transferencia(db, remito_data)
    return db_remito

@router.get("/{remito_id}", response_model=RemitoTransferenciaResponse)
async def get_remito_transferencia_by_id_endpoint(
    remito_id: int,
    db: AsyncSession = Depends(get_db)
):
    
    db_remito = await remito_transferencia_dal.get_remito_tranferencia_by_id(db, remito_id)
    if db_remito is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Remito de transferencia no encontrado")
    return db_remito

@router.get("/", response_model=List[RemitoTransferenciaResponse])
async def get_all_remitos_transferencia_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    
    remitos = await remito_transferencia_dal.get_all_remitos_transferencia(db, skip=skip, limit=limit)
    return remitos

@router.put("/{remito_id}", response_model=RemitoTransferenciaResponse)
async def update_remito_transferencia_endpoint(
    remito_id: int,
    remito_update: RemitoTransferenciaCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    
    updated_remito = await remito_transferencia_dal.update_remito_transferencia(db, remito_id, remito_update)
    if updated_remito is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Remito de transferencia no encontrado para actualizar")
    return updated_remito

@router.delete("/{remito_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_remito_transferenci_endpoint(
    remito_id: int,
    db: AsyncSession = Depends(get_db)
):
    
    was_deleted = await remito_transferencia_dal.delete_remito_transferencia(db, remito_id)
    if not was_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Remito de transferencia no encontrado para eliminar")
    return 