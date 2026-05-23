from fastapi import APIRouter
from app.schemas.auth import TokenRead, TokenCreate


router = APIRouter(prefix="/auth")


@router.post("/get_token", response_model=TokenRead)
async def get_token(body: TokenCreate):
    pass
