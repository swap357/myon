"""Noise generation module for organic patterns with Numba JIT optimization."""

from typing import Any

import numpy as np
from numba import njit  # type: ignore[import-untyped]


@njit(cache=True)
def _fade(t: Any) -> Any:  # type: ignore[misc]
    """Fade function for smooth interpolation."""
    return t * t * t * (t * (t * 6 - 15) + 10)


@njit(cache=True)
def _lerp(t: Any, a: Any, b: Any) -> Any:  # type: ignore[misc]
    """Linear interpolation."""
    return a + t * (b - a)


@njit(cache=True)
def _grad_2d(hash_val: Any, x: Any, y: Any) -> Any:  # type: ignore[misc]
    """Gradient function for 2D (scalar version)."""
    h = hash_val & 3
    if h == 0:
        return x + y
    elif h == 1:
        return -x + y
    elif h == 2:
        return x - y
    else:
        return -x - y


@njit(cache=True)
def _perlin_noise_2d_scalar(x: Any, y: Any, perm: Any) -> Any:  # type: ignore[misc]
    """Core Perlin noise computation for scalar inputs (JIT compiled).

    Args:
        x: X coordinate
        y: Y coordinate
        perm: Permutation table (length 512)

    Returns:
        Noise value in range [-1, 1]
    """
    # Find unit grid cell containing point
    xi = int(np.floor(x)) & 255
    yi = int(np.floor(y)) & 255

    # Get relative x, y within cell
    xf = x - np.floor(x)
    yf = y - np.floor(y)

    # Compute fade curves
    u = _fade(xf)
    v = _fade(yf)

    # Hash coordinates of the 4 cube corners
    aa = perm[perm[xi] + yi]
    ab = perm[perm[xi] + yi + 1]
    ba = perm[perm[xi + 1] + yi]
    bb = perm[perm[xi + 1] + yi + 1]

    # Calculate gradient values
    g1 = _grad_2d(aa, xf, yf)
    g2 = _grad_2d(ba, xf - 1, yf)
    g3 = _grad_2d(ab, xf, yf - 1)
    g4 = _grad_2d(bb, xf - 1, yf - 1)

    # Interpolate
    x1 = _lerp(u, g1, g2)
    x2 = _lerp(u, g3, g4)

    return _lerp(v, x1, x2)


@njit(cache=True)
def _perlin_noise_2d_array(x: Any, y: Any, perm: Any) -> Any:  # type: ignore[misc]
    """Core Perlin noise computation for array inputs (JIT compiled).

    Args:
        x: X coordinate(s) as array
        y: Y coordinate(s) as array
        perm: Permutation table (length 512)

    Returns:
        Noise value(s) in range [-1, 1]
    """
    # Ensure arrays
    x_flat = x.flatten()
    y_flat = y.flatten()
    result = np.empty(len(x_flat), dtype=np.float64)

    for i in range(len(x_flat)):
        result[i] = _perlin_noise_2d_scalar(x_flat[i], y_flat[i], perm)

    return result.reshape(x.shape)


@njit(cache=True)
def _octave_noise_2d_scalar(  # type: ignore[misc]
    x: Any, y: Any, perm: Any, octaves: Any, persistence: Any, lacunarity: Any
) -> Any:
    """Multi-octave Perlin noise for scalar inputs (JIT compiled).

    Args:
        x: X coordinate
        y: Y coordinate
        perm: Permutation table
        octaves: Number of noise layers to combine
        persistence: Amplitude multiplier per octave
        lacunarity: Frequency multiplier per octave

    Returns:
        Combined noise value
    """
    total = 0.0
    amplitude = 1.0
    frequency = 1.0
    max_value = 0.0

    for _ in range(octaves):
        total += _perlin_noise_2d_scalar(x * frequency, y * frequency, perm) * amplitude
        max_value += amplitude
        amplitude *= persistence
        frequency *= lacunarity

    return total / max_value


@njit(cache=True)
def _octave_noise_2d_array(  # type: ignore[misc]
    x: Any, y: Any, perm: Any, octaves: Any, persistence: Any, lacunarity: Any
) -> Any:
    """Multi-octave Perlin noise for array inputs (JIT compiled).

    Args:
        x: X coordinate(s)
        y: Y coordinate(s)
        perm: Permutation table
        octaves: Number of noise layers to combine
        persistence: Amplitude multiplier per octave
        lacunarity: Frequency multiplier per octave

    Returns:
        Combined noise value(s)
    """
    x_flat = x.flatten()
    y_flat = y.flatten()
    result = np.empty(len(x_flat), dtype=np.float64)

    for i in range(len(x_flat)):
        result[i] = _octave_noise_2d_scalar(
            x_flat[i], y_flat[i], perm, octaves, persistence, lacunarity
        )

    return result.reshape(x.shape)


class PerlinNoise:
    """Simple Perlin noise implementation for generative art.

    This implementation uses Numba JIT compilation for high performance.
    The first call to noise() will trigger JIT compilation, which may take
    a moment, but subsequent calls will be very fast.
    """

    def __init__(self, seed: int = 0) -> None:
        """Initialize Perlin noise generator.

        Args:
            seed: Random seed for reproducibility
        """
        self._seed = seed
        rng = np.random.default_rng(seed)

        # Generate permutation table
        perm = np.arange(256, dtype=np.int32)
        rng.shuffle(perm)
        self._perm = np.concatenate([perm, perm])

    def noise(self, x: float | np.ndarray, y: float | np.ndarray) -> float | np.ndarray:
        """Generate 2D Perlin noise.

        Args:
            x: X coordinate(s)
            y: Y coordinate(s)

        Returns:
            Noise value(s) in range [-1, 1]
        """
        # Handle scalar inputs
        if isinstance(x, int | float) and isinstance(y, int | float):
            return _perlin_noise_2d_scalar(float(x), float(y), self._perm)

        # Handle array inputs
        x_arr = np.asarray(x, dtype=np.float64)
        y_arr = np.asarray(y, dtype=np.float64)
        return _perlin_noise_2d_array(x_arr, y_arr, self._perm)

    def octave_noise(
        self,
        x: float | np.ndarray,
        y: float | np.ndarray,
        octaves: int = 4,
        persistence: float = 0.5,
        lacunarity: float = 2.0,
    ) -> float | np.ndarray:
        """Generate multi-octave Perlin noise (fractal noise).

        Args:
            x: X coordinate(s)
            y: Y coordinate(s)
            octaves: Number of noise layers to combine
            persistence: Amplitude multiplier per octave (0-1)
            lacunarity: Frequency multiplier per octave (>1)

        Returns:
            Combined noise value(s)
        """
        # Handle scalar inputs
        if isinstance(x, int | float) and isinstance(y, int | float):
            return _octave_noise_2d_scalar(
                float(x), float(y), self._perm, octaves, persistence, lacunarity
            )

        # Handle array inputs
        x_arr = np.asarray(x, dtype=np.float64)
        y_arr = np.asarray(y, dtype=np.float64)
        return _octave_noise_2d_array(x_arr, y_arr, self._perm, octaves, persistence, lacunarity)
