from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.core import database
from .schemas import ClienteResponse, ClienteCreateRequest
from .dal import obtener_clientes, crear_cliente

router = APIRouter()

async def get_db():
    async with database.AsyncSessionLocal() as session:
        yield session

@router.get("/", response_model = list[ClienteResponse])
async def listar(db: AsyncSession = Depends(get_db)):
    return await obtener_clientes(db)

@router.post("/", response_model = ClienteResponse)
async def crear(cliente: ClienteCreateRequest, db: AsyncSession = Depends(get_db)):
    return await crear_cliente(db, cliente)
