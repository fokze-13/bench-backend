from app.repositories.user_repo import UserRepository
from app.annotations import DeviceID, Token, LanguageID, ThemeID
from app.schemas.user_actions import GetPreferredLanguage, GetPreferredTheme
from app.core.security import create_access_token
import logging
from app.logger import setup_logger

logger = setup_logger(__name__, logging.INFO)


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repo = repository

    async def register(self, device_id: DeviceID) -> Token:
        logger.info(f"Registering user with device ID {device_id}")
        user_or_none = await self._repo.get_by_device_id(device_id)

        if not user_or_none:
            logger.info(f"Creating new user for device ID {device_id}")
            await self._repo.create(device_id=device_id)

        token = create_access_token(device_id=device_id)

        return token

    async def update_preferred_language(
        self, device_id: DeviceID, language_id: LanguageID
    ) -> None:
        logger.info(f"Updating preferred language for device ID {device_id}")
        await self._repo.update_by_device_id(
            device_id=device_id, preferred_language_id=language_id
        )

    async def update_preferred_session_theme(
        self, device_id: DeviceID, theme_id: ThemeID
    ) -> None:
        logger.info(f"Updating preferred session theme for device ID {device_id}")
        await self._repo.update_by_device_id(
            device_id=device_id, preferred_session_theme_id=theme_id
        )

    async def get_preferred_language(self, device_id: DeviceID) -> GetPreferredLanguage:
        logger.info(f"Fetching preferred language for device ID {device_id}")
        user = await self._repo.get_preferences_by_device_id(device_id)
        language = user.preferred_language if user else None

        if not language:
            return GetPreferredLanguage(language_id=None, language=None, is_null=True)

        return GetPreferredLanguage(
            language_id=language.id, language=language.lang, is_null=False
        )

    async def get_preferred_session_theme(
        self, device_id: DeviceID
    ) -> GetPreferredTheme:
        logger.info(f"Fetching preferred session theme for device ID {device_id}")
        user = await self._repo.get_preferences_by_device_id(device_id)
        theme = user.preferred_session_theme if user else None

        if not theme:
            return GetPreferredTheme(theme_id=None, theme=None, is_null=True)

        return GetPreferredTheme(
            theme_id=theme.id, theme=theme.theme_name, is_null=False
        )
