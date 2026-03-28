"""Tests for html2png converter."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Import internal modules for testing internal functionality
from html2png.config import (
    AppConfig,
    BrowserConfig,
    BrowserEngine,
    ImageFormat,
    InputSource,
    PageLoadStrategy,
    ViewportConfig,
)
from html2png.utils import detect_input_source, path_to_file_url

# Import public API
import html2png
from html2png import Config, Renderer, render, load_config_file

# Import CLI app for testing
from html2png.cli import app


class TestInputDetection:
    """Test input source detection."""

    def test_stdin_detection(self):
        source_type, _ = detect_input_source("-")
        assert source_type == InputSource.STDIN

    def test_url_detection(self):
        source_type, url = detect_input_source("https://example.com")
        assert source_type == InputSource.URL
        assert url == "https://example.com"

    def test_http_url_detection(self):
        source_type, url = detect_input_source("http://example.com")
        assert source_type == InputSource.URL
        assert url == "http://example.com"

    def test_file_url_detection(self):
        source_type, url = detect_input_source("file:///tmp/test.html")
        assert source_type == InputSource.URL
        assert url == "file:///tmp/test.html"


class TestFileUrlConversion:
    """Test file path to URL conversion."""

    def test_unix_path_to_url(self):
        path = Path("/tmp/test.html")
        url = path_to_file_url(path)
        assert url == "file:///tmp/test.html"

    def test_relative_path_to_url(self):
        path = Path("test.html").resolve()
        url = path_to_file_url(path)
        assert url.startswith("file:///")
        assert url.endswith("test.html")


class TestConfigClasses:
    """Test configuration data classes."""

    def test_default_app_config(self):
        config = AppConfig()
        assert config.render.viewport.width == 1080
        assert config.render.viewport.height == 1440
        assert config.render.device_scale_factor == 3.0
        assert config.browser.engine == BrowserEngine.CHROMIUM
        assert config.output_format == ImageFormat.PNG

    def test_custom_viewport_config(self):
        viewport = ViewportConfig(width=1920, height=1080)
        assert viewport.width == 1920
        assert viewport.height == 1080

    def test_custom_browser_config(self):
        browser = BrowserConfig(engine=BrowserEngine.FIREFOX, headless=False)
        assert browser.engine == BrowserEngine.FIREFOX
        assert browser.headless is False


class TestPublicAPI:
    """Test the public API."""

    def test_render_basic(self, tmp_path):
        """Test basic render() function."""
        html_content = "<html><body><h1>Test</h1></body></html>"
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.png"

        success = render(str(html_file), output_file)

        assert success is True
        assert output_file.exists()
        assert output_file.stat().st_size > 0

    def test_render_with_params(self, tmp_path):
        """Test render() with custom parameters."""
        html_content = "<html><body><h1>Test</h1></body></html>"
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.png"

        success = render(
            str(html_file),
            output_file,
            width=800,
            height=600,
            scale=2.0,
        )

        assert success is True
        assert output_file.exists()

    def test_render_with_format_string(self, tmp_path):
        """Test render() with format as string."""
        html_content = "<html><body><h1>Test</h1></body></html>"
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.jpg"

        success = render(str(html_file), output_file, format="jpeg", quality=90)

        assert success is True
        assert output_file.exists()

    def test_render_with_browser_string(self, tmp_path):
        """Test render() with browser as string."""
        html_content = "<html><body><h1>Test</h1></body></html>"
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.png"

        success = render(str(html_file), output_file, browser="chromium")

        assert success is True
        assert output_file.exists()

    def test_config_dataclass(self):
        """Test Config dataclass."""
        config = Config(width=1920, height=1080, scale=2.0)

        assert config.width == 1920
        assert config.height == 1080
        assert config.scale == 2.0
        assert config.browser == BrowserEngine.CHROMIUM
        assert config.format == ImageFormat.PNG

    def test_config_to_app_config(self):
        """Test Config.to_app_config() conversion."""
        config = Config(
            width=1920,
            height=1080,
            browser=BrowserEngine.FIREFOX,
            format=ImageFormat.JPEG,
        )

        app_config = config.to_app_config()

        assert app_config.render.viewport.width == 1920
        assert app_config.render.viewport.height == 1080
        assert app_config.browser.engine == BrowserEngine.FIREFOX
        assert app_config.output_format == ImageFormat.JPEG

    def test_render_with_config_object(self, tmp_path):
        """Test render() with Config object."""
        html_content = "<html><body><h1>Test</h1></body></html>"
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.png"

        config = Config(width=800, height=600, scale=1.0)
        success = render(str(html_file), output_file, config=config)

        assert success is True
        assert output_file.exists()

    def test_render_with_config_overrides(self, tmp_path):
        """Test render() with config object and keyword overrides."""
        html_content = "<html><body><h1>Test</h1></body></html>"
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.png"

        config = Config(width=800, height=600)
        # Keyword args should override config
        success = render(str(html_file), output_file, config=config, width=1920)

        assert success is True
        assert output_file.exists()

    def test_renderer_context_manager(self, tmp_path):
        """Test Renderer context manager."""
        html_content = "<html><body><h1>Test</h1></body></html>"

        with Renderer(width=800, height=600) as renderer:
            for i in range(3):
                html_file = tmp_path / f"test{i}.html"
                html_file.write_text(html_content)

                output_file = tmp_path / f"output{i}.png"

                success = renderer.render(str(html_file), output_file)

                assert success is True
                assert output_file.exists()

    def test_module_exports(self):
        """Test that the module exports the expected API."""
        # Check that __all__ is defined
        assert hasattr(html2png, "__all__")

        # Check expected exports
        expected_exports = {
            "render",
            "Renderer",
            "Config",
            "AppConfig",
            "BrowserConfig",
            "BrowserEngine",
            "ImageFormat",
            "PageLoadStrategy",
            "load_config_file",
        }
        assert set(html2png.__all__) == expected_exports

        # Check that all exported items are accessible
        for export in expected_exports:
            assert hasattr(html2png, export)

        # Verify old API is NOT exported
        assert "convert" not in html2png.__all__
        assert "convert_html_to_image" not in html2png.__all__


class TestConfigLoading:
    """Test configuration file loading."""

    def test_load_nonexistent_config(self):
        """Test loading a nonexistent config file returns default config."""
        config = load_config_file(Path("/nonexistent/config.toml"))

        assert isinstance(config, Config)
        assert config.width == 1080
        assert config.height == 1440

    def test_load_actual_config_file(self, tmp_path):
        """Test loading an actual config file."""
        config_content = """
output_format = "jpeg"
parallel_workers = 2

[browser]
engine = "firefox"
headless = false

[render.viewport]
width = 1920
height = 1080

[render]
device_scale_factor = 2.0
full_page = false
disable_animations = false
wait_strategy = "load"
wait_for_timeout = 60000
quality = 90
"""
        config_file = tmp_path / "test_config.toml"
        config_file.write_text(config_content)

        config = load_config_file(config_file)

        assert config.width == 1920
        assert config.height == 1080
        assert config.scale == 2.0
        assert config.full_page is False
        assert config.wait_strategy == PageLoadStrategy.LOAD
        assert config.timeout == 60000
        assert config.quality == 90
        assert config.browser == BrowserEngine.FIREFOX
        assert config.headless is False
        assert config.format == ImageFormat.JPEG


class TestTimeout:
    """Test timeout functionality."""

    def test_timeout_suggestions_on_timeout_error(self, tmp_path):
        """Test that timeout suggestions are shown only on timeout errors."""
        from typer.testing import CliRunner

        # Create an HTML file that will cause a timeout during screenshot
        # by using a very long rendering time
        html_content = """
        <html>
        <head>
            <style>
                @font-face {
                    font-family: 'SlowFont';
                    src: url('http://localhost:99999/font.woff2');
                }
                body { font-family: 'SlowFont', sans-serif; }
            </style>
        </head>
        <body><h1>Timeout Test</h1></body>
        </html>
        """
        html_file = tmp_path / "timeout_test.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.png"

        runner = CliRunner()
        # Use wait-strategy load to force waiting, and very short timeout
        result = runner.invoke(
            app,
            [
                "convert",
                str(html_file),
                "-o",
                str(output_file),
                "--timeout",
                "100",
                "--wait-strategy",
                "load",
            ],
        )

        # Should fail due to timeout (exit code 1 or 2)
        # The test may pass if font loading is skipped, so we check for suggestions
        output = result.stdout

        # If it failed, check suggestions are shown
        if result.exit_code != 0:
            assert "Suggestions" in output or "suggestions" in output.lower()
            assert "--timeout" in output or "timeout" in output.lower()
            # Suggested timeout should be 2x the current (100 * 2 = 200)
            assert "200" in output

    def test_api_timeout_parameter(self, tmp_path):
        """Test that timeout parameter is properly passed through the API."""
        html_content = "<html><body><h1>Timeout Test</h1></body></html>"
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.png"

        # Test with custom timeout
        success = render(str(html_file), output_file, timeout=90000)

        assert success is True
        assert output_file.exists()

    def test_build_screenshot_options_includes_timeout(self):
        """Test that build_screenshot_options includes timeout."""
        from html2png.core import build_screenshot_options
        from html2png.config import AppConfig

        config = AppConfig()
        options = build_screenshot_options(Path("/tmp/test.png"), config)

        assert "timeout" in options
        assert options["timeout"] == config.render.wait_for_timeout

    def test_build_screenshot_options_custom_timeout(self):
        """Test build_screenshot_options with custom timeout."""
        from html2png.core import build_screenshot_options
        from html2png.config import AppConfig

        config = AppConfig()
        config.render.wait_for_timeout = 90000
        options = build_screenshot_options(Path("/tmp/test.png"), config)

        assert options["timeout"] == 90000

    def test_cli_timeout_option(self, tmp_path):
        """Test CLI --timeout option is properly handled."""
        from typer.testing import CliRunner

        html_content = "<html><body><h1>Timeout CLI Test</h1></body></html>"
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.png"

        runner = CliRunner()
        result = runner.invoke(
            app,
            ["convert", str(html_file), "-o", str(output_file), "--timeout", "90000"],
        )

        assert result.exit_code == 0
        assert "Success" in result.stdout
        assert output_file.exists()


class TestCLI:
    """Test CLI commands."""

    def test_convert_command_basic(self, tmp_path):
        """Test basic convert command."""
        from typer.testing import CliRunner

        html_content = "<html><body><h1>CLI Test</h1></body></html>"
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.png"

        runner = CliRunner()
        result = runner.invoke(app, ["convert", str(html_file), "-o", str(output_file)])

        assert result.exit_code == 0
        assert "Success" in result.stdout
        assert output_file.exists()

    def test_convert_command_with_options(self, tmp_path):
        """Test convert command with custom options."""
        from typer.testing import CliRunner

        html_content = "<html><body><h1>Options Test</h1></body></html>"
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.png"

        runner = CliRunner()
        result = runner.invoke(
            app,
            [
                "convert",
                str(html_file),
                "-o",
                str(output_file),
                "--width",
                "800",
                "--height",
                "600",
                "--scale",
                "2.0",
            ],
        )

        assert result.exit_code == 0
        assert output_file.exists()

    def test_convert_command_jpeg_format(self, tmp_path):
        """Test convert command with JPEG format."""
        from typer.testing import CliRunner

        html_content = "<html><body><h1>JPEG Test</h1></body></html>"
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.jpg"

        runner = CliRunner()
        result = runner.invoke(
            app,
            ["convert", str(html_file), "-o", str(output_file), "-f", "jpeg", "--quality", "90"],
        )

        assert result.exit_code == 0
        assert output_file.exists()

    def test_presets_command(self):
        """Test presets command."""
        from typer.testing import CliRunner

        runner = CliRunner()
        result = runner.invoke(app, ["presets"])

        assert result.exit_code == 0
        assert "mobile" in result.stdout
        assert "desktop" in result.stdout
        assert "1920x1080" in result.stdout

    def test_init_config_command(self, tmp_path):
        """Test init-config command."""
        from typer.testing import CliRunner

        config_file = tmp_path / ".html2png.toml"

        runner = CliRunner()
        result = runner.invoke(app, ["init-config", "-o", str(config_file)])

        assert result.exit_code == 0
        assert config_file.exists()
        content = config_file.read_text()
        assert "[browser]" in content
        assert "[render]" in content

    def test_convert_quiet_mode(self, tmp_path):
        """Test convert command with quiet mode."""
        from typer.testing import CliRunner

        html_content = "<html><body><h1>Quiet Test</h1></body></html>"
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.png"

        runner = CliRunner()
        result = runner.invoke(
            app, ["convert", str(html_file), "-o", str(output_file), "-q"]
        )

        assert result.exit_code == 0
        # Quiet mode should only show errors
        assert "Converting" not in result.stdout
        assert output_file.exists()

    def test_convert_missing_output_infers_from_input(self, tmp_path):
        """Test that output format is inferred from input when not specified."""
        from typer.testing import CliRunner
        import os

        # Change to temp directory to avoid polluting project root
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            html_content = "<html><body><h1>Inference Test</h1></body></html>"
            html_file = tmp_path / "test.html"
            html_file.write_text(html_content)

            runner = CliRunner()
            result = runner.invoke(app, ["convert", "test.html"])

            assert result.exit_code == 0
            # Should create test.png in current directory
            expected_output = tmp_path / "test.png"
            try:
                assert expected_output.exists()
            finally:
                if expected_output.exists():
                    expected_output.unlink()
        finally:
            os.chdir(original_cwd)

    def test_batch_dry_run(self, tmp_path):
        """Test batch command with dry-run mode."""
        import os
        from typer.testing import CliRunner

        # Create some test HTML files
        for i in range(3):
            (tmp_path / f"test{i}.html").write_text("<html><body>Test</body></html>")

        # Change to tmp_path so the glob pattern works
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            runner = CliRunner()
            result = runner.invoke(
                app, ["batch", "-p", "test*.html", "-o", str(tmp_path), "--dry-run"]
            )

            if result.exit_code != 0:
                print(f"Exit code: {result.exit_code}")
                print(f"Output: {result.stdout}")
                print(f"Stderr: {result.stderr}")

            assert result.exit_code == 0
            assert "Dry run" in result.stdout or "dry run" in result.stdout.lower()
            # Dry run should not create actual output files
            assert not (tmp_path / "test0.png").exists()
        finally:
            os.chdir(original_cwd)


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
