"""File operation helpers without external dependencies."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Union

PathLike = Union[str, Path]


def ensure_directory(path: PathLike) -> Path:
    """Ensure that a directory exists and return it as Path."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def read_text(path: PathLike, encoding: str = "utf-8") -> str:
    """Read text from a file."""
    with Path(path).open("r", encoding=encoding) as handle:
        return handle.read()


def write_text(path: PathLike, content: str, encoding: str = "utf-8") -> Path:
    """Write text content to a file and return the Path."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding=encoding) as handle:
        handle.write(content)
    return file_path


def read_json(path: PathLike, encoding: str = "utf-8") -> Any:
    """Load JSON content from disk."""
    with Path(path).open("r", encoding=encoding) as handle:
        return json.load(handle)


def write_json(path: PathLike, data: Any, encoding: str = "utf-8", *, indent: int = 2) -> Path:
    """Dump JSON data to disk."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding=encoding) as handle:
        json.dump(data, handle, ensure_ascii=False, indent=indent)
    return file_path
