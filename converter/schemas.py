"""Data schemas and validations."""

from pydantic import BaseModel, field_validator
from pytesseract import get_languages


def is_supported_language(language: str) -> str:
    """Checks is the input language is supported."""
    if language not in get_languages():
        raise KeyError(f"Language {language} is not supported.")
    return language


class Request(BaseModel):
    """API request schema."""
    language: str

    @field_validator("language")
    def validate_language(cls, v):
        is_supported_language(v)
        return v
