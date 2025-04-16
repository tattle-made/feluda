#!/usr/bin/env python3
"""
Script to validate pyproject.toml files against best practices.
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any

import tomlkit
from tomlkit.exceptions import TOMLKitError


class PyprojectValidator:
    """Validator for pyproject.toml files."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.content = None
        self.errors = []
        self.warnings = []

    def load_file(self) -> bool:
        """Load and parse the pyproject.toml file."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.content = tomlkit.parse(f.read())
            return True
        except (TOMLKitError, FileNotFoundError) as e:
            self.errors.append(f"Failed to parse {self.file_path}: {str(e)}")
            return False

    def validate_required_sections(self) -> None:
        """Validate required sections are present."""
        if not self.content:
            return

        # Check build-system section
        if "build-system" not in self.content:
            self.errors.append("Missing [build-system] section")
        else:
            build_system = self.content["build-system"]
            if "requires" not in build_system:
                self.errors.append("Missing build-system.requires")
            if "build-backend" not in build_system:
                self.errors.append("Missing build-system.build-backend")

        # Check project section
        if "project" not in self.content:
            self.errors.append("Missing [project] section")
        else:
            project = self.content["project"]
            required_fields = ["name", "version", "requires-python"]
            for field in required_fields:
                if field not in project:
                    self.errors.append(f"Missing project.{field}")

    def validate_project_metadata(self) -> None:
        """Validate project metadata fields."""
        if not self.content or "project" not in self.content:
            return

        project = self.content["project"]
        recommended_fields = [
            "description",
            "readme",
            "license",
            "authors",
            "maintainers",
        ]
        for field in recommended_fields:
            if field not in project:
                self.warnings.append(f"Missing recommended project.{field}")

        # Check URLs
        if "urls" not in project:
            self.warnings.append("Missing project.urls section")
        else:
            urls = project["urls"]
            recommended_urls = ["Homepage", "Documentation", "Repository", "Issues"]
            for url in recommended_urls:
                if url not in urls:
                    self.warnings.append(f"Missing recommended project.urls.{url}")

        # Check classifiers
        if "classifiers" not in project:
            self.warnings.append("Missing project.classifiers")
        else:
            classifiers = project["classifiers"]
            recommended_classifiers = [
                "Development Status",
                "Intended Audience",
                "License",
                "Programming Language :: Python",
            ]
            for classifier in recommended_classifiers:
                if not any(c.startswith(classifier) for c in classifiers):
                    self.warnings.append(f"Missing recommended classifier: {classifier}")

    def validate_dependencies(self) -> None:
        """Validate dependencies configuration."""
        if not self.content or "project" not in self.content:
            return

        project = self.content["project"]
        
        # Check core dependencies
        if "dependencies" not in project:
            self.warnings.append("Missing project.dependencies")
        else:
            deps = project["dependencies"]
            for dep in deps:
                if not any(c in dep for c in [">=", "==", "~=", "<="]):
                    self.warnings.append(f"Consider specifying version for dependency: {dep}")

        # Check optional dependencies
        if "optional-dependencies" not in project:
            self.warnings.append("Missing project.optional-dependencies")
        else:
            opt_deps = project["optional-dependencies"]
            recommended_groups = ["dev", "docs", "test"]
            for group in recommended_groups:
                if group not in opt_deps:
                    self.warnings.append(f"Consider adding {group} optional dependencies")

    def validate_tool_configurations(self) -> None:
        """Validate tool-specific configurations."""
        if not self.content:
            return

        # Check Hatch configuration
        if "tool" not in self.content or "hatch" not in self.content["tool"]:
            self.warnings.append("Missing tool.hatch configuration")
        else:
            hatch = self.content["tool"]["hatch"]
            if "build" not in hatch:
                self.warnings.append("Missing tool.hatch.build configuration")

        # Check Ruff configuration
        if "tool" not in self.content or "ruff" not in self.content["tool"]:
            self.warnings.append("Missing tool.ruff configuration")
        else:
            ruff = self.content["tool"]["ruff"]
            recommended_settings = ["line-length", "target-version", "select"]
            for setting in recommended_settings:
                if setting not in ruff:
                    self.warnings.append(f"Consider adding tool.ruff.{setting}")

        # Check UV configuration
        if "tool" not in self.content or "uv" not in self.content["tool"]:
            self.warnings.append("Missing tool.uv configuration")
        else:
            uv = self.content["tool"]["uv"]
            if "workspace" not in uv:
                self.warnings.append("Missing tool.uv.workspace configuration")

    def validate(self) -> Tuple[List[str], List[str]]:
        """Run all validations and return errors and warnings."""
        if not self.load_file():
            return self.errors, self.warnings

        self.validate_required_sections()
        self.validate_project_metadata()
        self.validate_dependencies()
        self.validate_tool_configurations()

        return self.errors, self.warnings


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python validate_pyproject_toml.py <path-to-pyproject.toml>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File {file_path} does not exist")
        sys.exit(1)

    validator = PyprojectValidator(file_path)
    errors, warnings = validator.validate()

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  ❌ {error}")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  ⚠️  {warning}")

    if not errors and not warnings:
        print("✅ pyproject.toml is valid and follows best practices!")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main() 