from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ...core.database import get_db
from .schemas import RemitoDevolucionCreateRequest, RemitoDevolucionResponse
from . import dal as remito_devolucion_dal

router=APIRouter(
    prefix="/remito_devolucion",
    tags=["Remito Devolucion"],
    responses={404: {"description":"Remito de devolución no encontrado"}}
)

@router.post("/", response_model=RemitoDevolucionResponse, status_code=status.HTTP_201_CREATED)
async def create_remito_devolucion_endpoint(
    remito_data:RemitoDevolucionCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    db_remito=await remito_devolucion_dal.create_remito_devolucion(db, remito_data)
    return db_remito

@router.get("/{remito_id}", response_model=RemitoDevolucionResponse)
async def get_remito_devolucion_by_id_endpoint(
    remito_id:int,
    db:AsyncSession=Depends(get_db)
):
    db_remito=await remito_devolucion_dal.get_remito_by_id(db, remito_id)
    if db_remito is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Remito de devolución no encontrado")
    return db_remito

@router.get("/", response_model=List[RemitoDevolucionResponse])
async def get_all_remitos_devolucion_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    remitos = await remito_devolucion_dal.get_all_remito_devolucion(db, skip=skip, limit=limit)
    return remitos

@router.put("/{remito_id}", response_model=RemitoDevolucionResponse)
async def update_remito_devolucion_endpoint(
    remito_id:int,
    remito_update: RemitoDevolucionCreateRequest,
    db: AsyncSession = Depends (get_db)
):
    updated_remito = await remito_devolucion_dal.update_remito_devolucion(db, remito_id, remito_update)
    if updated_remito is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Remito de devolución no encontrado para actualizar")
    return updated_remito

@router.delete("/{remito_id}", status_code=status.HTTP_404_NOT_FOUND)
async def delete_remito_devolucion_endpoint(
    remito_id: int,
    db: AsyncSession = Depends (get_db)
):
    was_deleted = await remito_devolucion_dal.delete_remito_devolucion(db, remito_id)
    if not was_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Remito de devolución no encontrado para eliminar")
    

