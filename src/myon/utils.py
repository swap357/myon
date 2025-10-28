"""Utility functions for generative art."""

import random

import numpy as np


def seed(value: int) -> None:
    """Set random seed for reproducible results.

    Sets seeds for both Python's random module and NumPy.

    Args:
        value: Seed value
    """
    random.seed(value)
    np.random.seed(value)


def map_range(
    value: float, in_min: float, in_max: float, out_min: float, out_max: float, clamp: bool = False
) -> float:
    """Map a value from one range to another.

    Args:
        value: Input value
        in_min: Minimum of input range
        in_max: Maximum of input range
        out_min: Minimum of output range
        out_max: Maximum of output range
        clamp: Whether to clamp result to output range

    Returns:
        Mapped value
    """
    result = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    if clamp:
        result = max(out_min, min(out_max, result))

    return result


def constrain(value: float, min_val: float, max_val: float) -> float:
    """Constrain a value to a range.

    Args:
        value: Value to constrain
        min_val: Minimum value
        max_val: Maximum value

    Returns:
        Constrained value
    """
    return max(min_val, min(max_val, value))


def lerp(start: float, stop: float, amount: float) -> float:
    """Linear interpolation between two values.

    Args:
        start: Starting value
        stop: Ending value
        amount: Interpolation amount (0-1)

    Returns:
        Interpolated value
    """
    return start + (stop - start) * amount


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate Euclidean distance between two points.

    Args:
        x1: X coordinate of first point
        y1: Y coordinate of first point
        x2: X coordinate of second point
        y2: Y coordinate of second point

    Returns:
        Distance between points
    """
    return float(np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
