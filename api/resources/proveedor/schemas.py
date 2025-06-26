from pydantic import BaseModel
from ..location.schemas import CiudadResponse

#Request
class ProveedorCreateRequest(BaseModel):
    nombre: str
    telefono: str
    email: str
    direccion: str
    id_ciudad: int

#Response
class ProveedorResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    direccion: str
    ciudad: CiudadResponse

    class Config:
        orm_mode = True
