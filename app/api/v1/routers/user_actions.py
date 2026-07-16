import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.annotations import DeviceID
from app.api.v1.deps.session_deps import get_device_id
from app.api.v1.deps.user_deps import get_user_service
from app.schemas.user_actions import (
    UpdatePreferredLanguage,
    UpdatePreferredTheme,
    GetPreferredLanguage,
    GetPreferredTheme,
)
from app.services.user_service import UserService
from app.logger import setup_logger

router = APIRouter(prefix="/user")

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
DeviceIDDep = Annotated[DeviceID, Depends(get_device_id)]

logger = setup_logger(__name__, logging.DEBUG)


@router.post("/update_preferred_language")
async def set_preferred_language(
    body: UpdatePreferredLanguage,
    user_service: UserServiceDep,
    device_id: DeviceIDDep,
):
    try:
        await user_service.update_preferred_language(
            device_id=device_id, language_id=body.language_id
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Unexpected error")


@router.post("/update_preferred_session_theme")
async def set_preferred_session_theme(
    body: UpdatePreferredTheme,
    user_service: UserServiceDep,
    device_id: DeviceIDDep,
):
    try:
        await user_service.update_preferred_session_theme(
            device_id=device_id, theme_id=body.theme_id
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Unexpected error")


@router.get("/get_preferred_language", response_model=GetPreferredLanguage)
async def get_preferred_language(
    user_service: UserServiceDep,
    device_id: DeviceIDDep,
):
    try:
        return await user_service.get_preferred_language(device_id=device_id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Unexpected error")


@router.get("/get_preferred_session_theme", response_model=GetPreferredTheme)
async def get_preferred_session_theme(
    user_service: UserServiceDep,
    device_id: DeviceIDDep,
):
    try:
        return await user_service.get_preferred_session_theme(device_id=device_id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Unexpected error")
