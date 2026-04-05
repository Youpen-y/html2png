---
sidebar_position: 1
---

# 简介

**html2png** 是一个通用的 HTML 转图片工具，支持 CLI 和 Python API。

## 特性

- **高分辨率输出** - 自定义 DPR，默认 3.0 倍缩放，生成清晰锐利的图片
- **多浏览器支持** - Chromium、Firefox、WebKit 引擎可选
- **批量处理** - 支持批量转换多文件，可配置并行 worker
- **灵活配置** - 多种输出格式、尺寸预设、等待策略
- **完整页面截取** - 可选择截取整个页面或仅可视区域
- **配置文件支持** - TOML 配置文件，简化重复任务

## 技术栈

- **Playwright** - 浏览器自动化（Chromium/Firefox/WebKit）
- **Typer** - CLI 框架
- **Rich** - 终端输出美化
- **Python** - 3.11+

## 安装

```bash
# 安装依赖
uv sync

# 安装浏览器
uv run playwright install chromium

# 运行转换
uv run html2png convert input.html -o output.png
```

## 项目链接

- **仓库**: [github.com/Youpen-y/html2png](https://github.com/Youpen-y/html2png)
- **问题反馈**: [github.com/Youpen-y/html2png/issues](https://github.com/Youpen-y/html2png/issues)
- **许可证**: MIT
