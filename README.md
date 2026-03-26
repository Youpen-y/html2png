<div align="center">

# html2png

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Development Status](https://img.shields.io/badge/status-beta-yellow.svg)](https://github.com/Youpen-y/html2png)

**Universal HTML to Image Converter**

*Cross-platform CLI tool for converting HTML to images*

English | [**中文**](README.zh-CN.md)

</div>

## Features

- **Multiple Output Formats**: PNG, JPEG
- **Multiple Browser Engines**: Chromium, Firefox, WebKit
- **Multiple Input Sources**: Local files, URLs, stdin
- **Batch Processing**: Parallel conversion support
- **Configuration File**: TOML configuration support
- **Cross-platform**: Windows, macOS, Linux
- **High Resolution**: Default 3x DPR output
- **Modular Design**: Clean code structure, easy to extend

## Installation

> **Note**: The `html2png` package name on PyPI is currently occupied. Please install from source.

### Method 1: Install from Source (Recommended)

```bash
# Clone repository
git clone https://github.com/Youpen-y/html2png.git
cd html2png

# Install with pip (editable mode)
pip install -e .

# Install browser
playwright install chromium
```

### Method 2: Using uv

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone https://github.com/Youpen-y/html2png.git
cd html2png
uv sync

# Install browser
uv run playwright install chromium

# Run commands
uv run html2png --help
```

### Post-Installation

After installing, install the required browser:

```bash
playwright install chromium

# Or for all browsers
playwright install
```

## Usage

### Basic Usage

```bash
# Show version
html2png --version  # or: -V, -v

# Convert single file
html2png convert input.html -o output.png

# Convert URL
html2png convert https://example.com -o screenshot.png

# Read from stdin
cat input.html | html2png convert - -o output.png

# Batch conversion
html2png batch --pattern "*.html"

# Parallel batch conversion (4 workers)
html2png batch -p "cards/*.html" -o output/ -j 4
```

### Global Options

| Option | Short | Description |
|--------|-------|-------------|
| `--version` | `-V`, `-v` | Show version and exit |
| `--help` | `-h`, `-H` | Show help message |

### Command Options

#### convert Command

| Option | Short | Description |
|--------|-------|-------------|
| `--output` | `-o` | Output file path |
| `--format` | `-f` | Output format (png, jpeg) |
| `--size` | `-s` | Viewport size preset (mobile, tablet, desktop, 4k, etc.) |
| `--width` | `-W` | Viewport width (overrides --size) |
| `--height` | `-H` | Viewport height (overrides --size) |
| `--dpr` | `-d` | Device pixel ratio (default: 3.0) |
| `--zoom` | `-z` | Page zoom level (e.g., 1.5 = 150%, 2.0 = 200%) |
| `--quality` | | JPEG quality (0-100) |
| `--browser` | `-b` | Browser engine (chromium, firefox, webkit) |
| `--full-page` | `--viewport-only` | Capture full page (default) or only visible viewport |
| `--wait-for` | `-w` | Wait for specific CSS selector |
| `--wait-strategy` | `-ws` | Page load strategy (commit, domcontentloaded, load, networkidle) |
| `--timeout` | `-t` | Navigation timeout in milliseconds |
| `--config` | `-c` | Configuration file path |
| `--verbose` | `-v` | Verbose output |
| `--quiet` | `-q` | Suppress progress output (only show errors) |

#### batch Command

| Option | Short | Description |
|--------|-------|-------------|
| `--pattern` | `-p` | Glob pattern (default: *.html) |
| `--output-dir` | `-o` | Output directory |
| `--format` | `-f` | Output format |
| `--parallel` | `-j` | Number of parallel workers (1-16) |
| `--size` | `-s` | Viewport size preset (mobile, tablet, desktop, etc.) |
| `--dpr` | `-d` | Device pixel ratio (default: 3.0) |
| `--zoom` | `-z` | Page zoom level (e.g., 1.5 = 150%, 2.0 = 200%) |
| `--config` | `-c` | Configuration file path |
| `--dry-run` | `-n` | Preview mode |
| `--verbose` | `-v` | Verbose output |
| `--quiet` | `-q` | Suppress progress output (only show errors) |

### Available Commands

| Command | Description |
|---------|-------------|
| `convert` | Convert HTML to an image file |
| `batch` | Batch convert multiple HTML files |
| `init-config` | Create a default configuration file |
| `presets` | Show available size presets and their dimensions |

### Configuration File

Generate default configuration file:

```bash
html2png init-config
```

Generated `.html2png.toml` file:

```toml
[browser]
engine = "chromium"
headless = true
slow_mo = 0

[render.viewport]
width = 1080
height = 1440

device_scale_factor = 3.0     # equivalent to --dpr in CLI
full_page = true
disable_animations = true
wait_strategy = "domcontentloaded"
wait_for_timeout = 30000
quality = 80

output_format = "png"
parallel_workers = 1
```

## Examples

```bash
# Show version
html2png --version

# High resolution screenshot (3240x4320 with default 3x DPR)
html2png convert page.html -o output.png

# Use size preset (mobile, tablet, desktop, 4k, etc.)
html2png convert page.html -o output.png --size mobile
html2png convert page.html -o output.png --size 1920x1080

# Custom device pixel ratio (3x = high resolution)
html2png convert page.html -o output.png --dpr 3
html2png convert page.html -o output.png -d 2

# Zoom page content (1.5x = 150%, 2.0 = 200%)
html2png convert page.html -o output.png --zoom 1.5
html2png convert page.html -o output.png -z 2.0

# Custom dimensions and quality
html2png convert page.html -o output.jpg --width 1920 --height 1080 --quality 90

# Wait for page element to load
html2png convert https://example.com -o screenshot.png --wait-for ".loaded"

# Adjust timeout for slow pages
html2png convert slow-page.html -o output.png --timeout 60000

# Use different wait strategy
html2png convert page.html -o output.png --wait-strategy load
html2png convert page.html -o output.png --wait-strategy networkidle

# Use Firefox browser
html2png convert page.html -o output.png --browser firefox

# Capture only visible viewport
html2png convert page.html -o output.png --viewport-only

# Batch process all HTML files
html2png batch -p "*.html" -o output/

# Batch with size preset and parallel processing
html2png batch -p "cards/*.html" -o output/ --size mobile -j 4

# Show available size presets
html2png presets
```

## Project Structure

```
html2png/
├── html2png/
│   ├── __init__.py      # Package entry, version handling
│   ├── __main__.py      # Module execution support
│   ├── cli.py           # Typer command definitions
│   ├── config.py        # Configuration dataclasses and loading
│   ├── constants.py     # Constants definition
│   ├── core.py          # Core conversion logic
│   └── utils.py         # Utility functions
├── tests/
│   ├── fixtures/        # Test resources
│   └── test_html2png.py # Test cases
├── pyproject.toml       # Project configuration
├── uv.lock              # Dependency lock
└── README.md            # This document
```

### Module Descriptions

| Module | Responsibility |
|--------|---------------|
| `__init__.py` | Package entry, version handling, main entry point |
| `__main__.py` | Support for `python -m html2png` execution |
| `cli.py` | All Typer commands (convert, batch, init-config, presets) |
| `config.py` | Dataclasses, StrEnums, config loading and merging |
| `constants.py` | All magic numbers and constant strings |
| `core.py` | Browser management, screenshot building, HTML conversion |
| `utils.py` | Path handling, URL detection, output path generation |

## Development

```bash
# Install development dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Run code checks
uv run ruff check .

# Format code
uv run ruff format .

# Run command (local development)
uv run html2png --help
```

## Use as Python Library

Beyond the CLI tool, you can also use it directly in Python code:

### Quick Start

```python
import html2png
from html2png import BrowserEngine, ImageFormat, PageLoadStrategy

# Simple usage - render with default settings
html2png.render("input.html", "output.png")

# Custom dimensions
html2png.render("page.html", "output.png", width=1920, height=1080)

# JPEG with quality
html2png.render("page.html", "output.jpg", format="jpeg", quality=90)

# From URL
html2png.render("https://example.com", "screenshot.png")

# Adjust timeout for slow pages
html2png.render("slow-page.html", "output.png", timeout=60000)

# Use different wait strategy
html2png.render("page.html", "output.png", wait_strategy="load")
html2png.render("page.html", "output.png", wait_strategy=PageLoadStrategy.NETWORKIDLE)

# Zoom page content for larger text/elements
html2png.render("page.html", "output.png", zoom=1.5)  # 150% zoom
html2png.render("page.html", "output.png", zoom=2.0)  # 200% zoom
```

### Complete render() Parameters

```python
html2png.render(
    "page.html",                  # input: file path, URL, or "-" for stdin
    "output.png",                 # output: path to output image
    width=1920,                   # Viewport width in pixels
    height=1080,                  # Viewport height in pixels
    dpr=2.0,                      # Device pixel ratio (default: 3.0)
    browser="chromium",           # Browser engine: "chromium", "firefox", "webkit"
    format="jpeg",                # Output format: "png" or "jpeg"
    quality=90,                   # JPEG quality (0-100), only for JPEG format
    full_page=True,               # Capture full page (True) or viewport only (False)
    timeout=30000,                # Navigation timeout in milliseconds
    headless=True,                # Run browser in headless mode
    wait_for=".loaded",           # CSS selector to wait for before screenshot
    wait_strategy="load",         # Page load strategy: "commit", "domcontentloaded", "load", "networkidle"
    zoom=1.5,                     # Page zoom level (1.0 = 100%, 2.0 = 200%)
)
```

### Return Value and Error Handling

```python
# render() returns True on success, False on failure
success = html2png.render("page.html", "output.png")

if success:
    print("Conversion succeeded!")
else:
    print("Conversion failed!")

# For production use, wrap in try-except for unexpected errors
try:
    success = html2png.render("page.html", "output.png")
    if not success:
        raise RuntimeError("Failed to convert page")
except Exception as e:
    print(f"Error: {e}")
```

### Using Config Object

```python
# Create a reusable configuration
config = html2png.Config(
    width=1920,
    height=1080,
    dpr=2.0,
    browser=BrowserEngine.FIREFOX,
    format=ImageFormat.JPEG,
    wait_strategy=PageLoadStrategy.LOAD,
    timeout=60000,
)
html2png.render("page.html", "output.jpg", config=config)

# Keyword arguments override config values
config = html2png.Config(width=800, height=600)
html2png.render("page.html", "output.png", config=config, width=1920)  # uses 1920
```

### Loading Configuration File

```python
# Load settings from TOML file
config = html2png.load_config_file(".html2png.toml")
html2png.render("page.html", "output.png", config=config)

# Config file search order (if path not specified):
# 1. .html2png.toml (current directory)
# 2. html2png.toml (current directory)
# 3. ~/.config/html2png/config.toml
```

### Batch Processing with Renderer

```python
# Renderer reuses browser instance for better performance
with html2png.Renderer(width=1920, height=1080) as r:
    r.render("page1.html", "out1.png")
    r.render("page2.html", "out2.png")
    r.render("https://example.com", "screenshot.png")

# Renderer.render() supports parameter overrides
with html2png.Renderer(width=1920, height=1080, format="jpeg", quality=90) as r:
    r.render("page1.html", "out1.jpg")              # uses default JPEG
    r.render("page2.html", "out2.png", format="png")  # override to PNG
    r.render("page3.html", "out3.jpg", timeout=60000)  # override timeout
```

### Public API Reference

| Function/Class | Description |
|----------------|-------------|
| `render(input, output, **kwargs)` | Convert HTML to image (main entry point) |
| `Renderer(**kwargs)` | Context manager for batch processing with browser reuse |
| `Config(**kwargs)` | Configuration dataclass for reusable settings |
| `load_config_file(path)` | Load configuration from TOML file |
| `BrowserEngine` | Enum: `CHROMIUM`, `FIREFOX`, `WEBKIT` |
| `ImageFormat` | Enum: `PNG`, `JPEG` |
| `PageLoadStrategy` | Enum: `COMMIT`, `DOMCONTENTLOADED`, `LOAD`, `NETWORKIDLE` |

## Dependencies

- Python >= 3.11
- [Playwright](https://playwright.dev/) >= 1.58.0 - Browser automation
- [Typer](https://typer.tiangolo.com/) >= 0.24.1 - CLI framework
- [Rich](https://rich.readthedocs.io/) >= 14.3.3 - Terminal formatting

## License

MIT
