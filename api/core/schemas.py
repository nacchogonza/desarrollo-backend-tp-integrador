from pydantic import BaseModel

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
    
class StockCreateRequest(BaseModel):
    cantidad_sucursal: int
    cantidad_deposito: int
    id_producto: int
    id_sucursal: int
    id_deposito: int
    
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
        

class StockResponse(BaseModel):
    id: int
    cantidad_sucursal: int
    cantidad_deposito: int
    """ deposito: DepositoResponse
    sucursal: SucursalResponse
    producto: ProductoResponse """
    
    class Config:
        orm_mode = True
    