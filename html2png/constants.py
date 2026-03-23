"""Constants for html2png."""

import re

# Default values
DEFAULT_VIEWPORT_WIDTH = 1080
DEFAULT_VIEWPORT_HEIGHT = 1440
DEFAULT_DEVICE_SCALE_FACTOR = 3.0
DEFAULT_TIMEOUT_MS = 30000
DEFAULT_QUALITY = 80

# Compiled regex for URL detection (module-level for efficiency)
URL_PATTERN = re.compile(r"^(https?|file)://")

# Disable animations script (constant to avoid rebuilding)
DISABLE_ANIMATIONS_SCRIPT = """
() => {
    const style = document.createElement('style');
    style.innerHTML =
        `*, *::before, *::after { transition: none !important; animation: none !important; }`;
    document.head.appendChild(style);
}
"""

# Zoom script for scaling page content
ZOOM_SCRIPT = """
(zoomLevel) => {
    const style = document.createElement('style');
    style.innerHTML = `html { zoom: ${zoomLevel}; }`;
    document.head.appendChild(style);
}
"""

# Config file search paths
CONFIG_SEARCH_PATHS = [
    ".html2png.toml",
    "html2png.toml",
    "~/.config/html2png/config.toml",
]
