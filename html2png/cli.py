"""CLI commands for html2png."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from enum import StrEnum
from pathlib import Path

import typer
from rich.console import Console
from rich.status import Status

from .config import (
    AppConfig,
    BrowserEngine,
    ImageFormat,
    PageLoadStrategy,
    load_config_file,
    merge_cli_config,
)
from .constants import (
    DEFAULT_DEVICE_SCALE_FACTOR,
    DEFAULT_QUALITY,
    DEFAULT_TIMEOUT_MS,
    DEFAULT_VIEWPORT_HEIGHT,
    DEFAULT_VIEWPORT_WIDTH,
)
from .core import convert_html_to_image
from .utils import generate_output_path

console = Console()


# Create CLI app
app = typer.Typer(
    name="html2png",
    help="Universal HTML to Image Converter",
    add_completion=True,
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        "-v",
        help="Show version and exit",
        is_eager=True,
        show_default=False,
    ),
) -> None:
    """html2png - Universal HTML to Image Converter."""
    if version:
        # Version is handled in __init__.py before Typer processing
        raise typer.Exit()


class SizePreset(StrEnum):
    """Common viewport size presets."""

    MOBILE = "mobile"  # 375x667
    TABLET = "tablet"  # 768x1024
    LAPTOP = "laptop"  # 1366x768
    DESKTOP = "desktop"  # 1920x1080
    FULL_HD = "1080p"  # 1920x1080
    TWO_K = "2k"  # 2560x1440
    FOUR_K = "4k"  # 3840x2160


# Preset dimensions
PRESET_DIMENSIONS = {
    SizePreset.MOBILE: (375, 667),
    SizePreset.TABLET: (768, 1024),
    SizePreset.LAPTOP: (1366, 768),
    SizePreset.DESKTOP: (1920, 1080),
    SizePreset.FULL_HD: (1920, 1080),
    SizePreset.TWO_K: (2560, 1440),
    SizePreset.FOUR_K: (3840, 2160),
}


def parse_size(size: str | None) -> tuple[int, int] | None:
    """Parse size string to (width, height) tuple.

    Supports formats:
    - "WxH" (e.g., "1920x1080")
    - Preset names (mobile, tablet, desktop, etc.)

    Args:
        size: Size string or None

    Returns:
        Tuple of (width, height) or None if invalid
    """
    if not size:
        return None

    # Check if it's a preset
    try:
        preset = SizePreset(size.lower())
        return PRESET_DIMENSIONS[preset]
    except ValueError:
        pass

    # Parse "WxH" format
    if "x" in size.lower():
        try:
            w, h = size.lower().split("x")
            return int(w), int(h)
        except (ValueError, AttributeError):
            return None

    return None


@app.command()
def convert(
    input: str = typer.Argument(
        ...,
        help="Input source: file path, URL, or '-' for stdin",
    ),
    output: Path = typer.Option(
        None,
        "-o",
        "--output",
        help="Output image path (default: auto-generated with same name as input)",
    ),
    # Size options
    size: str = typer.Option(
        None,
        "--size",
        "-s",
        help='Viewport size (e.g., "1920x1080", "mobile", "desktop", "4k")',
    ),
    width: int = typer.Option(
        None,
        "--width",
        "-W",
        help="Viewport width (overrides --size)",
    ),
    height: int = typer.Option(
        None,
        "--height",
        "-H",
        help="Viewport height (overrides --size)",
    ),
    # Scale/quality options
    dpr: float = typer.Option(
        None,
        "--dpr",
        "-d",
        help="Device pixel ratio (default: 3.0)",
    ),
    quality: int = typer.Option(
        None,
        "--quality",
        help="Image quality for JPEG format (0-100, default: 80)",
        min=0,
        max=100,
    ),
    zoom: float = typer.Option(
        1.0,
        "--zoom",
        "-z",
        help="Page zoom level (e.g., 1.5 = 150%, 2.0 = 200%)",
        min=0.1,
        max=10.0,
    ),
    # Format and browser
    format: ImageFormat | None = typer.Option(
        None,
        "-f",
        "--format",
        help="Output format (default: inferred from output extension, or PNG)",
    ),
    browser: BrowserEngine = typer.Option(
        BrowserEngine.CHROMIUM,
        "-b",
        "--browser",
        help="Browser engine to use",
    ),
    # Capture options
    full_page: bool = typer.Option(
        True,
        "--full-page/--viewport-only",
        help="Capture full page or only visible viewport (default: full page)",
    ),
    wait_for: str = typer.Option(
        None,
        "--wait-for",
        "-w",
        help="CSS selector to wait for before screenshot",
    ),
    timeout: int = typer.Option(
        None,
        "--timeout",
        "-t",
        help="Navigation timeout in milliseconds (default: 60000)",
    ),
    wait_strategy: PageLoadStrategy = typer.Option(
        None,
        "--wait-strategy",
        "-ws",
        help="Page load strategy: commit, domcontentloaded, load, networkidle (default: domcontentloaded)",
    ),
    # Configuration and output
    config_file: Path = typer.Option(
        None,
        "-c",
        "--config",
        help="Path to configuration file (TOML)",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        help="Enable verbose output",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress progress output (only show errors)",
    ),
):
    """Convert HTML to an image file.

    Examples:
        html2png convert page.html -o output.png
        html2png convert https://example.com -o screenshot.png
        cat page.html | html2png convert - -o output.png
        html2png convert page.html --size mobile
        html2png convert page.html --dpr 3
        html2png convert page.html -s 1920x1080 -q 90
        html2png convert slow-page.html --timeout 60000
        html2png convert page.html --wait-strategy load
    """
    # Load configuration
    config = load_config_file(config_file)

    # Determine dimensions from --size, --width, --height
    final_dpr = DEFAULT_DEVICE_SCALE_FACTOR
    final_width = None
    final_height = None

    # Parse --size option
    if size:
        parsed = parse_size(size)
        if parsed:
            final_width, final_height = parsed
        else:
            console.print(f"[yellow]Warning: Invalid size format: {size}[/yellow]")

    # Override with explicit --width and --height
    if width is not None:
        final_width = width
    if height is not None:
        final_height = height

    # Determine DPR from --dpr or default
    if dpr is not None:
        final_dpr = dpr

    # Merge CLI overrides
    config = merge_cli_config(
        config,
        format=format,
        width=final_width,
        height=final_height,
        dpr=final_dpr,
        quality=quality,
        browser=browser,
        full_page=full_page,
        wait_for=wait_for,
        timeout=timeout,
        wait_strategy=wait_strategy,
        zoom=zoom,
    )

    # Determine output path
    if output is None:
        output = generate_output_path(input, Path.cwd(), config.output_format)
    else:
        # Infer format from output extension if not explicitly set via --format
        if format is None:
            from contextlib import suppress

            output_ext = output.suffix.lstrip(".").lower()
            with suppress(ValueError):
                config.output_format = ImageFormat(output_ext)
        else:
            config.output_format = format

    # Ensure output directory exists
    output.parent.mkdir(parents=True, exist_ok=True)

    # Verbose output
    if verbose:
        console.print("[dim]Configuration:[/dim]")
        console.print(f"  Browser: {config.browser.engine.value}")
        console.print(f"  Viewport: {config.render.viewport.width}x{config.render.viewport.height}")
        console.print(f"  DPR: {config.render.device_scale_factor}")
        console.print(f"  Format: {config.output_format.value}")
        console.print(f"  Full page: {config.render.full_page}")
        console.print()

    # Progress output (skip if quiet)
    if not quiet:
        status = Status(
            f"[cyan]Converting:[/cyan] {input} → [cyan]{output.name}[/cyan]",
            console=console,
            spinner="dots",
        )
        status.start()
        try:
            success = convert_html_to_image(input, output, config)
        finally:
            status.stop()
            console.print()  # Empty line to separate output
    else:
        success = convert_html_to_image(input, output, config)

    if success:
        if not quiet:
            size_bytes = output.stat().st_size
            console.print(f"[green]✓[/green] Success: {output.name} ({size_bytes:,} bytes)")
        raise typer.Exit(0)
    else:
        console.print("[red]✗[/red] Conversion failed")
        raise typer.Exit(1)


def _run_batch_conversion_with_progress(
    files: list[Path],
    output_dir: Path,
    config: AppConfig,
    parallel: int,
    verbose: bool,
) -> None:
    """Run batch conversion with spinner progress output."""
    results = []

    if parallel > 1:
        # Parallel processing with progress
        with ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = {}
            for f in files:
                output = generate_output_path(str(f), output_dir, config.output_format)
                future = executor.submit(convert_html_to_image, str(f), output, config)
                futures[future] = (f, output)

            completed = 0
            for future in as_completed(futures):
                input_file, output = futures[future]
                status = Status(
                    f"[cyan]Converting:[/cyan] {input_file.name} ({completed + 1}/{len(files)})",
                    console=console,
                    spinner="dots",
                )
                status.start()
                try:
                    success = future.result()
                    results.append(success)
                    completed += 1
                    status.stop()
                    if success:
                        size_bytes = output.stat().st_size if output.exists() else 0
                        console.print(
                            f"[green]✓[/green] Success: {output.name} ({size_bytes:,} bytes) [{completed}/{len(files)}]"
                        )
                    else:
                        console.print(
                            f"[red]✗[/red] Failed: {input_file.name} [{completed}/{len(files)}]"
                        )
                    if verbose and not success:
                        console.print(f"[yellow]Warning: Failed to convert {input_file}[/yellow]")
                except Exception as e:
                    results.append(False)
                    completed += 1
                    status.stop()
                    console.print(f"[red]✗[/red] Error: {input_file.name}: {e}")
    else:
        # Sequential processing with progress
        for i, input_file in enumerate(files, 1):
            output = generate_output_path(str(input_file), output_dir, config.output_format)
            status = Status(
                f"[cyan]Converting:[/cyan] {input_file.name} ({i}/{len(files)})",
                console=console,
                spinner="dots",
            )
            status.start()
            try:
                success = convert_html_to_image(str(input_file), output, config)
                results.append(success)
                status.stop()
                if success:
                    size_bytes = output.stat().st_size if output.exists() else 0
                    console.print(
                        f"[green]✓[/green] Success: {output.name} ({size_bytes:,} bytes) [{i}/{len(files)}]"
                    )
                else:
                    console.print(f"[red]✗[/red] Failed: {input_file.name} [{i}/{len(files)}]")
            except Exception as e:
                results.append(False)
                status.stop()
                console.print(f"[red]✗[/red] Error: {input_file.name}: {e}")

    # Report summary
    success_count = sum(results)
    if not results or all(results):
        return  # All succeeded

    if success_count < len(results):
        failed_count = len(results) - success_count
        console.print(f"\n[yellow]Warning: {failed_count}/{len(results)} file(s) failed[/yellow]")


@app.command()
def batch(
    pattern: str = typer.Option(
        "*.html",
        "-p",
        "--pattern",
        help="Glob pattern for HTML files",
    ),
    output_dir: Path = typer.Option(
        Path("."),
        "-o",
        "--output-dir",
        help="Output directory",
    ),
    format: ImageFormat | None = typer.Option(
        None,
        "-f",
        "--format",
        help="Output format",
    ),
    parallel: int = typer.Option(
        1,
        "-j",
        "--parallel",
        help="Number of parallel workers",
        min=1,
        max=16,
    ),
    size: str = typer.Option(
        None,
        "--size",
        "-s",
        help='Viewport size (e.g., "1920x1080", "mobile", "desktop")',
    ),
    dpr: float = typer.Option(
        None,
        "--dpr",
        "-d",
        help="Device pixel ratio (default: 3.0)",
    ),
    zoom: float = typer.Option(
        1.0,
        "--zoom",
        "-z",
        help="Page zoom level (e.g., 1.5 = 150%, 2.0 = 200%)",
        min=0.1,
        max=10.0,
    ),
    config_file: Path = typer.Option(
        None,
        "-c",
        "--config",
        help="Path to configuration file (TOML)",
    ),
    dry_run: bool = typer.Option(
        False,
        "-n",
        "--dry-run",
        help="Show what would be converted without doing it",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        help="Enable verbose output",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress progress output (only show errors)",
    ),
):
    """Batch convert multiple HTML files.

    Examples:
        html2png batch --pattern "*.html"
        html2png batch -p "cards/*.html" -o output/ -j 4
        html2png batch -p "*.html" --size mobile
        html2png batch -p "*.html" --dpr 3 -j 4
    """
    config = load_config_file(config_file)

    # Determine dimensions and DPR for merge
    final_width = None
    final_height = None
    final_dpr = DEFAULT_DEVICE_SCALE_FACTOR

    # Apply size preset
    if size:
        parsed = parse_size(size)
        if parsed:
            final_width, final_height = parsed

    # Apply dpr
    if dpr is not None:
        final_dpr = dpr

    # Merge CLI overrides (avoids mutating original config)
    config = merge_cli_config(
        config,
        format=format,
        width=final_width,
        height=final_height,
        dpr=final_dpr,
        zoom=zoom,
    )

    # Find matching files (single-pass filtering)
    files = [f for f in Path.cwd().glob(pattern) if f.is_file()]

    if not files:
        console.print(f"[yellow]No files found matching pattern: {pattern}[/yellow]")
        raise typer.Exit(1)

    if not quiet:
        console.print(f"Found {len(files)} file(s) to convert")

    if dry_run:
        for f in files:
            output = generate_output_path(str(f), output_dir, config.output_format)
            console.print(f"  {f.name} → [cyan]{output.name}[/cyan]")
        console.print(f"\n[dim]Dry run mode - {len(files)} file(s) would be converted[/dim]")
        raise typer.Exit(0)

    output_dir.mkdir(parents=True, exist_ok=True)

    if not quiet:
        _run_batch_conversion_with_progress(files, output_dir, config, parallel, verbose)
    else:
        _run_batch_conversion(files, output_dir, config, parallel, verbose)

    if not quiet:
        console.print("\n[green]✓[/green] Batch conversion complete")


def _run_batch_conversion(
    files: list[Path],
    output_dir: Path,
    config: AppConfig,
    parallel: int,
    verbose: bool,
) -> None:
    """Run batch conversion without progress output (for quiet mode)."""
    results = []

    if parallel > 1:
        # Parallel processing
        with ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = {}
            for f in files:
                output = generate_output_path(str(f), output_dir, config.output_format)
                future = executor.submit(convert_html_to_image, str(f), output, config)
                futures[future] = (f, output)

            for future in as_completed(futures):
                input_file, output = futures[future]
                try:
                    success = future.result()
                    results.append(success)
                    if verbose and not success:
                        console.print(f"[yellow]Warning: Failed to convert {input_file}[/yellow]")
                except Exception as e:
                    results.append(False)
                    console.print(f"[red]Error converting {input_file}: {e}[/red]")
    else:
        # Sequential processing
        for input_file in files:
            output = generate_output_path(str(input_file), output_dir, config.output_format)
            success = convert_html_to_image(str(input_file), output, config)
            results.append(success)

    # Report summary
    success_count = sum(results)
    if not results or all(results):
        return  # All succeeded

    if success_count < len(results):
        failed_count = len(results) - success_count
        console.print(f"\n[yellow]Warning: {failed_count}/{len(results)} file(s) failed[/yellow]")


@app.command()
def init_config(
    output: Path = typer.Option(
        Path(".html2png.toml"),
        "-o",
        "--output",
        help="Output configuration file path",
    ),
):
    """Create a default configuration file.

    Examples:
        html2png init-config
        html2png init-config -o ~/config/html2png.toml
    """
    default_config = f"""# html2png Configuration File

[browser]
# Browser engine: "chromium", "firefox", or "webkit"
engine = "chromium"
# Run in headless mode (set to false to see the browser window)
headless = true
# Slow down operations by N milliseconds (useful for debugging)
slow_mo = 0

[render]
# Viewport configuration
[render.viewport]
width = {DEFAULT_VIEWPORT_WIDTH}
height = {DEFAULT_VIEWPORT_HEIGHT}

# Device pixel ratio for high-resolution output
device_scale_factor = {DEFAULT_DEVICE_SCALE_FACTOR}

# Capture the full page or just the viewport
full_page = true

# Disable animations for consistent screenshots
disable_animations = true

# Wait for a specific CSS selector before taking screenshot
# wait_for_selector = ".content-loaded"

# Page load strategy: "commit", "domcontentloaded", "load", or "networkidle"
# - commit: start loading immediately (fastest, for local files)
# - domcontentloaded: wait for DOM to be parsed (default, most reliable)
# - load: wait for all resources (images, stylesheets, etc.)
# - networkidle: wait until no network requests for 500ms (may timeout on slow pages)
wait_strategy = "domcontentloaded"

# Navigation timeout in milliseconds
wait_for_timeout = {DEFAULT_TIMEOUT_MS}

# Image quality for JPEG (0-100)
quality = {DEFAULT_QUALITY}

# Output format: "png" or "jpeg"
output_format = "png"

# Number of parallel workers for batch operations
parallel_workers = 1
"""

    output.write_text(default_config)
    console.print(f"[green]✓[/green] Configuration file created: {output}")
    console.print("\n[dim]Edit this file to customize html2png behavior.[/dim]")


@app.command()
def presets():
    """Show available size presets and their dimensions."""
    console.print("[bold]Available Size Presets:[/bold]")
    console.print()

    for preset in SizePreset:
        width, height = PRESET_DIMENSIONS[preset]
        description = _get_preset_description(preset)
        console.print(f"  [cyan]{preset.value:<10}[/cyan] {width:>5}x{height:<5}  ({description})")


def _get_preset_description(preset: SizePreset) -> str:
    """Get description for a preset."""
    descriptions = {
        SizePreset.MOBILE: "Mobile devices",
        SizePreset.TABLET: "Tablet devices",
        SizePreset.LAPTOP: "Laptop screens",
        SizePreset.DESKTOP: "Desktop monitors",
        SizePreset.FULL_HD: "Full HD (1920x1080)",
        SizePreset.TWO_K: "2K monitors (2560x1440)",
        SizePreset.FOUR_K: "4K monitors (3840x2160)",
    }
    return descriptions.get(preset, "")
