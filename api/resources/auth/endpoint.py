from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.core.database import get_db

from .dal import login_for_access_token, create_db_user, get_user_by_username
from .schemas import Token, User, UserCreate

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