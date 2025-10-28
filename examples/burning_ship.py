#!/usr/bin/env python3
"""Example: Burning Ship Fractal - Stunning mathematical art.

The Burning Ship fractal creates intricate ship-like structures.
Uses Numba JIT for high-performance computation.

Formula: z = (|Re(z)| + i|Im(z)|)² + c
"""

import time
from pathlib import Path

import numpy as np
from numba import njit

from myon import Canvas, Color

# Create output directory
output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)


@njit(cache=True)
def burning_ship_fractal(width, height, xmin, xmax, ymin, ymax, max_iter=256):
    """Compute Burning Ship fractal using Numba JIT."""
    X = np.linspace(xmin, xmax, width)
    Y = np.linspace(ymin, ymax, height)

    iterations = np.zeros((height, width), dtype=np.int32)

    for i in range(height):
        for j in range(width):
            c_real = X[j]
            c_imag = Y[i]

            z_real = 0.0
            z_imag = 0.0

            for n in range(max_iter):
                # Burning Ship: z = (|Re(z)| + i|Im(z)|)² + c
                z_real_abs = abs(z_real)
                z_imag_abs = abs(z_imag)

                z_real_new = z_real_abs * z_real_abs - z_imag_abs * z_imag_abs + c_real
                z_imag = 2 * z_real_abs * z_imag_abs + c_imag
                z_real = z_real_new

                # Check if escaped
                if z_real * z_real + z_imag * z_imag > 4.0:
                    iterations[i, j] = n
                    break

            if iterations[i, j] == 0:
                iterations[i, j] = max_iter

    return iterations


def create_fire_colormap(iterations, max_iter):
    """Create dramatic fire-like coloring."""
    # Smooth coloring with multiple log scales
    smoothed = np.log1p(iterations) / np.log1p(max_iter)

    # Fire palette with dramatic gradients
    r = np.clip(255 * np.power(smoothed, 0.4), 0, 255).astype(np.uint8)
    g = np.clip(255 * np.power(smoothed * 1.5 - 0.2, 2.5), 0, 255).astype(np.uint8)
    b = np.clip(255 * np.power(smoothed * 2.5 - 0.5, 4.0), 0, 255).astype(np.uint8)

    return r, g, b


# Configuration - The classic "ship" view
width, height = 2000, 1600
xmin, xmax = -1.8, -1.7
ymin, ymax = -0.08, 0.0
max_iter = 512

print("Generating Burning Ship Fractal")
print(f"   Resolution: {width}x{height}")
print(f"   Region: [{xmin:.2f}, {xmax:.2f}] x [{ymin:.2f}, {ymax:.2f}]")
print(f"   Max iterations: {max_iter}")

# Compute fractal (Numba JIT accelerated)
print("\nComputing fractal (Numba JIT)...")
start = time.time()
iterations = burning_ship_fractal(width, height, xmin, xmax, ymin, ymax, max_iter)
compute_time = time.time() - start

print(f"   Computed in {compute_time:.2f}s")
print(f"   Performance: {width * height / compute_time:,.0f} pixels/second")

# Generate colors
print("\nGenerating fire palette...")
start = time.time()
r, g, b = create_fire_colormap(iterations, max_iter)
color_time = time.time() - start
print(f"   Colored in {color_time:.2f}s")

# Create canvas
print("\nCreating canvas...")
canvas = Canvas(width, height)

start = time.time()
for y in range(height):
    if y % 200 == 0:
        print(f"   Row {y}/{height}...")
    for x in range(width):
        canvas.set_pixel(x, y, Color(int(r[y, x]), int(g[y, x]), int(b[y, x])))

fill_time = time.time() - start

# Save result
output_path = output_dir / "burning_ship.png"
canvas.save(output_path)

# Summary
total_time = compute_time + color_time + fill_time
print(f"\n{'='*60}")
print("Burning Ship Fractal Complete!")
print(f"{'='*60}")
print(f"   Total time: {total_time:.2f}s")
print(f"   - Computation: {compute_time:.2f}s ({compute_time/total_time*100:.1f}%)")
print(f"   - Coloring: {color_time:.2f}s ({color_time/total_time*100:.1f}%)")
print(f"   - Canvas fill: {fill_time:.2f}s ({fill_time/total_time*100:.1f}%)")
print(f"   Overall rate: {width * height / total_time:,.0f} pixels/second")
print(f"\n   Saved to: {output_path}")
print(f"{'='*60}")
print("\nThe 'ship' structure is visible in this region!")
print("   Try adjusting xmin, xmax, ymin, ymax for different views.")
