from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api.core.schemas import (
    ClienteCreateRequest,
    CiudadCreateRequest,
    ProvinciaCreateRequest,
    PaisCreateRequest, 
    StockCreateRequest,
    SucursalCreateRequest,
    DepositoCreateRequest
)
from api.core.models import Cliente, Ciudad, Provincia, Pais, Stock, Sucursal, Deposito

# CLIENTE
async def obtener_clientes(db: AsyncSession):
    result = await db.execute(
        select(Cliente).options(
            selectinload(Cliente.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
    )
    return result.scalars().all()


async def crear_cliente(db: AsyncSession, cliente: ClienteCreateRequest):
    nuevo_cliente = Cliente(**cliente.dict())
    db.add(nuevo_cliente)
    await db.commit()
    await db.refresh(nuevo_cliente)

    result = await db.execute(
        select(Cliente)
        .options(
            selectinload(Cliente.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .where(Cliente.id == nuevo_cliente.id)
    )
    cliente_con_relacion = result.scalar_one()
    return cliente_con_relacion


# CIUDAD
async def obtener_ciudades(db: AsyncSession):
    result = await db.execute(
        select(Ciudad).options(
            selectinload(Ciudad.provincia).selectinload(Provincia.pais)
        )
    )
    return result.scalars().all()


async def crear_ciudad(db: AsyncSession, ciudad: CiudadCreateRequest):
    nueva_ciudad = Ciudad(**ciudad.dict())
    db.add(nueva_ciudad)
    await db.commit()
    await db.refresh(nueva_ciudad)

    result = await db.execute(
        select(Ciudad)
        .options(selectinload(Ciudad.provincia).selectinload(Provincia.pais))
        .where(Ciudad.id == nueva_ciudad.id)
    )
    ciudad_con_relacion = result.scalar_one()
    return ciudad_con_relacion


# PROVINCIA
async def obtener_provincias(db: AsyncSession):
    result = await db.execute(select(Provincia).options(selectinload(Provincia.pais)))
    return result.scalars().all()


async def crear_provincia(db: AsyncSession, provincia: ProvinciaCreateRequest):
    nueva_provincia = Provincia(**provincia.dict())
    db.add(nueva_provincia)
    await db.commit()
    await db.refresh(nueva_provincia)
    result = await db.execute(
        select(Provincia)
        .options(selectinload(Provincia.pais))
        .where(Provincia.id == nueva_provincia.id)
    )
    provincia_con_relacion = result.scalar_one()
    return provincia_con_relacion


# PAIS
async def obtener_paises(db: AsyncSession):
    result = await db.execute(select(Pais))
    return result.scalars().all()


async def crear_pais(db: AsyncSession, pais: PaisCreateRequest):
    nuevo_pais = Pais(**pais.dict())
    db.add(nuevo_pais)
    await db.commit()
    await db.refresh(nuevo_pais)
    return nuevo_pais

# STOCK
async def obtener_stocks(db: AsyncSession):
    result = await db.execute(
        select(Stock).options(
            selectinload(Stock.producto)
            .selectinload(Stock.deposito)
            .selectinload(Stock.sucursal)
        )
    )
    return result.scalars().all()


async def crear_stock(db: AsyncSession, stock: StockCreateRequest):
    nuevo_stock = Stock(**stock.dict())
    db.add(nuevo_stock)
    await db.commit()
    await db.refresh(nuevo_stock)
    result = await db.execute(
        select(Stock)
        .options(
            selectinload(Stock.producto)
            .selectinload(Stock.deposito)
            .selectinload(Stock.sucursal)
        )
        .where(Stock.id == nuevo_stock.id)
    )
    stock_con_relacion = result.scalar_one()
    return stock_con_relacion
  
# SUCURSAL  
async def obtener_sucursales(db: AsyncSession):
    result = await db.execute(select(Sucursal).options(selectinload(Sucursal.ciudad)))
    return result.scalars().all()


async def crear_sucursal(db: AsyncSession, sucursal: SucursalCreateRequest):
    nueva_sucursal = Sucursal(**sucursal.dict())
    db.add(nueva_sucursal)
    await db.commit()
    await db.refresh(nueva_sucursal)
    result = await db.execute(
        select(Sucursal).options(selectinload(Sucursal.ciudad)).where(Sucursal.id == nueva_sucursal.id)
    )
    sucursal_con_relacion = result.scalar_one()
    return sucursal_con_relacion

# DEPOSITO 
async def obtener_depositos(db: AsyncSession):
    result = await db.execute(select(Deposito).options(selectinload(Deposito.ciudad)))
    return result.scalars().all()


async def crear_depostio(db: AsyncSession, deposito: DepositoCreateRequest):
    nuevo_deposito = Deposito(**deposito.dict())
    db.add(nuevo_deposito)
    await db.commit()
    await db.refresh(nuevo_deposito)
    result = await db.execute(
        select(Deposito).options(selectinload(Deposito.ciudad)).where(Deposito.id == nuevo_deposito.id)
    )
    deposito_con_relacion = result.scalar_one()
    return deposito_con_relacion
