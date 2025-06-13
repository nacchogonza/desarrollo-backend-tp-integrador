from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from .schemas import (
    CiudadCreateRequest,
    ProvinciaCreateRequest,
    PaisCreateRequest
)
from api.core.models import Pais, Ciudad, Provincia

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