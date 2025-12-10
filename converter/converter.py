"""PDF to EPUB converter utils."""

import asyncio
import io
import logging
import re
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pathlib import Path
from typing import AsyncGenerator

from fastapi import File
from pdf2image import convert_from_bytes as convert_pdf_to_pil
from PIL.JpegImagePlugin import JpegImageFile
from pypandoc import convert_text as convert_text_to_epub
from pytesseract import image_to_string

logging.getLogger().setLevel("INFO")

CHUNK_SIZE = 1024 * 1024  # 1 MB
executor = ProcessPoolExecutor()


def _preprocess_text(text: str) -> str:
    """Removes extra \n and double whitespaces from a string."""
    # Repair sentences that have \n in the middle
    text = re.sub("(?<![\r\n])(\r?\n|\r)(?![\r\n])", " ", text)
    # Remove extra whitespaces (pypandoc cannot convert them)
    text = "\n".join(" ".join(line.split()) for line in text.split("\n"))
    return text


def _images2txt(images: list[JpegImageFile], language: str) -> str:
    """Converts PIL images to a TXT file using OCR."""
    buf = io.StringIO()
    for image in images:
        text = image_to_string(image, lang=language)
        text = _preprocess_text(text)
        buf.write(text + "\n")
    text = buf.getvalue()
    return text


async def _process_chunk(file: File, language: str, chunk_size: int) -> AsyncGenerator:
    """Converts chunk of PDF file into text."""
    loop = asyncio.get_running_loop()

    while chunk := await file.read(chunk_size):
        images = await loop.run_in_executor(executor, convert_pdf_to_pil, chunk, "jpeg")
        text = await loop.run_in_executor(executor, _images2txt, images, language)
        yield text


async def pdf2epub(file: File, language: str, chunk_size: int = CHUNK_SIZE) -> None:
    """Converts PDF file to a EPUB file using OCR."""
    logging.info("Processing PDF file ...")
    loop = asyncio.get_running_loop()
    chunks = []
    async for chunk in _process_chunk(file, language, chunk_size):
        chunks.append(chunk)
    text = "".join(chunks)

    # Use partial to allow passing kwargs to executor
    partial_convert_text_to_epub = partial(
        convert_text_to_epub,
        text,
        format="markdown",
        to="epub",
        outputfile=Path(file.filename).with_suffix(".epub"),
    )
    await loop.run_in_executor(executor, partial_convert_text_to_epub)
