from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.annotations import DeviceID
from app.api.v1.deps.session_deps import get_session_service, get_device_id
from app.exceptions import InvalidToken
from app.schemas.session import SessionHeaders, GetSession
from app.services.session_service import SessionService

router = APIRouter(prefix="/session")
SessionServiceDep = Annotated[SessionService, Depends(get_session_service)]
DeviceIDDep = Annotated[DeviceID, Depends(get_device_id)]


@router.get("/get_session", response_model=GetSession)
async def get_session(session_service: SessionServiceDep, device_id: DeviceIDDep):
    try:
        session_id = await session_service.match_session(device_id=device_id)

        return GetSession(session_id=session_id)
    except InvalidToken:
        raise HTTPException(status_code=401, detail="Invalid token")
    except:
        raise HTTPException(status_code=500, detail="Unexpected error")
