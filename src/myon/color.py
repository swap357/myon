"""Color module for handling colors in various formats."""

import numpy as np


class Color:
    """Represents a color in RGB format.

    Color values are stored as integers in the range [0, 255].
    """

    def __init__(self, r: int, g: int, b: int, a: int = 255) -> None:
        """Initialize a color.

        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
            a: Alpha/transparency component (0-255, default 255)
        """
        self._r = self._clamp(r)
        self._g = self._clamp(g)
        self._b = self._clamp(b)
        self._a = self._clamp(a)

    @staticmethod
    def _clamp(value: int) -> int:
        """Clamp value to valid color range [0, 255]."""
        return max(0, min(255, int(value)))

    @property
    def r(self) -> int:
        """Red component."""
        return self._r

    @property
    def g(self) -> int:
        """Green component."""
        return self._g

    @property
    def b(self) -> int:
        """Blue component."""
        return self._b

    @property
    def a(self) -> int:
        """Alpha component."""
        return self._a

    def to_tuple(self) -> tuple[int, int, int]:
        """Convert to RGB tuple."""
        return (self._r, self._g, self._b)

    def to_array(self) -> np.ndarray[tuple[int, ...], np.dtype[np.uint8]]:
        """Convert to NumPy array."""
        return np.array([self._r, self._g, self._b], dtype=np.uint8)

    def to_hex(self) -> str:
        """Convert to hexadecimal string (#RRGGBB)."""
        return f"#{self._r:02x}{self._g:02x}{self._b:02x}"

    @classmethod
    def from_hex(cls, hex_string: str) -> "Color":
        """Create color from hexadecimal string.

        Args:
            hex_string: Hex color string (e.g., "#FF0000" or "FF0000")

        Returns:
            New Color instance
        """
        hex_string = hex_string.lstrip("#")
        if len(hex_string) != 6:
            raise ValueError(f"Invalid hex color string: {hex_string}")

        r = int(hex_string[0:2], 16)
        g = int(hex_string[2:4], 16)
        b = int(hex_string[4:6], 16)
        return cls(r, g, b)

    @classmethod
    def from_hsv(cls, h: float, s: float, v: float) -> "Color":
        """Create color from HSV values.

        Args:
            h: Hue (0-360)
            s: Saturation (0-1)
            v: Value/brightness (0-1)

        Returns:
            New Color instance
        """
        h = h % 360
        s = max(0.0, min(1.0, s))
        v = max(0.0, min(1.0, v))

        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c

        r_val: float
        g_val: float
        b_val: float

        if h < 60:
            r_val, g_val, b_val = c, x, 0.0
        elif h < 120:
            r_val, g_val, b_val = x, c, 0.0
        elif h < 180:
            r_val, g_val, b_val = 0.0, c, x
        elif h < 240:
            r_val, g_val, b_val = 0.0, x, c
        elif h < 300:
            r_val, g_val, b_val = x, 0.0, c
        else:
            r_val, g_val, b_val = c, 0.0, x

        return cls(int((r_val + m) * 255), int((g_val + m) * 255), int((b_val + m) * 255))

    def lerp(self, other: "Color", t: float) -> "Color":
        """Linear interpolation between two colors.

        Args:
            other: Target color
            t: Interpolation factor (0-1)

        Returns:
            Interpolated color
        """
        t = max(0.0, min(1.0, t))
        r = int(self._r + (other._r - self._r) * t)
        g = int(self._g + (other._g - self._g) * t)
        b = int(self._b + (other._b - self._b) * t)
        return Color(r, g, b)

    def __eq__(self, other: object) -> bool:
        """Check color equality."""
        if not isinstance(other, Color):
            return NotImplemented
        return (self._r, self._g, self._b, self._a) == (other._r, other._g, other._b, other._a)

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Color(r={self._r}, g={self._g}, b={self._b}, a={self._a})"


# Common color constants
BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
YELLOW = Color(255, 255, 0)
CYAN = Color(0, 255, 255)
MAGENTA = Color(255, 0, 255)
