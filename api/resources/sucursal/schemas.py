from pydantic import BaseModel
from ..location.schemas import CiudadResponse

#REQUEST
class SucursalCreateRequest(BaseModel):
    nombre: str
    telefono: str
    email: str
    direccion: str
    id_ciudad: int

#RESPONSE
class SucursalResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    direccion: str
    ciudad: CiudadResponse

    class Config:
        orm_mode = True