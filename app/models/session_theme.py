from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.annotations import ThemeID, Theme
from app.models.base import Base


class SessionThemeModel(Base):
    __tablename__ = "session_themes"

    id: Mapped[ThemeID] = mapped_column(Integer, primary_key=True)
    theme_name: Mapped[Theme] = mapped_column(String, unique=True, nullable=False)
