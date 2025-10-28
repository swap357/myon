"""Myon: A Python library for generative art."""

from myon.canvas import Canvas
from myon.color import Color
from myon.noise import PerlinNoise
from myon.utils import seed

__version__ = "0.1.0"
__all__ = ["Canvas", "Color", "PerlinNoise", "seed"]
