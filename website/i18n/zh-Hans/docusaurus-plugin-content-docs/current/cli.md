---
sidebar_position: 3
---

# CLI 用法

## 命令

### `convert` - 转换单个文件

将单个 HTML 文件转换为图片。

```bash
html2png convert [OPTIONS] INPUT
```

**参数:**
- `INPUT` - 输入源：文件路径、URL 或 `-` 表示标准输入

**选项:**

| 选项 | 简写 | 描述 |
|------|------|------|
| `--output` | `-o` | 输出图片路径（默认：自动生成） |
| `--size` | `-s` | 视口尺寸（如 "1920x1080"、"mobile"、"4k"） |
| `--width` | `-W` | 视口宽度（覆盖 --size） |
| `--height` | `-H` | 视口高度（覆盖 --size） |
| `--dpr` | `-d` | 设备像素比（默认：3.0） |
| `--quality` | | JPEG 质量 0-100（默认：80） |
| `--zoom` | `-z` | 页面缩放级别（如 1.5 = 150%） |
| `--format` | `-f` | 输出格式（png/jpeg） |
| `--browser` | `-b` | 浏览器引擎（chromium/firefox/webkit） |
| `--full-page` | | 截取完整页面（默认：true） |
| `--viewport-only` | | 仅截取视口 |
| `--wait-for` | `-w` | 等待的 CSS 选择器 |
| `--timeout` | `-t` | 导航超时时间，单位毫秒（默认：60000） |
| `--wait-strategy` | `-ws` | 页面加载策略 |
| `--config` | `-c` | 配置文件路径 |
| `--verbose` | `-v` | 启用详细输出 |
| `--quiet` | `-q` | 隐藏进度输出 |

### `batch` - 批量转换

转换匹配模式的所有 HTML 文件。

```bash
html2png batch [OPTIONS]
```

**选项:**

| 选项 | 简写 | 描述 |
|------|------|------|
| `--pattern` | `-p` | HTML 文件的 glob 模式（默认："*.html"） |
| `--output-dir` | `-o` | 输出目录（默认：当前目录） |
| `--parallel` | `-j` | 并行 worker 数量（1-16） |
| `--dry-run` | `-n` | 显示将要转换的内容，不执行 |

`convert` 命令的所有选项也支持。

### `init-config` - 生成配置文件

创建默认配置文件。

```bash
html2png init-config [OPTIONS]
```

**选项:**

| 选项 | 简写 | 描述 |
|------|------|------|
| `--output` | `-o` | 输出文件路径（默认：.html2png.toml） |

### `presets` - 列出尺寸预设

显示可用的尺寸预设及其维度。

```bash
html2png presets
```

## 示例

### 基本转换

```bash
html2png convert page.html -o output.png
```

### 自定义尺寸

```bash
# 使用预设
html2png convert page.html --size mobile

# 自定义宽高
html2png convert page.html --width 1920 --height 1080

# 设置 DPR
html2png convert page.html --dpr 2.0
```

### 批量处理

```bash
# 转换所有 HTML 文件
html2png batch -p "*.html" -o output/

# 使用 4 个并行 worker
html2png batch -p "cards/*.html" -o output/ -j 4
```

### 不同浏览器

```bash
# 使用 Firefox
html2png convert page.html --browser firefox

# 使用 WebKit
html2png convert page.html --browser webkit
```

### JPEG 格式

```bash
html2png convert page.html -o output.jpg --format jpeg --quality 90
```

### 超时选项

```bash
html2png convert slow-page.html --timeout 120000
```
