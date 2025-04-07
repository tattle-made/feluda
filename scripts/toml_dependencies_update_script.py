import re
from pathlib import Path

import tomlkit


def find_pyproject_files(start_dir=None):
    """Find all pyproject.toml files in the project."""
    if start_dir is None:
        start_dir = Path(__file__).parent.parent.absolute()
    else:
        start_dir = Path(start_dir).absolute()

    ignore_dirs = {"dist", ".venv", ".ruff_cache", "__pycache__", ".git"}
    pyproject_files = []

    for path in start_dir.rglob("pyproject.toml"):
        # Check if any part of the path is in the ignore list
        if not any(ignored in path.parts for ignored in ignore_dirs):
            pyproject_files.append(path)

    return pyproject_files


def load_lock_file(lock_file_path):
    """
    Load the UV lock file in TOML format.
    Returns a dictionary mapping package names to their versions.
    """
    lock_data = {}

    with open(lock_file_path, "r", encoding="utf-8") as lock_file:
        content = lock_file.read()

    try:
        parsed = tomlkit.parse(content)
        for package in parsed.get("package", []):
            if isinstance(package, dict) and "name" in package and "version" in package:
                lock_data[package["name"]] = package["version"]

    except Exception as e:
        print(f"Error parsing lock file: {e}")
        # Try alternative parsing if tomlkit fails
        package_blocks = re.findall(
            r"\[\[package\]\](.*?)(?=\[\[package\]\]|\Z)", content, re.DOTALL
        )
        for block in package_blocks:
            name_match = re.search(r'name\s*=\s*"([^"]+)"', block)
            version_match = re.search(r'version\s*=\s*"([^"]+)"', block)
            if name_match and version_match:
                lock_data[name_match.group(1)] = version_match.group(1)

    return lock_data


def update_dependency_version(dependency_str, package_versions):
    """
    Update a single dependency string based on available package versions.
    Returns the updated dependency string or the original if no update is needed.
    """
    dep_match = re.match(r"([a-zA-Z0-9\-_\.]+)([><=~!]+.*)?", dependency_str.strip())

    if not dep_match:
        return dependency_str

    package_name = dep_match.group(1)
    version_constraint = dep_match.group(2) or ""

    if package_name in package_versions:
        new_version = package_versions[package_name]

        # Keep any existing comparison operators (>=, ==, etc.)
        constraint_type = re.match(r"([><=~!]+)", version_constraint)
        if constraint_type:
            # Replace only the version part, keeping the operator
            new_dependency = f"{package_name}{constraint_type.group(1)}{new_version}"
        else:
            # No operator, add >= with the new version
            new_dependency = f"{package_name}>={new_version}"

        return new_dependency

    return dependency_str


def update_dependencies_list(dependencies, package_versions):
    """
    Update a list of dependencies based on the lock file data.
    Modifies the list in-place and returns a count of updated packages.
    """
    updated_count = 0

    for idx, dependency in enumerate(dependencies):
        original = dependency
        dependencies[idx] = update_dependency_version(dependency, package_versions)
        if dependencies[idx] != original:
            updated_count += 1

    return updated_count


def update_pyproject_versions(toml_file_path, package_versions):
    """
    Update the dependencies in a pyproject.toml file.
    Returns the number of updated dependencies.
    """
    try:
        with open(toml_file_path, "r", encoding="utf-8") as file:
            toml_data = tomlkit.parse(file.read())

        total_updated = 0

        # Update [project.dependencies]
        if "project" in toml_data and "dependencies" in toml_data["project"]:
            updated = update_dependencies_list(
                toml_data["project"]["dependencies"], package_versions
            )
            total_updated += updated

        # Update [project.optional-dependencies]
        if "project" in toml_data and "optional-dependencies" in toml_data["project"]:
            for group, dependencies in toml_data["project"][
                "optional-dependencies"
            ].items():
                updated = update_dependencies_list(dependencies, package_versions)
                total_updated += updated

        if total_updated > 0:
            with open(toml_file_path, "w", encoding="utf-8") as file:
                file.write(tomlkit.dumps(toml_data))

            print(f"Updated {total_updated} dependencies in {toml_file_path}")
            return total_updated
        else:
            print(f"No dependencies to update in {toml_file_path}")
            return 0

    except Exception as e:
        print(f"Error updating {toml_file_path}: {e}")
        return 0


def main():
    """Main function to find and update pyproject.toml files."""
    try:
        project_root = Path(__file__).parent.parent.absolute()
        lock_file_path = project_root / "uv.lock"

        if not lock_file_path.exists():
            print(f"Error: Lock file not found at {lock_file_path}")
            return

        # Find all pyproject.toml files
        toml_file_paths = find_pyproject_files(project_root)
        if not toml_file_paths:
            print("No pyproject.toml files found")
            return
        print(f"Found {len(toml_file_paths)} pyproject.toml files")

        # Load lock file data
        print(f"Loading lock file from {lock_file_path}")
        package_versions = load_lock_file(lock_file_path)
        if not package_versions:
            print("No package information found in lock file")
            return
        print(f"Found {len(package_versions)} packages in lock file")

        # Update each pyproject.toml file
        total_updated_files = 0
        total_updated_deps = 0

        for toml_file_path in toml_file_paths:
            print(f"Processing {toml_file_path}")
            updated = update_pyproject_versions(toml_file_path, package_versions)
            if updated > 0:
                total_updated_files += 1
                total_updated_deps += updated

        print(
            f"\nSummary: Updated {total_updated_deps} dependencies in {total_updated_files} files"
        )

    except Exception as e:
        print(f"An error occurred during execution: {e}")


if __name__ == "__main__":
    main()
