from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from app.api.v1.deps.user_deps import get_user_service
from app.schemas.user_schema import UserRead, UserCreate
from app.services.user_service import UserService

router = APIRouter(prefix="/user-example", tags=["users"])
UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.get("/get-info/{user_id}", response_model=UserRead)
async def get_info(user_id: int, service: UserServiceDep):
    try:
        return await service.get(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/register", status_code=201)
async def register(data: UserCreate, service: UserServiceDep):
    try:
        await service.register(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
