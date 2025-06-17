from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.core import dal, database
from api.core.schemas import ClienteResponse, ClienteCreateRequest

router = APIRouter()

async def get_db():
    async with database.AsyncSessionLocal() as session:
        yield session

@router.get("/", response_model = list[ClienteResponse])
async def listar(db: AsyncSession = Depends(get_db)):
    return await dal.obtener_clientes(db)

@router.post("/", response_model = ClienteResponse)
async def crear(cliente: ClienteCreateRequest, db: AsyncSession = Depends(get_db)):
    return await dal.crear_cliente(db, cliente)
