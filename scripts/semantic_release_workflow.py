import glob
import os
import re
import subprocess
import sys

import tomli
import tomli_w


class PackageVersionManager:
    def __init__(self, repo_root, prev_commit, current_commit):
        """
        Initialize the version manager for a monorepo.

        Args:
            repo_root (str): Root directory of the monorepo
            prev_commit (str): Previous commit hash
            current_commit (str): Current commit hash

        Raises:
            FileNotFoundError: If the repo_root is invalid or inaccessible.
        """
        if not os.path.exists(repo_root):
            raise FileNotFoundError(f"Repository root '{repo_root}' does not exist.")

        self.repo_root = repo_root
        self.prev_commit = prev_commit
        self.current_commit = current_commit
        self.packages = self._discover_packages()

    def _discover_packages(self):
        """
        Discover all packages in the monorepo with their pyproject.toml.

        Returns:
            dict: Mapping of package paths to their current configuration.

        Raises:
            FileNotFoundError: If a pyproject.toml file is not found for a package.
        """
        packages = {}

        # Root package (feluda)
        package_roots = ["feluda"]

        # Discover packages inside 'operators' directory using glob
        operators_path = "operators"
        if os.path.isdir(operators_path):
            for folder in glob.glob(f"{operators_path}/*/pyproject.toml"):
                package_roots.append(os.path.dirname(folder))

        for package_root in package_roots:
            try:
                if package_root == "feluda":
                    pyproject_path = os.path.join(self.repo_root, "pyproject.toml")
                    full_path = os.path.join(self.repo_root, "feluda")
                else:
                    full_path = os.path.join(self.repo_root, package_root)
                    pyproject_path = os.path.join(full_path, "pyproject.toml")

                if os.path.exists(pyproject_path):
                    with open(pyproject_path, "rb") as f:
                        pyproject_data = tomli.load(f)

                    packages[package_root] = {
                        "package_path": full_path,
                        "pyproject_path": pyproject_path,
                        "current_version": pyproject_data["project"].get(
                            "version", "0.0.0"
                        ),
                    }
                else:
                    raise FileNotFoundError(
                        f"pyproject.toml not found in {package_root}"
                    )
            except (FileNotFoundError, tomli.TOMLDecodeError) as e:
                print(f"Error discovering package at {package_root}: {e}")

        return packages

    def _parse_conventional_commit(self, commit_message):
        """
        Parse a conventional commit message and determine version bump type.

        Args:
            commit_message (str): Commit message to parse.

        Returns:
            str: 'major', 'minor', 'patch', or None.

        Raises:
            ValueError: If the commit message format is invalid.

        Happy Path:
            - Commit message conforms to Conventional Commits, e.g., 'feat: Add new feature'.
            - Commit message does not conform to Conventional Commits
                but is non-empty, treated as a 'chore' type, returns "patch"
        Failure Path:
            - Commit message is invalid
            - Commit message is empty or in an invalid format and cannot be parsed.
        """
        try:
            # Normalize commit message
            message = commit_message.lower().strip()

            # Check for BREAKING CHANGE
            if "breaking change" in message:
                return "major"

            # Parse commit type
            """
            Regex can detect commits of the type
            <type>: <description>
            <type>(<optional scope>): <description>
            <type>[optional scope]: <description>
            """
            match = re.match(r"^(\w+)(?:\(|\[)?[^\)\]]*(?:\)|\])?:", message)
            if not match:
                # If the commit message does not match the conventional commit format
                # and is not empty, treat it as a "chore:" and return "patch".
                if message:
                    return "patch"
                return None

            commit_type = match.group(1)

            # Mapping of commit types to version bump
            type_bump_map = {
                "feat": "minor",
                "fix": "patch",
                "chore": "patch",
                "docs": "patch",
                "refactor": "patch",
                "test": "patch",
                "perf": "patch",
                "style": "patch",
                "build": "patch",
                "ci": "patch",
                "revert": "patch",
            }

            return type_bump_map.get(commit_type)
        except Exception as e:
            print(f"Error parsing commit message: {e}")
            return None

    def _bump_version(self, current_version, bump_type):
        """
        Bump version based on semantic versioning rules.

        Args:
            current_version (str): Current version string in the format 'x.y.z'.
            bump_type (str): Type of version bump ('major', 'minor', 'patch').

        Returns:
            str: New version string.

        Raises:
            ValueError: If the current_version format is invalid.

        Happy Path:
            Current version is valid, and a valid bump type is provided.
        Failure Path:
            Current version is not in 'x.y.z' format or bump_type is invalid.
        """
        try:
            major, minor, patch = map(int, current_version.split("."))

            if bump_type == "major":
                major += 1
                minor = 0
                patch = 0
            elif bump_type == "minor":
                minor += 1
                patch = 0
            elif bump_type == "patch":
                patch += 1
            else:
                return current_version

            return f"{major}.{minor}.{patch}"
        except ValueError:
            print(f"Invalid version format: {current_version}")
            raise

    def get_package_commits(self, package_path):
        """
        Get commits specific to a package between two commit ranges.

        Args:
            package_path (str): Relative path to the package.

        Returns:
            list: Commit messages affecting this package.

        Raises:
            subprocess.CalledProcessError: If the git command fails.

        Happy Path:
            Git command runs successfully, and commits are returned.
        Failure Path:
            Git command fails due to invalid commit range or other issues.
        """
        try:
            paths_to_check = [package_path]

            # Special handling for feluda package to include root pyproject.toml
            if package_path == "feluda":
                paths_to_check.append("pyproject.toml")

            all_commits = []
            for path in paths_to_check:
                # Get commits that modified files in this path between two commits
                cmd = [
                    "git",
                    "log",
                    f"{self.prev_commit}^..{self.current_commit}",
                    "--pretty=format:%s",
                    "--",
                    path,
                ]

                result = subprocess.run(
                    cmd, cwd=self.repo_root, capture_output=True, text=True, check=True
                )

                # Add commits for this path to the total list
                all_commits.extend(result.stdout.splitlines())

            # Remove duplicates while preserving order
            return list(dict.fromkeys(all_commits))
        except subprocess.CalledProcessError as e:
            print(f"Error getting commits for {package_path}: {e}")
            return []

    def determine_package_bump(self, package_path):
        """
        Determine the version bump type for a specific package.

        Args:
            package_path (str): Relative path to the package.

        Returns:
            str or None: Version bump type.

        Happy Path:
            Commit messages for the package result in a clear version bump type.
        Failure Path:
            No relevant commits or errors occur during commit parsing.
        """
        try:
            # Get commits for this package
            package_commits = self.get_package_commits(package_path)

            # If no commits, skip this package
            if not package_commits:
                print(f"No changes found for {package_path}. Skipping version bump.")
                return None

            bump_priority = {"major": 3, "minor": 2, "patch": 1, None: 0}
            highest_bump = None

            for commit in package_commits:
                commit_bump = self._parse_conventional_commit(commit)
                if commit_bump and bump_priority.get(
                    commit_bump, 0
                ) > bump_priority.get(highest_bump, 0):
                    highest_bump = commit_bump

            return highest_bump
        except Exception as e:
            print(f"Error determining version bump for {package_path}: {e}")
            return None

    def _get_tag_format(self, package_info):
        """
        Get the tag format for a package from its pyproject.toml.

        Args:
            package_info (dict): A dictionary containing the package's pyproject path.
                                Expected format: {"pyproject_path": "<path_to_pyproject>"}

        Returns:
            str: The tag format string, e.g., "{version}".

        Raises:
            ValueError: If the tag format or project name is not found in pyproject.toml.
            FileNotFoundError: If the pyproject.toml file is not found at the specified path.
            tomli.TOMLDecodeError: If the pyproject.toml file is not properly formatted.

        Happy Path:
            - If the `pyproject.toml` file exists and is properly formatted,
            the function retrieves the `tag_format` specified under `tool.semantic_release.branches.main.tag_format`.

        Failure Path:
            - If the `pyproject.toml` file is missing or malformed.
            - If the `tag_format` is not found in the `pyproject.toml`.
            - If the `name` or `version` fields are missing in the `pyproject.toml`.
        """
        try:
            with open(package_info["pyproject_path"], "rb") as f:
                pyproject_data = tomli.load(f)

            # Retrieve project name and version
            project_name = pyproject_data.get("project", {}).get("name")
            if not project_name:
                raise ValueError(
                    f"Project name not found in {package_info['pyproject_path']}. Please specify it in the pyproject.toml."
                )

            current_version = pyproject_data.get("project", {}).get("version")
            if not current_version:
                raise ValueError(
                    f"Version not found in {package_info['pyproject_path']}. Please specify it in the pyproject.toml."
                )

            # Retrieve tag format
            tag_format = (
                pyproject_data.get("tool", {})
                .get("semantic_release", {})
                .get("branches", {})
                .get("main", {})
                .get("tag_format")
            )
            if not tag_format:
                raise ValueError(
                    f"Tag format not found in {package_info['pyproject_path']}. Please ensure it's specified in the pyproject.toml."
                )

            # Return the raw tag format
            return tag_format

        except FileNotFoundError:
            print(
                f"Error: pyproject.toml not found at {package_info['pyproject_path']}"
            )
            raise
        except tomli.TOMLDecodeError:
            print(
                f"Error: Failed to parse {package_info['pyproject_path']} due to a TOML format error."
            )
            raise
        except ValueError as e:
            print(f"Error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error in _get_tag_format: {e}")
            raise

    def tag_exists(self, package_info, new_version):
        """
        Check if a Git tag exists for the package version based on tag format.

        Args:
            package_info (dict): A dictionary containing tag format details from pyproject.toml.
                                Expected format: {"package_path": "<path>", "pyproject_path": "<path_to_pyproject>"}
            new_version (str): The new version to check for in Git tags.

        Returns:
            bool: True if the tag exists, otherwise False.

        Raises:
            subprocess.CalledProcessError: If the git command fails.
            ValueError: If tag format cannot be generated from pyproject.toml.

        Happy Path:
            - If the `tag_format` is found in `pyproject.toml` and the tag already exists for the new version,
            the function returns `True`.

        Failure Path:
            - If the `tag_format` is not found in `pyproject.toml`.
            - If the git command fails due to issues with fetching tags or accessing the repository.
        """
        try:
            with open(package_info["pyproject_path"], "rb") as f:
                pyproject_data = tomli.load(f)

            # Retrieve project name and version
            project_name = pyproject_data.get("project", {}).get("name")
            if not project_name:
                raise ValueError(
                    f"Project name not found in {package_info['pyproject_path']}. Please specify it in the pyproject.toml."
                )

            tag_format = self._get_tag_format(package_info)

            tag_name = tag_format.format(name=project_name, version=new_version)

            cmd = ["git", "tag", "--list", tag_name]
            result = subprocess.run(
                cmd, cwd=self.repo_root, capture_output=True, text=True, check=True
            )

            return tag_name in result.stdout.splitlines()
        except subprocess.CalledProcessError as e:
            print(
                f"Error: Failed to run git tag command to check tag for {package_info['package_path']}: {e}"
            )
            raise
        except ValueError as e:
            print(f"Error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error in tag_exists: {e}")
            raise

    def create_tag(self, package_info, new_version):
        """
        Create a Git tag for the updated package version using the tag format from pyproject.toml.

        Args:
            package_info (dict): A dictionary containing tag format details from pyproject.toml.
                                Expected format: {"package_path": "<path>", "pyproject_path": "<path_to_pyproject>"}
            new_version (str): The new version to tag.

        Returns:
            None

        Raises:
            subprocess.CalledProcessError: If the git command fails to create the tag.
            ValueError: If the tag format cannot be generated from pyproject.toml.

        Happy Path:
            - If the tag format is found in `pyproject.toml` and the git tag command succeeds,
            a new tag is created in the repository.

        Failure Path:
            - If the `tag_format` is not found in `pyproject.toml`.
            - If the git command to create the tag fails.
        """
        try:
            with open(package_info["pyproject_path"], "rb") as f:
                pyproject_data = tomli.load(f)

            # Retrieve project name
            project_name = pyproject_data.get("project", {}).get("name")
            if not project_name:
                raise ValueError(
                    f"Project name not found in {package_info['pyproject_path']}. Please specify it in the pyproject.toml."
                )

            tag_format = self._get_tag_format(package_info)

            tag_name = tag_format.format(name=project_name, version=new_version)

            cmd = ["git", "tag", tag_name]
            subprocess.run(cmd, cwd=self.repo_root, check=True)

            print(f"Created tag {tag_name}")
        except subprocess.CalledProcessError as e:
            print(
                f"Error: Failed to create tag for {package_info['package_path']}: {e}"
            )
            raise
        except ValueError as e:
            print(f"Error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error in create_tag: {e}")
            raise

    def update_package_versions(self):
        """
        Update versions for packages with changes.

        Returns:
            dict: A dictionary mapping package paths to their updated versions.

        Raises:
            subprocess.CalledProcessError: If the git command fails to fetch commits or create tags.
            ValueError: If version bump cannot be determined or applied.
            FileNotFoundError: If pyproject.toml is missing or inaccessible.

        Happy Path:
            - If version bumps are detected for any package, the function updates the versions in `pyproject.toml`,
            creates Git tags, and returns a dictionary of updated packages with their old and new versions.
            - If a package does not have any changes, the version is not bumped.
            - If the tag already exists for the new version, version bumping is skipped

        Failure Path:
            - If any error occurs during version bump, tag creation, or updating pyproject.toml.
        """
        updated_versions = {}

        for package_path, package_info in self.packages.items():
            try:
                bump_type = self.determine_package_bump(package_path)

                if not bump_type:
                    continue

                current_version = package_info["current_version"]
                new_version = self._bump_version(current_version, bump_type)

                if self.tag_exists(package_info, new_version):
                    print(
                        f"Tag already exists for {package_path}. Skipping version bump."
                    )
                    continue

                with open(package_info["pyproject_path"], "rb") as f:
                    pyproject_data = tomli.load(f)

                pyproject_data["project"]["version"] = new_version

                with open(package_info["pyproject_path"], "wb") as f:
                    tomli_w.dump(pyproject_data, f)

                self.create_tag(package_info, new_version)

                updated_versions[package_path] = {
                    "old_version": current_version,
                    "new_version": new_version,
                    "bump_type": bump_type,
                }

                print(
                    f"Updated {package_path}: {current_version} -> {new_version} ({bump_type} bump)"
                )

            except Exception as e:
                print(f"Failed to update version for {package_path}: {e}")

        return updated_versions


# Main script execution
if __name__ == "__main__":
    # Ensure correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python semantic_release.py <prev_commit> <current_commit>")
        sys.exit(1)

    # Get repository root (assumes script is run from repo root)
    repo_root = os.getcwd()

    # Get commit range from command line arguments
    prev_commit = sys.argv[1]
    current_commit = sys.argv[2]

    # Initialize version manager
    try:
        version_manager = PackageVersionManager(repo_root, prev_commit, current_commit)

        # Analyze changes and update package versions
        updated_versions = version_manager.update_package_versions()

        if updated_versions:
            print("\nVersion updates completed successfully:")
            for package, info in updated_versions.items():
                print(
                    f"{package}: {info['old_version']} -> {info['new_version']} ({info['bump_type']} bump)"
                )
        else:
            print("\nNo packages required version updates.")

    except Exception as e:
        print(f"An error occurred during the version update process: {e}")
        sys.exit(1)
