"""Tests for the Canvas class."""

import tempfile
from pathlib import Path

import numpy as np
import pytest

from myon.canvas import Canvas
from myon.color import BLACK, WHITE, Color


def test_canvas_initialization():
    """Test canvas creation with default and custom backgrounds."""
    canvas = Canvas(100, 100)
    assert canvas.width == 100
    assert canvas.height == 100
    assert canvas.shape == (100, 100)

    # Test with custom background
    canvas = Canvas(50, 50, BLACK)
    assert canvas.get_pixel(0, 0) == BLACK


def test_canvas_invalid_dimensions():
    """Test that invalid dimensions raise ValueError."""
    with pytest.raises(ValueError):
        Canvas(0, 100)

    with pytest.raises(ValueError):
        Canvas(100, -1)


def test_set_and_get_pixel():
    """Test setting and getting individual pixels."""
    canvas = Canvas(10, 10)
    red = Color(255, 0, 0)

    canvas.set_pixel(5, 5, red)
    assert canvas.get_pixel(5, 5) == red


def test_get_pixel_out_of_bounds():
    """Test that getting out-of-bounds pixel raises ValueError."""
    canvas = Canvas(10, 10)

    with pytest.raises(ValueError):
        canvas.get_pixel(-1, 0)

    with pytest.raises(ValueError):
        canvas.get_pixel(10, 10)


def test_fill_canvas():
    """Test filling canvas with a color."""
    canvas = Canvas(10, 10)
    canvas.fill(BLACK)

    # Check all pixels are black
    for x in range(10):
        for y in range(10):
            assert canvas.get_pixel(x, y) == BLACK


def test_clear_canvas():
    """Test clearing canvas to background."""
    canvas = Canvas(10, 10, WHITE)
    canvas.fill(BLACK)
    canvas.clear()

    assert canvas.get_pixel(0, 0) == WHITE


def test_pixels_property():
    """Test pixels property returns correct array."""
    canvas = Canvas(5, 5, BLACK)
    pixels = canvas.pixels

    assert pixels.shape == (5, 5, 3)
    assert np.all(pixels == 0)


def test_save_and_load_canvas():
    """Test saving and loading canvas from file."""
    canvas = Canvas(10, 10)
    canvas.set_pixel(5, 5, Color(255, 0, 0))

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test.png"
        canvas.save(filepath)

        assert filepath.exists()

        # Load and verify
        loaded = Canvas.from_image(filepath)
        assert loaded.width == canvas.width
        assert loaded.height == canvas.height
        assert loaded.get_pixel(5, 5).r > 200  # Account for compression artifacts


def test_canvas_repr():
    """Test string representation of canvas."""
    canvas = Canvas(100, 50)
    assert "Canvas" in repr(canvas)
    assert "100" in repr(canvas)
    assert "50" in repr(canvas)
