import os
import re

import toml


def find_pyproject_files():
    current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    pyproject_files = []

    for root, dirs, files in os.walk(current_dir):
        # Ignore "dist" and ".venv" folders
        dirs[:] = [d for d in dirs if d not in {"dist", ".venv"}]

        if "pyproject.toml" in files:
            pyproject_files.append(os.path.join(root, "pyproject.toml"))

    return pyproject_files


def load_lock_file(lock_file_path):
    with open(lock_file_path, "r") as lock_file:
        lock_data = toml.load(lock_file)
    return lock_data


def update_pyproject_versions(toml_file_path, lock_data):
    with open(toml_file_path, "r") as file:
        toml_data = toml.load(file)

    for idx, dependency in enumerate(toml_data["project"]["dependencies"]):
        dep_match = re.match(r"([a-zA-Z0-9\-_]+)([><=~!]*[\d\.]+)?", dependency)

        if dep_match:
            dep_name = dep_match.group(1)  # Get the package name
            dep_version_spec = dep_match.group(2)  # Get the version specifier (if any)

            for pkg in lock_data["package"]:
                # If the lock file package name matches, update the version
                if pkg["name"] == dep_name:
                    new_version = pkg["version"]
                    if dep_version_spec:
                        toml_data["project"]["dependencies"][idx] = (
                            f"{dep_name}{dep_version_spec.replace(dep_version_spec, f'>={new_version}')}"
                        )
                    else:
                        toml_data["project"]["dependencies"][idx] = (
                            f"{dep_name}>={new_version}"
                        )

    with open(toml_file_path, "w") as file:
        toml.dump(toml_data, file)


if __name__ == "__main__":
    toml_file_paths = find_pyproject_files()
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    lock_file_path = os.path.join(project_root, "uv.lock")

    lock_data = load_lock_file(lock_file_path)

    print("Updating TOML file packages...")
    for toml_file_path in toml_file_paths:
        update_pyproject_versions(toml_file_path, lock_data)

    print("Updating Done")
