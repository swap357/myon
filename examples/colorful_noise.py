#!/usr/bin/env python3
"""Example: Create colorful noise patterns using HSV color space.

This example uses vectorized NumPy operations with Numba JIT-compiled
functions for high performance. Multiple noise layers create rich,
organic color patterns.
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

print(f"Generating colorful {width}x{height} noise field...")
start = time.time()

# Initialize Perlin noise generators for different color channels
noise_h = PerlinNoise(seed=100)
noise_s = PerlinNoise(seed=200)
noise_v = PerlinNoise(seed=300)

# Generate colorful noise field using vectorized operations
scale = 0.005

# Create coordinate grids
x_coords = np.arange(width) * scale
y_coords = np.arange(height) * scale
xx, yy = np.meshgrid(x_coords, y_coords)

# Generate noise for ALL pixels at once using Numba JIT (FAST!)
print("  Computing hue channel...")
h_values = noise_h.octave_noise(xx, yy, octaves=3)
h_values = (h_values + 1) * 180  # Map [-1, 1] to [0, 360]

print("  Computing saturation channel...")
s_values = noise_s.octave_noise(xx * 2, yy * 2, octaves=2)
s_values = s_values * 0.25 + 0.75  # Map [-1, 1] to [0.5, 1.0]

print("  Computing value/brightness channel...")
v_values = noise_v.octave_noise(xx * 1.5, yy * 1.5, octaves=2)
v_values = v_values * 0.2 + 0.8  # Map [-1, 1] to [0.6, 1.0]

# Convert HSV to RGB and fill canvas
print("  Converting to RGB and filling canvas...")
for y in range(height):
    for x in range(width):
        h = float(h_values[y, x])
        s = float(np.clip(s_values[y, x], 0, 1))
        v = float(np.clip(v_values[y, x], 0, 1))

        # Create color from HSV
        color = Color.from_hsv(h, s, v)
        canvas.set_pixel(x, y, color)

elapsed = time.time() - start
print(f"Generated in {elapsed:.2f}s ({width * height / elapsed:,.0f} pixels/sec)")

# Save result
canvas.save(output_dir / "colorful_noise.png")
print(f"Saved colorful noise to {output_dir / 'colorful_noise.png'}")
