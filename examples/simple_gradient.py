#!/usr/bin/env python3
"""Example: Create a simple gradient image."""

from pathlib import Path

from myon import Canvas, Color

# Create output directory
output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)

# Create canvas
canvas = Canvas(800, 600)

# Create gradient from blue to red
blue = Color(0, 100, 200)
red = Color(200, 50, 50)

# Draw horizontal gradient
for x in range(canvas.width):
    t = x / canvas.width
    color = blue.lerp(red, t)

    for y in range(canvas.height):
        canvas.set_pixel(x, y, color)

# Save result
canvas.save(output_dir / "gradient.png")
print(f"Saved gradient to {output_dir / 'gradient.png'}")
