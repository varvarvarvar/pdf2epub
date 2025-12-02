"""PDF to EPUB converter utils."""

import logging
import os
import re
from pathlib import Path

from pdf2image import convert_from_path as convert_pdf2images
from PIL.JpegImagePlugin import JpegImageFile
from pypandoc import convert_file as convert_txt2epub
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


def _images2txt(images: list[JpegImageFile], txt_filepath: Path, lang: str) -> None:
    """Converts PIL images to a TXT file using OCR."""
    with open(txt_filepath, "w", encoding="utf-8") as file:
        for image in tqdm(images):
            text = image_to_string(image, lang=lang)
            text = _preprocess_text(text)
            file.write(f"{text}\n")


def _txt2epub(txt_filepath: Path, epub_filepath: Path) -> None:
    """Converts TXT file to a EPUB file."""
    convert_txt2epub(
        txt_filepath, format="markdown", to="epub", outputfile=epub_filepath
    )


def pdf2epub(pdf_filepath: Path, lang: str) -> None:
    """Converts PDF file to a EPUB file using OCR."""
    images = convert_pdf2images(pdf_filepath, fmt="jpeg")
    txt_filepath = pdf_filepath.with_suffix(".txt")
    _images2txt(images, txt_filepath, lang)
    epub_filepath = pdf_filepath.with_suffix(".epub")
    _txt2epub(txt_filepath, epub_filepath)
    os.remove(txt_filepath)
