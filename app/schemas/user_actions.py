from pydantic import BaseModel
from app.annotations import LanguageID, ThemeID, Language, Theme


class UpdatePreferredLanguage(BaseModel):
    language_id: LanguageID


class UpdatePreferredTheme(BaseModel):
    theme_id: ThemeID


class GetPreferredLanguage(BaseModel):
    language_id: LanguageID | None
    language: Language | None
    is_null: bool


class GetPreferredTheme(BaseModel):
    theme_id: ThemeID | None
    theme: Theme | None
    is_null: bool
