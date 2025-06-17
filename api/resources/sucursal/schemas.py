from pydantic import BaseModel

#REQUEST
class SucursalCreateRequest(BaseModel):
    nombre: str
    telefono: str
    email: str
    direccion: str
    id_ciudad: int

#RESPONSE
class SucursalResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    direccion: str

    class Config:
        orm_mode = True