from pydantic import BaseModel
from api.core.schemas import CiudadResponse

# REQUEST
class ClienteCreateRequest(BaseModel):
    nombre: str
    telefono: str
    email: str
    direccion: str
    id_ciudad: int

# RESPONSE
class ClienteResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    direccion: str
    ciudad: CiudadResponse

    class Config:
        orm_mode = True
