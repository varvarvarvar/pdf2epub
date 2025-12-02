"""API endpoints definition."""

import logging
from pathlib import Path

from fastapi import Depends, FastAPI, File, UploadFile
from pytesseract import get_languages

from converter.converter import pdf2epub
from converter.schemas import Request, get_request

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
async def convert(
    file: UploadFile = File(...), request: Request = Depends(get_request)
) -> dict:
    """Runs the file conversion."""
    logging.info(
        "Received file %s and language code %s", file.filename, request.language
    )
    pdf2epub(Path(file.filename), request.language)
    return {"response": "Successfully converted file"}
