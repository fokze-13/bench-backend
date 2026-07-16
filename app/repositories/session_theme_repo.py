from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.annotations import Theme, ThemeID
from app.models.session_theme import SessionThemeModel


class SessionThemeRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_themes_list(self) -> list[tuple[ThemeID, Theme]]:
        themes = await self._session.execute(
            select(SessionThemeModel.id, SessionThemeModel.theme_name)
        )

        return list(themes.scalars().all())
