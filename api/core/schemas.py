from datetime import date
from pydantic import BaseModel
from datetime import date

from api.resources.location.schemas import CiudadResponse


# REQUEST
class SucursalCreateRequest(BaseModel):
    nombre: str
    telefono: str
    email: str
    direccion: str
    id_ciudad: int


class DepositoCreateRequest(BaseModel):
    nombre: str
    telefono: int
    email: str
    direccion: str
    id_ciudad: int


class SucursalResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    direccion: str
    ciudad: CiudadResponse

    class Config:
        orm_mode = True
        
class DepositoResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    direccion: str

    class Config:
        orm_mode = True
