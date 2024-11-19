import os
import subprocess
import re
from semantic_release.version import Version

def get_modified_packages(base_sha, head_sha):
    """
    Get the list of modified packages between two Git commits.
    Returns a list of package names.
    """
    try:
        # Get the list of modified files
        result = subprocess.run(
            ["git", "diff", "--name-only", base_sha, head_sha],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        modified_files = result.stdout.splitlines()

        modified_packages = set()
        for file in modified_files:
            if file.startswith("feluda/"):
                modified_packages.add("feluda")
            elif file.startswith("operators/"):
                parts = file.split("/")
                if len(parts) > 1:
                    modified_packages.add(parts[1])
        
        return list(modified_packages)
    except subprocess.CalledProcessError as e:
        print(f"Error running git diff: {e.stderr}")
        return []

def bump_version_in_pyproject(pyproject_path):
    """
    Read the version from pyproject.toml, bump it using semantic versioning, and update the file.
    """
    try:
        with open(pyproject_path, 'r') as file:
            content = file.read()

        # Extract the current version using regex
        match = re.search(r'version = "(\d+\.\d+\.\d+)"', content)
        if not match:
            print(f"No version found in {pyproject_path}. Skipping...")
            return

        current_version = match.group(1)
        version = Version.parse(current_version)
        new_version = version.bump('patch')  # Bump the patch version

        # Replace the version in the content
        new_content = re.sub(r'version = "\d+\.\d+\.\d+"', f'version = "{new_version}"', content)
        
        # Write the updated content back to the file
        with open(pyproject_path, 'w') as file:
            file.write(new_content)
        
        print(f"Bumped version in {pyproject_path}: {current_version} -> {new_version}")
    except FileNotFoundError:
        print(f"{pyproject_path} not found. Skipping...")
    except Exception as e:
        print(f"Error processing {pyproject_path}: {e}")

def main():
    # Replace these with the actual base and head SHA values
    base_sha = "f6811bc0a6749f6cc219b675cd2a033c10a62fa8"
    head_sha = "f9d642263ebe0ef8cd4b29b5a93c6401cfd8ebcb"

    print("Detecting modified packages...")
    modified_packages = get_modified_packages(base_sha, head_sha)

    if not modified_packages:
        print("No modified packages found.")
        return

    print(f"Modified packages: {modified_packages}")

    for package in modified_packages:
        if package == "feluda":
            pyproject_path = "pyproject.toml"
        else:
            pyproject_path = f"operators/{package}/pyproject.toml"

        bump_version_in_pyproject(pyproject_path)

if __name__ == "__main__":
    main()
