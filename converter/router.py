"""API endpoints definition."""

import logging
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from pytesseract import get_languages

from converter.converter import pdf2epub
from converter.schemas import Request

logging.getLogger().setLevel(logging.INFO)

app = FastAPI(title="PDF to EPUB converter")


@app.post("/buildinfo", tags=["Buildinfo"])
def get_buildinfo() -> dict:
    """Checks that the service is operational by returning buildinfo."""
    return {"build_id": "Local"}


@app.get("/languages/", tags=["Languages"])
def supported_languages() -> list[str]:
    """Returns the list of supported language codes."""
    return get_languages()


@app.post("/convert/", tags=["Convert"])
async def convert(file: UploadFile = File(...), language: str = Form(...)) -> dict:
    """Runs the file conversion."""
    request = Request(language=language)
    logging.info(
        "Received file %s and language code %s", file.filename, request.language
    )
    pdf2epub(Path(file.filename), request.language)
    return {"response": "Successfully converted file"}
