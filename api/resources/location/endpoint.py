from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.core import database
from .schemas import (
    PaisResponse,
    PaisCreateRequest,
    ProvinciaResponse,
    ProvinciaCreateRequest,
    CiudadResponse,
    CiudadCreateRequest,
)

from .dal import (
    obtener_ciudades,
    obtener_paises,
    obtener_provincias,
    crear_ciudad,
    crear_pais,
    crear_provincia
)

from ..auth.dal import get_current_active_user

router = APIRouter(
    dependencies=[Depends(get_current_active_user)],
)


async def get_db():
    async with database.AsyncSessionLocal() as session:
        yield session


@router.get("/ciudad/", response_model=list[CiudadResponse])
async def listarCiudades(db: AsyncSession = Depends(get_db)):
    return await obtener_ciudades(db)


@router.post("/ciudad/", response_model=CiudadResponse)
async def crearCiudad(ciudad: CiudadCreateRequest, db: AsyncSession = Depends(get_db)):
    return await crear_ciudad(db, ciudad)


@router.get("/provincia/", response_model=list[ProvinciaResponse])
async def listarProvincias(db: AsyncSession = Depends(get_db)):
    return await obtener_provincias(db)


@router.post("/provincia/", response_model=ProvinciaResponse)
async def crearProvincia(
    provincia: ProvinciaCreateRequest, db: AsyncSession = Depends(get_db)
):
    return await crear_provincia(db, provincia)

@router.get("/pais/", response_model=list[PaisResponse])
async def listarPaises(db: AsyncSession = Depends(get_db)):
    return await obtener_paises(db)

@router.post("/pais/", response_model=PaisResponse)
async def crearPais(pais: PaisCreateRequest, db: AsyncSession = Depends(get_db)):
    return await crear_pais(db, pais)
