"""PDF to EPUB converter utils."""

import io
import logging
import re
from pathlib import Path
from typing import Generator

from pdf2image import convert_from_path as convert_pdf2images
from PIL.JpegImagePlugin import JpegImageFile
from pypandoc import convert_text as convert_txt2epub
from pytesseract import image_to_string
from tqdm import tqdm

logging.getLogger().setLevel("INFO")


def _preprocess_text(text: str) -> str:
    """Removes extra \n and double whitespaces from a string."""
    # Repair sentences that have \n in the middle
    text = re.sub("(?<![\r\n])(\r?\n|\r)(?![\r\n])", " ", text)
    # Remove extra whitespaces (pypandoc cannot convert them)
    text = "\n".join(" ".join(line.split()) for line in text.split("\n"))
    return text


def _images2txt(images: list[JpegImageFile], lang: str) -> str:
    """Converts PIL images to a TXT file using OCR."""
    buf = io.StringIO()
    for image in tqdm(images, desc="Processing page"):
        text = image_to_string(image, lang=lang)
        text = _preprocess_text(text)
        buf.write(text + "\n")
    text = buf.getvalue()
    return text


def pdf2epub(pdf_filepath: Path, lang: str) -> None:
    """Converts PDF file to a EPUB file using OCR."""
    images = convert_pdf2images(pdf_filepath, fmt="jpeg")
    text = _images2txt(images, lang)

    convert_txt2epub(
        text, format="markdown", to="epub", outputfile=pdf_filepath.with_suffix(".epub")
    )
