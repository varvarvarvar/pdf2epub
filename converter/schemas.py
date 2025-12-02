"""Data schemas and validations."""

from pathlib import Path
from typing import Annotated

from pydantic import AfterValidator, BaseModel
from pytesseract import get_languages


def is_supported_language(language: str) -> str:
    """Checks is the input language is supported."""
    if language not in get_languages():
        raise KeyError(f"Language {language} is not supported.")
    return language


class Request(BaseModel):
    """API request schema."""

    filepath: Path
    language: Annotated[str, AfterValidator(is_supported_language)]
