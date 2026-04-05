---
sidebar_position: 1
---

# Introduction

**html2png** is a universal HTML to image converter that supports both CLI and Python API.

## Features

- **High Resolution Output** - Custom DPR support, default 3.0x scaling for crystal clear images
- **Multi-Browser Support** - Chromium, Firefox, and WebKit engines available
- **Batch Processing** - Convert multiple files with configurable parallel workers
- **Flexible Configuration** - Multiple output formats, size presets, wait strategies
- **Full Page Capture** - Capture entire page or viewport only
- **Config File Support** - TOML configuration files for simplified repetitive tasks

## Tech Stack

- **Playwright** - Browser automation (Chromium/Firefox/WebKit)
- **Typer** - CLI framework
- **Rich** - Terminal output formatting
- **Python** - 3.11+

## Installation

```bash
# Install dependencies
uv sync

# Install browser
uv run playwright install chromium

# Run conversion
uv run html2png convert input.html -o output.png
```

## Project Links

- **Repository**: [github.com/Youpen-y/html2png](https://github.com/Youpen-y/html2png)
- **Issues**: [github.com/Youpen-y/html2png/issues](https://github.com/Youpen-y/html2png/issues)
- **License**: MIT
