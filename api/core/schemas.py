from pydantic import BaseModel
from typing import Optional
from api.location.schemas import CiudadResponse

# REQUEST
class ClienteCreateRequest(BaseModel):
    nombre: str
    telefono: str
    email: str
    direccion: str
    id_ciudad: int
    
class PaisCreateRequest(BaseModel):
    nombre: str
    
class ProvinciaCreateRequest(BaseModel):
    nombre: str
    id_pais: int
    
class CiudadCreateRequest(BaseModel):
    nombre: str
    id_provincia: int
    
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
        
class PaisResponse(BaseModel):
    id: int
    nombre: str
    
    class Config:
        orm_mode = True
        
class ProvinciaResponse(BaseModel):
    id: int
    nombre: str
    pais: PaisResponse
    
    class Config:
        orm_mode = True

class CiudadResponse(BaseModel):
    id: int
    nombre: str
    provincia: ProvinciaResponse
    
    class Config:
        orm_mode = True