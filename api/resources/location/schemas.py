from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(from_attributes=True)


class ProvinciaResponse(BaseModel):
    id: int
    nombre: str
    pais: PaisResponse

    model_config = ConfigDict(from_attributes=True)


class CiudadResponse(BaseModel):
    id: int
    nombre: str
    provincia: ProvinciaResponse

    model_config = ConfigDict(from_attributes=True)