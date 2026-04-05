---
sidebar_position: 4
---

# Python API

## `render()` - 简单转换

最简单的 HTML 转图片方式。

```python
import html2png

html2png.render("page.html", "output.png")
```

### 参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `input_source` | `str` | 必填 | HTML 文件路径、URL 或 "-" 表示标准输入 |
| `output_path` | `str \| Path` | 必填 | 输出图片文件路径 |
| `width` | `int` | `1080` | 视口宽度（像素） |
| `height` | `int` | `1440` | 视口高度（像素） |
| `dpr` | `float` | `3.0` | 设备像素比 |
| `browser` | `str \| BrowserEngine` | `"chromium"` | 浏览器引擎 |
| `format` | `str \| ImageFormat` | `"png"` | 输出格式（png/jpeg） |
| `quality` | `int` | `None` | JPEG 质量 0-100 |
| `full_page` | `bool` | `True` | 截取完整页面 |
| `timeout` | `int` | `60000` | 导航超时时间（毫秒） |
| `headless` | `bool` | `True` | 无头模式运行浏览器 |
| `wait_for` | `str` | `None` | 等待的 CSS 选择器 |
| `wait_strategy` | `str \| PageLoadStrategy` | `"domcontentloaded"` | 页面加载策略 |
| `zoom` | `float` | `1.0` | 页面缩放级别 |
| `config` | `Config` | `None` | 配置对象 |

### 返回值

`bool` - 转换成功返回 `True`，否则返回 `False`

### 示例

```python
import html2png

# 基本用法
html2png.render("page.html", "output.png")

# 自定义尺寸
html2png.render("page.html", "output.png", width=1920, height=1080)

# 高 DPI
html2png.render("page.html", "output.png", dpr=2.0)

# JPEG 格式
html2png.render("page.html", "output.jpg", format="jpeg", quality=90)

# 从 URL 转换
html2png.render("https://example.com", "screenshot.png")

# 缩放
html2png.render("page.html", "output.png", zoom=1.5)
```

## `Renderer` - 批量处理

复用浏览器实例进行多次转换。

```python
with html2png.Renderer(width=1920, height=1080) as r:
    r.render("page1.html", "out1.png")
    r.render("page2.html", "out2.png")
    r.render("https://example.com", "screenshot.png")
```

### 构造函数参数

与 `render()` 函数参数相同。

### 方法

#### `render(input_source, output_path, **kwargs)`

使用共享浏览器实例渲染 HTML 为图片。

**额外可覆盖参数:** `format`、`quality`、`wait_for`、`timeout`

### 示例

```python
import html2png

# 批量处理，共享浏览器
with html2png.Renderer(width=1920, height=1080, dpr=2.0) as r:
    r.render("page1.html", "out1.png")
    r.render("page2.html", "out2.png")
    r.render("page3.html", "out3.png")

# 每次渲染覆盖格式
with html2png.Renderer() as r:
    r.render("page1.html", "out1.png")
    r.render("page2.html", "out2.jpg", format="jpeg", quality=90)
```

## `Config` - 配置对象

创建可复用的配置。

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

### 属性

| 属性 | 类型 | 默认值 |
|------|------|--------|
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

## 高级类型

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
