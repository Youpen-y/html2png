---
sidebar_position: 3
---

# CLI Usage

## Commands

### `convert` - Convert Single File

Convert a single HTML file to an image.

```bash
html2png convert [OPTIONS] INPUT
```

**Arguments:**
- `INPUT` - Input source: file path, URL, or `-` for stdin

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--output` | `-o` | Output image path (default: auto-generated) |
| `--size` | `-s` | Viewport size (e.g., "1920x1080", "mobile", "4k") |
| `--width` | `-W` | Viewport width (overrides --size) |
| `--height` | `-H` | Viewport height (overrides --size) |
| `--dpr` | `-d` | Device pixel ratio (default: 3.0) |
| `--quality` | | JPEG quality 0-100 (default: 80) |
| `--zoom` | `-z` | Page zoom level (e.g., 1.5 = 150%) |
| `--format` | `-f` | Output format (png/jpeg) |
| `--browser` | `-b` | Browser engine (chromium/firefox/webkit) |
| `--full-page` | | Capture full page (default: true) |
| `--viewport-only` | | Capture viewport only |
| `--wait-for` | `-w` | CSS selector to wait for |
| `--timeout` | `-t` | Navigation timeout in ms (default: 60000) |
| `--wait-strategy` | `-ws` | Page load strategy |
| `--config` | `-c` | Path to config file |
| `--verbose` | `-v` | Enable verbose output |
| `--quiet` | `-q` | Suppress progress output |

### `batch` - Batch Convert Multiple Files

Convert multiple HTML files matching a pattern.

```bash
html2png batch [OPTIONS]
```

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--pattern` | `-p` | Glob pattern for HTML files (default: "*.html") |
| `--output-dir` | `-o` | Output directory (default: current) |
| `--parallel` | `-j` | Number of parallel workers (1-16) |
| `--dry-run` | `-n` | Show what would be converted |

All other options from `convert` command are also supported.

### `init-config` - Generate Config File

Create a default configuration file.

```bash
html2png init-config [OPTIONS]
```

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--output` | `-o` | Output file path (default: .html2png.toml) |

### `presets` - List Size Presets

Show available size presets and their dimensions.

```bash
html2png presets
```

## Examples

### Basic Conversion

```bash
html2png convert page.html -o output.png
```

### Custom Dimensions

```bash
# Use preset
html2png convert page.html --size mobile

# Custom width/height
html2png convert page.html --width 1920 --height 1080

# Set DPR
html2png convert page.html --dpr 2.0
```

### Batch Processing

```bash
# Convert all HTML files
html2png batch -p "*.html" -o output/

# Use 4 parallel workers
html2png batch -p "cards/*.html" -o output/ -j 4
```

### Different Browsers

```bash
# Use Firefox
html2png convert page.html --browser firefox

# Use WebKit
html2png convert page.html --browser webkit
```

### JPEG Format

```bash
html2png convert page.html -o output.jpg --format jpeg --quality 90
```

### Timeout Options

```bash
html2png convert slow-page.html --timeout 120000
```
