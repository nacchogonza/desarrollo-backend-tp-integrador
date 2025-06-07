from fastapi import FastAPI, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from api.auth import Token, login_for_access_token
from api.users import endpoint as users_routes


import api.cliente.endpoint
import api.core
import api.core.endpoint
""" import api.deposito.endpoint """

app = FastAPI()

prefix_base = "/api/v1"

auth_router = APIRouter()

@auth_router.post("/token", response_model=Token)
async def get_token_for_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para obtener un token de acceso JWT.
    """
    return await login_for_access_token(form_data)


app.include_router(auth_router, prefix=prefix_base, tags=["Auth"]) # Incluimos el router de auth
app.include_router(users_routes.router, prefix=f"{prefix_base}/users", tags=["Users"])
app.include_router(api.cliente.endpoint.router, prefix=f"{prefix_base}/cliente", tags=["Cliente"])
app.include_router(api.core.endpoint.router, prefix=f"{prefix_base}/core", tags=["Core"])