# Contributing to Feluda

Thank you for your interest in contributing to Feluda! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- Basic understanding of Python and machine learning concepts

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/feluda.git
   cd feluda
   ```

3. Install in development mode:
   ```bash
   pip install -e .[dev]
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Guidelines

### Code Style

Feluda uses [Ruff](https://github.com/astral-sh/ruff) for code formatting and linting. The configuration is in `pyproject.toml`.

To format your code:
```bash
ruff format
```

To check for issues:
```bash
ruff check
```

You can run the pre-commit hooks before a commit:
```bash
pre-commit run --all-files
```

### Testing

Run tests to ensure your changes work correctly:

```bash
pytest
```

For integration tests:
```bash
pytest tests/feluda_integration_tests/
```

### Adding New Operators

To add a new operator:

1. Create a new directory in `operators/` with your operator name
2. Create the following files:
   - `__init__.py` - Module initialization
   - `your_operator.py` - Main operator implementation
   - `pyproject.toml` - Operator-specific dependencies
   - `test.py` - Unit tests
   - `README.md` - Documentation

3. Your operator should inherit from `feluda.operator.Operator`

Example structure:
```
operators/
└── your_new_operator/
    ├── __init__.py
    ├── your_new_operator.py
    ├── pyproject.toml
    ├── test.py
    └── README.md
```

## Documentation

### Updating Documentation

When adding new features, please update the documentation:

1. Update docstrings in your code
2. Add examples if applicable
3. Update the API documentation if needed

### Building Documentation

To build the documentation locally:

```bash
cd docs
pip install sphinx sphinx-rtd-theme myst-nb sphinx-copybutton sphinx-design
make html
```

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Update documentation if needed
6. Submit a pull request

### Pull Request Guidelines

- Provide a clear description of the changes
- Include tests for new functionality
- Update documentation if needed
- Follow the existing code style
- Ensure all CI checks pass

## Reporting Issues

When reporting issues, please include:

- Python version
- Feluda version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)

## Code of Conduct

Please read and follow our [Code of Conduct](https://github.com/tattle-made/feluda/blob/main/CODE_OF_CONDUCT.md).

## License

By contributing to Feluda, you agree that your contributions will be licensed under the GNU General Public License v3 (GPLv3).

## Questions?

If you have questions about contributing, please:

- Check the existing documentation
- Search existing issues
- Open a new issue for discussion

Thank you for contributing to Feluda!
