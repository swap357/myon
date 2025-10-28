# Setup Guide

Quick guide to get started with Myon development.

## Initial Setup

1. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install in development mode:**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Verify installation:**
   ```bash
   python -c "import myon; print(myon.__version__)"
   ```

## Development Workflow

### Running Tests
```bash
# Quick test
pytest

# With coverage
pytest --cov=src/myon --cov-report=html
open htmlcov/index.html  # View coverage report
```

### Code Quality
```bash
# Format code
make format

# Run linter
make lint

# Type checking
make type-check

# All at once
make format lint type-check test
```

### Running Examples
```bash
# Make sure you're in the virtual environment
python examples/simple_gradient.py
python examples/perlin_noise_field.py
python examples/colorful_noise.py

# Check output/
ls examples/output/
```

## Building for PyPI

### Test Build
```bash
# Build package
make build

# Install from built wheel
pip install dist/myon-0.1.0-py3-none-any.whl
```

### Publishing to PyPI

1. **Update version** in `pyproject.toml`

2. **Update CHANGELOG.md** with changes

3. **Create a git tag:**
   ```bash
   git tag -a v0.1.0 -m "Release version 0.1.0"
   git push origin v0.1.0
   ```

4. **Build and publish:**
   ```bash
   # Test on TestPyPI first
   python -m build
   twine upload --repository testpypi dist/*
   
   # Then publish to real PyPI
   twine upload dist/*
   ```

## Configuration Files

- `pyproject.toml` - Project metadata and tool configuration
- `.gitignore` - Files to ignore in git
- `.python-version` - Python version for pyenv
- `Makefile` - Development shortcuts
- `.github/workflows/` - CI/CD configuration

## Project Structure

```
myon/
├── src/myon/              # Source code
│   ├── __init__.py        # Package exports
│   ├── canvas.py          # Canvas implementation
│   ├── color.py           # Color handling
│   ├── noise.py           # Noise generation
│   └── utils.py           # Utilities
├── tests/                 # Test suite
├── examples/              # Example scripts
├── .github/workflows/     # CI/CD
└── pyproject.toml         # Project config
```

## Tips

- Use `make help` to see all available commands
- Keep test coverage above 90%
- Run `make format lint type-check test` before committing
- Follow semantic versioning (MAJOR.MINOR.PATCH)

