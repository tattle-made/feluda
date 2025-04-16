#!/usr/bin/env python3
"""
Script to identify packages with updated versions that need to be published to PyPI.
This script checks each package's current version against the latest version on PyPI.
"""

import glob
import os
import json
import sys
import requests
import tomlkit
from pathlib import Path

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

                packages[package_root] = {
                    "path": full_path,
                    "name": package_name,
                    "current_version": current_version,
                }
                print(f"Discovered package: {package_name} ({current_version}) at {package_root}")
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
            print(f"Package {package_name} not found on {'Test PyPI' if test_pypi else 'PyPI'} (this might be the first release)")
            return None
        else:
            print(f"Error fetching {'Test PyPI' if test_pypi else 'PyPI'} version for {package_name}: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Error checking {'Test PyPI' if test_pypi else 'PyPI'} for {package_name}: {e}")
        return None

def main():
    repo_root = os.getcwd()
    packages = discover_packages(repo_root)
    packages_to_publish = []

    # Determine whether to check Test PyPI or production PyPI
    # If CHECK_TEST_PYPI is set to "true" in environment variables, use Test PyPI
    check_test_pypi = os.environ.get("CHECK_TEST_PYPI", "true").lower() == "true"
    
    print(f"Checking package versions against {'Test PyPI' if check_test_pypi else 'production PyPI'}")
    
    for package_root, package_info in packages.items():
        try:
            package_name = package_info["name"]
            current_version = package_info["current_version"]
            
            # Get the latest version from PyPI (Test or production)
            pypi_version = get_pypi_version(package_name, test_pypi=check_test_pypi)
            
            if pypi_version is None:
                # Package not found on PyPI, include it for first-time publishing
                print(f"Package {package_name} will be published for the first time")
                packages_to_publish.append(package_root)
            elif current_version != pypi_version:
                # Version is different, include it for publishing
                print(f"Package {package_name} needs publishing: Local={current_version}, PyPI={pypi_version}")
                packages_to_publish.append(package_root)
            else:
                print(f"Package {package_name} is up to date (version {current_version})")
        except Exception as e:
            print(f"Error checking version for {package_info['name']}: {e}")

    # Write the list of packages to publish to a file
    with open("packages_to_publish.txt", "w") as f:
        f.write(",".join(packages_to_publish))

    if packages_to_publish:
        print(f"\nPackages to publish: {', '.join(packages_to_publish)}")
    else:
        print("\nNo packages need to be published.")

if __name__ == "__main__":
    main()