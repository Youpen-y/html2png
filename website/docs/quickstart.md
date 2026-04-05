---
sidebar_position: 2
---

# Quick Start

## Installation

### 1. Install Dependencies

```bash
uv sync
```

### 2. Install Browser

```bash
uv run playwright install chromium
```

You can also install Firefox or WebKit:

```bash
uv run playwright install firefox
uv run playwright install webkit
```

### 3. Start Converting

```bash
uv run html2png convert input.html -o output.png
```

## Your First Conversion

### CLI Usage

```bash
# Convert a single file
html2png convert page.html -o output.png

# Convert a URL
html2png convert https://example.com -o screenshot.png

# Use pipe input
cat page.html | html2png convert - -o output.png
```

### Python API

```python
import html2png

# Simple usage
html2png.render("page.html", "output.png")

# With parameters
html2png.render("page.html", "output.png", width=1920, height=1080, dpr=2.0)
```

## What's Next?

- Learn more about [CLI Usage](/docs/cli)
- Explore the [Python API](/docs/api)
- Configure with [Configuration Files](/docs/configuration)
