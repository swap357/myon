# Myon Examples

This directory contains example scripts demonstrating the capabilities of Myon for generative art.

## Performance Note

All examples use **Numba JIT-compiled functions** for high performance. The first run will include a brief compilation overhead (~0.2-0.3s), but subsequent operations are extremely fast.

## Examples

### 1. Simple Gradient (`simple_gradient.py`)

Creates a basic horizontal color gradient using color interpolation.

```bash
python examples/simple_gradient.py
```

**Concepts:** Canvas creation, color interpolation, pixel manipulation

---

### 2. Perlin Noise Field (`perlin_noise_field.py`)

Generates a grayscale Perlin noise field using vectorized operations.

```bash
python examples/perlin_noise_field.py
```

**Performance:** ~383,000 pixels/second (800x600)
**Concepts:** 
- Vectorized NumPy operations with meshgrid
- Numba JIT-compiled noise generation
- Octave noise for organic patterns

---

### 3. Colorful Noise (`colorful_noise.py`)

Creates vibrant, organic color patterns by combining multiple noise layers in HSV color space.

```bash
python examples/colorful_noise.py
```

**Performance:** ~80,000 pixels/second (800x600 with 3 noise layers)
**Concepts:**
- Multiple independent noise generators
- HSV color space for artistic control
- Layered noise at different frequencies
- Vectorized noise computation

---

### 4. Turbulent Flow (`organic_flow.py`)

Creates flowing, turbulent patterns using domain warping with multiple noise layers.

```bash
python examples/organic_flow.py
```

**Performance:** ~400,000 pixels/second (1600x1200)
**Concepts:**
- Domain warping for organic distortion
- Multi-scale noise combination
- Advanced color mapping in HSV space
- Turbulent flow simulation

---

### 5. Burning Ship Fractal (`burning_ship.py`)

Stunning mathematical fractal with ship-like structures.

```bash
python examples/burning_ship.py
```

**Performance:** ~2.4M pixels/second (2000x1600, computation only)
**Concepts:**
- Complex dynamics: z = (|Re(z)| + i|Im(z)|)² + c
- Escape-time algorithm
- Numba JIT for high performance
- Fire palette coloring

---

### 6. Julia Set (`julia_set.py`)

Classic Julia set fractals with multiple presets.

```bash
python examples/julia_set.py
```

**Performance:** ~4.5M pixels/second (1600x1600)
**Concepts:**
- Complex dynamics: f(z) = z² + c
- Multiple famous Julia sets (dragon, dendrite, spiral, etc.)
- Smooth coloring with logarithmic scaling
- Custom color palettes

## Performance Tips

### 1. Use Vectorized Operations

Instead of loops:
```python
# SLOW: Loop over each pixel
for y in range(height):
    for x in range(width):
        value = noise.noise(x * scale, y * scale)
```

Use vectorized operations:
```python
# FAST: Compute all at once
xx, yy = np.meshgrid(x_coords, y_coords)
values = noise.noise(xx, yy)  # All pixels at once!
```

### 2. Pre-warm JIT Compiler

For interactive applications:
```python
noise = PerlinNoise(seed=42)
# Warm up compiler during initialization
_ = noise.noise(0.0, 0.0)
_ = noise.octave_noise(0.0, 0.0, octaves=4)
# Now all subsequent calls are fast!
```

### 3. Reuse Noise Generators

Create once, use many times:
```python
# GOOD: Create once
noise = PerlinNoise(seed=42)
for frame in range(100):
    values = noise.noise(...)  # Fast every time

# BAD: Don't recreate each time
for frame in range(100):
    noise = PerlinNoise(seed=42)  # Unnecessary overhead
    values = noise.noise(...)
```

## Generated Outputs

All examples save their output to the `examples/output/` directory:

- `gradient.png` - Simple color gradient
- `noise_field.png` - Grayscale Perlin noise
- `colorful_noise.png` - Multi-channel HSV noise art
- `turbulent_flow.png` - Domain-warped turbulent patterns
- `burning_ship.png` - Burning Ship fractal (2000x1600)
- `julia_dragon.png` - Julia set fractal (and other variants)

## Requirements

All dependencies are installed with Myon:
- NumPy >= 1.24.0
- Numba >= 0.58.0 (for JIT compilation)
- Pillow >= 10.0.0 (for image I/O)

## Performance Summary

| Example | Resolution | Pixels | Time | Rate |
|---------|-----------|--------|------|------|
| Simple Gradient | 800x600 | 480K | ~0.1s | N/A |
| Perlin Noise | 800x600 | 480K | ~1.3s | 383K/s |
| Colorful Noise | 800x600 | 480K | ~6.0s | 80K/s |
| Turbulent Flow | 1600x1200 | 1.92M | ~5.0s | 400K/s |
| Burning Ship | 2000x1600 | 3.2M | ~1.4s | 2.4M/s |
| Julia Set | 1600x1600 | 2.56M | ~0.6s | 4.5M/s |

*Note: Times include JIT compilation on first run. Subsequent runs are faster.*

## Creating Your Own

Use these examples as templates for your own generative art:

1. **Start simple** - Begin with `simple_gradient.py`
2. **Add noise** - Experiment with `perlin_noise_field.py`
3. **Layer complexity** - Combine multiple noise layers like `colorful_noise.py`
4. **Scale up** - Generate high-resolution art like `organic_flow.py`

## Resources

- [Main README](../README.md) - Full documentation
- [PERFORMANCE.md](../PERFORMANCE.md) - Detailed performance guide
- [API Reference](../README.md#api-reference) - Function documentation

Happy creating!

