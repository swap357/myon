# Contributing to Myon

Thank you for your interest in contributing to Myon! This document provides guidelines and information for contributors.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/myon.git`
3. Set up development environment:
   ```bash
   cd myon
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

## Development Principles

Myon follows these design principles:

1. **Make Illegal States Unrepresentable** - Encode invariants in types
2. **Minimal Surface, Maximal Clarity** - Keep APIs simple and obvious
3. **DRY & Orthogonality** - Each component has one clear purpose
4. **Code is for Readers** - Optimize for understanding
5. **Iterative Design** - Make it easy to evolve
6. **Abstraction with Taste** - Abstract when it reduces complexity

## Contribution Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Write clear, documented code
- Follow existing code style
- Add tests for new functionality
- Update documentation as needed

### 3. Run Quality Checks

```bash
# Format code
make format

# Check linting
make lint

# Type check
make type-check

# Run tests
make test
```

All checks must pass before submitting.

### 4. Commit Your Changes

Write clear commit messages:

```
feat: add circle drawing to canvas

- Implement circle drawing using midpoint algorithm
- Add tests for circle drawing
- Update documentation with examples
```

Commit prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `chore:` - Maintenance tasks

### 5. Submit a Pull Request

1. Push to your fork
2. Open a pull request against `main`
3. Describe your changes clearly
4. Link any related issues
5. Wait for review and address feedback

## Code Style

### Python Style

- Follow PEP 8
- Use type hints for all functions
- Maximum line length: 100 characters
- Use descriptive variable names

### Documentation

- Docstrings for all public functions/classes
- Use Google-style docstrings
- Include examples in docstrings when helpful

Example:
```python
def my_function(x: int, y: int) -> int:
    """Calculate something useful.
    
    Args:
        x: First input value
        y: Second input value
        
    Returns:
        The computed result
        
    Examples:
        >>> my_function(2, 3)
        5
    """
    return x + y
```

### Testing

- Write tests for all new functionality
- Aim for >90% code coverage
- Use descriptive test names
- Follow AAA pattern: Arrange, Act, Assert

Example:
```python
def test_color_creation():
    """Test that colors are created with correct values."""
    # Arrange
    r, g, b = 100, 150, 200
    
    # Act
    color = Color(r, g, b)
    
    # Assert
    assert color.r == r
    assert color.g == g
    assert color.b == b
```

## Adding New Features

### Core Modules

When adding to core modules (`canvas.py`, `color.py`, etc.):

1. Discuss in an issue first
2. Ensure it fits the library's purpose
3. Keep API minimal and clear
4. Add comprehensive tests
5. Document thoroughly

### Examples

New examples are always welcome!

1. Create a new file in `examples/`
2. Add a clear docstring explaining what it does
3. Use `output/` directory for generated images
4. Keep examples focused and educational

## Reporting Issues

### Bug Reports

Include:
- Python version
- Operating system
- Minimal code to reproduce
- Expected vs actual behavior
- Error messages/stack traces

### Feature Requests

Include:
- Clear description of the feature
- Use cases and examples
- How it fits with existing functionality
- Willingness to implement it yourself

## Questions?

- Open a discussion on GitHub
- Check existing issues and PRs
- Read the documentation thoroughly

Thank you for contributing to Myon!

