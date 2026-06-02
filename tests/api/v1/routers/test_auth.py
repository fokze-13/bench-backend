import pytest
from uuid import uuid4
from httpx import AsyncClient
from unittest.mock import AsyncMock

@pytest.mark.anyio
async def test_get_token(test_client: AsyncClient, mock_user_repo: AsyncMock):
    device_id = str(uuid4())
    
    mock_user_repo.get_by_device_id.return_value = None
    mock_user_repo.create.return_value = None

    response = await test_client.post("/auth/get_token", json={"device_id": device_id})

    assert response.status_code == 200
    
    data = response.json()
    assert "token" in data
    
    mock_user_repo.get_by_device_id.assert_called_once_with(device_id)
    mock_user_repo.create.assert_called_once_with(device_id=device_id)
