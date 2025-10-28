"""Tests for utility functions."""

import random

import numpy as np

from myon.utils import constrain, distance, lerp, map_range, seed


def test_seed():
    """Test that seed function sets random seeds."""
    seed(42)

    py_val1 = random.random()
    np_val1 = np.random.random()

    seed(42)

    py_val2 = random.random()
    np_val2 = np.random.random()

    assert py_val1 == py_val2
    assert np_val1 == np_val2


def test_map_range():
    """Test value mapping between ranges."""
    # Map 5 from [0,10] to [0,100]
    result = map_range(5, 0, 10, 0, 100)
    assert result == 50.0

    # Map 0.5 from [0,1] to [100,200]
    result = map_range(0.5, 0, 1, 100, 200)
    assert result == 150.0


def test_map_range_with_clamping():
    """Test map_range with clamping enabled."""
    # Value outside input range, clamped to output range
    result = map_range(15, 0, 10, 0, 100, clamp=True)
    assert result == 100.0

    result = map_range(-5, 0, 10, 0, 100, clamp=True)
    assert result == 0.0


def test_constrain():
    """Test value constraining."""
    assert constrain(5, 0, 10) == 5
    assert constrain(-5, 0, 10) == 0
    assert constrain(15, 0, 10) == 10


def test_lerp():
    """Test linear interpolation."""
    assert lerp(0, 10, 0.0) == 0
    assert lerp(0, 10, 1.0) == 10
    assert lerp(0, 10, 0.5) == 5
    assert lerp(100, 200, 0.25) == 125


def test_distance():
    """Test Euclidean distance calculation."""
    # Distance between (0,0) and (3,4) should be 5
    assert distance(0, 0, 3, 4) == 5.0

    # Distance from point to itself is 0
    assert distance(5, 5, 5, 5) == 0.0

    # Test with floating point coordinates
    d = distance(0, 0, 1, 1)
    assert abs(d - np.sqrt(2)) < 1e-10
