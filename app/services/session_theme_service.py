from app.repositories.session_theme_repo import SessionThemeRepository
from app.schemas.session_theme import ThemesMap
import logging
from app.logger import setup_logger

logger = setup_logger(__name__, logging.INFO)


class SessionThemeService:
    def __init__(self, repository: SessionThemeRepository) -> None:
        self._repo = repository

    async def get_all(self) -> ThemesMap:
        logger.info("Fetching all session themes")
        themes = await self._repo.get_themes_list()

        return dict(themes)
