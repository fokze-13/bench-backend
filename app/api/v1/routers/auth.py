import logging
from typing import Annotated
from fastapi import APIRouter, HTTPException
from app.schemas.auth import TokenRead, TokenCreate
from app.api.v1.deps.user_deps import get_user_service
from fastapi import Depends
from app.services.user_service import UserService
from app.logger import setup_logger


router = APIRouter(prefix="/auth")
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
logger = setup_logger(__name__, logging.DEBUG)


@router.post("/get_token", response_model=TokenRead)
async def get_token(body: TokenCreate, user_service: UserServiceDep):
    try:
        device_id = body.device_id
        token = await user_service.register(device_id)

        return TokenRead(token=token)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Unexpected error")
