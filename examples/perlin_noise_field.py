#!/usr/bin/env python3
"""Example: Create a Perlin noise field visualization.

This example uses vectorized NumPy operations with Numba JIT-compiled
functions for high performance.
"""

import time
from pathlib import Path

import numpy as np

from myon import Canvas, Color, PerlinNoise

# Create output directory
output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)

# Create canvas
width, height = 800, 600
canvas = Canvas(width, height)

# Initialize Perlin noise
noise = PerlinNoise(seed=42)

# Generate noise field using vectorized operations (FAST!)
print(f"Generating {width}x{height} noise field...")
start = time.time()

scale = 0.01  # Scale factor for noise coordinates

# Create coordinate grids (vectorized approach)
x_coords = np.arange(width) * scale
y_coords = np.arange(height) * scale
xx, yy = np.meshgrid(x_coords, y_coords)

# Generate noise for ALL pixels at once using Numba JIT
values = noise.octave_noise(xx, yy, octaves=4, persistence=0.5)

# Map noise values from [-1, 1] to [0, 255]
gray_values = ((values + 1) * 127.5).astype(np.uint8)

# Fill canvas with noise values
for y in range(height):
    for x in range(width):
        gray = int(gray_values[y, x])
        canvas.set_pixel(x, y, Color(gray, gray, gray))

elapsed = time.time() - start
print(f"Generated in {elapsed:.2f}s ({width * height / elapsed:,.0f} pixels/sec)")

# Save result
canvas.save(output_dir / "noise_field.png")
print(f"Saved noise field to {output_dir / 'noise_field.png'}")
