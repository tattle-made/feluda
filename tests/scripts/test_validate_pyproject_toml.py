#!/usr/bin/env python3
"""Tests for the pyproject.toml validator."""

import os
import tempfile
from pathlib import Path

import pytest
import tomlkit

from scripts.validate_pyproject_toml import PyprojectValidator


def create_test_pyproject(content: str) -> Path:
    """Create a temporary pyproject.toml file with the given content."""
    fd, path = tempfile.mkstemp(suffix=".toml")
    with os.fdopen(fd, "w") as f:
        f.write(content)
    return Path(path)


def test_valid_pyproject():
    """Test validation of a valid pyproject.toml file."""
    content = """
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "test-package"
version = "0.1.0"
description = "A test package"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Test Author", email = "test@example.com"}
]
maintainers = [
    {name = "Test Maintainer", email = "maintainer@example.com"}
]

[project.urls]
Homepage = "https://github.com/test/test"
Documentation = "https://test.readthedocs.io"
Repository = "https://github.com/test/test.git"
Issues = "https://github.com/test/test/issues"

[project.classifiers]
"Development Status :: 4 - Beta"
"Intended Audience :: Developers"
"License :: OSI Approved :: MIT License"
"Programming Language :: Python :: 3"
"Programming Language :: Python :: 3.10"

[project.dependencies]
requests = ">=2.0.0"
pytest = ">=7.0.0"

[project.optional-dependencies]
dev = [
    "black>=23.0.0",
    "ruff>=0.1.0",
]
docs = [
    "sphinx>=7.0.0",
]

[tool.hatch.build]
include = ["src/**/*.py"]

[tool.ruff]
line-length = 88
target-version = "py310"
select = ["E", "F", "I"]

[tool.uv]
python = "3.10"

[tool.uv.workspace]
members = ["package1", "package2"]
"""
    path = create_test_pyproject(content)
    validator = PyprojectValidator(path)
    errors, warnings = validator.validate()
    assert not errors
    assert not warnings
    os.unlink(path)


def test_missing_required_sections():
    """Test validation of a pyproject.toml file missing required sections."""
    content = """
[project]
name = "test-package"
"""
    path = create_test_pyproject(content)
    validator = PyprojectValidator(path)
    errors, warnings = validator.validate()
    assert "Missing [build-system] section" in errors
    assert "Missing project.version" in errors
    assert "Missing project.requires-python" in errors
    os.unlink(path)


def test_missing_recommended_fields():
    """Test validation of a pyproject.toml file missing recommended fields."""
    content = """
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "test-package"
version = "0.1.0"
requires-python = ">=3.10"
"""
    path = create_test_pyproject(content)
    validator = PyprojectValidator(path)
    errors, warnings = validator.validate()
    assert not errors
    assert "Missing recommended project.description" in warnings
    assert "Missing recommended project.readme" in warnings
    assert "Missing recommended project.license" in warnings
    os.unlink(path)


def test_invalid_dependencies():
    """Test validation of dependencies configuration."""
    content = """
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "test-package"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "requests",  # Missing version
    "pytest>=7.0.0",
]
"""
    path = create_test_pyproject(content)
    validator = PyprojectValidator(path)
    errors, warnings = validator.validate()
    assert not errors
    assert "Consider specifying version for dependency: requests" in warnings
    os.unlink(path)


def test_missing_tool_configurations():
    """Test validation of tool configurations."""
    content = """
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "test-package"
version = "0.1.0"
requires-python = ">=3.10"
"""
    path = create_test_pyproject(content)
    validator = PyprojectValidator(path)
    errors, warnings = validator.validate()
    assert not errors
    assert "Missing tool.hatch configuration" in warnings
    assert "Missing tool.ruff configuration" in warnings
    assert "Missing tool.uv configuration" in warnings
    os.unlink(path)


def test_invalid_toml():
    """Test validation of an invalid TOML file."""
    content = """
[build-system
requires = ["hatchling"]
"""
    path = create_test_pyproject(content)
    validator = PyprojectValidator(path)
    errors, warnings = validator.validate()
    assert "Failed to parse" in errors[0]
    assert not warnings
    os.unlink(path)


def test_nonexistent_file():
    """Test validation of a nonexistent file."""
    path = Path("/nonexistent/path/pyproject.toml")
    validator = PyprojectValidator(path)
    errors, warnings = validator.validate()
    assert "Failed to parse" in errors[0]
    assert not warnings 