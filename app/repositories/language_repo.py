from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.annotations import LanguageID, Language
from app.models.language import LanguageModel


class LanguageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_languages_list(self) -> list[tuple[LanguageID, Language]]:
        langs = await self._session.execute(
            select(LanguageModel.id, LanguageModel.lang)
        )

        return list(langs.scalars().all())
