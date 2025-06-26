from pydantic import BaseModel
from ..location.schemas import CiudadResponse

#REQUEST

class DepositoCreateRequest(BaseModel):
    nombre: str
    telefono: str
    email: str
    direccion: str
    id_ciudad: int

#RESPONSE

class DepositoResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    direccion: str
    ciudad: CiudadResponse

    class Config:
        orm_mode = True