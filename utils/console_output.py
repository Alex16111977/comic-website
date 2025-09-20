"""Console output helpers that enforce ASCII status tags."""
from typing import Callable

_TAG_PREFIXES = {
    "info": "[INFO]",
    "warning": "[WARNING]",
    "error": "[ERROR]",
    "success": "[OK]",
}


def _emit(tag: str, message: str, printer: Callable[[str], None]) -> None:
    prefix = _TAG_PREFIXES.get(tag, "[INFO]")
    printer(f"{prefix} {message}")


def console_line(tag: str, message: str, printer: Callable[[str], None] = print) -> None:
    """Print a tagged console line."""
    _emit(tag, message, printer)


def info(message: str, printer: Callable[[str], None] = print) -> None:
    """Print informational message."""
    _emit("info", message, printer)


def warning(message: str, printer: Callable[[str], None] = print) -> None:
    """Print warning message."""
    _emit("warning", message, printer)


def error(message: str, printer: Callable[[str], None] = print) -> None:
    """Print error message."""
    _emit("error", message, printer)


def success(message: str, printer: Callable[[str], None] = print) -> None:
    """Print success message."""
    _emit("success", message, printer)
