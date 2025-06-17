from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session # Importa Session para la dependencia de DB
from api.core.endpoint import get_db # Importa la dependencia de sesión de DB

from api.auth import Token, login_for_access_token, User, UserCreate, create_db_user, get_user_by_username # Importa lo necesario de auth.py
from api.users import endpoint as users_routes


import api.cliente.endpoint
import api.core
import api.core.endpoint
""" import api.deposito.endpoint """

app = FastAPI()

prefix_base = "/api/v1"

auth_router = APIRouter()

@auth_router.post("/token", response_model=Token, tags=["Auth"])
async def get_token_for_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await login_for_access_token(form_data, db)

@auth_router.post("/register/", response_model=User, tags=["Auth"])
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = await get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nombre de usuario ya registrado")
    new_user = await create_db_user(db, user)
    return new_user


app.include_router(auth_router, prefix=prefix_base, tags=["Auth"]) # Incluimos el router de auth
app.include_router(users_routes.router, prefix=f"{prefix_base}/users", tags=["Users"])
app.include_router(api.cliente.endpoint.router, prefix=f"{prefix_base}/cliente", tags=["Cliente"])
app.include_router(api.core.endpoint.router, prefix=f"{prefix_base}/core", tags=["Core"])