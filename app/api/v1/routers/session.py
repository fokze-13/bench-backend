import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from app.annotations import DeviceID, SessionID
from app.api.v1.deps.session_deps import (
    get_session_service,
    get_device_id,
    websocket_get_device_id,
    websocket_get_session_id,
)
from app.exceptions import InvalidToken
from app.schemas.session import GetSession
from app.services.session_service import SessionService
from app.logger import setup_logger

router = APIRouter(prefix="/session")

SessionServiceDep = Annotated[SessionService, Depends(get_session_service)]
DeviceIDDep = Annotated[DeviceID, Depends(get_device_id)]

WebSocketDeviceIDDep = Annotated[DeviceID, Depends(websocket_get_device_id)]
WebSocketSessionIDDep = Annotated[SessionID, Depends(websocket_get_session_id)]

logger = setup_logger(__name__, logging.DEBUG)


@router.get("/get_session", response_model=GetSession)
async def get_session(session_service: SessionServiceDep, device_id: DeviceIDDep):
    try:
        session_id = await session_service.match_session(device_id=device_id)

        return GetSession(session_id=session_id)
    except InvalidToken as e:
        logger.error(e)
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Unexpected error")


@router.websocket("/connect")
async def connect(
    websocket: WebSocket,
    session_service: SessionServiceDep,
    device_id: WebSocketDeviceIDDep,
    session_id: WebSocketSessionIDDep,
):
    try:

        while True:
            ...

    except WebSocketDisconnect:
        logger.info("disconnect")
    except InvalidToken as e:
        logger.error(e)
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Unexpected error")
