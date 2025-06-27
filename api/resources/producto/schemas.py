from pydantic import BaseModel, ConfigDict
from ..proveedor.schemas import ProveedorResponse

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
    proveedor: ProveedorResponse

    model_config = ConfigDict(from_attributes=True)
