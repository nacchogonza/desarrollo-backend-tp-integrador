from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.core import dal, database
from api.core.schemas import (
    ProductoResponse, 
    ProductoCreateRequest, 
    ProveedorResponse, 
    ProveedorCreateRequest, 
    DepositoResponse,
    SucursalResponse,
    StockCreateRequest, 
    StockResponse, 
    SucursalCreateRequest,
    DepositoCreateRequest
)

router = APIRouter()


async def get_db():
    async with database.AsyncSessionLocal() as session:
        yield session


@router.get("/producto/", response_model= list[ProductoResponse])
async def listar(db: AsyncSession = Depends(get_db)):
    return await dal.obtener_productos(db)

@router.post("/producto/", response_model= ProductoResponse)
async def crear_producto(producto: ProductoCreateRequest, db: AsyncSession = Depends(get_db)):
    return await dal.crear_producto(db, producto)

@router.get("/proveedor/", response_model= list[ProveedorResponse])
async def listar(db: AsyncSession = Depends(get_db)):
    return await dal.obtener_proveedores(db)

@router.post("/proveedor/", response_model= ProveedorResponse)
async def crear_proveedor(proveedor: ProveedorCreateRequest, db: AsyncSession = Depends(get_db)):
    return await dal.crear_proveedor(db, proveedor)
  
@router.get("/stock/", response_model=list[StockResponse])
async def listar(db: AsyncSession = Depends(get_db)):
    return await dal.obtener_paises(db)

@router.post("/stock/", response_model=StockResponse)
async def crear_stock(stock: StockCreateRequest, db: AsyncSession = Depends(get_db)):
    return await dal.crear_stock(db, stock)

@router.get("/sucursal/", response_model = list[SucursalResponse])
async def listar(db: AsyncSession = Depends(get_db)):
    return await dal.obtener_sucursales(db)

@router.post("/sucursal/", response_model = SucursalResponse)
async def crear_sucursal(sucursal: SucursalCreateRequest, db: AsyncSession = Depends(get_db)):
    return await dal.crear_sucursal(db, sucursal)

@router.get("/deposito/", response_model = list[DepositoResponse])
async def listar(db: AsyncSession = Depends(get_db)):
    return await dal.obtener_depositos(db)

@router.post("/deposito/", response_model = DepositoResponse)
async def crear_deposito(deposito: DepositoCreateRequest, db: AsyncSession = Depends(get_db)):
    return await dal.crear_depostio(db, deposito)
