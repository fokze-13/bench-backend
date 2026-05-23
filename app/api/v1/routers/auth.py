from typing import Annotated
from fastapi import APIRouter, HTTPException
from app.exceptions import UnexpectedError
from app.schemas.auth import TokenRead, TokenCreate
from app.api.v1.deps.user_deps import get_user_service
from fastapi import Depends
from app.services.user_service import UserService

router = APIRouter(prefix="/auth")
UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.post("/get_token", response_model=TokenRead)
async def get_token(body: TokenCreate, user_service: UserServiceDep):
    try:
        device_id = body.device_id
        token = await user_service.register(device_id)

        return TokenRead(
            token=token
        )
    except UnexpectedError:
        raise HTTPException(status_code=500, detail="Unexpected error")
