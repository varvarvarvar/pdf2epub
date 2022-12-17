"""PDF to EPUB converter utils."""
import logging
import os
import re
from pathlib import Path, PosixPath
from typing import List

import pypandoc
import pytesseract
from pdf2image import convert_from_path
from PIL.JpegImagePlugin import JpegImageFile
from tqdm import tqdm

logging.getLogger().setLevel("INFO")

LANG = "rus"
SRC_FILE = Path("sample.pdf")


def preprocess_text(text: str) -> str:
    """Removes extra \n and double whitespaces from a string."""
    text = re.sub(
        "(?<![\r\n])(\r?\n|\r)(?![\r\n])", " ", text
    )  # Repair sentences that have \n in the middle
    text = "\n".join(
        " ".join(line.split()) for line in text.split("\n")
    )  # Remove extra whitespaces (pypandoc cannot convert them)
    return text


def txt2epub(txt_filepath: PosixPath, epub_filepath: PosixPath) -> None:
    """Converts TXT file to a EPUB file."""
    pypandoc.convert_file(
        txt_filepath, format="markdown", to="epub", outputfile=epub_filepath
    )


def images2txt(images: List[JpegImageFile], txt_filepath: PosixPath):
    """Converts PIL images to a TXT file using OCR."""
    with open(txt_filepath, "w", encoding="utf-8") as file:
        for image in tqdm(images):
            text = pytesseract.image_to_string(image, lang=LANG)
            text = preprocess_text(text)
            file.write(f"{text}\n")


def pdf2epub(pdf_filpath: PosixPath) -> None:
    """Converts PDF file to a EPUB file using OCR."""
    txt_filepath = pdf_filpath.with_suffix(".txt")
    epub_filepath = pdf_filpath.with_suffix(".epub")

    images = convert_from_path(pdf_filpath, fmt="jpeg")
    images2txt(images, txt_filepath)
    txt2epub(txt_filepath, epub_filepath)
    os.remove(txt_filepath)
