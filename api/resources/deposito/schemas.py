from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)