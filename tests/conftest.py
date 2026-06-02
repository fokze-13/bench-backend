import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from unittest.mock import AsyncMock

from app.main import app
from app.repositories.user_repo import UserRepository
from app.repositories.session_repo import SessionRepository
from app.core.connections import ConnectionManager
from app.api.v1.deps.user_deps import get_user_repo
from app.api.v1.deps.session_deps import get_session_repo


@pytest.fixture
def mock_user_repo() -> AsyncMock:
    repo = AsyncMock(spec=UserRepository)
    return repo


@pytest.fixture
def mock_session_repo() -> AsyncMock:
    repo = AsyncMock(spec=SessionRepository)
    return repo


@pytest.fixture
def mock_connection_manager() -> AsyncMock:
    manager = AsyncMock(spec=ConnectionManager)
    return manager


@pytest.fixture
async def test_client(
    mock_user_repo: AsyncMock, mock_session_repo: AsyncMock
) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_user_repo] = lambda: mock_user_repo
    app.dependency_overrides[get_session_repo] = lambda: mock_session_repo

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()

@pytest.fixture
def anyio_backend():
    return 'asyncio'

