from pathlib import Path
from typing import Iterable

from downloader.config import DATA_DIR


def create_data_dir() -> None:
    try:
        DATA_DIR.mkdir()
    except FileExistsError:
        pass


def clear_data_dir() -> None:
    if not DATA_DIR.exists() or DATA_DIR.is_file():
        return

    for path in DATA_DIR.iterdir():
        if path.is_file():
            path.unlink()


def sort_files_by_name(files: Iterable[Path]) -> Iterable[Path]:
    """
    Sorts files in ascending order by their names.
    Each input file name is a number: 1.pdf, 24.pdf etc.
    """
    d = {int(file.stem): file for file in files}
    return [d[key] for key in sorted(d.keys())]
