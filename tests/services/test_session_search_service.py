import pytest
from unittest.mock import AsyncMock
from app.services.session_search_service import SessionSearchService
from uuid import uuid4

@pytest.mark.anyio
async def test_match_session_no_existing(mock_session_repo: AsyncMock):
    service = SessionSearchService(redis_repository=mock_session_repo)
    device_id = str(uuid4())
    new_session_id = str(uuid4())
    
    mock_session_repo.get_sessions.return_value = set()
    mock_session_repo.create_new_session.return_value = new_session_id
    
    matched_session_id = await service.match_session(device_id)
    
    assert matched_session_id == new_session_id
    mock_session_repo.create_new_session.assert_called_once()
    mock_session_repo.add_session_user.assert_called_once_with(
        session_id=new_session_id, device_id=device_id
    )

@pytest.mark.anyio
async def test_match_session_existing_with_space(mock_session_repo: AsyncMock):
    service = SessionSearchService(redis_repository=mock_session_repo)
    device_id = str(uuid4())
    existing_session_id = str(uuid4())
    
    mock_session_repo.get_sessions.return_value = {existing_session_id}
    mock_session_repo.get_session_users_count.return_value = 1
    
    matched_session_id = await service.match_session(device_id)
    
    assert matched_session_id == existing_session_id
    mock_session_repo.create_new_session.assert_not_called()
    mock_session_repo.add_session_user.assert_called_once_with(
        session_id=existing_session_id, device_id=device_id
    )

@pytest.mark.anyio
async def test_match_session_existing_full(mock_session_repo: AsyncMock, monkeypatch: pytest.MonkeyPatch):
    service = SessionSearchService(redis_repository=mock_session_repo)
    monkeypatch.setattr(service, "_MAX_USERS_PER_SESSION", 2)
    
    device_id = str(uuid4())
    existing_session_id = str(uuid4())
    new_session_id = str(uuid4())
    
    mock_session_repo.get_sessions.return_value = {existing_session_id}
    mock_session_repo.get_session_users_count.return_value = 3
    mock_session_repo.create_new_session.return_value = new_session_id
    
    matched_session_id = await service.match_session(device_id)
    
    assert matched_session_id == new_session_id
    mock_session_repo.create_new_session.assert_called_once()
    mock_session_repo.add_session_user.assert_called_once_with(
        session_id=new_session_id, device_id=device_id
    )
