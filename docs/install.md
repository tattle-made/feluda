# Installation

## Prerequisites

Feluda requires Python 3.10 or higher.

## Basic Installation

Install Feluda using pip:

```bash
pip install feluda
```

## Optional Dependencies

Feluda supports optional dependencies for different media types:

### Audio Processing

```bash
pip install feluda[audio]
```

### Video Processing

```bash
pip install feluda[video]
```

### Image Processing

```bash
pip install feluda[image]
```

### All Dependencies

```bash
pip install feluda[all]
```

## Development Installation

For development, clone the repository and install in editable mode:

```bash
git clone https://github.com/tattle-made/feluda.git
cd feluda
pip install -e .
```

### Development Dependencies

```bash
pip install -e .[dev]
```

## Operator Dependencies

Some operators may require additional dependencies. Check the individual operator documentation for specific requirements.

## Verification

After installation, you can verify it works:

```python
import feluda
print(feluda.__version__)
```

## Getting Help

- Check the [examples](examples/README) for usage patterns
- Review the [API documentation](api/feluda) for detailed information
- Open an issue on [GitHub](https://github.com/tattle-made/feluda/issues) for bugs.
