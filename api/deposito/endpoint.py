from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def deposito():
    return {"deposito": "deposito"}