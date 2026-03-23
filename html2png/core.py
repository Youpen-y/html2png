"""Core conversion logic and browser management."""

import shutil
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

from playwright.sync_api import BrowserType, sync_playwright
from playwright.sync_api import Error as PlaywrightError
from rich.console import Console

from .config import (
    AppConfig,
    BrowserConfig,
    BrowserEngine,
    ImageFormat,
    InputSource,
    RenderConfig,
)
from .constants import DISABLE_ANIMATIONS_SCRIPT, ZOOM_SCRIPT
from .utils import detect_input_source, path_to_file_url

console = Console()


def _show_error_suggestions(error_str: str) -> None:
    """Show helpful suggestions based on error message content.

    Args:
        error_str: Error message string to analyze
    """
    if "Timeout" in error_str or "timeout" in error_str:
        console.print("\n[yellow]Suggestions:[/yellow]")
        console.print(
            "  • Increase timeout: [cyan]--timeout[/cyan] or [cyan]-t[/cyan] (e.g., --timeout 60000)"
        )
        console.print(
            "  • For slow pages, wait for specific element: [cyan]--wait-for[/cyan] selector"
        )
        console.print("  • Use viewport-only mode: [cyan]--viewport-only[/cyan]")
        console.print("  • Try a different browser: [cyan]--browser firefox[/cyan]")
    elif "Navigation" in error_str:
        console.print("\n[yellow]Suggestions:[/yellow]")
        console.print("  • Check if the URL is accessible")
        console.print("  • Try with [cyan]--timeout 60000[/cyan] for slower connections")


def get_browser_type(playwright_context, engine: BrowserEngine) -> BrowserType:
    """Get the browser type from Playwright context."""
    browser_map = {
        BrowserEngine.CHROMIUM: playwright_context.chromium,
        BrowserEngine.FIREFOX: playwright_context.firefox,
        BrowserEngine.WEBKIT: playwright_context.webkit,
    }
    return browser_map[engine]


def build_screenshot_options(output_path: Path, config: AppConfig) -> dict:
    """Build screenshot options dict from config.

    Args:
        output_path: Path to output file
        config: Application configuration

    Returns:
        Dictionary of screenshot options for Playwright
    """
    options = {
        "path": str(output_path),
        "full_page": config.render.full_page,
    }

    # Add format-specific options (JPEG supports quality)
    if config.output_format == ImageFormat.JPEG:
        options["type"] = config.output_format.value
        if config.render.quality is not None:
            options["quality"] = config.render.quality

    return options


@contextmanager
def browser_context(config: BrowserConfig, render_config: RenderConfig):
    """Context manager for browser setup and teardown.

    Args:
        config: Browser configuration
        render_config: Render configuration for viewport settings

    Yields:
        Tuple of (page, browser) objects
    """
    with sync_playwright() as p:
        browser_type = get_browser_type(p, config.engine)
        browser = browser_type.launch(
            headless=config.headless,
            slow_mo=config.slow_mo,
        )

        page = browser.new_page(
            viewport={
                "width": render_config.viewport.width,
                "height": render_config.viewport.height,
            },
            device_scale_factor=render_config.device_scale_factor,
        )

        try:
            yield page, browser
        finally:
            browser.close()


def _convert_with_page(
    page,
    input_source: str,
    output_path: Path,
    config: AppConfig,
) -> bool:
    """Convert HTML to image using an existing page instance.

    Args:
        page: Existing Playwright page object
        input_source: HTML file path, URL, or "-" for stdin
        output_path: Path to output image file
        config: Application configuration

    Returns:
        True if successful, False otherwise
    """
    source_type, processed_source = detect_input_source(input_source)

    # Handle stdin input
    temp_path: Path | None = None

    if source_type == InputSource.STDIN:
        # Validate stdin is not a terminal (interactive input not supported)
        if sys.stdin.isatty():
            console.print("[red]Error:[/red] stdin input requires piped or redirected input")
            console.print("\n[yellow]Usage:[/yellow]")
            console.print("  cat file.html | html2png convert - -o output.png")
            console.print("  html2png convert - -o output.png < file.html")
            return False

        # Create temp file for stdin content (stream to avoid loading all in memory)
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".html", delete=False) as f:
            temp_path = Path(f.name)
            # Stream stdin in chunks
            shutil.copyfileobj(sys.stdin.buffer, f)
        url = path_to_file_url(temp_path)
    elif source_type == InputSource.FILE:
        url = path_to_file_url(Path(processed_source))
        temp_path = None
    else:  # URL
        url = processed_source
        temp_path = None

    try:
        # Determine wait strategy
        # - Local files: use 'commit' (fastest, DOM starts loading)
        # - Configured strategy: use what user specified
        # - Default: domcontentloaded (more forgiving than networkidle)
        if source_type == InputSource.FILE:
            wait_strategy = "commit"
        else:
            wait_strategy = config.render.wait_strategy.value

        # Disable animations if configured (must be before goto)
        if config.render.disable_animations:
            page.add_init_script(DISABLE_ANIMATIONS_SCRIPT)

        # Navigate to the page
        page.goto(
            url,
            wait_until=wait_strategy,
            timeout=config.render.wait_for_timeout,
        )

        # Apply zoom if configured
        if config.render.zoom != 1.0:
            page.evaluate(ZOOM_SCRIPT, config.render.zoom)

        # Wait for specific selector if configured
        if config.render.wait_for_selector:
            page.wait_for_selector(
                config.render.wait_for_selector,
                timeout=config.render.wait_for_timeout,
            )

        # Take screenshot
        screenshot_options = build_screenshot_options(output_path, config)
        page.screenshot(**screenshot_options)

        return True

    except PlaywrightError as e:
        console.print(f"\n[red]Browser error:[/red] {e}")
        _show_error_suggestions(str(e))
        return False
    except OSError as e:
        console.print(f"\n[red]File error: {e}[/red]")
        return False
    except Exception as e:
        console.print(f"\n[red]Error converting {input_source}: {e}[/red]")
        return False
    finally:
        # Cleanup temp file if created
        if temp_path is not None:
            from contextlib import suppress

            with suppress(OSError):
                temp_path.unlink()


def convert_html_to_image(
    input_source: str,
    output_path: Path,
    config: AppConfig,
) -> bool:
    """Convert HTML content to an image file.

    Creates a new browser instance for this conversion.
    For batch processing, use the Renderer class instead.

    Args:
        input_source: HTML file path, URL, or "-" for stdin
        output_path: Path to output image file
        config: Application configuration

    Returns:
        True if successful, False otherwise
    """
    try:
        with browser_context(config.browser, config.render) as (page, _browser):
            return _convert_with_page(page, input_source, output_path, config)
    except PlaywrightError as e:
        console.print(f"\n[red]Browser error:[/red] {e}")
        _show_error_suggestions(str(e))
        return False
    except OSError as e:
        console.print(f"\n[red]File error: {e}[/red]")
        return False
    except Exception as e:
        console.print(f"\n[red]Error converting {input_source}: {e}[/red]")
        return False
