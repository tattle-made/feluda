# Pyproject.toml Best Practices for Python Libraries

This document outlines the best practices for writing pyproject.toml files when building Python libraries, with specific focus on Feluda's requirements and tooling.

## Absolute Minimum Required Sections

### 1. [build-system]

This section is mandatory and specifies the build backend requirements:

```toml
[build-system]
requires = ["hatchling"]  # For Hatch build system
build-backend = "hatchling.build"
```

### 2. [project]

This section contains the core metadata about your project. The minimum required fields are:

```toml
[project]
name = "your-package-name"
version = "0.1.0"
requires-python = ">=3.10"  # Minimum Python version
```

## Recommended Project Metadata

### 1. Basic Information

```toml
[project]
name = "your-package-name"
version = "0.1.0"
description = "A clear, concise description of your package"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}  # Or other license
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
maintainers = [
    {name = "Maintainer Name", email = "maintainer@example.com"}
]
```

### 2. Project URLs

```toml
[project.urls]
Homepage = "https://github.com/your-org/your-repo"
Documentation = "https://your-docs-url.com"
Repository = "https://github.com/your-org/your-repo.git"
Issues = "https://github.com/your-org/your-repo/issues"
```

### 3. Classifiers

```toml
[project.classifiers]
"Development Status :: 4 - Beta"
"Intended Audience :: Developers"
"License :: OSI Approved :: MIT License"
"Programming Language :: Python :: 3"
"Programming Language :: Python :: 3.10"
"Programming Language :: Python :: 3.11"
"Topic :: Software Development :: Libraries :: Python Modules"
```

## Dependencies Management

### 1. Core Dependencies

```toml
[project]
dependencies = [
    "package-name>=1.0.0",
    "another-package>=2.0.0",
]
```

### 2. Optional Dependencies

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]
docs = [
    "sphinx>=7.0.0",
    "sphinx-rtd-theme>=1.0.0",
]
```

## Hatch-specific Configuration

### 1. Build Configuration

```toml
[tool.hatch.build.targets.wheel]
packages = ["your_package_name"]

[tool.hatch.build]
include = [
    "src/**/*.py",
    "tests/**/*.py",
]
```

### 2. Version Management

```toml
[tool.hatch.version]
path = "src/__init__.py"
pattern = '__version__ = ["\'](.*)["\']'
```

## UV Package Manager Configuration

### 1. Workspace Configuration

```toml
[tool.uv.workspace]
members = [
    "operators/package1",
    "operators/package2",
]
```

### 2. UV-specific Settings

```toml
[tool.uv]
python = "3.10"
```

## Tool Configurations

### 1. Ruff Configuration

```toml
[tool.ruff]
line-length = 88
target-version = "py310"
select = ["E", "F", "I"]
exclude = ["src", "dist", ".docker", ".pytest_cache", ".ruff_cache"]
```

### 2. Semantic Release Configuration

```toml
[tool.semantic_release]
version_variable = ["pyproject.toml:project.version"]

[tool.semantic_release.branches.main]
match = "main"
prerelease = false
tag_format = "{name}-{version}"
```

## Example from Marimo

Marimo's pyproject.toml serves as a good reference for a well-structured configuration. Key aspects to note:

1. Clear separation of core and optional dependencies
2. Comprehensive project metadata
3. Well-organized tool configurations
4. Proper version management setup

## Best Practices Summary

1. **Version Management**:

   - Use semantic versioning
   - Keep version in sync between pyproject.toml and **init**.py
   - Use semantic-release for automated version management

2. **Dependencies**:

   - Specify minimum version requirements
   - Group optional dependencies logically
   - Keep dependencies up to date
   - Use version constraints appropriately

3. **Build Configuration**:

   - Use Hatch as the build backend
   - Configure package discovery correctly
   - Set up proper include/exclude patterns

4. **Tool Integration**:

   - Configure Ruff for linting and formatting
   - Set up UV workspace for monorepo management
   - Configure semantic-release for version management

5. **Documentation**:
   - Include comprehensive project metadata
   - Provide clear descriptions
   - Link to relevant resources
   - Use appropriate classifiers

## References

1. [PEP 621](https://peps.python.org/pep-0621/) - Python packaging metadata
2. [Hatch Documentation](https://hatch.pypa.io/latest/)
3. [UV Documentation](https://github.com/astral-sh/uv)
4. [Ruff Documentation](https://beta.ruff.rs/docs/)
5. [Semantic Release Documentation](https://python-semantic-release.readthedocs.io/)
