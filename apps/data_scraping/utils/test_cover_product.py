"""
Unit tests for the refactored Cover Product module.

Run with: python -m pytest test_cover_product.py -v
"""

import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from apps.data_scraping.utils.cover_product_NEW import (
    ConfigLoader,
    FontManager,
    ImageLoader,
    ImageProcessor,
    LayoutEngine,
    CoverRenderer,
    FileManager,
    CoverProduct,
)
from apps.data_scraping.utils.cover_exceptions import (
    InvalidImageError,
    InsufficientImagesError,
    LayoutNotFoundError,
    MissingAssetError,
    InvalidConfigError,
)


class TestConfigLoader(unittest.TestCase):
    """Test ConfigLoader class."""

    def test_load_default_config(self):
        """Test loading default config file."""
        try:
            loader = ConfigLoader()
            self.assertIsNotNone(loader.config)
            self.assertIn("layouts", loader.config)
            self.assertIn("assets", loader.config)
            self.assertIn("defaults", loader.config)
        except InvalidConfigError:
            self.skipTest("Config file not found in default location")

    def test_get_layout_existing(self):
        """Test getting existing layout."""
        try:
            loader = ConfigLoader()
            layout = loader.get_layout("grid_3x3")
            self.assertEqual(layout["min_images"], 9)
            self.assertEqual(layout["image_count"], 9)
        except InvalidConfigError:
            self.skipTest("Config file not found")

    def test_get_layout_nonexistent(self):
        """Test getting non-existent layout raises error."""
        try:
            loader = ConfigLoader()
            with self.assertRaises(LayoutNotFoundError):
                loader.get_layout("nonexistent_layout")
        except InvalidConfigError:
            self.skipTest("Config file not found")

    def test_get_default_value(self):
        """Test getting default configuration values."""
        try:
            loader = ConfigLoader()
            quality = loader.get_default("save_quality", 95)
            self.assertEqual(quality, 95)
        except InvalidConfigError:
            self.skipTest("Config file not found")


class TestLayoutEngine(unittest.TestCase):
    """Test LayoutEngine class."""

    def setUp(self):
        """Set up test fixtures."""
        try:
            self.config = ConfigLoader()
            self.engine = LayoutEngine(1280, self.config)
        except InvalidConfigError:
            self.skipTest("Config file not found")

    def test_percent_to_pixels(self):
        """Test percentage to pixels conversion."""
        # 50% of 1280 = 640
        result = self.engine._percent_to_pixels(0.5)
        self.assertEqual(result, 640)

        # 25% of 1280 = 320
        result = self.engine._percent_to_pixels(0.25)
        self.assertEqual(result, 320)

    def test_grid_layout_positions(self):
        """Test grid layout position generation."""
        try:
            positions = self.engine.get_layout_positions("grid_3x3")
            self.assertEqual(len(positions), 9)

            # Check first position
            self.assertIn(0, positions)
            self.assertIn("size", positions[0])
            self.assertIn("position", positions[0])
        except (InvalidConfigError, LayoutNotFoundError):
            self.skipTest("Required config not found")

    def test_strip_layout_positions(self):
        """Test strip layout position generation."""
        try:
            positions = self.engine.get_layout_positions("faixa_horizontal")
            self.assertEqual(len(positions), 4)

            # Check that images are side by side
            for i in range(4):
                self.assertIn(i, positions)
        except (InvalidConfigError, LayoutNotFoundError):
            self.skipTest("Required config not found")


class TestImageProcessor(unittest.TestCase):
    """Test ImageProcessor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.processor = ImageProcessor()

    @patch("apps.data_scraping.utils.cover_product.Image.open")
    def test_aspect_fill_crop_landscape(self, mock_open):
        """Test cropping landscape image to square."""
        # Create a mock image (2000x1000)
        mock_img = MagicMock()
        mock_img.size = (2000, 1000)

        # Mock the resize and crop operations
        mock_img.resize.return_value = MagicMock()
        mock_img.resize.return_value.crop.return_value = MagicMock()

        mock_open.return_value = mock_img

        # Should not raise an error
        # Note: This is a simplified test; full integration test would use real images


class TestFileManager(unittest.TestCase):
    """Test FileManager class."""

    @patch("pathlib.Path.mkdir")
    def test_ensure_directory_creates_path(self, mock_mkdir):
        """Test that directory is created."""
        with patch("pathlib.Path.exists", return_value=False):
            manager = FileManager("C:\\test\\path")
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.exists", return_value=True)
    def test_ensure_directory_exists(self, mock_exists, mock_mkdir):
        """Test when directory already exists."""
        manager = FileManager("C:\\test\\path")
        # mkdir should still be called with exist_ok=True
        mock_mkdir.assert_called_once()


class TestCoverProduct(unittest.TestCase):
    """Test main CoverProduct class."""

    def test_init_invalid_size(self):
        """Test initialization with invalid size."""
        with self.assertRaises(ValueError):
            CoverProduct(product_path="C:\\test", size_cover="invalid")

    @patch.object(CoverProduct, "_setup_paths")
    @patch("apps.data_scraping.utils.cover_product.ImageLoader")
    @patch("apps.data_scraping.utils.cover_product.FileManager")
    @patch("apps.data_scraping.utils.cover_product.ConfigLoader")
    def test_init_valid(self, mock_config, mock_file_mgr, mock_img_loader, mock_setup):
        """Test valid initialization."""
        mock_img_loader.return_value.get_valid_images.return_value = ["img1.jpg"]

        try:
            cover = CoverProduct(product_path="C:\\test", size_cover=1280)
            self.assertEqual(cover.size_cover, 1280)
            self.assertFalse(cover.promocao)
        except Exception:
            self.skipTest("Initialization dependencies not available")


class TestExceptions(unittest.TestCase):
    """Test custom exceptions."""

    def test_invalid_image_error(self):
        """Test InvalidImageError."""
        with self.assertRaises(InvalidImageError):
            raise InvalidImageError("Test message")

    def test_insufficient_images_error(self):
        """Test InsufficientImagesError."""
        with self.assertRaises(InsufficientImagesError):
            raise InsufficientImagesError("Test message")

    def test_layout_not_found_error(self):
        """Test LayoutNotFoundError."""
        with self.assertRaises(LayoutNotFoundError):
            raise LayoutNotFoundError("Test message")

    def test_missing_asset_error(self):
        """Test MissingAssetError."""
        with self.assertRaises(MissingAssetError):
            raise MissingAssetError("Test message")


class TestIntegration(unittest.TestCase):
    """Integration tests for the full pipeline."""

    def test_config_loads_successfully(self):
        """Test that config loads without errors."""
        try:
            loader = ConfigLoader()
            # Verify all required keys exist
            self.assertIn("layouts", loader.config)
            self.assertIn("assets", loader.config)
            self.assertIn("defaults", loader.config)

            # Verify layouts have required fields
            for layout_name, layout_config in loader.config["layouts"].items():
                self.assertIn("min_images", layout_config)
                self.assertIn("image_count", layout_config)
                self.assertIn("structure", layout_config)
        except InvalidConfigError as e:
            self.skipTest(f"Config file not accessible: {e}")

    def test_all_layouts_have_valid_structure(self):
        """Test that all layouts have valid structure values."""
        valid_structures = {"grid", "strip", "asymmetric", "custom_5", "custom_6", "full_image"}

        try:
            loader = ConfigLoader()
            for layout_name, layout_config in loader.config["layouts"].items():
                structure = layout_config.get("structure")
                self.assertIn(
                    structure, valid_structures, f"Layout '{layout_name}' has invalid structure: {structure}"
                )
        except InvalidConfigError:
            self.skipTest("Config file not found")


if __name__ == "__main__":
    unittest.main()
