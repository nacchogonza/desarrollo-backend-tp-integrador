# auth.py (versión con DB y Async SQLAlchemy)
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, ConfigDict # Importa ConfigDict
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession # Importa AsyncSession
from sqlalchemy import select # Importa select de sqlalchemy

from passlib.context import CryptContext

from api.core.endpoint import get_db # Importa la dependencia de sesión de DB
from api.core.models import DBUser # Importa el modelo de SQLAlchemy

# --- Configuración JWT (sin cambios) ---
SECRET_KEY = "tu_super_clave_secreta_y_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

# --- Hashing de Contraseñas (sin cambios) ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# --- Modelos Pydantic (con ConfigDict para Pydantic V2) ---
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    disabled: bool = False
    # Para Pydantic V2
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Funciones CRUD para Usuarios (interactúan con la DB) ---
# ¡Ahora son async!
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(DBUser).filter(DBUser.username == username))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str): # <--- Tipo de db es AsyncSession
    result = await db.execute(select(DBUser).filter(DBUser.email == email))
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(DBUser).offset(skip).limit(limit))
    return result.scalars().all()

async def create_db_user(db: AsyncSession, user: UserCreate): # <--- Tipo de db es AsyncSession
    hashed_password = get_password_hash(user.password)
    db_user = DBUser(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit() # <--- await para commit
    await db.refresh(db_user) # <--- await para refresh
    return db_user

# --- Funciones para JWT (modificadas para usar la DB) ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# get_current_user ahora es async
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)): # <--- AsyncSession
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(db, token_data.username) # <--- ¡await aquí!
    if user is None:
        raise credentials_exception
    return user # Retorna el objeto DBUser

async def get_current_active_user(current_user: DBUser = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return current_user

# login_for_access_token ahora es async
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)): # <--- AsyncSession
    user = await get_user_by_username(db, form_data.username) # <--- ¡await aquí!
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}