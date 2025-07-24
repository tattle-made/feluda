# Feluda Documentation

This directory contains the documentation for Feluda, built with Sphinx and MyST-NB.

## Building the Documentation

### Prerequisites

Install the documentation dependencies:

```bash
uv pip install -e ".[dev]"
```

### Build Commands

From the `docs/` directory:

```bash
# Clean build directory
make clean

# Build HTML documentation
make html
```

### Viewing the Documentation

After building with `make html`, you can view the documentation by opening `docs/_build/html/index.html` in your web browser.

## Documentation Structure

- `index.md` - Main documentation page
- `install.md` - Installation guide
- `quickstart.md` - Quick start guide
- `contributing.md` - Contributing guidelines
- `api/` - API documentation
  - `feluda.md` - Core Feluda API
  - `operators.md` - Operators API
- `examples/` - Example notebooks
  - `01_plot_tsne_videos.md` - t-SNE visualization example
  - `02_plot_cluster_videos.md` - Clustering example
  - `03_classify_video_zero_shot.md` - Zero-shot classification example

## Configuration

The documentation is configured in `conf.py` with the following key features:

- **AutoDoc**: Automatically generates API documentation from docstrings
- **MyST-NB**: Executes and displays Jupyter notebooks
- **Read the Docs Theme**: Clean, responsive theme
- **Copy Button**: Easy code copying
- **Design Components**: Enhanced UI components

## Adding New Documentation

### Adding API Documentation

1. Add docstrings to your Python code
2. Create a new `.md` file in the appropriate directory
3. Use `{eval-rst}` blocks with `.. automodule::` directives

### Adding Examples

1. Create a Jupyter notebook in `examples/`
2. Create a corresponding `.md` file with `{nb-exec}` directive
3. Add the example to the main index

### Adding General Pages

1. Create a new `.md` file
2. Add it to the appropriate toctree in `index.md`
3. Use MyST Markdown syntax for enhanced features
