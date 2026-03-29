# html2png - Claude Code Project Guide

## Project Overview

html2png is a universal HTML to image converter that supports both CLI and Python API. Built on Playwright for cross-platform browser automation, supporting Chromium, Firefox, and WebKit engines.

## Tech Stack

- **Python**: 3.11+
- **Playwright**: Browser automation
- **Typer**: CLI framework
- **Rich**: Terminal output formatting
- **uv**: Dependency management
- **ruff**: Code lint and format
- **pytest**: Testing framework

## Common Commands

```bash
# Install dependencies
uv sync

# Install browser
uv run playwright install chromium

# Run CLI
uv run html2png --help
uv run html2png convert input.html -o output.png
uv run html2png batch -p "*.html" -o output/

# Run tests
uv run pytest

# Code check
uv run ruff check .

# Code format
uv run ruff format .
```

## Project Structure

```
html2png/
├── html2png/
│   ├── __init__.py      # Package entry, public API (render, Renderer, Config)
│   ├── __main__.py      # Module execution support (python -m html2png)
│   ├── cli.py           # Typer CLI command definitions
│   ├── config.py        # Config dataclasses and loading logic
│   ├── constants.py     # Constants definition
│   ├── core.py          # Core conversion logic and browser management
│   └── utils.py         # Utility functions
├── tests/
│   ├── fixtures/        # Test resources
│   └── test_html2png.py # Test cases
└── pyproject.toml       # Project configuration
```

## Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `__init__.py` | Public API exports, `render()` function, `Renderer` context manager, `Config` dataclass |
| `cli.py` | CLI commands: `convert`, `batch`, `init-config`, `presets` |
| `config.py` | Config classes: `AppConfig`, `BrowserConfig`, `RenderConfig`, enum types |
| `constants.py` | Default values, URL regex, disable animations script, zoom script |
| `core.py` | `convert_html_to_image()`, `browser_context()` context manager |
| `utils.py` | Path handling, URL detection, output path generation |

## Public API

```python
import html2png

# Simple usage
html2png.render("input.html", "output.png")

# With parameters
html2png.render("page.html", "output.png", width=1920, height=1080, dpr=2.0)

# Batch processing (browser reuse)
with html2png.Renderer(width=1920, height=1080) as r:
    r.render("page1.html", "out1.png")
    r.render("page2.html", "out2.png")

# Using config object
config = html2png.Config(width=1920, height=1080, format="jpeg", quality=90)
html2png.render("page.html", "output.jpg", config=config)
```

## CLI Commands

### convert command
```bash
html2png convert input.html -o output.png
html2png convert https://example.com -o screenshot.png
html2png convert page.html --size mobile --dpr 3
html2png convert page.html --width 1920 --height 1080 --quality 90
```

### batch command
```bash
html2png batch -p "*.html" -o output/
html2png batch -p "cards/*.html" -o output/ -j 4  # 4 parallel workers
```

## Configuration System

Config file search order:
1. `.html2png.toml` (current directory)
2. `html2png.toml` (current directory)
3. `~/.config/html2png/config.toml`

Config merge priority: CLI args > Config file > Default values

## Coding Standards

- **Line length**: 100 characters
- **Quote style**: Double quotes
- **Indent**: Spaces
- **Lint rules**: E, F, I, N, W, UP, SIM (pycodestyle, Pyflakes, isort, pep8-naming, pyupgrade, flake8-simplify)

## Default Values

| Parameter | Default |
|-----------|---------|
| viewport | 1080 x 1440 |
| dpr | 3.0 |
| timeout | 60000ms |
| quality | 80 (JPEG) |
| browser | chromium |
| format | png |
| full_page | true |

## Size Presets

| Preset | Dimensions |
|--------|------------|
| mobile | 375 x 667 |
| tablet | 768 x 1024 |
| laptop | 1366 x 768 |
| desktop / 1080p | 1920 x 1080 |
| 2k | 2560 x 1440 |
| 4k | 3840 x 2160 |

## Development Notes

1. **Immutable config**: `merge_cli_config()` uses `deepcopy` to avoid mutating original config
2. **Local file optimization**: Local HTML files use `commit` wait strategy for faster processing
3. **Temp file cleanup**: stdin input creates temp files, cleaned in `finally` block
4. **Browser context**: Use `@contextmanager` to ensure browser is properly closed
5. **Error suggestions**: Timeout errors show suggested timeout value and other solutions
