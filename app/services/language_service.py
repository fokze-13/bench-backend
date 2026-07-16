from app.repositories.language_repo import LanguageRepository
from app.schemas.language import LanguagesMap
import logging
from app.logger import setup_logger

logger = setup_logger(__name__, logging.INFO)


class LanguageService:
    def __init__(self, repository: LanguageRepository) -> None:
        self._repo = repository

    async def get_all(self) -> LanguagesMap:
        logger.info("Fetching all languages")
        languages = await self._repo.get_languages_list()

        return dict(languages)
