import sys
from pathlib import Path
from pprint import pprint

import tomli


def validate_pyproject_toml(file_path: Path) -> tuple[bool, list[str]]:
    """
    Validates a pyproject.toml file for required sections and values.
    Returns (is_valid, list of error messages).
    """
    try:
        with open(file_path, "rb") as f:
            content = tomli.load(f)
    except Exception as e:
        return False, [f"Failed to parse {file_path}: {str(e)}"]

    errors = []

    # Check [project] section
    if "project" not in content:
        errors.append(f"{file_path}: Missing [project] section")
    else:
        project = content["project"]
        if "name" not in project:
            errors.append(f"{file_path}: Missing project.name")
        if "version" not in project:
            errors.append(f"{file_path}: Missing project.version")

    # Check semantic release configuration
    try:
        tag_format = content["tool"]["semantic_release"]["branches"]["main"][
            "tag_format"
        ]
        if tag_format != "{name}-{version}":
            errors.append(
                f"{file_path}: Invalid tag_format. Expected '{{name}}-{{version}}', got '{tag_format}'"
            )
    except KeyError:
        errors.append(f"{file_path}: Missing or invalid semantic_release configuration")

    return len(errors) == 0, errors


def main():
    # Find all pyproject.toml files
    root_dir = Path(".")
    pyproject_files = [root_dir / "pyproject.toml"]  # Root pyproject.toml
    pyproject_files.extend(root_dir.glob("operators/**/pyproject.toml"))
    print("######## pyproject.toml files in the codebase ########")
    pprint(pyproject_files)

    all_valid = True
    all_errors = []

    for file_path in pyproject_files:
        if not file_path.exists():
            print(f"Warning: {file_path} does not exist")
            continue

        is_valid, errors = validate_pyproject_toml(file_path)
        if not is_valid:
            all_valid = False
            all_errors.extend(errors)

    if all_valid:
        print("✅ All pyproject.toml files are valid")
        sys.exit(0)
    else:
        print("❌ Validation failed:")
        for error in all_errors:
            print(f"  - {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
