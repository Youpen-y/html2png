"""Utility functions for html2png."""

import sys
from pathlib import Path

from .config import ImageFormat, InputSource
from .constants import URL_PATTERN


def generate_output_path(input_source: str, output_dir: Path, format: ImageFormat) -> Path:
    """Generate output path from input source and format.

    Args:
        input_source: Input file path or "-" for stdin
        output_dir: Output directory path
        format: Output image format

    Returns:
        Complete output file path
    """
    stem = "stdin" if input_source == "-" else Path(input_source).stem
    return output_dir / f"{stem}.{format.value}"


def path_to_file_url(path: Path) -> str:
    """Convert a file path to a file:// URL, handling cross-platform issues.

    Args:
        path: Path object representing the file

    Returns:
        file:// URL string
    """
    absolute = path.resolve()
    if sys.platform == "win32":
        # Windows: file:///C:/path/to/file.html
        return f"file:///{absolute.as_posix()}"
    else:
        # Unix/Mac: file:///path/to/file.html
        return f"file://{absolute}"


def detect_input_source(source: str) -> tuple[InputSource, str]:
    """Detect the type of input source.

    Args:
        source: Input source string (file path, URL, or "-")

    Returns:
        Tuple of (InputSource, processed source string)
    """
    if source == "-":
        return InputSource.STDIN, "-"

    # Check for URL patterns using compiled regex
    if URL_PATTERN.match(source):
        return InputSource.URL, source

    # Try to resolve as file path first (EAFP pattern)
    try:
        path = Path(source).resolve()
        if path.exists():
            return InputSource.FILE, str(path)
    except (OSError, RuntimeError):
        pass

    # If it looks like a path but doesn't exist, treat as potential URL
    if "." in source or "/" in source:
        url = source if "://" in source else f"https://{source}"
        return InputSource.URL, url

    # Default: treat as file path (will fail if doesn't exist)
    return InputSource.FILE, source
