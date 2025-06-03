from pydantic import BaseModel
from datetime import date

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

class ProductoCreateRequest(BaseModel):
    nombre: str
    descripcion: str
    categoria: str
    precioCompra: float
    precioVenta: float

class ProveedorCreateRequest(BaseModel):
    nombre: str
    direccion: str
    id_ciudad: int
    telefono: str
    email: str
    condicionRecepcion: date

    
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
class ClienteResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    direccion: str
    ciudad: CiudadResponse
    
    class Config:
        orm_mode = True
    
class ProductoResponse(BaseModel):
    nombre: str
    descripcion: str
    categoria: str
    precioCompra: float
    precioVenta: float

    class Config:
        orm_mode = True

class ProveedorResponse(BaseModel):
    nombre: str
    direccion: str
    telefono: str
    email: str
    condicionRecepcion: date
    ciudad: CiudadResponse

    class Config:
        orm_mode = True