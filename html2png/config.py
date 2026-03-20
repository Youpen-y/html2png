"""Configuration data classes and loading logic."""

import tomllib
from copy import deepcopy
from dataclasses import dataclass, field, replace
from enum import StrEnum
from pathlib import Path

from rich.console import Console

from .constants import (
    DEFAULT_DEVICE_SCALE_FACTOR,
    DEFAULT_TIMEOUT_MS,
    DEFAULT_VIEWPORT_HEIGHT,
    DEFAULT_VIEWPORT_WIDTH,
)

console = Console()


class ImageFormat(StrEnum):
    """Supported output image formats.

    Note: Playwright only supports PNG and JPEG formats.
    """

    PNG = "png"
    JPEG = "jpeg"


class BrowserEngine(StrEnum):
    """Supported browser engines."""

    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"


class InputSource(StrEnum):
    """Input source types."""

    FILE = "file"
    URL = "url"
    STDIN = "stdin"


class PageLoadStrategy(StrEnum):
    """Page load strategies for navigation."""

    COMMIT = "commit"
    DOMCONTENTLOADED = "domcontentloaded"
    LOAD = "load"
    NETWORKIDLE = "networkidle"


@dataclass
class ViewportConfig:
    """Viewport configuration."""

    width: int = DEFAULT_VIEWPORT_WIDTH
    height: int = DEFAULT_VIEWPORT_HEIGHT


@dataclass
class RenderConfig:
    """Rendering configuration."""

    viewport: ViewportConfig = field(default_factory=ViewportConfig)
    device_scale_factor: float = DEFAULT_DEVICE_SCALE_FACTOR
    full_page: bool = True
    disable_animations: bool = True
    wait_for_selector: str | None = None
    wait_for_timeout: int = DEFAULT_TIMEOUT_MS
    wait_strategy: PageLoadStrategy = PageLoadStrategy.DOMCONTENTLOADED
    quality: int | None = None  # For JPEG format only


@dataclass
class BrowserConfig:
    """Browser configuration."""

    engine: BrowserEngine = BrowserEngine.CHROMIUM
    headless: bool = True
    slow_mo: int = 0


@dataclass
class AppConfig:
    """Main application configuration."""

    render: RenderConfig = field(default_factory=RenderConfig)
    browser: BrowserConfig = field(default_factory=BrowserConfig)
    output_format: ImageFormat = ImageFormat.PNG
    parallel_workers: int = 1


# Default configuration (deepcopy to prevent mutation)
DEFAULT_CONFIG = AppConfig()


def load_config_file(config_path: Path | None = None) -> AppConfig:
    """Load configuration from a TOML file.

    Args:
        config_path: Path to the configuration file. If None, looks for .html2png.toml

    Returns:
        AppConfig instance with loaded or default values
    """
    config = AppConfig()

    # Search for config file if not specified
    if config_path is None:
        candidates = [
            Path.cwd() / ".html2png.toml",
            Path.cwd() / "html2png.toml",
            Path.home() / ".config" / "html2png" / "config.toml",
        ]
        for candidate in candidates:
            try:
                if candidate.is_file():
                    config_path = candidate
                    break
            except OSError:
                continue
        else:
            return config

    # Try to load the config file (EAFP pattern)
    if not config_path:
        return config

    try:
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
    except (FileNotFoundError, OSError, tomllib.TOMLDecodeError) as e:
        console.print(f"[yellow]Warning: Failed to load config file: {e}[/yellow]")
        return config

    # Parse browser config
    if browser_data := data.get("browser"):
        if engine := browser_data.get("engine"):
            try:
                config.browser.engine = BrowserEngine(engine)
            except ValueError:
                console.print(f"[yellow]Warning: Unknown browser engine: {engine}[/yellow]")
        if (headless := browser_data.get("headless")) is not None:
            config.browser.headless = headless
        if (slow_mo := browser_data.get("slow_mo")) is not None:
            # Ensure slow_mo is an integer
            config.browser.slow_mo = int(slow_mo) if slow_mo else 0

    # Parse render config
    if render_data := data.get("render"):
        # Parse viewport
        if viewport_data := render_data.get("viewport"):
            config.render.viewport = ViewportConfig(
                width=viewport_data.get("width", DEFAULT_VIEWPORT_WIDTH),
                height=viewport_data.get("height", DEFAULT_VIEWPORT_HEIGHT),
            )

        # Parse other render options
        if (dpr := render_data.get("device_scale_factor")) is not None:
            config.render.device_scale_factor = dpr
        if (full_page := render_data.get("full_page")) is not None:
            config.render.full_page = full_page
        if (disable_animations := render_data.get("disable_animations")) is not None:
            config.render.disable_animations = disable_animations
        if (wait_selector := render_data.get("wait_for_selector")) is not None:
            config.render.wait_for_selector = wait_selector
        if (wait_timeout := render_data.get("wait_for_timeout")) is not None:
            config.render.wait_for_timeout = wait_timeout
        if (wait_strategy := render_data.get("wait_strategy")) is not None:
            try:
                config.render.wait_strategy = PageLoadStrategy(wait_strategy)
            except ValueError:
                console.print(f"[yellow]Warning: Unknown wait strategy: {wait_strategy}[/yellow]")
        if (quality := render_data.get("quality")) is not None:
            config.render.quality = quality

    # Parse output format
    if fmt := data.get("output_format"):
        try:
            config.output_format = ImageFormat(fmt)
        except ValueError:
            console.print(f"[yellow]Warning: Unknown output format: {fmt}[/yellow]")

    # Parse parallel workers
    if (workers := data.get("parallel_workers")) is not None:
        config.parallel_workers = workers

    return config


def merge_cli_config(config: AppConfig, **overrides) -> AppConfig:
    """Merge CLI overrides into configuration.

    Args:
        config: Base configuration
        **overrides: CLI option overrides

    Returns:
        New AppConfig with overrides applied (doesn't mutate original)
    """
    # Use deepcopy to avoid mutating the original config
    result = deepcopy(config)

    # Apply overrides
    if "format" in overrides and overrides["format"] is not None:
        result.output_format = overrides["format"]

    viewport_overrides = {}
    if "width" in overrides and overrides["width"] is not None:
        viewport_overrides["width"] = overrides["width"]
    if "height" in overrides and overrides["height"] is not None:
        viewport_overrides["height"] = overrides["height"]

    if viewport_overrides:
        result.render.viewport = replace(result.render.viewport, **viewport_overrides)

    render_overrides = {}
    if "dpr" in overrides and overrides["dpr"] is not None:
        render_overrides["device_scale_factor"] = overrides["dpr"]
    if "quality" in overrides and overrides["quality"] is not None:
        render_overrides["quality"] = overrides["quality"]
    if "full_page" in overrides:
        render_overrides["full_page"] = overrides["full_page"]
    if "wait_for" in overrides and overrides["wait_for"] is not None:
        render_overrides["wait_for_selector"] = overrides["wait_for"]
    if "timeout" in overrides and overrides["timeout"] is not None:
        render_overrides["wait_for_timeout"] = overrides["timeout"]
    if "wait_strategy" in overrides and overrides["wait_strategy"] is not None:
        render_overrides["wait_strategy"] = overrides["wait_strategy"]

    if render_overrides:
        result.render = replace(result.render, **render_overrides)

    browser_overrides = {}
    if "browser" in overrides and overrides["browser"] is not None:
        browser_overrides["engine"] = overrides["browser"]

    if browser_overrides:
        result.browser = replace(result.browser, **browser_overrides)

    return result
