from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from ...core.database import get_db


from .schemas import RemitoCompraCreateRequest, RemitoCompraResponse


from . import dal as remito_compra_dal

from ..auth.dal import get_current_active_user

router = APIRouter(
    responses={404: {"description": "Remito de Compra no encontrado"}},
    dependencies=[Depends(get_current_active_user)],
)

@router.post(
    "/", response_model=RemitoCompraResponse, status_code=status.HTTP_201_CREATED
)
async def create_remito_compra_endpoint(
    remito_data: RemitoCompraCreateRequest, db: AsyncSession = Depends(get_db)
):
    db_remito = await remito_compra_dal.create_remito_compra(db, remito_data)
    return db_remito


@router.get("/{remito_id}", response_model=RemitoCompraResponse)
async def get_remito_compra_by_id_endpoint(
    remito_id: int, db: AsyncSession = Depends(get_db)
):

    db_remito = await remito_compra_dal.get_remito_compra_by_id(db, remito_id)
    if db_remito is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Remito de compra no encontrado",
        )
    return db_remito


@router.get("/", response_model=List[RemitoCompraResponse])
async def get_all_remitos_compra_endpoint(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):

    remitos = await remito_compra_dal.get_all_remitos_compra(db, skip=skip, limit=limit)
    return remitos


@router.put("/{remito_id}", response_model=RemitoCompraResponse)
async def update_remito_compra_endpoint(
    remito_id: int,
    remito_update: RemitoCompraCreateRequest,
    db: AsyncSession = Depends(get_db),
):

    updated_remito = await remito_compra_dal.update_remito_compra(
        db, remito_id, remito_update
    )
    if updated_remito is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Remito de compra no encontrado para actualizar",
        )
    return updated_remito


@router.delete("/{remito_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_remito_compra_endpoint(
    remito_id: int, db: AsyncSession = Depends(get_db)
):

    was_deleted = await remito_compra_dal.delete_remito_compra(db, remito_id)
    if not was_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Remito de compra no encontrado para eliminar",
        )
    return
