# users/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.resources.auth.dal import get_current_active_user, get_user_by_username, get_users
from ..auth.schemas import User

from api.core.database import get_db

router = APIRouter(dependencies=[Depends(get_current_active_user)])

@router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Obtiene la información del usuario actualmente autenticado.
    Esta ruta está protegida por JWT.
    """
    return current_user

@router.get("/{username}/", response_model=User)
async def read_user_by_username(
    username: str,
    db: AsyncSession = Depends(get_db), # Necesitamos la DB para buscar por username
):
    """
    Obtiene la información de un usuario específico por su nombre de usuario.
    Requiere autenticación.
    """
    # Llama a la función CRUD async
    db_user = await get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return db_user # Retorna el objeto DBUser, que se mapeará a schemas.User

@router.get("/", response_model=list[User]) # Para listar todos los usuarios
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """
    Lista todos los usuarios (solo para usuarios autenticados).
    """
    users = await get_users(db, skip=skip, limit=limit)
    return users # Retorna una lista de objetos DBUser