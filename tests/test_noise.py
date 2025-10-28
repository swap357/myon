"""Tests for noise generation."""

import numpy as np

from myon.noise import PerlinNoise


def test_perlin_noise_initialization():
    """Test Perlin noise generator initialization."""
    noise = PerlinNoise(seed=42)
    assert noise._seed == 42


def test_perlin_noise_single_value():
    """Test generating single noise value."""
    noise = PerlinNoise(seed=42)
    value = noise.noise(0.5, 0.5)

    assert isinstance(value, float)
    assert -1.0 <= value <= 1.0


def test_perlin_noise_array():
    """Test generating noise for arrays."""
    noise = PerlinNoise(seed=42)
    x = np.linspace(0, 10, 100)
    y = np.linspace(0, 10, 100)

    values = noise.noise(x, y)

    assert values.shape == (100,)
    assert np.all(values >= -1.0)
    assert np.all(values <= 1.0)


def test_perlin_noise_reproducibility():
    """Test that same seed produces same results."""
    noise1 = PerlinNoise(seed=42)
    noise2 = PerlinNoise(seed=42)

    value1 = noise1.noise(1.5, 2.5)
    value2 = noise2.noise(1.5, 2.5)

    assert value1 == value2


def test_perlin_noise_different_seeds():
    """Test that different seeds produce different results."""
    noise1 = PerlinNoise(seed=42)
    noise2 = PerlinNoise(seed=43)

    value1 = noise1.noise(1.5, 2.5)
    value2 = noise2.noise(1.5, 2.5)

    assert value1 != value2


def test_octave_noise():
    """Test multi-octave noise generation."""
    noise = PerlinNoise(seed=42)
    value = noise.octave_noise(1.5, 2.5, octaves=4)

    assert isinstance(value, float)
    assert -1.0 <= value <= 1.0


def test_octave_noise_parameters():
    """Test octave noise with different parameters."""
    noise = PerlinNoise(seed=42)

    # More octaves should create more detailed noise
    value1 = noise.octave_noise(1.5, 2.5, octaves=1)
    value2 = noise.octave_noise(1.5, 2.5, octaves=8)

    assert isinstance(value1, float)
    assert isinstance(value2, float)

    # Different persistence values should generally produce different patterns
    # Test across multiple points to ensure they differ
    x_coords = [1.5, 2.0, 2.5, 3.0]
    y_coords = [2.5, 3.0, 3.5, 4.0]

    values_low_persistence = [
        noise.octave_noise(x, y, octaves=4, persistence=0.3)
        for x, y in zip(x_coords, y_coords, strict=False)
    ]
    values_high_persistence = [
        noise.octave_noise(x, y, octaves=4, persistence=0.7)
        for x, y in zip(x_coords, y_coords, strict=False)
    ]

    # At least some values should differ
    assert values_low_persistence != values_high_persistence


def test_noise_continuity():
    """Test that noise values change smoothly."""
    noise = PerlinNoise(seed=42)

    # Generate values at close coordinates
    values = [noise.noise(i * 0.01, 0.5) for i in range(10)]

    # Calculate differences between consecutive values
    diffs = [abs(values[i + 1] - values[i]) for i in range(len(values) - 1)]

    # All differences should be relatively small (continuity)
    assert all(d < 0.1 for d in diffs)
