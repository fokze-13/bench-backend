from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.annotations import LanguageID, Language
from app.models.base import Base


class LanguageModel(Base):
    __tablename__ = "languages"

    id: Mapped[LanguageID] = mapped_column(Integer, primary_key=True)
    lang: Mapped[Language] = mapped_column(String, unique=True, nullable=False)
