import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Iterable

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from PyPDF2 import PdfFileMerger

from downloader.config import (
    DATA_DIR,
    PDF_FILE_PATTERN,
    PDF_SUFFIX,
    SVG_FILE_PATTERN,
    RESULT_FILE
)
from downloader.util import sort_files_by_name


def merge_pdf_files() -> None:
    _merge_pdfs(
        sort_files_by_name(DATA_DIR.glob(PDF_FILE_PATTERN))
    )


def _merge_pdfs(files: Iterable[Path]) -> None:
    merger = PdfFileMerger()

    for pdf in files:
        merger.append(pdf)

    merger.write(RESULT_FILE)
    merger.close()


def convert_svg_files_to_pdf() -> None:
    os.chdir(DATA_DIR)

    with ProcessPoolExecutor() as executor:
        executor.map(_convert_svg_to_pdf, Path.cwd().glob(SVG_FILE_PATTERN))

    os.chdir(Path.cwd().parent)


def _convert_svg_to_pdf(file: Path) -> None:
    drawing = svg2rlg(file)
    renderPDF.drawToFile(drawing, f'{file.stem}{PDF_SUFFIX}')
