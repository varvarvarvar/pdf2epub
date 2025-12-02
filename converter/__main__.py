"""Parse CLI argument and convert to .epub."""

from pathlib import Path

import click
from pytesseract import get_languages

from converter.converter import pdf2epub


@click.command()
@click.option("--file", type=Path, required=True, help="Path to the .PDF file.")
@click.option(
    "--lang",
    type=click.Choice(get_languages()),
    required=True,
    help=f"The .PDF file language.\nSupported languages:\n{get_languages()}.",
)
def main(file, lang):
    """Parses CLI arguments and passes them to function call."""
    pdf2epub(file, lang)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
