"""PDF to EPUB converter utils."""

import logging
import os
import re
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from fastapi import File
from pdf2image import convert_from_bytes as convert_pdf_to_pil
from PIL.JpegImagePlugin import JpegImageFile
from pypandoc import convert_text as convert_text_to_epub
from pytesseract import image_to_string
from tqdm import tqdm

logging.getLogger().setLevel("INFO")

MAX_WORKERS = os.cpu_count()


def _preprocess_text(text: str) -> str:
    """Remove extra line breaks and double whitespaces from a string."""
    # Repair sentences that have \n in the middle
    text = re.sub("(?<![\r\n])(\r?\n|\r)(?![\r\n])", " ", text)
    # Remove extra whitespaces (pypandoc cannot convert them)
    text = "\n".join(" ".join(line.split()) for line in text.split("\n"))
    return text


def _image2txt(image: JpegImageFile, language: str) -> str:
    """Convert PIL image to a TXT file using OCR."""
    text = image_to_string(image, lang=language)
    return _preprocess_text(text)


def _images2txt(images: list[JpegImageFile], language: str) -> str:
    """Convert PIL images to a TXT file using OCR."""
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = [pool.submit(_image2txt, image, language) for image in images]
        text_chunks = [
            f.result() for f in tqdm(futures, desc="Processing document pages")
        ]
    return "\n".join(text_chunks)


def pdf2epub(file: File, language: str) -> None:
    """Convert PDF file to a EPUB file using OCR."""
    logging.info("Processing PDF file ...")
    bytes_file = file.file.read()
    logging.info("Converting pdf to images")
    images = convert_pdf_to_pil(bytes_file, fmt="jpeg")
    logging.info("Converting images to text")
    text = _images2txt(images, language)
    logging.info("Converting text to epub")

    convert_text_to_epub(
        text,
        format="markdown",
        to="epub",
        outputfile=Path(file.filename).with_suffix(".epub"),
    )
