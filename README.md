# myon

A Python library for generative art, designed for clarity, performance, and creative expression.

## Features

- **Canvas**: Simple and powerful drawing canvas with pixel-level control
- **Color**: Comprehensive color handling with RGB, HSV, and hex support
- **Noise**: Perlin noise implementation for organic patterns and textures
- **Utils**: Helper functions for common generative art operations

## Installation

### From PyPI

```bash
pip install myon
```

### For Development

```bash
# Clone the repository
git clone https://github.com/swap357/myon.git
cd myon

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

## Quick Start

### Create a Simple Gradient

```python
from myon import Canvas, Color

# Create a canvas
canvas = Canvas(800, 600)

# Define colors
blue = Color(0, 100, 200)
red = Color(200, 50, 50)

# Draw a gradient
for x in range(canvas.width):
    t = x / canvas.width
    color = blue.lerp(red, t)
    for y in range(canvas.height):
        canvas.set_pixel(x, y, color)

# Save the result
canvas.save("gradient.png")
```

### Generate Perlin Noise

```python
from myon import Canvas, Color, PerlinNoise
from myon.utils import map_range

# Create canvas and noise generator
canvas = Canvas(800, 600)
noise = PerlinNoise(seed=42)

# Generate noise field
scale = 0.01
for y in range(canvas.height):
    for x in range(canvas.width):
        value = noise.octave_noise(x * scale, y * scale, octaves=4)
        gray = int(map_range(value, -1, 1, 0, 255))
        canvas.set_pixel(x, y, Color(gray, gray, gray))

canvas.save("noise.png")
```

## Examples

Check out the `examples/` directory for more inspiration:

- `simple_gradient.py` - Basic color gradients
- `perlin_noise_field.py` - Grayscale noise patterns
- `colorful_noise.py` - Multi-layered colorful noise using HSV

Run examples:

```bash
python examples/simple_gradient.py
python examples/perlin_noise_field.py
python examples/colorful_noise.py
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/myon --cov-report=html

# Run specific test file
pytest tests/test_canvas.py
```


## Project Structure

```
myon/
├── src/
│   └── myon/
│       ├── __init__.py      # Package exports
│       ├── canvas.py        # Canvas implementation
│       ├── color.py         # Color handling
│       ├── noise.py         # Noise generation
│       └── utils.py         # Utility functions
├── tests/
│   ├── test_canvas.py
│   ├── test_color.py
│   ├── test_noise.py
│   └── test_utils.py
├── examples/
│   ├── simple_gradient.py
│   ├── perlin_noise_field.py
│   └── colorful_noise.py
├── pyproject.toml           # Project configuration
├── README.md
└── LICENSE
```

## API Reference

### Canvas

```python
Canvas(width: int, height: int, background: Optional[Color] = None)
```

Main drawing surface for generative art.

**Methods:**
- `set_pixel(x, y, color)` - Set a single pixel
- `get_pixel(x, y)` - Get pixel color
- `fill(color)` - Fill entire canvas
- `clear()` - Clear to background color
- `save(filepath)` - Save as image file

### Color

```python
Color(r: int, g: int, b: int, a: int = 255)
```

Represents colors in RGB format.

**Methods:**
- `from_hex(hex_string)` - Create from hex string
- `from_hsv(h, s, v)` - Create from HSV values
- `lerp(other, t)` - Interpolate between colors
- `to_hex()` - Convert to hex string

### PerlinNoise

```python
PerlinNoise(seed: int = 0)
```

Generate smooth, organic noise patterns. Uses Numba JIT compilation for high performance.

**Methods:**
- `noise(x, y)` - Generate 2D Perlin noise (supports scalars and arrays)
- `octave_noise(x, y, octaves, persistence, lacunarity)` - Multi-layered noise

**Performance Note:** The first call to `noise()` will be slower due to JIT compilation (~0.3s overhead), but subsequent calls are very fast (4M+ pixels/second with vectorized operations).

### Utilities

Helper functions for common operations:

- `seed(value)` - Set random seed
- `map_range(value, in_min, in_max, out_min, out_max)` - Map value between ranges
- `constrain(value, min_val, max_val)` - Clamp value to range
- `lerp(start, stop, amount)` - Linear interpolation
- `distance(x1, y1, x2, y2)` - Euclidean distance

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Inspired by Processing, p5.js, and the generative art community.
