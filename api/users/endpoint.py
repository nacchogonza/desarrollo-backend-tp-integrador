# users/routes.py
from fastapi import APIRouter, Depends
from typing import Dict
from api.auth import User, get_current_active_user # Importamos desde nuestro módulo auth

router = APIRouter()

@router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Obtiene la información del usuario actualmente autenticado.
    Esta ruta está protegida por JWT.
    """
    return current_user

@router.get("/{username}", response_model=User)
async def read_user(username: str, current_user: User = Depends(get_current_active_user)):
    """
    Obtiene la información de un usuario específico (solo para usuarios autenticados).
    """
    # En una aplicación real, agregarías lógica para que solo un admin pueda ver otros usuarios,
    # o que un usuario solo pueda ver su propio perfil.
    return {"username": username, "email": "user@example.com", "full_name": "Example User"}