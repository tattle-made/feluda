import glob
import os
import subprocess

import requests
import tomlkit


def discover_packages(repo_root):
    """
    Discover all packages in the monorepo with their pyproject.toml.
    """
    packages = {}

    # Root package (feluda)
    package_roots = ["feluda"]

    # Discover packages inside 'operators' directory using glob
    operators_path = os.path.join(repo_root, "operators")
    if os.path.isdir(operators_path):
        for folder in glob.glob(f"{operators_path}/*/pyproject.toml"):
            package_roots.append(os.path.dirname(folder).replace(f"{repo_root}/", ""))

    for package_root in package_roots:
        try:
            if package_root == "feluda":
                pyproject_path = os.path.join(repo_root, "pyproject.toml")
                full_path = os.path.join(repo_root, "feluda")
            else:
                full_path = os.path.join(repo_root, package_root)
                pyproject_path = os.path.join(full_path, "pyproject.toml")

            if os.path.exists(pyproject_path):
                with open(pyproject_path, "r") as f:
                    pyproject_data = tomlkit.parse(f.read())

                # Get package name and version
                package_name = pyproject_data.get("project", {}).get("name")
                current_version = pyproject_data.get("project", {}).get("version")

                if not package_name or not current_version:
                    print(f"Warning: Missing name or version in {pyproject_path}")
                    continue

                # Get the tag format from pyproject.toml if available
                tag_format = (
                    pyproject_data.get("tool", {})
                    .get("semantic_release", {})
                    .get("branches", {})
                    .get("main", {})
                    .get("tag_format", "{name}-{version}")
                )

                packages[package_root] = {
                    "path": full_path,
                    "name": package_name,
                    "current_version": current_version,
                    "tag_format": tag_format,
                }
                print(
                    f"Discovered package: {package_name} ({current_version}) at {package_root}"
                )
            else:
                print(f"Warning: pyproject.toml not found in {package_root}")
        except Exception as e:
            print(f"Error discovering package at {package_root}: {e}")

    return packages


def get_pypi_version(package_name, test_pypi=True):
    """
    Get the latest version of a package on PyPI.
    Returns None if the package is not found or in case of an error.

    Args:
        package_name (str): The name of the package.
        test_pypi (bool, optional): Whether to check Test PyPI instead of production PyPI.
    """
    try:
        # Use Test PyPI or production PyPI based on the parameter
        base_url = "https://test.pypi.org" if test_pypi else "https://pypi.org"
        response = requests.get(f"{base_url}/pypi/{package_name}/json")

        if response.status_code == 200:
            data = response.json()
            return data["info"]["version"]
        elif response.status_code == 404:
            print(
                f"Package {package_name} not found on {'Test PyPI' if test_pypi else 'PyPI'} (this might be the first release)"
            )
            return None
        else:
            print(
                f"Error fetching {'Test PyPI' if test_pypi else 'PyPI'} version for {package_name}: HTTP {response.status_code}"
            )
            return None
    except Exception as e:
        print(
            f"Error checking {'Test PyPI' if test_pypi else 'PyPI'} for {package_name}: {e}"
        )
        return None


def verify_git_tag_exists(package_name, version, tag_format):
    """
    Verify that a git tag exists for the specified package version.

    Args:
        package_name (str): Name of the package.
        version (str): Version to check.
        tag_format (str): Tag format template.

    Returns:
        bool: True if the tag exists, False otherwise.
    """
    try:
        # Format the tag according to the tag_format
        tag_name = tag_format.format(name=package_name, version=version)

        # Check if the tag exists
        cmd = ["git", "tag", "--list", tag_name]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        exists = tag_name in result.stdout.splitlines()
        if exists:
            print(f"Found git tag {tag_name} for {package_name} version {version}")
        else:
            print(
                f"Warning: No git tag found for {package_name} version {version} (expected tag: {tag_name})"
            )
        return exists
    except subprocess.CalledProcessError as e:
        print(f"Error checking git tag for {package_name}: {e}")
        return False


def main():
    repo_root = os.getcwd()
    packages = discover_packages(repo_root)
    packages_to_publish = []
    packages_with_tag_issues = []

    # Determine whether to check Test PyPI or production PyPI
    # If CHECK_TEST_PYPI is set to "true" in environment variables, use Test PyPI
    check_test_pypi = os.environ.get("CHECK_TEST_PYPI", "false").lower() == "true"

    # Force tag verification or not (default to true)
    verify_tags = os.environ.get("VERIFY_TAGS", "true").lower() == "true"

    print(
        f"Checking package versions against {'Test PyPI' if check_test_pypi else 'production PyPI'}"
    )
    if verify_tags:
        print("Git tag verification is enabled")
    else:
        print("Warning: Git tag verification is disabled")

    for package_root, package_info in packages.items():
        try:
            package_name = package_info["name"]
            current_version = package_info["current_version"]
            tag_format = package_info["tag_format"]

            # First verify the git tag exists if verification is enabled
            tag_valid = True
            if verify_tags:
                tag_valid = verify_git_tag_exists(
                    package_name, current_version, tag_format
                )
                if not tag_valid:
                    packages_with_tag_issues.append(
                        f"{package_name} (version {current_version})"
                    )

            if not tag_valid and verify_tags:
                print(f"Skipping {package_name} due to missing git tag")
                continue

            # Get the latest version from PyPI (Test or production)
            pypi_version = get_pypi_version(package_name, test_pypi=check_test_pypi)

            if pypi_version is None:
                # Package not found on PyPI, include it for first-time publishing
                print(f"Package {package_name} will be published for the first time")
                packages_to_publish.append(package_root)
            elif current_version != pypi_version:
                # Version is different, include it for publishing
                print(
                    f"Package {package_name} needs publishing: Local={current_version}, PyPI={pypi_version}"
                )
                packages_to_publish.append(package_root)
            else:
                print(
                    f"Package {package_name} is up to date (version {current_version})"
                )
        except Exception as e:
            print(f"Error checking version for {package_info['name']}: {e}")

    # Write the list of packages to publish to a file
    with open("packages_to_publish.txt", "w") as f:
        f.write(",".join(packages_to_publish))

    # Write a report of tag issues if any were found
    if packages_with_tag_issues:
        with open("tag_verification_issues.txt", "w") as f:
            f.write("\n".join(packages_with_tag_issues))
        print(
            f"\nWarning: {len(packages_with_tag_issues)} packages have git tag verification issues. See tag_verification_issues.txt"
        )

    if packages_to_publish:
        print(f"\nPackages to publish: {', '.join(packages_to_publish)}")
    else:
        print("\nNo packages need to be published.")


if __name__ == "__main__":
    main()
