"""html2png - Universal HTML to Image Converter

A cross-platform tool to convert HTML files to images using Playwright.

CLI Usage:
    html2png convert input.html -o output.png
    html2png convert https://example.com -o screenshot.png

Library Usage:
    >>> import html2png
    >>>
    >>> # Simple usage
    >>> html2png.render("page.html", "output.png")
    >>>
    >>> # With parameters
    >>> html2png.render("page.html", "output.png", width=1920, height=1080)
    >>>
    >>> # Using config object
    >>> config = html2png.Config(width=1920, height=1080, dpr=2.0)
    >>> html2png.render("page.html", "output.png", config=config)
    >>>
    >>> # Batch processing (browser reuse)
    >>> with html2png.Renderer(width=1920) as r:
    ...     r.render("page1.html", "out1.png")
    ...     r.render("page2.html", "out2.png")
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Self

from .cli import app
from .config import (
    AppConfig,
    BrowserConfig,
    BrowserEngine,
    ImageFormat,
    PageLoadStrategy,
    ViewportConfig,
    merge_cli_config,
)
from .config import (
    load_config_file as _load_config_file,
)
from .constants import (
    DEFAULT_DEVICE_SCALE_FACTOR,
    DEFAULT_TIMEOUT_MS,
    DEFAULT_VIEWPORT_HEIGHT,
    DEFAULT_VIEWPORT_WIDTH,
)
from .core import convert_html_to_image

# Version - keep in sync with pyproject.toml
__version__ = "0.2.0"


# ============================================================================
# Simplified Configuration
# ============================================================================


@dataclass
class Config:
    """Simplified configuration for html2png.

    Attributes:
        width: Viewport width in pixels
        height: Viewport height in pixels
        dpr: Device pixel ratio (default: 3.0)
        browser: Browser engine to use
        format: Output format
        quality: JPEG quality 0-100 (only for JPEG)
        full_page: Capture full page or just viewport
        timeout: Navigation timeout in milliseconds
        headless: Run browser in headless mode
        wait_for: CSS selector to wait for before screenshot
        wait_strategy: Page load strategy
        zoom: Page zoom level (1.0 = 100%, 2.0 = 200%)
    """

    width: int = DEFAULT_VIEWPORT_WIDTH
    height: int = DEFAULT_VIEWPORT_HEIGHT
    dpr: float = DEFAULT_DEVICE_SCALE_FACTOR
    browser: BrowserEngine | str = BrowserEngine.CHROMIUM
    format: ImageFormat | str = ImageFormat.PNG
    quality: int | None = None
    full_page: bool = True
    timeout: int = DEFAULT_TIMEOUT_MS
    headless: bool = True
    wait_for: str | None = None
    wait_strategy: PageLoadStrategy | str = PageLoadStrategy.DOMCONTENTLOADED
    zoom: float = 1.0

    def to_app_config(self) -> AppConfig:
        """Convert to internal AppConfig."""
        config = AppConfig()

        # Set viewport
        config.render.viewport = ViewportConfig(width=self.width, height=self.height)
        config.render.device_scale_factor = self.dpr
        config.render.full_page = self.full_page
        config.render.wait_for_selector = self.wait_for
        config.render.wait_for_timeout = self.timeout
        config.render.wait_strategy = (
            self.wait_strategy
            if isinstance(self.wait_strategy, PageLoadStrategy)
            else PageLoadStrategy(self.wait_strategy)
        )
        config.render.quality = self.quality
        config.render.zoom = self.zoom

        # Set browser (convert string to enum)
        config.browser.engine = (
            self.browser if isinstance(self.browser, BrowserEngine) else BrowserEngine(self.browser)
        )
        config.browser.headless = self.headless

        # Set format (convert string to enum)
        config.output_format = (
            self.format if isinstance(self.format, ImageFormat) else ImageFormat(self.format)
        )

        return config


# ============================================================================
# Public API - render() function
# ============================================================================


def render(
    input_source: str,
    output_path: str | Path,
    *,
    width: int | None = None,
    height: int | None = None,
    dpr: float | None = None,
    browser: BrowserEngine | str | None = None,
    format: ImageFormat | str | None = None,
    quality: int | None = None,
    full_page: bool | None = None,
    timeout: int | None = None,
    headless: bool | None = None,
    wait_for: str | None = None,
    wait_strategy: PageLoadStrategy | str | None = None,
    zoom: float | None = None,
    config: Config | None = None,
) -> bool:
    """Render HTML to image.

    This is the main entry point for converting HTML to images.
    Supports both simple usage with keyword arguments and advanced usage
    with a Config object.

    Args:
        input_source: HTML file path, URL, or "-" for stdin
        output_path: Output image file path
        width: Viewport width in pixels
        height: Viewport height in pixels
        dpr: Device pixel ratio for high-resolution output
        browser: Browser engine (BrowserEngine enum or string)
        format: Output format (ImageFormat enum or string)
        quality: JPEG quality (0-100), only for JPEG format
        full_page: Capture full page (True) or viewport only (False)
        timeout: Navigation timeout in milliseconds
        headless: Run browser in headless mode
        wait_for: CSS selector to wait for before screenshot
        wait_strategy: Page load strategy (PageLoadStrategy enum or string)
        zoom: Page zoom level (e.g., 1.5 = 150%, 2.0 = 200%)
        config: Optional Config object (keyword arguments override config values)

    Returns:
        True if conversion succeeded, False otherwise

    Examples:
        >>> import html2png
        >>>
        >>> # Simple usage
        >>> html2png.render("page.html", "output.png")
        True
        >>>
        >>> # With custom dimensions
        >>> html2png.render("page.html", "output.png", width=1920, height=1080)
        True
        >>>
        >>> # JPEG with quality
        >>> html2png.render("page.html", "output.jpg", format="jpeg", quality=90)
        True
        >>>
        >>> # From URL
        >>> html2png.render("https://example.com", "screenshot.png")
        True
        >>>
        >>> # Using config object
        >>> config = html2png.Config(width=1920, height=1080, dpr=2.0)
        >>> html2png.render("page.html", "output.png", config=config)
        True
        >>>
        >>> # With zoom
        >>> html2png.render("page.html", "output.png", zoom=1.5)
        True
    """
    output = Path(output_path)

    # Build configuration - keyword args override config
    if config is None:
        config = Config()

    # Apply keyword overrides (they take precedence over config)
    if width is not None:
        config.width = width
    if height is not None:
        config.height = height
    if dpr is not None:
        config.dpr = dpr
    if browser is not None:
        config.browser = browser if isinstance(browser, BrowserEngine) else BrowserEngine(browser)
    if format is not None:
        config.format = format if isinstance(format, ImageFormat) else ImageFormat(format)
    if quality is not None:
        config.quality = quality
    if full_page is not None:
        config.full_page = full_page
    if timeout is not None:
        config.timeout = timeout
    if headless is not None:
        config.headless = headless
    if wait_for is not None:
        config.wait_for = wait_for
    if wait_strategy is not None:
        config.wait_strategy = (
            wait_strategy
            if isinstance(wait_strategy, PageLoadStrategy)
            else PageLoadStrategy(wait_strategy)
        )
    if zoom is not None:
        config.zoom = zoom

    # Ensure output directory exists
    output.parent.mkdir(parents=True, exist_ok=True)

    # Perform conversion
    return convert_html_to_image(input_source, output, config.to_app_config())


# ============================================================================
# Public API - Renderer context manager
# ============================================================================


class Renderer:
    """Browser renderer with context management for batch processing.

    This class provides a way to reuse browser instances across multiple
    conversions, which is more efficient for batch processing.

    Examples:
        >>> import html2png
        >>>
        >>> # Batch processing
        >>> with html2png.Renderer(width=1920, height=1080) as r:
        ...     r.render("page1.html", "out1.png")
        ...     r.render("page2.html", "out2.png")
        ...     r.render("https://example.com", "screenshot.png")
    """

    def __init__(
        self,
        *,
        width: int = DEFAULT_VIEWPORT_WIDTH,
        height: int = DEFAULT_VIEWPORT_HEIGHT,
        dpr: float = DEFAULT_DEVICE_SCALE_FACTOR,
        browser: BrowserEngine | str = BrowserEngine.CHROMIUM,
        format: ImageFormat | str = ImageFormat.PNG,
        quality: int | None = None,
        full_page: bool = True,
        timeout: int = DEFAULT_TIMEOUT_MS,
        headless: bool = True,
        wait_for: str | None = None,
        wait_strategy: PageLoadStrategy | str = PageLoadStrategy.DOMCONTENTLOADED,
        zoom: float = 1.0,
    ):
        """Initialize the Renderer.

        Args:
            width: Viewport width in pixels
            height: Viewport height in pixels
            dpr: Device pixel ratio
            browser: Browser engine (BrowserEngine enum or string)
            format: Output format (ImageFormat enum or string)
            quality: JPEG quality (0-100)
            full_page: Capture full page or viewport only
            timeout: Navigation timeout in milliseconds
            headless: Run browser in headless mode
            wait_for: CSS selector to wait for
            wait_strategy: Page load strategy (PageLoadStrategy enum or string)
            zoom: Page zoom level (1.0 = 100%, 2.0 = 200%)
        """
        self._config = Config(
            width=width,
            height=height,
            dpr=dpr,
            browser=browser if isinstance(browser, BrowserEngine) else BrowserEngine(browser),
            format=format if isinstance(format, ImageFormat) else ImageFormat(format),
            quality=quality,
            full_page=full_page,
            timeout=timeout,
            headless=headless,
            wait_for=wait_for,
            wait_strategy=wait_strategy
            if isinstance(wait_strategy, PageLoadStrategy)
            else PageLoadStrategy(wait_strategy),
            zoom=zoom,
        )
        self._app_config = self._config.to_app_config()
        # These will be set in __enter__
        self._playwright = None
        self._browser = None
        self._page = None

    def render(
        self,
        input_source: str,
        output_path: str | Path,
        *,
        format: ImageFormat | str | None = None,
        quality: int | None = None,
        wait_for: str | None = None,
        timeout: int | None = None,
    ) -> bool:
        """Render HTML to image using the shared browser instance.

        Args:
            input_source: HTML file path, URL, or "-" for stdin
            output_path: Output image file path
            format: Output format override (ImageFormat enum or string)
            quality: JPEG quality override
            wait_for: CSS selector wait override
            timeout: Timeout override

        Returns:
            True if conversion succeeded, False otherwise
        """
        if self._page is None:
            raise RuntimeError(
                "Renderer not initialized. Use as a context manager: "
                "'with Renderer() as r: r.render(...)'"
            )

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        # Use shared config with optional overrides
        app_config = self._app_config

        if format is not None:
            fmt = format if isinstance(format, ImageFormat) else ImageFormat(format)
            app_config = merge_cli_config(app_config, format=fmt)
        if quality is not None:
            app_config = merge_cli_config(app_config, quality=quality)
        if wait_for is not None:
            app_config = merge_cli_config(app_config, wait_for=wait_for)
        if timeout is not None:
            app_config = merge_cli_config(app_config, timeout=timeout)

        from .core import _convert_with_page

        return _convert_with_page(self._page, input_source, output, app_config)

    def __enter__(self) -> Self:
        """Enter the context manager and initialize browser."""
        from playwright.sync_api import sync_playwright

        from .core import get_browser_type

        self._playwright = sync_playwright().start()
        # Convert browser to enum if it's a string
        browser_engine = (
            self._config.browser
            if isinstance(self._config.browser, BrowserEngine)
            else BrowserEngine(self._config.browser)
        )
        browser_type = get_browser_type(self._playwright, browser_engine)
        self._browser = browser_type.launch(headless=self._config.headless)
        self._page = self._browser.new_page(
            viewport={"width": self._config.width, "height": self._config.height},
            device_scale_factor=self._config.dpr,
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager and cleanup browser resources."""
        if hasattr(self, "_page") and self._page is not None:
            self._page.close()
            self._page = None
        if hasattr(self, "_browser") and self._browser is not None:
            self._browser.close()
            self._browser = None
        if hasattr(self, "_playwright") and self._playwright is not None:
            self._playwright.stop()
            self._playwright = None


# ============================================================================
# CLI Entry Point
# ============================================================================


def main() -> None:
    """Main entry point for CLI usage."""
    import sys

    # Check for --version, -V, or standalone -v
    if len(sys.argv) == 2 and sys.argv[1] in ("--version", "-V", "-v"):
        from rich.console import Console

        console = Console()
        console.print(f"html2png v{__version__}")
        sys.exit(0)

    # Check for --help, -h, or -H and convert to --help for Typer
    if len(sys.argv) == 2 and sys.argv[1] in ("--help", "-h", "-H"):
        sys.argv[1] = "--help"

    # Delegate to Typer for all other commands
    app()


# ============================================================================
# Public API Exports
# ============================================================================

__all__ = [
    # Main API
    "render",
    "Renderer",
    "Config",
    # Advanced/internal (for power users)
    "AppConfig",
    "BrowserConfig",
    "BrowserEngine",
    "ImageFormat",
    "PageLoadStrategy",
    "load_config_file",
]


# ============================================================================
# Utility Functions
# ============================================================================


def load_config_file(config_path: str | Path) -> Config:
    """Load configuration from a TOML file.

    Args:
        config_path: Path to the TOML configuration file

    Returns:
        Config object with loaded settings
    """
    app_config = _load_config_file(Path(config_path))

    return Config(
        width=app_config.render.viewport.width,
        height=app_config.render.viewport.height,
        dpr=app_config.render.device_scale_factor,
        browser=app_config.browser.engine,
        format=app_config.output_format,
        quality=app_config.render.quality,
        full_page=app_config.render.full_page,
        timeout=app_config.render.wait_for_timeout,
        headless=app_config.browser.headless,
        wait_for=app_config.render.wait_for_selector,
        wait_strategy=app_config.render.wait_strategy,
    )
