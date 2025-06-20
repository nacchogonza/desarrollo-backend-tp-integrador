from pydantic import BaseModel

#Request
class ProductoCreateRequest(BaseModel):
    nombre: str
    descripcion: str
    categoria: str
    precioCompra: float
    precioVenta: float

    id_proveedor: int

#Response
class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    categoria: str
    precioCompra: float
    precioVenta: float

    class Config:
        orm_mode = True
