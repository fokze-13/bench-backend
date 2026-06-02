import pytest
from unittest.mock import AsyncMock, patch
from app.services.session_manager_service import SessionManagerService
from app.config import SessionUserStatus
from uuid import uuid4
from fastapi import WebSocket

@pytest.mark.anyio
async def test_connect_to_session(mock_session_repo: AsyncMock, mock_connection_manager: AsyncMock):
    service = SessionManagerService(
        redis_repository=mock_session_repo, 
        connection_manager=mock_connection_manager
    )
    device_id = str(uuid4())
    session_id = str(uuid4())
    websocket = AsyncMock(spec=WebSocket)
    alias = "User-1"
    
    mock_session_repo.get_session_users_count.return_value = 1
    mock_session_repo.get_session_users.return_value = {}
    
    with patch("app.services.session_manager_service.generate_alias", return_value=alias):
        await service.connect_to_session(device_id, session_id, websocket)
        
        mock_connection_manager.connect.assert_called_once_with(device_id, websocket)
        mock_session_repo.update_session_user_status.assert_called_once_with(
            session_id, device_id, str(SessionUserStatus.CONNECTED)
        )
        mock_session_repo.add_session_user_alias.assert_called_once_with(
            session_id, device_id, alias
        )

@pytest.mark.anyio
async def test_disconnect_from_session(mock_session_repo: AsyncMock, mock_connection_manager: AsyncMock):
    service = SessionManagerService(
        redis_repository=mock_session_repo, 
        connection_manager=mock_connection_manager
    )
    device_id = str(uuid4())
    session_id = str(uuid4())
    alias = "User-1"
    
    mock_session_repo.get_session_user_alias.return_value = alias
    mock_session_repo.get_session_users.return_value = {}
    
    await service.disconnect_from_session(device_id, session_id)
    
    mock_connection_manager.disconnect.assert_called_once_with(device_id)
    mock_session_repo.delete_session_user.assert_called_once_with(session_id, device_id)
