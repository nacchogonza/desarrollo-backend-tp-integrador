from pydantic import BaseModel
from typing import Optional


# REQUEST
class PaisCreateRequest(BaseModel):
    nombre: str
    
class ProvinciaCreateRequest(BaseModel):
    nombre: str
    id_pais: int
    
class CiudadCreateRequest(BaseModel):
    nombre: str
    id_provincia: int
    
# RESPONSE
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