---
sidebar_position: 6
---

# 尺寸预设

## 可用预设

html2png 包含常用的视口尺寸预设，可快速配置。

| 预设 | 宽度 | 高度 | 描述 |
|------|------|------|------|
| `mobile` | 375 | 667 | 移动设备（iPhone SE） |
| `tablet` | 768 | 1024 | 平板设备（iPad） |
| `laptop` | 1366 | 768 | 笔记本屏幕 |
| `desktop` / `1080p` | 1920 | 1080 | 桌面显示器（全高清） |
| `2k` | 2560 | 1440 | 2K 显示器（QHD） |
| `4k` | 3840 | 2160 | 4K 显示器（UHD） |

## 用法

### CLI

```bash
# 使用预设
html2png convert page.html --size mobile

# 覆盖一个维度
html2png convert page.html --size desktop --width 2560
```

### Python API

```python
import html2png

# API 不直接支持预设
# 使用显式维度代替
html2png.render("page.html", "output.png",
                width=375, height=667)  # mobile
```

## 自定义尺寸

可以使用 `WxH` 格式或单独选项指定自定义尺寸。

### CLI

```bash
# WxH 格式
html2png convert page.html --size 2560x1440

# 分开指定
html2png convert page.html --width 2560 --height 1440
```

### Python API

```python
html2png.render("page.html", "output.png",
                width=2560, height=1440)
```

## 常见用例

### 社交媒体卡片

```bash
# Twitter/Facebook: 1200 x 630
html2png convert card.html --width 1200 --height 630 --dpr 2

# Instagram Post: 1080 x 1080
html2png convert card.html --width 1080 --height 1080 --dpr 2
```

### 文档截图

```bash
# 全高清截图
html2png convert docs.html --size desktop --dpr 2
```

### 移动端预览

```bash
# iPhone 预览
html2png convert page.html --size mobile --dpr 2

# 平板预览
html2png convert page.html --size tablet --dpr 2
```

## DPR 推荐

| 用例 | 推荐 DPR |
|------|----------|
| 网页展示 | 2.0 - 3.0 |
| 打印/高分辨率 | 3.0 - 4.0 |
| 标准质量 | 1.0 - 2.0 |
| 快速预览 | 1.0 |
