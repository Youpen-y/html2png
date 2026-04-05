---
sidebar_position: 5
---

# 配置

## 配置文件

html2png 支持 TOML 配置文件，用于设置默认值和简化工作流程。

### 生成配置文件

```bash
html2png init-config
```

这将在当前目录创建 `.html2png.toml`，包含默认值。

### 搜索顺序

配置文件按以下顺序搜索：

1. `.html2png.toml`（当前目录）
2. `html2png.toml`（当前目录）
3. `~/.config/html2png/config.toml`（用户配置）

### 配置优先级

CLI 参数 > 配置文件 > 默认值

## 配置文件结构

```toml
[browser]
# 浏览器引擎："chromium"、"firefox" 或 "webkit"
engine = "chromium"
# 无头模式运行
headless = true
# 慢速操作，延迟 N 毫秒（用于调试）
slow_mo = 0

[render]
# 视口配置
[render.viewport]
width = 1080
height = 1440

# 设备像素比，用于高分辨率输出
device_scale_factor = 3.0

# 截取完整页面或仅视口
full_page = true

# 禁用动画以获得一致的截图
disable_animations = true

# 截图前等待特定的 CSS 选择器
# wait_for_selector = ".content-loaded"

# 页面加载策略："commit"、"domcontentloaded"、"load" 或 "networkidle"
wait_strategy = "domcontentloaded"

# 导航超时时间（毫秒）
wait_for_timeout = 60000

# JPEG 图像质量（0-100）
quality = 80

# 输出格式："png" 或 "jpeg"
output_format = "png"

# 批量操作的并行 worker 数量
parallel_workers = 1
```

## 选项参考

### 浏览器选项

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `engine` | `str` | `"chromium"` | 使用的浏览器引擎 |
| `headless` | `bool` | `true` | 无头模式运行浏览器 |
| `slow_mo` | `int` | `0` | 慢速操作，延迟 N 毫秒 |

### 渲染选项

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `viewport.width` | `int` | `1080` | 视口宽度（像素） |
| `viewport.height` | `int` | `1440` | 视口高度（像素） |
| `device_scale_factor` | `float` | `3.0` | 设备像素比 |
| `full_page` | `bool` | `true` | 截取完整页面 |
| `disable_animations` | `bool` | `true` | 禁用动画 |
| `wait_for_selector` | `str \| null` | `null` | 等待的 CSS 选择器 |
| `wait_strategy` | `str` | `"domcontentloaded"` | 页面加载策略 |
| `wait_for_timeout` | `int` | `60000` | 超时时间（毫秒） |
| `quality` | `int \| null` | `null` | JPEG 质量（0-100） |
| `zoom` | `float` | `1.0` | 页面缩放级别 |

### 输出选项

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `output_format` | `str` | `"png"` | 输出格式（png/jpeg） |
| `parallel_workers` | `int` | `1` | 批量处理的并行 worker 数 |

## 页面加载策略

| 策略 | 描述 |
|------|------|
| `commit` | 立即开始加载（最快，用于本地文件） |
| `domcontentloaded` | 等待 DOM 解析完成（默认，最可靠） |
| `load` | 等待所有资源加载（图片、样式表等） |
| `networkidle` | 等待 500ms 无网络请求（可能在慢页面超时） |

## 示例

### 移动端预览配置

```toml
[render.viewport]
width = 375
height = 667

[render]
device_scale_factor = 2.0
```

### 高质量 JPEG 配置

```toml
[render]
quality = 95
device_scale_factor = 2.0

[browser]
engine = "chromium"
```

### 快速批量处理

```toml
[render]
wait_strategy = "commit"
disable_animations = true
full_page = false

parallel_workers = 4
```
