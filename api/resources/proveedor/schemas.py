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

#PARA LA FUNCIONALIDAD DE REPORTE DE PROVEEDORES (SEGUN CHATGPT):

class ProductoReporte(BaseModel):  #(Deberia estar en producto/schemas.py?)
    id: int                          #representa los productos dentro del reporte, incluyendo el precio.
    nombre: str
    descripcion: str
    categoria: str
    precioCompra: float
    precioVenta: float

    class config:
        orm_mode= True

class ProveedorReporte(BaseModel):     #Incluye todos los datos del proveedor y, lo más importante, una lista de productos
    id: int
    nombre: str
    telefono: str
    email: str
    direccion: str
    Ciudad: CiudadResponse
    producto: list[ProductoReporte] = []   # Optional se usa para indicar que podría no haber productos si un proveedor no tiene ninguno, pero en este caso [] como valor por defecto es más preciso.

    class Config:
        orm_mode= True