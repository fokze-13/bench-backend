import pytest
from unittest.mock import AsyncMock
from app.services.user_service import UserService
from app.core.security import verify_token
from uuid import uuid4

@pytest.mark.anyio
async def test_register_new_user(mock_user_repo: AsyncMock):
    service = UserService(repository=mock_user_repo)
    device_id = str(uuid4())
    mock_user_repo.get_by_device_id.return_value = None
    
    token = await service.register(device_id=device_id)
    
    mock_user_repo.get_by_device_id.assert_called_once_with(device_id)
    mock_user_repo.create.assert_called_once_with(device_id=device_id)
    
    assert verify_token(token) == device_id

@pytest.mark.anyio
async def test_register_existing_user(mock_user_repo: AsyncMock):
    service = UserService(repository=mock_user_repo)
    device_id = str(uuid4())
    
    mock_user_repo.get_by_device_id.return_value = {"id": 1, "device_id": device_id}
    
    token = await service.register(device_id=device_id)
    
    mock_user_repo.get_by_device_id.assert_called_once_with(device_id)
    mock_user_repo.create.assert_not_called()
    
    assert verify_token(token) == device_id
