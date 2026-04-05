---
sidebar_position: 4
---

# Python API

## `render()` - Simple Conversion

The easiest way to convert HTML to image.

```python
import html2png

html2png.render("page.html", "output.png")
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input_source` | `str` | required | HTML file path, URL, or "-" for stdin |
| `output_path` | `str \| Path` | required | Output image file path |
| `width` | `int` | `1080` | Viewport width in pixels |
| `height` | `int` | `1440` | Viewport height in pixels |
| `dpr` | `float` | `3.0` | Device pixel ratio |
| `browser` | `str \| BrowserEngine` | `"chromium"` | Browser engine |
| `format` | `str \| ImageFormat` | `"png"` | Output format (png/jpeg) |
| `quality` | `int` | `None` | JPEG quality 0-100 |
| `full_page` | `bool` | `True` | Capture full page |
| `timeout` | `int` | `60000` | Navigation timeout in ms |
| `headless` | `bool` | `True` | Run browser in headless mode |
| `wait_for` | `str` | `None` | CSS selector to wait for |
| `wait_strategy` | `str \| PageLoadStrategy` | `"domcontentloaded"` | Page load strategy |
| `zoom` | `float` | `1.0` | Page zoom level |
| `config` | `Config` | `None` | Config object |

### Returns

`bool` - `True` if conversion succeeded, `False` otherwise

### Examples

```python
import html2png

# Basic usage
html2png.render("page.html", "output.png")

# Custom dimensions
html2png.render("page.html", "output.png", width=1920, height=1080)

# High DPI
html2png.render("page.html", "output.png", dpr=2.0)

# JPEG with quality
html2png.render("page.html", "output.jpg", format="jpeg", quality=90)

# From URL
html2png.render("https://example.com", "screenshot.png")

# With zoom
html2png.render("page.html", "output.png", zoom=1.5)
```

## `Renderer` - Batch Processing

Reuse browser instance for multiple conversions.

```python
with html2png.Renderer(width=1920, height=1080) as r:
    r.render("page1.html", "out1.png")
    r.render("page2.html", "out2.png")
    r.render("https://example.com", "screenshot.png")
```

### Constructor Parameters

Same as `render()` function parameters.

### Methods

#### `render(input_source, output_path, **kwargs)`

Render HTML to image using the shared browser instance.

**Additional kwargs override:** `format`, `quality`, `wait_for`, `timeout`

### Examples

```python
import html2png

# Batch processing with shared browser
with html2png.Renderer(width=1920, height=1080, dpr=2.0) as r:
    r.render("page1.html", "out1.png")
    r.render("page2.html", "out2.png")
    r.render("page3.html", "out3.png")

# Override format per render
with html2png.Renderer() as r:
    r.render("page1.html", "out1.png")
    r.render("page2.html", "out2.jpg", format="jpeg", quality=90)
```

## `Config` - Configuration Object

Create reusable configuration.

```python
config = html2png.Config(
    width=1920,
    height=1080,
    dpr=2.0,
    format="jpeg",
    quality=90
)
html2png.render("page.html", "output.jpg", config=config)
```

### Attributes

| Attribute | Type | Default |
|-----------|------|---------|
| `width` | `int` | `1080` |
| `height` | `int` | `1440` |
| `dpr` | `float` | `3.0` |
| `browser` | `str \| BrowserEngine` | `"chromium"` |
| `format` | `str \| ImageFormat` | `"png"` |
| `quality` | `int \| None` | `None` |
| `full_page` | `bool` | `True` |
| `timeout` | `int` | `60000` |
| `headless` | `bool` | `True` |
| `wait_for` | `str \| None` | `None` |
| `wait_strategy` | `str \| PageLoadStrategy` | `"domcontentloaded"` |
| `zoom` | `float` | `1.0` |

## Advanced Types

### `BrowserEngine`

```python
from html2png import BrowserEngine

BrowserEngine.CHROMIUM  # "chromium"
BrowserEngine.FIREFOX   # "firefox"
BrowserEngine.WEBKIT    # "webkit"
```

### `ImageFormat`

```python
from html2png import ImageFormat

ImageFormat.PNG   # "png"
ImageFormat.JPEG  # "jpeg"
```

### `PageLoadStrategy`

```python
from html2png import PageLoadStrategy

PageLoadStrategy.COMMIT            # "commit"
PageLoadStrategy.DOMCONTENTLOADED  # "domcontentloaded"
PageLoadStrategy.LOAD              # "load"
PageLoadStrategy.NETWORKIDLE       # "networkidle"
```
