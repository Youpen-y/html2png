"""Additional tests for html2png API - covering previously untested parameters."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

from html2png import BrowserEngine, Config, ImageFormat, PageLoadStrategy, Renderer, render


class TestRenderParameters:
    """Test render() function with various parameters."""

    def test_render_full_page_true(self, tmp_path):
        """Test render() with full_page=True."""
        html_content = """
        <html>
        <head><style>body { height: 2000px; background: linear-gradient(to bottom, red, blue); }</style></head>
        <body><h1>Long Page</h1></body>
        </html>
        """
        html_file = tmp_path / "long_page.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.png"

        success = render(str(html_file), output_file, full_page=True)

        assert success is True
        assert output_file.exists()
        # Full page screenshot should be larger than viewport
        assert output_file.stat().st_size > 1000  # Basic size check

    def test_render_full_page_false(self, tmp_path):
        """Test render() with full_page=False (viewport only)."""
        html_content = """
        <html>
        <head><style>body { height: 2000px; background: red; }</style></head>
        <body><h1>Long Page</h1></body>
        </html>
        """
        html_file = tmp_path / "long_page.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.png"

        success = render(str(html_file), output_file, full_page=False, width=800, height=600)

        assert success is True
        assert output_file.exists()

    def test_render_with_wait_for_selector(self, tmp_path):
        """Test render() with wait_for selector."""
        html_content = """
        <html>
        <body>
        <h1>Test</h1>
        <script>
            setTimeout(() => {
                const el = document.createElement('div');
                el.id = 'loaded-content';
                el.textContent = 'Loaded!';
                document.body.appendChild(el);
            }, 100);
        </script>
        </body>
        </html>
        """
        html_file = tmp_path / "delayed.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.png"

        success = render(str(html_file), output_file, wait_for="#loaded-content", timeout=5000)

        assert success is True
        assert output_file.exists()

    def test_render_with_wait_strategy_string(self, tmp_path):
        """Test render() with wait_strategy as string."""
        html_content = "<html><body><h1>Test</h1></body></html>"
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.png"

        # Test with string value
        success = render(str(html_file), output_file, wait_strategy="load")

        assert success is True
        assert output_file.exists()

    def test_render_with_wait_strategy_enum(self, tmp_path):
        """Test render() with wait_strategy as PageLoadStrategy enum."""
        html_content = "<html><body><h1>Test</h1></body></html>"
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.png"

        success = render(str(html_file), output_file, wait_strategy=PageLoadStrategy.COMMIT)

        assert success is True
        assert output_file.exists()

    def test_render_error_on_invalid_input(self, tmp_path):
        """Test render() returns False on invalid input."""
        output_file = tmp_path / "output.png"

        # Non-existent file should fail gracefully
        success = render("/nonexistent/file.html", output_file)

        # Should return False, not raise exception
        assert success is False

    def test_render_with_all_parameters(self, tmp_path):
        """Test render() with all parameters specified."""
        html_content = "<html><body><h1>Full Test</h1></body></html>"
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.jpg"

        success = render(
            str(html_file),
            output_file,
            width=1920,
            height=1080,
            scale=2.0,
            browser="chromium",
            format="jpeg",
            quality=85,
            full_page=True,
            timeout=30000,
            headless=True,
            wait_for="h1",
            wait_strategy="domcontentloaded",
        )

        assert success is True
        assert output_file.exists()


class TestRendererParameters:
    """Test Renderer class with parameter overrides."""

    def test_renderer_format_override(self, tmp_path):
        """Test Renderer.render() with format override."""
        html_content = "<html><body><h1>Test</h1></body></html>"
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output_png = tmp_path / "output.png"
        output_jpg = tmp_path / "output.jpg"

        with Renderer(width=800, height=600, format="jpeg") as r:
            # First render uses default JPEG from Renderer
            success1 = r.render(str(html_file), output_jpg)
            # Second render overrides to PNG
            success2 = r.render(str(html_file), output_png, format="png")

        assert success1 is True
        assert success2 is True
        assert output_jpg.exists()
        assert output_png.exists()

    def test_renderer_quality_override(self, tmp_path):
        """Test Renderer.render() with quality override."""
        html_content = "<html><body><h1>Test</h1></body></html>"
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output1 = tmp_path / "output1.jpg"
        output2 = tmp_path / "output2.jpg"

        with Renderer(width=800, height=600, format="jpeg", quality=50) as r:
            # First render uses default quality=50
            success1 = r.render(str(html_file), output1)
            # Second render overrides quality to 95
            success2 = r.render(str(html_file), output2, quality=95)

        assert success1 is True
        assert success2 is True
        assert output1.exists()
        assert output2.exists()
        # Higher quality should result in larger file
        assert output2.stat().st_size > output1.stat().st_size

    def test_renderer_timeout_override(self, tmp_path):
        """Test Renderer.render() with timeout override."""
        html_content = """
        <html>
        <body>
        <h1>Test</h1>
        <script>
            setTimeout(() => {
                document.body.style.backgroundColor = 'green';
            }, 500);
        </script>
        </body>
        </html>
        """
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.png"

        with Renderer(width=800, height=600) as r:
            # Override timeout for this specific render
            success = r.render(str(html_file), output_file, timeout=2000)

        assert success is True
        assert output_file.exists()

    def test_renderer_wait_for_override(self, tmp_path):
        """Test Renderer.render() with wait_for override."""
        html_content = """
        <html>
        <body>
        <h1>Test</h1>
        <script>
            setTimeout(() => {
                const el = document.createElement('div');
                el.className = 'dynamic-content';
                el.textContent = 'Dynamic!';
                document.body.appendChild(el);
            }, 200);
        </script>
        </body>
        </html>
        """
        html_file = tmp_path / "test.html"
        html_file.write_text(html_content)

        output_file = tmp_path / "output.png"

        with Renderer(width=800, height=600) as r:
            # Override wait_for for this specific render
            success = r.render(
                str(html_file), output_file, wait_for=".dynamic-content", timeout=2000
            )

        assert success is True
        assert output_file.exists()


class TestConfigEdgeCases:
    """Test Config class edge cases."""

    def test_config_all_fields(self):
        """Test Config with all possible fields."""
        config = Config(
            width=1920,
            height=1080,
            scale=2.5,
            browser=BrowserEngine.WEBKIT,
            format=ImageFormat.JPEG,
            quality=95,
            full_page=False,
            timeout=45000,
            headless=False,
            wait_for=".content",
            wait_strategy=PageLoadStrategy.NETWORKIDLE,
        )

        assert config.width == 1920
        assert config.height == 1080
        assert config.scale == 2.5
        assert config.browser == BrowserEngine.WEBKIT
        assert config.format == ImageFormat.JPEG
        assert config.quality == 95
        assert config.full_page is False
        assert config.timeout == 45000
        assert config.headless is False
        assert config.wait_for == ".content"
        assert config.wait_strategy == PageLoadStrategy.NETWORKIDLE

    def test_config_with_string_browser(self):
        """Test Config accepts browser as string."""
        config = Config(browser="firefox")

        assert config.browser == BrowserEngine.FIREFOX

    def test_config_with_string_format(self):
        """Test Config accepts format as string."""
        config = Config(format="jpeg")

        assert config.format == ImageFormat.JPEG

    def test_config_with_string_wait_strategy(self):
        """Test Config accepts wait_strategy as string."""
        config = Config(wait_strategy="networkidle")

        assert config.wait_strategy == PageLoadStrategy.NETWORKIDLE


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
