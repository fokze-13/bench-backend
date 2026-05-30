from app.config import SessionUserStatus, MAX_USERS_PER_SESSION
from app.repositories.session_repo import SessionRepository
from app.annotations import SessionID, DeviceID
import asyncio


class SessionService:
    _MAX_USERS_PER_SESSION = MAX_USERS_PER_SESSION

    def __init__(self, redis_repository: SessionRepository) -> None:
        self._redis_repo = redis_repository

    async def connect_user(self, device_id: DeviceID, session_id: SessionID) -> None:
        await self._redis_repo.update_session_user_status(
            session_id=session_id,
            device_id=device_id,
            status=str(SessionUserStatus.CONNECTED),
        )

    async def match_session(self, device_id: DeviceID) -> SessionID:
        matched_session_id = await self._find_open_session()

        await self._redis_repo.add_session_user(
            session_id=matched_session_id, device_id=device_id
        )

        return matched_session_id

    async def _find_open_session(self) -> SessionID:
        sessions_ids = list(await self._redis_repo.get_sessions())

        if not sessions_ids:
            return await self._open_new_session()

        sessions_user_counts = await asyncio.gather(
            *(
                self._redis_repo.get_session_users_count(session_id)
                for session_id in sessions_ids
            )
        )

        sessions_dict = {
            session_id: user_count
            for session_id, user_count in zip(sessions_ids, sessions_user_counts)
        }

        min_user_count_session_id = min(sessions_dict, key=lambda x: sessions_dict[x])

        if sessions_dict[min_user_count_session_id] <= self._MAX_USERS_PER_SESSION:
            return min_user_count_session_id

        return await self._open_new_session()

    async def _open_new_session(self) -> SessionID:
        return await self._redis_repo.create_new_session()
