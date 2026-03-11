"""
Custom exceptions for the Cover Product module.
"""


class CoverProductError(Exception):
    """Base exception for Cover Product errors."""

    pass


class InvalidImageError(CoverProductError):
    """Raised when an image cannot be loaded or validated."""

    pass


class InsufficientImagesError(CoverProductError):
    """Raised when there are not enough images for the requested layout."""

    pass


class LayoutNotFoundError(CoverProductError):
    """Raised when the requested layout does not exist."""

    pass


class MissingAssetError(CoverProductError):
    """Raised when a required asset (font, logo) is missing."""

    pass


class InvalidConfigError(CoverProductError):
    """Raised when the configuration is invalid."""

    pass
