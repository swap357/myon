"""Canvas module for creating and manipulating images."""

from pathlib import Path

import numpy as np
from PIL import Image

from myon.color import Color


class Canvas:
    """A canvas for generative art drawing.

    The canvas uses a coordinate system where (0, 0) is the top-left corner.
    """

    def __init__(self, width: int, height: int, background: Color | None = None) -> None:
        """Initialize a new canvas.

        Args:
            width: Canvas width in pixels
            height: Canvas height in pixels
            background: Background color (defaults to white)
        """
        if width <= 0 or height <= 0:
            raise ValueError("Canvas dimensions must be positive")

        self.width = width
        self.height = height
        self._background = background or Color(255, 255, 255)

        # Initialize pixel array (height, width, RGB)
        self._pixels = np.full((height, width, 3), self._background.to_array(), dtype=np.uint8)

    @property
    def shape(self) -> tuple[int, int]:
        """Return canvas dimensions as (width, height)."""
        return (self.width, self.height)

    def set_pixel(self, x: int, y: int, color: Color) -> None:
        """Set a single pixel color.

        Args:
            x: X coordinate
            y: Y coordinate
            color: Color to set
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self._pixels[y, x] = color.to_array()

    def get_pixel(self, x: int, y: int) -> Color:
        """Get a single pixel color.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Color at the specified coordinates
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"Coordinates ({x}, {y}) out of bounds")
        return Color(*self._pixels[y, x])

    def fill(self, color: Color) -> None:
        """Fill entire canvas with a color.

        Args:
            color: Color to fill with
        """
        self._pixels[:] = color.to_array()

    def clear(self) -> None:
        """Clear canvas to background color."""
        self.fill(self._background)

    @property
    def pixels(self) -> np.ndarray[tuple[int, int, int], np.dtype[np.uint8]]:
        """Get read-only view of pixel array.

        Returns:
            NumPy array of shape (height, width, 3)
        """
        return self._pixels.copy()

    def save(self, filepath: Path | str, format: str | None = None) -> None:
        """Save canvas to an image file.

        Args:
            filepath: Path to save the image
            format: Image format (PNG, JPEG, etc.). If None, inferred from filename
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        image = Image.fromarray(self._pixels, mode="RGB")
        image.save(filepath, format=format)

    @classmethod
    def from_image(cls, filepath: Path | str) -> "Canvas":
        """Create a canvas from an existing image file.

        Args:
            filepath: Path to the image file

        Returns:
            New Canvas instance with image data
        """
        image = Image.open(filepath).convert("RGB")
        width, height = image.size

        canvas = cls(width, height)
        canvas._pixels = np.array(image, dtype=np.uint8)
        return canvas

    def __repr__(self) -> str:
        """Return string representation of canvas."""
        return f"Canvas(width={self.width}, height={self.height})"
