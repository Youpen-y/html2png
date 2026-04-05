---
sidebar_position: 2
---

# 快速开始

## 安装

### 1. 安装依赖

```bash
uv sync
```

### 2. 安装浏览器

```bash
uv run playwright install chromium
```

也可以安装 Firefox 或 WebKit：

```bash
uv run playwright install firefox
uv run playwright install webkit
```

### 3. 开始转换

```bash
uv run html2png convert input.html -o output.png
```

## 你的第一次转换

### CLI 用法

```bash
# 转换单个文件
html2png convert page.html -o output.png

# 转换 URL
html2png convert https://example.com -o screenshot.png

# 使用管道输入
cat page.html | html2png convert - -o output.png
```

### Python API

```python
import html2png

# 简单用法
html2png.render("page.html", "output.png")

# 自定义参数
html2png.render("page.html", "output.png", width=1920, height=1080, dpr=2.0)
```

## 下一步

- 了解更多 [CLI 用法](/docs/cli)
- 探索 [Python API](/docs/api)
- 使用 [配置文件](/docs/configuration)
