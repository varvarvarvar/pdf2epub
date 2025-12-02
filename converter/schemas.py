from pathlib import Path
from typing import Annotated

from pydantic import AfterValidator, BaseModel
from pytesseract import get_languages


def is_supported_language(language: str) -> int:
    if language not in get_languages():
        raise KeyError(f"Language {language} is not supported.")
    return language


class Language(BaseModel):
    language: Annotated[str, AfterValidator(is_supported_language)]


class Request(BaseModel):
    filepath: Path
    language: Language
