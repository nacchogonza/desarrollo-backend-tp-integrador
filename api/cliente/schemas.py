from pydantic import BaseModel
from typing import Optional

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
    id_ciudad: int
    
    class Config:
        orm_mode = True