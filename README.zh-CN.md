<div align="center">

# html2png

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Development Status](https://img.shields.io/badge/status-beta-yellow.svg)](https://github.com/Youpen-y/html2png)

**通用 HTML 转图片转换器**

*跨平台 HTML 转图片命令行工具*

[**English**](README.md) | 中文

</div>

## 特性

- **多输出格式**: PNG, JPEG
- **多浏览器引擎**: Chromium, Firefox, WebKit
- **多输入源**: 本地文件、URL、标准输入
- **批量处理**: 支持并行转换
- **配置文件**: 支持 TOML 配置
- **跨平台**: Windows、macOS、Linux
- **高清输出**: 默认 3x DPR
- **模块化设计**: 清晰的代码结构，易于扩展

## 安装

> **注意**: PyPI 上的 `html2png` 包名已被占用，请从源码安装。

### 方法 1: 从源码安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/Youpen-y/html2png.git
cd html2png

# 使用 pip 安装（可编辑模式）
pip install -e .

# 安装浏览器
playwright install chromium
```

### 方法 2: 使用 uv

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆并安装
git clone https://github.com/Youpen-y/html2png.git
cd html2png
uv sync

# 安装浏览器
uv run playwright install chromium

# 运行命令
uv run html2png --help
```

### 安装后步骤

安装完成后，需要安装所需的浏览器：

```bash
playwright install chromium

# 或安装所有浏览器
playwright install
```

## 使用方法

### 基本用法

```bash
# 显示版本
html2png --version  # 或: -V, -v

# 转换单个文件
html2png convert input.html -o output.png

# 转换 URL
html2png convert https://example.com -o screenshot.png

# 从标准输入读取
cat input.html | html2png convert - -o output.png

# 批量转换
html2png batch --pattern "*.html"

# 并行批量转换 (4 个 worker)
html2png batch -p "cards/*.html" -o output/ -j 4
```

### 全局选项

| 选项 | 简写 | 说明 |
|------|------|------|
| `--version` | `-V`, `-v` | 显示版本并退出 |
| `--help` | `-h`, `-H` | 显示帮助信息 |

### 命令选项

#### convert 命令

| 选项 | 简写 | 说明 |
|------|------|------|
| `--output` | `-o` | 输出文件路径 |
| `--format` | `-f` | 输出格式 (png, jpeg) |
| `--size` | `-s` | 视口尺寸预设 (mobile, tablet, desktop, 4k 等) |
| `--width` | `-W` | 视口宽度 (覆盖 --size) |
| `--height` | `-H` | 视口高度 (覆盖 --size) |
| `--dpr` | `-d` | 设备像素比 (默认: 3.0) |
| `--quality` | | JPEG 质量 (0-100) |
| `--zoom` | `-z` | 页面缩放级别 (例如: 1.5 = 150%, 2.0 = 200%) |
| `--browser` | `-b` | 浏览器引擎 (chromium, firefox, webkit) |
| `--full-page` | `--viewport-only` | 截取完整页面 (默认) 或仅可见区域 |
| `--wait-for` | `-w` | 等待指定 CSS 选择器 |
| `--wait-strategy` | `-ws` | 页面加载策略 (commit, domcontentloaded, load, networkidle) |
| `--timeout` | `-t` | 导航超时 (毫秒) |
| `--config` | `-c` | 配置文件路径 |
| `--verbose` | `-v` | 详细输出 |
| `--quiet` | `-q` | 静默模式 (仅显示错误) |

#### batch 命令

| 选项 | 简写 | 说明 |
|------|------|------|
| `--pattern` | `-p` | Glob 匹配模式 (默认: *.html) |
| `--output-dir` | `-o` | 输出目录 |
| `--format` | `-f` | 输出格式 |
| `--parallel` | `-j` | 并行 worker 数量 (1-16) |
| `--size` | `-s` | 视口尺寸预设 (mobile, tablet, desktop 等) |
| `--width` | `-W` | 视口宽度 (覆盖 --size) |
| `--height` | `-H` | 视口高度 (覆盖 --size) |
| `--dpr` | `-d` | 设备像素比 (默认: 3.0) |
| `--zoom` | `-z` | 页面缩放级别 (例如: 1.5 = 150%, 2.0 = 200%) |
| `--quality` | | JPEG 质量 (0-100) |
| `--timeout` | `-t` | 导航超时 (毫秒) |
| `--wait-strategy` | `-ws` | 页面加载策略 (commit, domcontentloaded, load, networkidle) |
| `--config` | `-c` | 配置文件路径 |
| `--dry-run` | `-n` | 预览模式 |
| `--verbose` | `-v` | 详细输出 |
| `--quiet` | `-q` | 静默模式 (仅显示错误) |

### 可用命令

| 命令 | 说明 |
|------|------|
| `convert` | 转换 HTML 为图片文件 |
| `batch` | 批量转换多个 HTML 文件 |
| `init-config` | 创建默认配置文件 |
| `presets` | 显示可用的尺寸预设及其维度 |

### 配置文件

创建默认配置文件：

```bash
html2png init-config
```

生成的 `.html2png.toml` 文件：

```toml
[browser]
engine = "chromium"
headless = true
slow_mo = 0

[render.viewport]
width = 1080
height = 1440

device_scale_factor = 3.0     # 等同于 CLI 中的 --dpr
full_page = true
disable_animations = true
wait_strategy = "domcontentloaded"
wait_for_timeout = 30000
quality = 80

output_format = "png"
parallel_workers = 1
```

## 示例

```bash
# 显示版本
html2png --version

# 高清截图 (默认 3x DPR，输出 3240x4320)
html2png convert page.html -o output.png

# 使用尺寸预设 (mobile, tablet, desktop, 4k 等)
html2png convert page.html -o output.png --size mobile
html2png convert page.html -o output.png --size 1920x1080

# 自定义设备像素比 (3x = 高清)
html2png convert page.html -o output.png --dpr 3
html2png convert page.html -o output.png -d 2

# 指定尺寸和质量
html2png convert page.html -o output.jpg --width 1920 --height 1080 --quality 90

# 等待页面元素加载完成
html2png convert https://example.com -o screenshot.png --wait-for ".loaded"

# 调整超时时间 (慢速页面)
html2png convert slow-page.html -o output.png --timeout 60000

# 使用不同的等待策略
html2png convert page.html -o output.png --wait-strategy load
html2png convert page.html -o output.png --wait-strategy networkidle

# 使用 Firefox 浏览器
html2png convert page.html -o output.png --browser firefox

# 仅截取可见区域
html2png convert page.html -o output.png --viewport-only

# 批量处理所有 HTML 文件
html2png batch -p "*.html" -o output/

# 批量处理：使用尺寸预设和并行处理
html2png batch -p "cards/*.html" -o output/ --size mobile -j 4

# 显示可用的尺寸预设
html2png presets
```

## 项目结构

```
html2png/
├── html2png/
│   ├── __init__.py      # 包入口，版本处理
│   ├── __main__.py      # 模块执行支持
│   ├── cli.py           # Typer 命令定义
│   ├── config.py        # 配置数据类和加载
│   ├── constants.py     # 常量定义
│   ├── core.py          # 核心转换逻辑
│   └── utils.py         # 工具函数
├── tests/
│   ├── fixtures/        # 测试资源
│   └── test_html2png.py # 测试用例
├── pyproject.toml       # 项目配置
├── uv.lock              # 依赖锁定
└── README.md            # 本文档
```

### 模块说明

| 模块 | 职责 |
|------|------|
| `__init__.py` | 包入口，版本处理，主入口点 |
| `__main__.py` | 支持 `python -m html2png` 执行 |
| `cli.py` | 所有 Typer 命令（convert, batch, init-config, presets） |
| `config.py` | 数据类、StrEnum、配置加载和合并 |
| `constants.py` | 所有魔法数字和常量字符串 |
| `core.py` | 浏览器管理、截图构建、HTML 转换 |
| `utils.py` | 路径处理、URL 检测、输出路径生成 |

## 开发

```bash
# 安装开发依赖
uv sync --all-extras

# 运行测试
uv run pytest

# 运行代码检查
uv run ruff check .

# 格式化代码
uv run ruff format .

# 运行命令（本地开发）
uv run html2png --help
```

## 作为 Python 库使用

除了命令行工具，你也可以在 Python 代码中直接使用：

### 快速开始

```python
import html2png
from html2png import BrowserEngine, ImageFormat, PageLoadStrategy

# 简单用法 - 使用默认设置渲染
html2png.render("input.html", "output.png")

# 自定义尺寸
html2png.render("page.html", "output.png", width=1920, height=1080)

# JPEG 格式与质量
html2png.render("page.html", "output.jpg", format="jpeg", quality=90)

# 从 URL 渲染
html2png.render("https://example.com", "screenshot.png")

# 调整超时时间 (慢速页面)
html2png.render("slow-page.html", "output.png", timeout=60000)

# 使用不同的等待策略
html2png.render("page.html", "output.png", wait_strategy="load")
html2png.render("page.html", "output.png", wait_strategy=PageLoadStrategy.NETWORKIDLE)
```

### render() 完整参数列表

```python
html2png.render(
    "page.html",                  # input: 文件路径、URL 或 "-" 表示标准输入
    "output.png",                 # output: 输出图片路径
    width=1920,                   # 视口宽度（像素）
    height=1080,                  # 视口高度（像素）
    dpr=2.0,                      # 设备像素比（默认: 3.0）
    browser="chromium",           # 浏览器引擎: "chromium", "firefox", "webkit"
    format="jpeg",                # 输出格式: "png" 或 "jpeg"
    quality=90,                   # JPEG 质量 (0-100)，仅对 JPEG 格式有效
    full_page=True,               # 截取完整页面 (True) 或仅视口 (False)
    timeout=30000,                # 导航超时时间（毫秒）
    headless=True,                # 无头模式运行浏览器
    wait_for=".loaded",           # 截图前等待的 CSS 选择器
    wait_strategy="load",         # 页面加载策略: "commit", "domcontentloaded", "load", "networkidle"
)
```

### 返回值与错误处理

```python
# render() 成功返回 True，失败返回 False
success = html2png.render("page.html", "output.png")

if success:
    print("转换成功！")
else:
    print("转换失败！")

# 生产环境建议使用 try-except 捕获意外错误
try:
    success = html2png.render("page.html", "output.png")
    if not success:
        raise RuntimeError("页面转换失败")
except Exception as e:
    print(f"错误: {e}")
```

### 使用 Config 对象

```python
# 创建可复用的配置
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

# 关键字参数会覆盖配置值
config = html2png.Config(width=800, height=600)
html2png.render("page.html", "output.png", config=config, width=1920)  # 使用 1920
```

### 加载配置文件

```python
# 从 TOML 文件加载配置
config = html2png.load_config_file(".html2png.toml")
html2png.render("page.html", "output.png", config=config)

# 配置文件查找顺序（未指定路径时）：
# 1. .html2png.toml（当前目录）
# 2. html2png.toml（当前目录）
# 3. ~/.config/html2png/config.toml
```

### 批量处理（Renderer）

```python
# Renderer 复用浏览器实例，性能更佳
with html2png.Renderer(width=1920, height=1080) as r:
    r.render("page1.html", "out1.png")
    r.render("page2.html", "out2.png")
    r.render("https://example.com", "screenshot.png")

# Renderer.render() 支持参数覆盖
with html2png.Renderer(width=1920, height=1080, format="jpeg", quality=90) as r:
    r.render("page1.html", "out1.jpg")              # 使用默认 JPEG
    r.render("page2.html", "out2.png", format="png")  # 覆盖为 PNG
    r.render("page3.html", "out3.jpg", timeout=60000)  # 覆盖超时时间
```

### 公共 API 参考

| 函数/类 | 说明 |
|---------|------|
| `render(input, output, **kwargs)` | 转换 HTML 为图片（主入口） |
| `Renderer(**kwargs)` | 批量处理上下文管理器，复用浏览器实例 |
| `Config(**kwargs)` | 配置数据类，用于可复用的设置 |
| `load_config_file(path)` | 从 TOML 文件加载配置 |
| `BrowserEngine` | 枚举: `CHROMIUM`, `FIREFOX`, `WEBKIT` |
| `ImageFormat` | 枚举: `PNG`, `JPEG` |
| `PageLoadStrategy` | 枚举: `COMMIT`, `DOMCONTENTLOADED`, `LOAD`, `NETWORKIDLE` |

## 依赖

- Python >= 3.11
- [Playwright](https://playwright.dev/) >= 1.58.0 - 浏览器自动化
- [Typer](https://typer.tiangolo.com/) >= 0.24.1 - CLI 框架
- [Rich](https://rich.readthedocs.io/) >= 14.3.3 - 终端美化

## 许可

MIT
