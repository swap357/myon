#!/usr/bin/env python3
"""Example: Turbulent Flow Field - Organic flowing patterns.

Creates flowing, turbulent patterns using multiple layers of Perlin noise
with domain warping. Uses Numba JIT for high performance.
"""

import time
from pathlib import Path

import numpy as np

from myon import Canvas, Color, PerlinNoise

# Create output directory
output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)

# Create canvas
width, height = 1600, 1200
canvas = Canvas(width, height)

print(f"Generating turbulent flow field ({width}x{height})...")
start = time.time()

# Initialize noise generators
noise_warp_x = PerlinNoise(seed=42)
noise_warp_y = PerlinNoise(seed=123)
noise_color = PerlinNoise(seed=456)
noise_detail = PerlinNoise(seed=789)

# Create coordinate grids
scale = 3.0  # Zoom level
x_coords = np.linspace(0, scale, width)
y_coords = np.linspace(0, scale, height)
xx, yy = np.meshgrid(x_coords, y_coords)

print("  Computing domain warping...")
# Domain warping for organic distortion
warp_x = noise_warp_x.octave_noise(xx * 2, yy * 2, octaves=4, persistence=0.5)
warp_y = noise_warp_y.octave_noise(xx * 2, yy * 2, octaves=4, persistence=0.5)

# Apply warping
warped_x = xx + warp_x * 0.3
warped_y = yy + warp_y * 0.3

print("  Computing color field...")
# Main color flow through warped space
flow = noise_color.octave_noise(warped_x * 3, warped_y * 3, octaves=5, persistence=0.6)

print("  Adding fine details...")
# Fine details for texture
detail = noise_detail.octave_noise(xx * 10, yy * 10, octaves=6, persistence=0.4)

print("  Generating colors...")
# Combine flow and detail
combined = flow * 0.8 + detail * 0.2

# Create color mapping with smooth gradients
# Map to hue range for beautiful color transitions
hue = (combined * 180 + 180) % 360  # Cycle through colors

# Saturation varies with detail for visual interest
saturation = np.clip(0.6 + detail * 0.4, 0.3, 1.0)

# Value/brightness varies smoothly
value = np.clip(0.5 + combined * 0.3 + detail * 0.2, 0.4, 1.0)

# Fill canvas with generated colors
for y in range(height):
    if y % 100 == 0:
        print(f"  Processing row {y}/{height}...")
    for x in range(width):
        h = float(hue[y, x])
        s = float(saturation[y, x])
        v = float(value[y, x])

        color = Color.from_hsv(h, s, v)
        canvas.set_pixel(x, y, color)

elapsed = time.time() - start
total_pixels = width * height
print(f"\nGenerated {total_pixels:,} pixels in {elapsed:.2f}s")
print(f"   Performance: {total_pixels / elapsed:,.0f} pixels/second")

# Save result
output_path = output_dir / "turbulent_flow.png"
canvas.save(output_path)
print(f"   Saved to {output_path}")

print("\nTurbulent flow field created successfully!")
