---
sidebar_position: 6
---

# Size Presets

## Available Presets

html2png includes common viewport size presets for quick configuration.

| Preset | Width | Height | Description |
|--------|-------|--------|-------------|
| `mobile` | 375 | 667 | Mobile devices (iPhone SE) |
| `tablet` | 768 | 1024 | Tablet devices (iPad) |
| `laptop` | 1366 | 768 | Laptop screens |
| `desktop` / `1080p` | 1920 | 1080 | Desktop monitors (Full HD) |
| `2k` | 2560 | 1440 | 2K monitors (QHD) |
| `4k` | 3840 | 2160 | 4K monitors (UHD) |

## Usage

### CLI

```bash
# Use preset
html2png convert page.html --size mobile

# Override one dimension
html2png convert page.html --size desktop --width 2560
```

### Python API

```python
import html2png

# Presets not directly supported in API
# Use explicit dimensions instead
html2png.render("page.html", "output.png",
                width=375, height=667)  # mobile
```

## Custom Dimensions

You can specify custom dimensions using `WxH` format or separate options.

### CLI

```bash
# WxH format
html2png convert page.html --size 2560x1440

# Separate options
html2png convert page.html --width 2560 --height 1440
```

### Python API

```python
html2png.render("page.html", "output.png",
                width=2560, height=1440)
```

## Common Use Cases

### Social Media Cards

```bash
# Twitter/Facebook: 1200 x 630
html2png convert card.html --width 1200 --height 630 --dpr 2

# Instagram Post: 1080 x 1080
html2png convert card.html --width 1080 --height 1080 --dpr 2
```

### Documentation Screenshots

```bash
# Full HD screenshot
html2png convert docs.html --size desktop --dpr 2
```

### Mobile Preview

```bash
# iPhone preview
html2png convert page.html --size mobile --dpr 2

# Tablet preview
html2png convert page.html --size tablet --dpr 2
```

## DPR Recommendations

| Use Case | Recommended DPR |
|----------|-----------------|
| Web display | 2.0 - 3.0 |
| Print/High-res | 3.0 - 4.0 |
| Standard quality | 1.0 - 2.0 |
| Quick preview | 1.0 |
