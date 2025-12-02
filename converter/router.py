import logging

from fastapi import FastAPI
from pytesseract import get_languages

from converter.converter import pdf2epub
from converter.schemas import Request

logging.getLogger().setLevel(logging.INFO)

app = FastAPI()


@app.post("/buildinfo")
def root():
    return {"build_id": "Local"}


@app.get("/languages/")
def supported_languages():
    return get_languages()


@app.post("/url/")
def post_url(request: Request):
    logging.info(
        "Received file %s and language code %s", request.filepath, request.language
    )
    pdf2epub(request.filepath, request.language)
    return {"response": "Successfully converted file"}
