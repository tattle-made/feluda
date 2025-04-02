import os
import re

import tomlkit


def find_pyproject_files():
    """Find all pyproject.toml files in the project."""
    current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    pyproject_files = []

    for root, dirs, files in os.walk(current_dir):
        # Ignore a set of folders
        dirs[:] = [
            d for d in dirs if d not in {"dist", ".venv", ".ruff_cache", ".docker"}
        ]

        if "pyproject.toml" in files:
            pyproject_files.append(os.path.join(root, "pyproject.toml"))

    return pyproject_files


def load_lock_file(lock_file_path):
    """Load the lock file in custom format."""
    lock_data = {"package": []}

    with open(lock_file_path, "r", encoding="utf-8") as lock_file:
        for line in lock_file:
            match = re.match(r"^([a-zA-Z0-9\-_]+)==([\d\.]+)", line.strip())
            if match:
                package_name = match.group(1)
                package_version = match.group(2)
                lock_data["package"].append(
                    {"name": package_name, "version": package_version}
                )

    return lock_data


def update_dependencies(dependencies, lock_data):
    """Update dependencies based on the lock file."""
    for idx, dependency in enumerate(dependencies):
        dep_match = re.match(r"([a-zA-Z0-9\-_]+)([><=~!]*[\d\.]+)?", dependency)

        if dep_match:
            dep_name = dep_match.group(1)
            dep_version_spec = dep_match.group(2)

            for pkg in lock_data["package"]:
                if pkg["name"] == dep_name:
                    new_version = pkg["version"]
                    if dep_version_spec:
                        dependencies[idx] = (
                            f"{dep_name}{dep_version_spec.replace(dep_version_spec, f'>={new_version}')}"
                        )
                    else:
                        dependencies[idx] = f"{dep_name}>={new_version}"


def update_pyproject_versions(toml_file_path, lock_data):
    """Update the dependencies in a pyproject.toml file."""
    with open(toml_file_path, "r", encoding="utf-8") as file:
        toml_data = tomlkit.parse(file.read())

    # Update [project.dependencies]
    if "dependencies" in toml_data["project"]:
        update_dependencies(toml_data["project"]["dependencies"], lock_data)

    # Update [project.optional-dependencies]
    if "optional-dependencies" in toml_data["project"]:
        for group, dependencies in toml_data["project"][
            "optional-dependencies"
        ].items():
            update_dependencies(dependencies, lock_data)

    with open(toml_file_path, "w", encoding="utf-8") as file:
        file.write(tomlkit.dumps(toml_data))


if __name__ == "__main__":
    toml_file_paths = find_pyproject_files()

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    lock_file_path = os.path.join(project_root, "uv.lock")
    lock_data = load_lock_file(lock_file_path)

    print("Updating TOML file packages...")
    for toml_file_path in toml_file_paths:
        update_pyproject_versions(toml_file_path, lock_data)

    print("Updating Done")
