# PDF 2 EPUB

Sometimes ebooks cannot display .pdf properly and that's when pdf2epub comes in handy.
<br>
<br>
Convert .pdf documents to .epub using Optical Character Recognition.

## Running API backend

```bash
poetry install --all-extras
poetry run python -m converter
```

This should set up API Swagger on `http://localhost:8000/docs#/`.

## Prerequisites on Mac OS

```
brew install poppler
brew install tesseract-lang
```
