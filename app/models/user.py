from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from app.annotations import UserID, DeviceID, LanguageID, ThemeID
from app.models.language import LanguageModel
from app.models.session_theme import SessionThemeModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UserID] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[DeviceID] = mapped_column(String, unique=True, nullable=False)
    preferred_language_id: Mapped[LanguageID | None] = mapped_column(
        ForeignKey("languages.id"), nullable=True
    )
    preferred_session_theme_id: Mapped[ThemeID | None] = mapped_column(
        ForeignKey("session_themes.id"), nullable=True
    )
    preferred_language: Mapped["LanguageModel | None"] = relationship()
    preferred_session_theme: Mapped["SessionThemeModel | None"] = relationship()
