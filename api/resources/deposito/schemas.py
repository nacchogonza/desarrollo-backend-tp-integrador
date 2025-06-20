from pydantic import BaseModel

#REQUEST

class DepositoCreateRequest(BaseModel):
    nombre: str
    telefono: str
    email: str
    direccion: str
    id_ciudad: int

#RESPONSE

class DepositoResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    direccion: str

    class Config:
        orm_mode = True