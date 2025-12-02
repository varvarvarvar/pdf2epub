"""API endpoints definition."""

import logging

from fastapi import APIRouter, Depends, FastAPI, File, UploadFile
from pytesseract import get_languages

from converter.converter import pdf2epub
from converter.schemas import Request, get_request

logging.getLogger().setLevel(logging.INFO)

API_VERSION = "/v1"

app = FastAPI(title="PDF to EPUB converter")
version_router = APIRouter(prefix=API_VERSION)


@version_router.post("/buildinfo", tags=["Buildinfo"])
def get_buildinfo() -> dict:
    """Checks that the service is operational by returning buildinfo."""
    return {"build_id": "Local"}


@version_router.get("/languages/", tags=["Languages"])
def supported_languages() -> list[str]:
    """Returns the list of supported language codes."""
    return get_languages()


@version_router.post("/convert/", tags=["Convert"])
async def convert(
    file: UploadFile = File(...), request: Request = Depends(get_request)
) -> dict:
    """Runs the file conversion."""
    logging.info(
        "Received file %s with language code %s", file.filename, request.language
    )
    await pdf2epub(file, request.language)
    return {"response": "Successfully converted file"}


app.include_router(version_router)
