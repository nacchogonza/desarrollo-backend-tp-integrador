from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.core import dal, database
from api.core.schemas import ClienteResponse, ClienteCreateRequest

from ..auth import get_current_active_user, User

router = APIRouter()

async def get_db():
    async with database.AsyncSessionLocal() as session:
        yield session

@router.get("/", response_model = list[ClienteResponse])
async def listar(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return await dal.obtener_clientes(db)

@router.post("/", response_model = ClienteResponse)
async def crear(cliente: ClienteCreateRequest, db: AsyncSession = Depends(get_db)):
    return await dal.crear_cliente(db, cliente)
