import pytest
from httpx import AsyncClient
from app.core.security import create_access_token
from uuid import uuid4
from unittest.mock import AsyncMock

@pytest.mark.anyio
async def test_get_session(test_client: AsyncClient, mock_session_repo: AsyncMock):
    device_id = str(uuid4())
    token = create_access_token(device_id=device_id)
    new_session_id = str(uuid4())
    
    mock_session_repo.get_sessions.return_value = set()
    mock_session_repo.create_new_session.return_value = new_session_id
    
    response = await test_client.get(
        "/session/get_session", 
        headers={"token": token}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == new_session_id
    
    mock_session_repo.add_session_user.assert_called_once_with(
        session_id=new_session_id, device_id=device_id
    )

@pytest.mark.anyio
async def test_get_session_invalid_token(test_client: AsyncClient):
    # Act
    response = await test_client.get(
        "/session/get_session", 
        headers={"token": "invalid.token.here"}
    )
    
    # Assert
    assert response.status_code == 401
