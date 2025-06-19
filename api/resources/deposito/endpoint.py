from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.core import database
from api.resources.deposito import dal
from api.resources.deposito.schemas import (
    DepositoResponse,
    DepositoCreateRequest
)

router = APIRouter()


async def get_db():
    async with database.AsyncSessionLocal() as session:
        yield session

@router.get("/", response_model = list[DepositoResponse])
async def listar(db: AsyncSession = Depends(get_db)):
    return await dal.obtener_deposito(db)

@router.post("/", response_model = DepositoResponse)
async def crear_deposito(deposito: DepositoCreateRequest, db: AsyncSession = Depends(get_db)):
    return await dal.crear_deposito(db, deposito)