---
sidebar_position: 5
---

# Configuration

## Config File

html2png supports TOML configuration files for default values and simplified workflows.

### Generate Config File

```bash
html2png init-config
```

This creates `.html2png.toml` in the current directory with default values.

### Search Order

Configuration files are searched in the following order:

1. `.html2png.toml` (current directory)
2. `html2png.toml` (current directory)
3. `~/.config/html2png/config.toml` (user config)

### Config Priority

CLI arguments > Config file > Default values

## Config File Structure

```toml
[browser]
# Browser engine: "chromium", "firefox", or "webkit"
engine = "chromium"
# Run in headless mode
headless = true
# Slow down operations by N milliseconds (useful for debugging)
slow_mo = 0

[render]
# Viewport configuration
[render.viewport]
width = 1080
height = 1440

# Device pixel ratio for high-resolution output
device_scale_factor = 3.0

# Capture the full page or just the viewport
full_page = true

# Disable animations for consistent screenshots
disable_animations = true

# Wait for a specific CSS selector before taking screenshot
# wait_for_selector = ".content-loaded"

# Page load strategy: "commit", "domcontentloaded", "load", or "networkidle"
wait_strategy = "domcontentloaded"

# Navigation timeout in milliseconds
wait_for_timeout = 60000

# Image quality for JPEG (0-100)
quality = 80

# Output format: "png" or "jpeg"
output_format = "png"

# Number of parallel workers for batch operations
parallel_workers = 1
```

## Options Reference

### Browser Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `engine` | `str` | `"chromium"` | Browser engine to use |
| `headless` | `bool` | `true` | Run browser in headless mode |
| `slow_mo` | `int` | `0` | Slow down operations by N ms |

### Render Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `viewport.width` | `int` | `1080` | Viewport width in pixels |
| `viewport.height` | `int` | `1440` | Viewport height in pixels |
| `device_scale_factor` | `float` | `3.0` | Device pixel ratio |
| `full_page` | `bool` | `true` | Capture full page |
| `disable_animations` | `bool` | `true` | Disable animations |
| `wait_for_selector` | `str \| null` | `null` | CSS selector to wait for |
| `wait_strategy` | `str` | `"domcontentloaded"` | Page load strategy |
| `wait_for_timeout` | `int` | `60000` | Timeout in milliseconds |
| `quality` | `int \| null` | `null` | JPEG quality (0-100) |
| `zoom` | `float` | `1.0` | Page zoom level |

### Output Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `output_format` | `str` | `"png"` | Output format (png/jpeg) |
| `parallel_workers` | `int` | `1` | Parallel workers for batch |

## Page Load Strategies

| Strategy | Description |
|----------|-------------|
| `commit` | Start loading immediately (fastest, for local files) |
| `domcontentloaded` | Wait for DOM to be parsed (default, most reliable) |
| `load` | Wait for all resources (images, stylesheets, etc.) |
| `networkidle` | Wait until no network requests for 500ms (may timeout on slow pages) |

## Examples

### Mobile Preview Config

```toml
[render.viewport]
width = 375
height = 667

[render]
device_scale_factor = 2.0
```

### High Quality JPEG Config

```toml
[render]
quality = 95
device_scale_factor = 2.0

[browser]
engine = "chromium"
```

### Fast Batch Processing

```toml
[render]
wait_strategy = "commit"
disable_animations = true
full_page = false

parallel_workers = 4
```
