"""
Cover Product Generator - Generates product cover images with various layouts.

This module provides functionality to create professional product covers
with configurable layouts, fonts, and logos.
"""

import json
import os
import random
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError

from apps.data_scraping.utils.write_cover_title import write_cover_title
from apps.data_scraping.utils.cover_exceptions import (
    InvalidImageError,
    InsufficientImagesError,
    LayoutNotFoundError,
    MissingAssetError,
    InvalidConfigError,
)


class ConfigLoader:
    """Loads and manages configuration for cover generation."""

    def __init__(self, config_path: Optional[str] = None) -> None:
        """
        Initialize the configuration loader.

        Args:
            config_path: Path to config JSON file. If None, uses default location.

        Raises:
            InvalidConfigError: If config file is not found or invalid.
        """
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "cover_config.json")

        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError as e:
            raise InvalidConfigError(f"Config file not found: {self.config_path}") from e
        except json.JSONDecodeError as e:
            raise InvalidConfigError(f"Invalid JSON in config file: {self.config_path}") from e

    def get_layout(self, layout_name: str) -> Dict[str, Any]:
        """
        Get layout configuration.

        Args:
            layout_name: Name of the layout.

        Returns:
            Dictionary with layout configuration.

        Raises:
            LayoutNotFoundError: If layout doesn't exist.
        """
        layouts = self.config.get("layouts", {})
        if layout_name not in layouts:
            raise LayoutNotFoundError(f"Layout '{layout_name}' not found. Available: {list(layouts.keys())}")
        return layouts[layout_name]

    def get_asset_path(self, asset_type: str, asset_name: str) -> Path:
        """
        Get asset path relative to config directory.

        Args:
            asset_type: Type of asset (e.g., 'logos', 'fonts').
            asset_name: Name of the specific asset.

        Returns:
            Full path to the asset.

        Raises:
            MissingAssetError: If asset doesn't exist.
        """
        assets = self.config.get("assets", {})
        asset_dict = assets.get(asset_type, {})

        if asset_name not in asset_dict:
            raise MissingAssetError(f"Asset '{asset_name}' of type '{asset_type}' not found.")

        relative_path = asset_dict[asset_name]
        full_path = self.config_path.parent / relative_path

        if not full_path.exists():
            raise MissingAssetError(f"Asset file not found: {full_path}")

        return full_path

    def get_default(self, key: str, default: Any = None) -> Any:
        """Get default configuration value."""
        defaults = self.config.get("defaults", {})
        return defaults.get(key, default)


class FontManager:
    """Manages font loading and caching."""

    def __init__(self, config_loader: ConfigLoader) -> None:
        """
        Initialize the font manager.

        Args:
            config_loader: ConfigLoader instance.
        """
        self.config_loader = config_loader
        self._font_cache: Dict[Tuple[str, int], ImageFont.FreeTypeFont] = {}

    def get_font(self, font_name: str, size: int) -> ImageFont.ImageFont:
        """
        Get or load a font.

        Args:
            font_name: Name of the font (e.g., 'default', 'title').
            size: Font size in pixels.

        Returns:
            PIL ImageFont object.

        Raises:
            MissingAssetError: If font cannot be loaded.
        """
        cache_key = (font_name, size)

        if cache_key in self._font_cache:
            return self._font_cache[cache_key]

        try:
            font_path = self.config_loader.get_asset_path("fonts", font_name)
            font = ImageFont.truetype(str(font_path), size)
            self._font_cache[cache_key] = font
            return font
        except MissingAssetError:
            # Try system font as fallback
            try:
                return ImageFont.truetype(font_name, size)
            except (IOError, OSError) as e:
                raise MissingAssetError(f"Could not load font: {font_name}") from e


class ImageLoader:
    """Loads and validates images."""

    def __init__(self, images_path: str) -> None:
        """
        Initialize the image loader.

        Args:
            images_path: Path to directory containing images.

        Raises:
            InvalidImageError: If path doesn't exist.
        """
        self.images_path = Path(images_path)

        if not self.images_path.exists():
            raise InvalidImageError(f"Images directory not found: {images_path}")

    def get_valid_images(self) -> List[str]:
        """
        Get list of valid image files.

        Returns:
            List of valid image filenames.
        """
        images = []

        for file in self.images_path.iterdir():
            if file.name == "desktop.ini":
                continue

            if not file.is_file():
                continue

            if self._is_valid_image(file):
                images.append(file.name)

        return images

    def _is_valid_image(self, file_path: Path) -> bool:
        """Check if a file is a valid image."""
        try:
            with Image.open(file_path) as img:
                img.verify()
            return True
        except (UnidentifiedImageError, FileNotFoundError, Exception):
            return False

    def load_image(self, filename: str) -> Image.Image:
        """
        Load an image file.

        Args:
            filename: Name of the image file.

        Returns:
            PIL Image object.

        Raises:
            InvalidImageError: If image cannot be loaded.
        """
        file_path = self.images_path / filename

        try:
            return Image.open(file_path).convert("RGB")
        except Exception as e:
            raise InvalidImageError(f"Could not load image: {filename}") from e


class ImageProcessor:
    """Processes images for cover generation."""

    @staticmethod
    def aspect_fill_crop(image: Image.Image, target_width: int, target_height: int) -> Image.Image:
        """
        Resize image proportionally and crop to fill target dimensions.

        Args:
            image: PIL Image object.
            target_width: Target width in pixels.
            target_height: Target height in pixels.

        Returns:
            Processed PIL Image object.
        """
        width, height = image.size

        # Calculate scale to cover entire target area
        ratio_w = target_width / width
        ratio_h = target_height / height
        scale = max(ratio_w, ratio_h)

        new_w = int(width * scale)
        new_h = int(height * scale)

        # Resize
        img_resized = image.resize((new_w, new_h), Image.LANCZOS)

        # Center crop
        left = (new_w - target_width) // 2
        top = (new_h - target_height) // 2
        right = left + target_width
        bottom = top + target_height

        return img_resized.crop((left, top, right, bottom))


class LayoutEngine:
    """Generates layouts based on configuration."""

    def __init__(self, size_cover: int, config_loader: ConfigLoader) -> None:
        """
        Initialize the layout engine.

        Args:
            size_cover: Canvas size in pixels.
            config_loader: ConfigLoader instance.
        """
        self.size_cover = size_cover
        self.config_loader = config_loader

    def _percent_to_pixels(self, percent: float) -> int:
        """Convert percentage to pixel value."""
        return int(round(self.size_cover * percent))

    def get_layout_positions(self, layout_name: str) -> Dict[int, Dict[str, Any]]:
        """
        Get image positions and sizes for a layout.

        Args:
            layout_name: Name of the layout.

        Returns:
            Dictionary mapping image index to position/size data.

        Raises:
            LayoutNotFoundError: If layout doesn't exist.
        """
        layout = self.config_loader.get_layout(layout_name)
        structure = layout.get("structure")

        if structure == "grid":
            return self._generate_grid_layout(layout)
        elif structure == "strip":
            return self._generate_strip_layout(layout)
        elif structure == "asymmetric":
            return self._generate_asymmetric_layout(layout)
        elif structure in ("custom_5", "custom_6"):
            return self._generate_custom_layout(layout)
        elif structure == "full_image":
            return {0: {}}  # Full image has no specific positions
        else:
            raise LayoutNotFoundError(f"Unknown layout structure: {structure}")

    def _generate_grid_layout(self, layout: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
        """Generate 3x3 grid layout."""
        positions_data = layout.get("positions", {})
        size_percent = positions_data.get("size_percent", 0.32421875)
        spacing_percent = positions_data.get("spacing_percent", 0.33828125)

        size = self._percent_to_pixels(size_percent)
        spacing = self._percent_to_pixels(spacing_percent)

        positions = {}
        index = 0

        for row in range(3):
            for col in range(3):
                x = col * spacing
                y = row * spacing
                positions[index] = {"size": (size, size), "position": (x, y)}
                index += 1

        return positions

    def _generate_strip_layout(self, layout: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
        """Generate horizontal strip layout."""
        image_count = layout.get("image_count", 4)
        banner_height_percent = layout.get("banner_height_percent", 0.1171875)

        banner_height = self._percent_to_pixels(banner_height_percent)
        image_height = self.size_cover - banner_height
        image_width = self.size_cover // image_count

        positions = {}
        for i in range(image_count):
            x = i * image_width
            positions[i] = {"size": (image_width, image_height), "position": (x, 0)}

        return positions

    def _generate_asymmetric_layout(self, layout: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
        """Generate asymmetric layout."""
        positions_data = layout.get("positions", {})
        positions = {}

        for idx_str, pos_data in positions_data.items():
            idx = int(idx_str)
            size_percents = pos_data.get("size", [1, 1])
            pos_percents = pos_data.get("position", [0, 0])

            size = (self._percent_to_pixels(size_percents[0]), self._percent_to_pixels(size_percents[1]))
            position = (self._percent_to_pixels(pos_percents[0]), self._percent_to_pixels(pos_percents[1]))

            positions[idx] = {"size": size, "position": position}

        return positions

    def _generate_custom_layout(self, layout: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
        """Generate custom layout from config."""
        return self._generate_asymmetric_layout(layout)


class CoverRenderer:
    """Renders cover images."""

    def __init__(
        self,
        size_cover: int,
        image_processor: ImageProcessor,
        font_manager: FontManager,
        config_loader: ConfigLoader,
    ) -> None:
        """
        Initialize the renderer.

        Args:
            size_cover: Canvas size in pixels.
            image_processor: ImageProcessor instance.
            font_manager: FontManager instance.
            config_loader: ConfigLoader instance.
        """
        self.size_cover = size_cover
        self.image_processor = image_processor
        self.font_manager = font_manager
        self.config_loader = config_loader

    def create_canvas(
        self, background_color: Optional[Tuple[int, int, int]] = None, mode: str = "RGB"
    ) -> Image.Image:
        """
        Create a blank canvas.

        Args:
            background_color: RGB color tuple. Uses config default if None.
            mode: Image mode (RGB, RGBA).

        Returns:
            PIL Image object.
        """
        if background_color is None:
            background_color = tuple(self.config_loader.get_default("background_color", [255, 255, 255]))

        if mode == "RGBA" and len(background_color) == 3:
            background_color = (*background_color, 255)

        return Image.new(mode, (self.size_cover, self.size_cover), background_color)

    def render_layout(
        self,
        layout_name: str,
        images: List[Image.Image],
        layout_engine: LayoutEngine,
    ) -> Image.Image:
        """
        Render images on canvas according to layout.

        Args:
            layout_name: Name of the layout.
            images: List of PIL Image objects.
            layout_engine: LayoutEngine instance.

        Returns:
            Canvas with rendered images.
        """
        canvas = self.create_canvas()
        positions = layout_engine.get_layout_positions(layout_name)

        for idx, image in enumerate(images):
            if idx not in positions:
                break

            pos_data = positions[idx]
            size = pos_data.get("size")
            position = pos_data.get("position")

            if size:
                processed_image = self.image_processor.aspect_fill_crop(image, size[0], size[1])
            else:
                # Full image case
                processed_image = image.resize((self.size_cover, self.size_cover), Image.LANCZOS)

            canvas.paste(processed_image, position)

        return canvas

    def add_banner(
        self,
        canvas: Image.Image,
        banner_height: int,
        fill_color: Optional[Tuple[int, int, int]] = None,
        text: Optional[str] = None,
        font_name: str = "default",
        text_color: str = "#000",
    ) -> Image.Image:
        """
        Add bottom banner to canvas.

        Args:
            canvas: PIL Image object.
            banner_height: Height of banner in pixels.
            fill_color: RGB color for banner.
            text: Optional text to add to banner.
            font_name: Name of font to use.
            text_color: Color of text.

        Returns:
            Updated canvas.
        """
        draw = ImageDraw.Draw(canvas)

        if fill_color is None:
            fill_color = tuple(
                self.config_loader.get_default("fill_color", [255, 255, 255]) or [255, 255, 255]
            )

        # Draw banner rectangle
        banner_y = self.size_cover - banner_height
        draw.rectangle([(0, banner_y), (self.size_cover, self.size_cover)], fill=fill_color)

        # Draw text if provided
        if text:
            font_size = int(self.size_cover * 0.0703125)  # ~90px for 1280
            font = self.font_manager.get_font(font_name, font_size)

            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

            x = (self.size_cover - text_w) / 2
            y = banner_y + (banner_height - text_h) / 2 - 10

            draw.text((x, y), text, fill=text_color, font=font)

        return canvas


class FileManager:
    """Manages file I/O operations."""

    def __init__(self, save_path: str) -> None:
        """
        Initialize the file manager.

        Args:
            save_path: Directory where covers will be saved.
        """
        self.save_path = Path(save_path)
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Ensure save directory exists."""
        self.save_path.mkdir(parents=True, exist_ok=True)

    def save_cover(self, image: Image.Image, filename: str, quality: int = 95) -> Path:
        """
        Save cover image to file.

        Args:
            image: PIL Image object.
            filename: Filename (without extension).
            quality: JPEG quality (1-100).

        Returns:
            Path to saved file.
        """
        filepath = self.save_path / f"{filename}.jpg"
        image.save(str(filepath), quality=quality)
        return filepath


class CoverProduct:
    """
    Main class for generating product cover images.

    Provides methods to generate covers in various layouts with
    customizable fonts, colors, and logos.
    """

    def __init__(
        self,
        product_path: str,
        size_cover: int = 1280,
        promocao: bool = False,
        config_path: Optional[str] = None,
    ) -> None:
        """
        Initialize CoverProduct.

        Args:
            product_path: Path to product folder.
            size_cover: Canvas size in pixels (default: 1280).
            promocao: Whether this is a promotional cover.
            config_path: Optional path to custom config file.

        Raises:
            ValueError: If size_cover is not int or float.
            InvalidImageError: If images directory is not found.
        """
        if not isinstance(size_cover, (int, float)):
            raise ValueError("size_cover must be int or float")

        self.product_path = Path(product_path)
        self.size_cover = int(round(size_cover))
        self.promocao = promocao

        # Initialize components
        self.config_loader = ConfigLoader(config_path)
        self.font_manager = FontManager(self.config_loader)
        self.image_processor = ImageProcessor()
        self.layout_engine = LayoutEngine(self.size_cover, self.config_loader)
        self.renderer = CoverRenderer(
            self.size_cover,
            self.image_processor,
            self.font_manager,
            self.config_loader,
        )

        # Setup paths and resources
        self._setup_paths()
        self.image_loader = ImageLoader(str(self.images_path))
        self.file_manager = FileManager(str(self.save_path))

        # Load available images
        self.available_images = self.image_loader.get_valid_images()

    def _setup_paths(self) -> None:
        """Setup product-related paths."""
        folder_name = self.product_path.name
        self.images_path = self.product_path / f"{folder_name} - Fotos"
        self.save_path = self.product_path / "Capa"

        if not self.images_path.exists():
            raise InvalidImageError(f"Images directory not found: {self.images_path}")

    def generate_cover(
        self,
        layout_name: str,
        name_save: str,
        title: Optional[str] = None,
        fill: Optional[Tuple[int, int, int]] = None,
        stroke_fill: str = "#fff",
        stroke_width: int = 5,
        font_color: str = "#000",
    ) -> Path:
        """
        Generate a cover with the specified layout.

        Args:
            layout_name: Name of the layout to use.
            name_save: Filename for the saved cover (without extension).
            title: Optional title text for the cover.
            fill: RGB color tuple for banner/background.
            stroke_fill: Stroke color for title.
            stroke_width: Stroke width for title.
            font_color: Color of the title text.

        Returns:
            Path to the saved cover image.

        Raises:
            LayoutNotFoundError: If layout doesn't exist.
            InsufficientImagesError: If not enough images for layout.
        """
        layout = self.config_loader.get_layout(layout_name)
        min_images = layout.get("min_images", 1)

        if len(self.available_images) < min_images:
            raise InsufficientImagesError(
                f"Layout '{layout_name}' requires at least {min_images} images. "
                f"Found: {len(self.available_images)}"
            )

        # Load random images
        selected_images = random.sample(self.available_images, min(min_images, len(self.available_images)))
        loaded_images = [self.image_loader.load_image(img) for img in selected_images]

        # Render layout
        canvas = self.renderer.render_layout(layout_name, loaded_images, self.layout_engine)

        # Add title if provided
        if title:
            canvas = self._add_title_to_canvas(
                canvas, layout_name, title, fill, stroke_fill, stroke_width, font_color
            )

        # Save cover
        quality = self.config_loader.get_default("save_quality", 95)
        filepath = self.file_manager.save_cover(canvas, name_save, quality)

        return filepath

    def _add_title_to_canvas(
        self,
        canvas: Image.Image,
        layout_name: str,
        title: str,
        fill: Optional[Tuple[int, int, int]],
        stroke_fill: str,
        stroke_width: int,
        font_color: str,
    ) -> Image.Image:
        """
        Add title to canvas using write_cover_title function.

        Args:
            canvas: PIL Image object.
            layout_name: Name of layout (for reference).
            title: Title text.
            fill: Banner color.
            stroke_fill: Stroke color.
            stroke_width: Stroke width.
            font_color: Text color.

        Returns:
            Updated canvas.
        """
        # Save temporarily to apply write_cover_title
        temp_path = self.file_manager.save_path / "_temp_cover.jpg"
        canvas.save(str(temp_path), quality=95)

        write_cover_title(
            str(temp_path),
            title,
            fill=fill,
            stroke_fill=stroke_fill,
            stroke_width=stroke_width,
            font_color=font_color,
            promocao=self.promocao,
        )

        # Reload the modified image
        result = Image.open(str(temp_path))

        # Clean up temp file
        temp_path.unlink()

        return result

    # Legacy method names for backward compatibility
    def layout_faixa_horizontal(
        self,
        name_save: str,
        title: Optional[str] = None,
        fill: Optional[Tuple[int, int, int]] = None,
        font_color: str = "#000",
        altura_banner: int = 150,
    ) -> Path:
        """
        Legacy method: Create horizontal strip layout.

        Args:
            name_save: Filename for save.
            title: Optional title text.
            fill: Banner color.
            font_color: Title text color.
            altura_banner: Banner height (deprecated, uses config).

        Returns:
            Path to saved cover.
        """
        return self.generate_cover(
            "faixa_horizontal",
            name_save,
            title=title,
            fill=fill,
            font_color=font_color,
        )

    def cover_grid(
        self,
        name_save: str,
        title: Optional[str] = None,
        fill: Optional[Tuple[int, int, int]] = None,
        stroke_fill: str = "#fff",
        stroke_width: int = 5,
        font_color: str = "#000",
    ) -> Path:
        """
        Legacy method: Create 3x3 grid layout.

        Args:
            name_save: Filename for save.
            title: Optional title text.
            fill: Banner color.
            stroke_fill: Stroke color.
            stroke_width: Stroke width.
            font_color: Text color.

        Returns:
            Path to saved cover.
        """
        return self.generate_cover(
            "grid_3x3",
            name_save,
            title=title,
            fill=fill,
            stroke_fill=stroke_fill,
            stroke_width=stroke_width,
            font_color=font_color,
        )

    def cover_three(
        self,
        name_save: str,
        title: Optional[str] = None,
        fill: Optional[Tuple[int, int, int]] = None,
        stroke_fill: str = "#fff",
        stroke_width: int = 5,
        font_color: str = "#000",
    ) -> Path:
        """
        Legacy method: Create 3-image asymmetric layout.

        Args:
            name_save: Filename for save.
            title: Optional title text.
            fill: Banner color.
            stroke_fill: Stroke color.
            stroke_width: Stroke width.
            font_color: Text color.

        Returns:
            Path to saved cover.
        """
        return self.generate_cover(
            "cover_three",
            name_save,
            title=title,
            fill=fill,
            stroke_fill=stroke_fill,
            stroke_width=stroke_width,
            font_color=font_color,
        )

    def cover_grid_2(
        self,
        name_save: str,
        title: Optional[str] = None,
        fill: Optional[Tuple[int, int, int]] = None,
        stroke_fill: str = "#fff",
        stroke_width: int = 5,
        font_color: str = "#000",
    ) -> Path:
        """
        Legacy method: Create 5-image custom layout.

        Args:
            name_save: Filename for save.
            title: Optional title text.
            fill: Banner color.
            stroke_fill: Stroke color.
            stroke_width: Stroke width.
            font_color: Text color.

        Returns:
            Path to saved cover.
        """
        return self.generate_cover(
            "grid_5_images",
            name_save,
            title=title,
            fill=fill,
            stroke_fill=stroke_fill,
            stroke_width=stroke_width,
            font_color=font_color,
        )

    def cover_grid_3(
        self,
        name_save: str,
        title: Optional[str] = None,
        fill: Optional[Tuple[int, int, int]] = None,
        stroke_fill: str = "#fff",
        stroke_width: int = 5,
        font_color: str = "#000",
    ) -> Path:
        """
        Legacy method: Create 6-image custom layout.

        Args:
            name_save: Filename for save.
            title: Optional title text.
            fill: Banner color.
            stroke_fill: Stroke color.
            stroke_width: Stroke width.
            font_color: Text color.

        Returns:
            Path to saved cover.
        """
        return self.generate_cover(
            "grid_6_images",
            name_save,
            title=title,
            fill=fill,
            stroke_fill=stroke_fill,
            stroke_width=stroke_width,
            font_color=font_color,
        )

    def cover_full_logo(
        self,
        name_save: str,
        title: str,
        company: str = "LEGITIMA",
    ) -> Path:
        """
        Legacy method: Create full-image cover with logo overlay.

        Args:
            name_save: Filename for save.
            title: Title text.
            company: Company name for logo selection.

        Returns:
            Path to saved cover.

        Raises:
            InsufficientImagesError: If no images available.
            MissingAssetError: If logo is not found.
        """
        if len(self.available_images) < 1:
            raise InsufficientImagesError("At least 1 image is required for full_image layout")

        # Load image
        image = self.image_loader.load_image(random.choice(self.available_images))

        # Create canvas
        canvas = self.renderer.create_canvas(mode="RGBA")

        # Get logo
        logo_path = self.config_loader.get_asset_path("logos", company)
        logo = Image.open(str(logo_path))
        logo_size = int(self.size_cover * 0.2)
        logo = logo.resize((logo_size, logo_size))

        # Draw background
        draw = ImageDraw.Draw(canvas)

        # Draw text background ellipse
        ellipse_coords = (
            int(self.size_cover * 0.0859375),
            int(self.size_cover * 0.63359375),
            int(self.size_cover * 0.9140625),
            int(self.size_cover * 0.9),
        )
        draw.ellipse(ellipse_coords, fill=(255, 255, 255, 100))

        # Draw text
        font_size = int(self.size_cover * 0.05)
        font = self.font_manager.get_font("title", font_size)

        text_pos = (
            int(self.size_cover * 0.5),
            int(self.size_cover * 0.766796875),
        )

        draw.text(
            text_pos,
            title,
            font=font,
            anchor="mm",
            fill="black",
            stroke_fill="white",
            stroke_width=3,
        )

        # Composite with image
        logo_pos = (
            int(self.size_cover * 0.4),
            int(self.size_cover * 0.05),
        )
        canvas.paste(logo, logo_pos, logo)

        # Resize image and composite
        image_resized = image.convert("RGBA").resize((self.size_cover, self.size_cover), Image.LANCZOS)
        result = Image.alpha_composite(image_resized, canvas)
        result = result.convert("RGB")

        # Save
        quality = self.config_loader.get_default("save_quality", 95)
        filepath = self.file_manager.save_cover(result, name_save, quality)

        return filepath

    def layout_coluna_vertical(
        self,
        name_save: str,
        title: str,
        fill: Optional[Tuple[int, int, int]] = None,
        font_color: str = "#000",
    ) -> Path:
        """
        Layout com 4 imagens empilhadas verticalmente e banner lateral rotacionado.

        Args:
            name_save: Filename for save.
            title: Title text (required).
            fill: Banner color.
            font_color: Title text color.

        Returns:
            Path to saved cover.
        """
        if len(self.available_images) < 4:
            raise InsufficientImagesError(
                f"layout_coluna_vertical requires at least 4 images. Found: {len(self.available_images)}"
            )

        LARGURA_TOTAL = self.size_cover
        ALTURA_TOTAL = int(self.size_cover * 1.5)
        LARGURA_BANNER = int(self.size_cover * 0.25)

        canvas = Image.new("RGB", (LARGURA_TOTAL, ALTURA_TOTAL), (255, 255, 255))

        # Processar e colar as 4 imagens
        largura_img = LARGURA_TOTAL - LARGURA_BANNER
        altura_img = ALTURA_TOTAL // 4

        images = random.sample(self.available_images, 4)
        for i, img_name in enumerate(images):
            img = self.image_loader.load_image(img_name)
            img_processada = self.image_processor.aspect_fill_crop(img, largura_img, altura_img)
            canvas.paste(img_processada, (0, i * altura_img))

        # Criar banner lateral com texto rotacionado
        banner_color = fill or tuple(self.config_loader.get_default("banner_color_rgb", [0, 165, 165]))
        text_color_rgb = tuple(self.config_loader.get_default("text_color_rgb", [255, 255, 255]))

        banner_lateral = Image.new("RGB", (LARGURA_BANNER, ALTURA_TOTAL), banner_color)
        txt_layer = Image.new("RGBA", (ALTURA_TOTAL, LARGURA_BANNER), (255, 255, 255, 0))
        draw_txt = ImageDraw.Draw(txt_layer)

        font_size = int(self.size_cover * 0.07)
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            font = FONTE_PADRAO

        bbox = draw_txt.textbbox((0, 0), title, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        txt_pos_x = (ALTURA_TOTAL - text_w) / 2
        txt_pos_y = (LARGURA_BANNER - text_h) / 2 - 15

        draw_txt.text((txt_pos_x, txt_pos_y), title, fill=text_color_rgb, font=font)

        rotated_txt = txt_layer.rotate(90, expand=1)
        offset_x = (LARGURA_BANNER - rotated_txt.width) // 2
        offset_y = (ALTURA_TOTAL - rotated_txt.height) // 2

        banner_lateral.paste(rotated_txt, (offset_x, offset_y), rotated_txt)
        canvas.paste(banner_lateral, (largura_img, 0))

        quality = self.config_loader.get_default("save_quality", 95)
        filepath = self.file_manager.save_cover(canvas, name_save, quality)

        return filepath

    def layout_hero_thumbnails(
        self,
        name_save: str,
        title: str,
        fill: Optional[Tuple[int, int, int]] = None,
        font_color: str = "#000",
    ) -> Path:
        """
        Hero image on top with 3 thumbnail strips below and central banner.

        Args:
            name_save: Filename for save.
            title: Title text (required).
            fill: Banner color.
            font_color: Title text color.

        Returns:
            Path to saved cover.
        """
        if len(self.available_images) < 4:
            raise InsufficientImagesError(
                f"layout_hero_thumbnails requires at least 4 images. Found: {len(self.available_images)}"
            )

        TAMANHO = self.size_cover
        ALTURA_HERO = int(TAMANHO * 0.55)
        ALTURA_BANNER = int(TAMANHO * 0.12)
        ALTURA_THUMBS = TAMANHO - ALTURA_HERO - ALTURA_BANNER

        canvas = Image.new("RGB", (TAMANHO, TAMANHO), (255, 255, 255))
        draw = ImageDraw.Draw(canvas)

        # Hero image
        hero_img_name = random.choice(self.available_images)
        hero_img = self.image_loader.load_image(hero_img_name)
        hero_img_processed = self.image_processor.aspect_fill_crop(hero_img, TAMANHO, ALTURA_HERO)
        canvas.paste(hero_img_processed, (0, 0))

        # Banner central
        banner_color = fill or tuple(self.config_loader.get_default("banner_color_rgb", [0, 165, 165]))
        text_color_rgb = tuple(self.config_loader.get_default("text_color_rgb", [255, 255, 255]))

        draw.rectangle([(0, ALTURA_HERO), (TAMANHO, ALTURA_HERO + ALTURA_BANNER)], fill=banner_color)

        font_size = int(self.size_cover * 0.07)
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            font = FONTE_PADRAO

        bbox = draw.textbbox((0, 0), title, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        pos_x = (TAMANHO - text_w) / 2
        pos_y = ALTURA_HERO + (ALTURA_BANNER - text_h) / 2 - 10
        draw.text((pos_x, pos_y), title, fill=text_color_rgb, font=font)

        # Thumbnails
        largura_thumb = TAMANHO // 3
        y_start_thumbs = ALTURA_HERO + ALTURA_BANNER

        thumb_images = random.sample(self.available_images, min(3, len(self.available_images)))
        for i, img_name in enumerate(thumb_images):
            thumb_img = self.image_loader.load_image(img_name)
            thumb_processed = self.image_processor.aspect_fill_crop(thumb_img, largura_thumb, ALTURA_THUMBS)
            canvas.paste(thumb_processed, (i * largura_thumb, y_start_thumbs))

        quality = self.config_loader.get_default("save_quality", 95)
        filepath = self.file_manager.save_cover(canvas, name_save, quality)

        return filepath

    def layout_grid_translucido(
        self,
        name_save: str,
        title: str,
        fill: Optional[Tuple[int, int, int]] = None,
        font_color: str = "#fff",
    ) -> Path:
        """
        2x2 grid with translucent horizontal band and text overlay.

        Args:
            name_save: Filename for save.
            title: Title text (required).
            fill: Banner color.
            font_color: Title text color.

        Returns:
            Path to saved cover.
        """
        if len(self.available_images) < 4:
            raise InsufficientImagesError(
                f"layout_grid_translucido requires at least 4 images. Found: {len(self.available_images)}"
            )

        TAMANHO = self.size_cover
        METADE = TAMANHO // 2

        # Create base grid
        canvas_base = Image.new("RGB", (TAMANHO, TAMANHO), (255, 255, 255))
        posicoes = [(0, 0), (METADE, 0), (0, METADE), (METADE, METADE)]

        grid_images = random.sample(self.available_images, 4)
        for i, img_name in enumerate(grid_images):
            img = self.image_loader.load_image(img_name)
            img_processed = self.image_processor.aspect_fill_crop(img, METADE, METADE)
            canvas_base.paste(img_processed, posicoes[i])

        # Create translucent overlay
        overlay = Image.new("RGBA", (TAMANHO, TAMANHO), (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay)

        ALTURA_FAIXA = int(TAMANHO * 0.2)
        y_faixa_inicio = (TAMANHO - ALTURA_FAIXA) // 2
        y_faixa_fim = y_faixa_inicio + ALTURA_FAIXA

        banner_color = fill or tuple(self.config_loader.get_default("banner_color_rgb", [0, 165, 165]))
        cor_translucida = banner_color + (220,)
        draw_overlay.rectangle([(0, y_faixa_inicio), (TAMANHO, y_faixa_fim)], fill=cor_translucida)

        # Add text
        text_color = font_color if isinstance(font_color, tuple) else (255, 255, 255)

        font_size = int(self.size_cover * 0.07)
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            font = FONTE_PADRAO

        bbox = draw_overlay.textbbox((0, 0), title, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        pos_x = (TAMANHO - text_w) / 2
        pos_y = (TAMANHO - text_h) / 2 - 10

        draw_overlay.text((pos_x, pos_y), title, fill=text_color, font=font)

        # Composite
        canvas_final = Image.alpha_composite(canvas_base.convert("RGBA"), overlay)
        canvas_final = canvas_final.convert("RGB")

        quality = self.config_loader.get_default("save_quality", 95)
        filepath = self.file_manager.save_cover(canvas_final, name_save, quality)

        return filepath

    def layout_mosaic_pro(
        self,
        name_save: str,
        title: str,
        fill: Optional[Tuple[int, int, int]] = None,
        font_color: str = "#fff",
    ) -> Path:
        """
        Large image on left with 3 stacked smaller images on right.

        Args:
            name_save: Filename for save.
            title: Title text (required).
            fill: Badge background color.
            font_color: Text color.

        Returns:
            Path to saved cover.
        """
        if len(self.available_images) < 4:
            raise InsufficientImagesError(
                f"layout_mosaic_pro requires at least 4 images. Found: {len(self.available_images)}"
            )

        TAMANHO = self.size_cover
        LARGURA_GRANDE = int(TAMANHO * 0.65)
        LARGURA_PEQUENA = TAMANHO - LARGURA_GRANDE
        ALTURA_PEQUENA = TAMANHO // 3

        canvas = Image.new("RGB", (TAMANHO, TAMANHO), (255, 255, 255))
        draw = ImageDraw.Draw(canvas)

        # Large image
        mosaic_images = random.sample(self.available_images, 4)
        img_grande = self.image_loader.load_image(mosaic_images[0])
        img_grande_processed = self.image_processor.aspect_fill_crop(img_grande, LARGURA_GRANDE, TAMANHO)
        canvas.paste(img_grande_processed, (0, 0))

        # Three smaller images
        for i in range(1, 4):
            img_sm = self.image_loader.load_image(mosaic_images[i])
            img_sm_processed = self.image_processor.aspect_fill_crop(img_sm, LARGURA_PEQUENA, ALTURA_PEQUENA)
            canvas.paste(img_sm_processed, (LARGURA_GRANDE, (i - 1) * ALTURA_PEQUENA))

        # Text badge
        banner_color = fill or tuple(self.config_loader.get_default("banner_color_rgb", [0, 165, 165]))
        text_color_rgb = tuple(self.config_loader.get_default("text_color_rgb", [255, 255, 255]))

        font_size = int(self.size_cover * 0.07)
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            font = FONTE_PADRAO

        padding_h, padding_v = 40, 20
        bbox = draw.textbbox((0, 0), title, font=font)
        txt_w = bbox[2] - bbox[0]
        txt_h = bbox[3] - bbox[1]

        rect_x0, rect_y0 = 30, TAMANHO - txt_h - (padding_v * 2) - 30
        rect_x1, rect_y1 = rect_x0 + txt_w + (padding_h * 2), TAMANHO - 30

        draw.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill=banner_color)
        draw.text((rect_x0 + padding_h, rect_y0 + padding_v - 5), title, fill=text_color_rgb, font=font)

        quality = self.config_loader.get_default("save_quality", 95)
        filepath = self.file_manager.save_cover(canvas, name_save, quality)

        return filepath

    def layout_gallery_clean(
        self,
        name_save: str,
        title: str,
        fill: Optional[Tuple[int, int, int]] = None,
        font_color: str = "#000",
    ) -> Path:
        """
        4 images with margins and centered banner bar.

        Args:
            name_save: Filename for save.
            title: Title text (required).
            fill: Banner color.
            font_color: Title text color.

        Returns:
            Path to saved cover.
        """
        if len(self.available_images) < 4:
            raise InsufficientImagesError(
                f"layout_gallery_clean requires at least 4 images. Found: {len(self.available_images)}"
            )

        TAMANHO = self.size_cover
        MARGEM = int(TAMANHO * 0.02)
        TAM_IMG = (TAMANHO - (MARGEM * 3)) // 2

        canvas = Image.new("RGB", (TAMANHO, TAMANHO), (255, 255, 255))
        draw = ImageDraw.Draw(canvas)

        # Position 4 images with margins
        posicoes = [
            (MARGEM, MARGEM),
            (TAM_IMG + MARGEM * 2, MARGEM),
            (MARGEM, TAM_IMG + MARGEM * 2),
            (TAM_IMG + MARGEM * 2, TAM_IMG + MARGEM * 2),
        ]

        gallery_images = random.sample(self.available_images, 4)
        for i, img_name in enumerate(gallery_images):
            img = self.image_loader.load_image(img_name)
            img_processed = self.image_processor.aspect_fill_crop(img, TAM_IMG, TAM_IMG)
            canvas.paste(img_processed, posicoes[i])

        # Central bar with text
        ALTURA_BARRA = int(TAMANHO * 0.1)
        y0 = (TAMANHO - ALTURA_BARRA) // 2

        banner_color = fill or tuple(self.config_loader.get_default("banner_color_rgb", [0, 165, 165]))
        draw.rectangle([0, y0, TAMANHO, y0 + ALTURA_BARRA], fill=banner_color)

        # Text
        font_size = int(self.size_cover * 0.06)
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            font = FONTE_PADRAO

        text_color_rgb = tuple(self.config_loader.get_default("text_color_rgb", [255, 255, 255]))
        bbox = draw.textbbox((0, 0), title, font=font)
        txt_w, txt_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(
            ((TAMANHO - txt_w) // 2, y0 + (ALTURA_BARRA - txt_h) // 2 - 5),
            title,
            fill=text_color_rgb,
            font=font,
        )

        quality = self.config_loader.get_default("save_quality", 95)
        filepath = self.file_manager.save_cover(canvas, name_save, quality)

        return filepath

    def layout_split_vertical(
        self,
        name_save: str,
        title: str,
        fill: Optional[Tuple[int, int, int]] = None,
        font_color: str = "#000",
    ) -> Path:
        """
        4 vertical slices with centered banner box.

        Args:
            name_save: Filename for save.
            title: Title text (required).
            fill: Box background color.
            font_color: Text color.

        Returns:
            Path to saved cover.
        """
        if len(self.available_images) < 4:
            raise InsufficientImagesError(
                f"layout_split_vertical requires at least 4 images. Found: {len(self.available_images)}"
            )

        TAMANHO = self.size_cover
        LARGURA_FATIA = TAMANHO // 4

        canvas = Image.new("RGB", (TAMANHO, TAMANHO), (255, 255, 255))
        draw = ImageDraw.Draw(canvas)

        # 4 vertical slices
        split_images = random.sample(self.available_images, 4)
        for i, img_name in enumerate(split_images):
            img = self.image_loader.load_image(img_name)
            img_processed = self.image_processor.aspect_fill_crop(img, LARGURA_FATIA, TAMANHO)
            canvas.paste(img_processed, (i * LARGURA_FATIA, 0))

        # Central box
        largura_box, altura_box = int(TAMANHO * 0.7), int(TAMANHO * 0.18)
        x0, y0 = (TAMANHO - largura_box) // 2, (TAMANHO - altura_box) // 2
        x1, y1 = x0 + largura_box, y0 + altura_box

        draw.rectangle([x0 - 5, y0 - 5, x1 + 5, y1 + 5], fill="white")

        banner_color = fill or tuple(self.config_loader.get_default("banner_color_rgb", [0, 165, 165]))
        draw.rectangle([x0, y0, x1, y1], fill=banner_color)

        # Text
        font_size = int(self.size_cover * 0.07)
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            font = FONTE_PADRAO

        text_color_rgb = tuple(self.config_loader.get_default("text_color_rgb", [255, 255, 255]))
        bbox = draw.textbbox((0, 0), title, font=font)
        txt_w, txt_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(
            ((TAMANHO - txt_w) // 2, (TAMANHO - txt_h) // 2 - 10), title, fill=text_color_rgb, font=font
        )

        quality = self.config_loader.get_default("save_quality", 95)
        filepath = self.file_manager.save_cover(canvas, name_save, quality)

        return filepath

    def layout_circular_focus(
        self,
        name_save: str,
        title: str,
        fill: Optional[Tuple[int, int, int]] = None,
        font_color: str = "#000",
    ) -> Path:
        """
        3 horizontal slices with centered circular image overlay.

        Args:
            name_save: Filename for save.
            title: Title text (required).
            fill: Bottom banner color.
            font_color: Text color.

        Returns:
            Path to saved cover.
        """
        if len(self.available_images) < 4:
            raise InsufficientImagesError(
                f"layout_circular_focus requires at least 4 images. Found: {len(self.available_images)}"
            )

        TAMANHO = self.size_cover
        canvas = Image.new("RGB", (TAMANHO, TAMANHO), (255, 255, 255))
        draw_border = ImageDraw.Draw(canvas)

        # 3 horizontal slices
        altura_fatia = TAMANHO // 3
        circle_images = random.sample(self.available_images, 4)

        for i in range(3):
            img = self.image_loader.load_image(circle_images[i])
            img_processed = self.image_processor.aspect_fill_crop(img, TAMANHO, altura_fatia)
            canvas.paste(img_processed, (0, i * altura_fatia))

        # Central circle with 4th image
        diametro = int(TAMANHO * 0.45)
        img_circ = self.image_loader.load_image(circle_images[3])
        img_circ_processed = self.image_processor.aspect_fill_crop(img_circ, diametro, diametro)

        # Circular mask
        mask = Image.new("L", (diametro, diametro), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, diametro, diametro), fill=255)

        # Position and border
        pos_central = ((TAMANHO - diametro) // 2, (TAMANHO - diametro) // 2)
        borda = 15
        draw_border.ellipse(
            (
                pos_central[0] - borda,
                pos_central[1] - borda,
                pos_central[0] + diametro + borda,
                pos_central[1] + diametro + borda,
            ),
            fill="white",
        )

        canvas.paste(img_circ_processed, pos_central, mask)

        # Bottom banner
        draw = ImageDraw.Draw(canvas)
        banner_color = fill or tuple(self.config_loader.get_default("banner_color_rgb", [0, 165, 165]))
        draw.rectangle([250, 850, TAMANHO - 250, 950], fill=banner_color)

        font_size = int(self.size_cover * 0.07)
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            font = FONTE_PADRAO

        text_color_rgb = tuple(self.config_loader.get_default("text_color_rgb", [255, 255, 255]))
        bbox = draw.textbbox((0, 0), title, font=font)
        draw.text(((TAMANHO - (bbox[2] - bbox[0])) // 2, 875), title, fill=text_color_rgb, font=font)

        quality = self.config_loader.get_default("save_quality", 95)
        filepath = self.file_manager.save_cover(canvas, name_save, quality)

        return filepath

    def layout_diagonal_split(
        self,
        name_save: str,
        title: str,
        fill: Optional[Tuple[int, int, int]] = None,
        font_color: str = "#fff",
    ) -> Path:
        """
        2 images with diagonal split and centered text.

        Args:
            name_save: Filename for save.
            title: Title text (required).
            fill: Not used in this layout.
            font_color: Text color.

        Returns:
            Path to saved cover.
        """
        if len(self.available_images) < 2:
            raise InsufficientImagesError(
                f"layout_diagonal_split requires at least 2 images. Found: {len(self.available_images)}"
            )

        TAMANHO = self.size_cover

        # Load 2 images
        diag_images = random.sample(self.available_images, 2)
        img_esq = self.image_loader.load_image(diag_images[0])
        img_dir = self.image_loader.load_image(diag_images[1])

        img_esq_processed = self.image_processor.aspect_fill_crop(img_esq, TAMANHO, TAMANHO)
        img_dir_processed = self.image_processor.aspect_fill_crop(img_dir, TAMANHO, TAMANHO)

        # Diagonal mask
        mask = Image.new("L", (TAMANHO, TAMANHO), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.polygon([(TAMANHO, 0), (TAMANHO, TAMANHO), (0, TAMANHO)], fill=255)

        img_esq_processed.paste(img_dir_processed, (0, 0), mask)
        canvas = img_esq_processed

        # Diagonal line
        overlay = Image.new("RGBA", (TAMANHO, TAMANHO), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)
        draw_ov.line([(0, TAMANHO), (TAMANHO, 0)], fill=(100, 100, 100, 255), width=30)
        canvas.paste(overlay, (0, 0), overlay)

        # Add text
        draw = ImageDraw.Draw(canvas)
        font_size = int(self.size_cover * 0.08)
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            font = FONTE_PADRAO

        text_color_rgb = (255, 255, 255)
        bbox = draw.textbbox((0, 0), title, font=font)
        draw.text(
            ((TAMANHO - (bbox[2] - bbox[0])) // 2, (TAMANHO // 2) - 50), title, fill=text_color_rgb, font=font
        )

        quality = self.config_loader.get_default("save_quality", 95)
        filepath = self.file_manager.save_cover(canvas, name_save, quality)

        return filepath

    def layout_masonry(
        self,
        name_save: str,
        title: str,
        fill: Optional[Tuple[int, int, int]] = None,
        font_color: str = "#fff",
    ) -> Path:
        """
        Asymmetric masonry-style layout with 4 images and centered overlay box.

        Args:
            name_save: Filename for save.
            title: Title text (required).
            fill: Overlay box background color.
            font_color: Text color.

        Returns:
            Path to saved cover.
        """
        if len(self.available_images) < 4:
            raise InsufficientImagesError(
                f"layout_masonry requires at least 4 images. Found: {len(self.available_images)}"
            )

        TAMANHO = self.size_cover
        canvas = Image.new("RGB", (TAMANHO, TAMANHO), (255, 255, 255))
        draw = ImageDraw.Draw(canvas)

        # Asymmetric blocks
        blocos = [
            (0, 0, 400, 600),  # Tall left
            (400, 0, 600, 400),  # Wide top right
            (0, 600, 600, 400),  # Wide bottom left
            (600, 400, 400, 600),  # Tall bottom right
        ]

        masonry_images = random.sample(self.available_images, 4)
        for i in range(4):
            x, y, w, h = blocos[i]
            img = self.image_loader.load_image(masonry_images[i])
            img_processed = self.image_processor.aspect_fill_crop(img, w, h)
            canvas.paste(img_processed, (x, y))

        # Central overlay
        side = 300
        banner_color = fill or tuple(self.config_loader.get_default("banner_color_rgb", [0, 165, 165]))
        draw.rectangle(
            [(TAMANHO - side) // 2, (TAMANHO - side) // 2, (TAMANHO + side) // 2, (TAMANHO + side) // 2],
            fill=banner_color,
            outline="white",
            width=5,
        )

        # Text
        font_size = int(self.size_cover * 0.05)
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            font = FONTE_PADRAO

        text_color_rgb = tuple(self.config_loader.get_default("text_color_rgb", [255, 255, 255]))

        # Handle multi-line text if needed
        text_lines = title.split("\n") if "\n" in title else [title]
        y_offset = 450 if len(text_lines) > 1 else 470

        for line in text_lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            draw.text(
                (int((TAMANHO - (bbox[2] - bbox[0])) // 2), y_offset), line, fill=text_color_rgb, font=font
            )
            y_offset += 60

        quality = self.config_loader.get_default("save_quality", 95)
        filepath = self.file_manager.save_cover(canvas, name_save, quality)

        return filepath
