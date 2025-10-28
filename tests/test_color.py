"""Tests for the Color class."""

import numpy as np
import pytest

from myon.color import BLACK, BLUE, GREEN, RED, WHITE, Color


def test_color_initialization():
    """Test color creation with valid values."""
    color = Color(128, 64, 32)
    assert color.r == 128
    assert color.g == 64
    assert color.b == 32
    assert color.a == 255


def test_color_clamping():
    """Test that color values are clamped to [0, 255]."""
    color = Color(-10, 300, 128)
    assert color.r == 0
    assert color.g == 255
    assert color.b == 128


def test_color_to_tuple():
    """Test conversion to RGB tuple."""
    color = Color(100, 150, 200)
    assert color.to_tuple() == (100, 150, 200)


def test_color_to_array():
    """Test conversion to NumPy array."""
    color = Color(100, 150, 200)
    arr = color.to_array()
    assert isinstance(arr, np.ndarray)
    assert np.array_equal(arr, np.array([100, 150, 200], dtype=np.uint8))


def test_color_to_hex():
    """Test conversion to hex string."""
    color = Color(255, 128, 0)
    assert color.to_hex() == "#ff8000"


def test_color_from_hex():
    """Test creation from hex string."""
    color = Color.from_hex("#ff8000")
    assert color.r == 255
    assert color.g == 128
    assert color.b == 0

    # Test without # prefix
    color2 = Color.from_hex("00ff80")
    assert color2.r == 0
    assert color2.g == 255
    assert color2.b == 128


def test_color_from_hex_invalid():
    """Test that invalid hex strings raise ValueError."""
    with pytest.raises(ValueError):
        Color.from_hex("#fff")  # Too short

    with pytest.raises(ValueError):
        Color.from_hex("#fffffff")  # Too long


def test_color_from_hsv():
    """Test creation from HSV values."""
    # Pure red
    color = Color.from_hsv(0, 1.0, 1.0)
    assert color.r == 255
    assert color.g == 0
    assert color.b == 0

    # Pure green
    color = Color.from_hsv(120, 1.0, 1.0)
    assert color.r == 0
    assert color.g == 255
    assert color.b == 0

    # Pure blue
    color = Color.from_hsv(240, 1.0, 1.0)
    assert color.r == 0
    assert color.g == 0
    assert color.b == 255


def test_color_lerp():
    """Test linear interpolation between colors."""
    # Interpolate from black to white
    color = BLACK.lerp(WHITE, 0.5)
    assert 125 <= color.r <= 130  # Should be around 127-128
    assert 125 <= color.g <= 130
    assert 125 <= color.b <= 130

    # Endpoints
    assert BLACK.lerp(WHITE, 0.0) == BLACK
    assert BLACK.lerp(WHITE, 1.0) == WHITE


def test_color_equality():
    """Test color equality comparison."""
    color1 = Color(100, 150, 200)
    color2 = Color(100, 150, 200)
    color3 = Color(100, 150, 201)

    assert color1 == color2
    assert color1 != color3


def test_color_constants():
    """Test predefined color constants."""
    assert Color(0, 0, 0) == BLACK
    assert Color(255, 255, 255) == WHITE
    assert Color(255, 0, 0) == RED
    assert Color(0, 255, 0) == GREEN
    assert Color(0, 0, 255) == BLUE


def test_color_repr():
    """Test string representation of color."""
    color = Color(100, 150, 200)
    assert "Color" in repr(color)
    assert "100" in repr(color)
    assert "150" in repr(color)
    assert "200" in repr(color)
