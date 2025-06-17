from pydantic import BaseModel

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

    class Config:
        orm_mode = True
