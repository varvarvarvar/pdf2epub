"""Data schemas and validations."""

from fastapi import Form, HTTPException
from pydantic import BaseModel
from pytesseract import get_languages


def is_supported_language(language: str) -> bool:
    """Checks is the input language is supported."""
    return language in get_languages()


class Request(BaseModel):
    """API request schema."""
    language: str


def get_request(language: str = Form(...)) -> Request:
    """Re-raises pydantic exceptions to pass them to FastAPI."""
    if not is_supported_language(language):
        detail = [
            {
                "type": "value_error.language_not_supported",
                "loc": ["body", "language"],
                "msg": f"Unsupported language code: {language}",
                "input": language,
            }
        ]
        raise HTTPException(status_code=422, detail=detail)
    return Request(language=language)
