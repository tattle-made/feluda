import glob
import os
import re
import subprocess
import sys

import tomlkit


class PackageVersionManager:
    def __init__(self, repo_root, prev_commit, current_commit):
        """
        Initialize the version manager for a monorepo.

        Args:
            repo_root (str): Root directory of the monorepo.
            prev_commit (str): Previous commit hash.
            current_commit (str): Current commit hash.

        Raises:
            FileNotFoundError: If the repo_root is invalid or inaccessible.
        """
        if not os.path.exists(repo_root):
            raise FileNotFoundError(f"Repository root '{repo_root}' does not exist.")

        self.repo_root = repo_root
        self.prev_commit = prev_commit
        self.current_commit = current_commit

        try:
            self.packages = self._discover_packages()
        except Exception:
            self.packages = {}

    def _discover_packages(self):
        """
        Discover all packages in the monorepo with their pyproject.toml.

        Returns:
            dict: A dictionary of discovered packages with their metadata.

        Raises:
            ValueError: If no valid packages are discovered.
        """
        packages = {}

        operators_path = os.path.join(self.repo_root, "operators")
        package_roots = ["feluda"]

        if os.path.isdir(operators_path):
            for folder in glob.glob(f"{operators_path}/*/pyproject.toml"):
                package_roots.append(os.path.dirname(folder))

        for package_root in package_roots:
            try:
                if package_root == "feluda":
                    pyproject_path = os.path.join(self.repo_root, "pyproject.toml")
                    full_path = os.path.join(self.repo_root, "feluda")
                    include_root_files = True  # Special handling for feluda
                else:
                    full_path = os.path.join(self.repo_root, package_root)
                    pyproject_path = os.path.join(full_path, "pyproject.toml")
                    include_root_files = False

                if not os.path.exists(pyproject_path):
                    raise FileNotFoundError(f"pyproject.toml not found in {package_root}")

                with open(pyproject_path, "r", encoding="utf-8") as f:
                    pyproject_data = tomlkit.parse(f.read())

                self._validate_pyproject(pyproject_data, pyproject_path)

                packages[package_root] = {
                    "package_path": full_path,
                    "pyproject_path": pyproject_path,
                    "pyproject_data": pyproject_data,
                    "current_version": pyproject_data["project"].get("version", "0.0.0"),
                    "include_root_files": include_root_files,  # Add this flag
                }

            except (FileNotFoundError, tomlkit.exceptions.ParseError, ValueError):
                pass

        if not packages:
            raise ValueError("No valid packages discovered in the repository")

        return packages

    def _parse_conventional_commit(self, commit_message):
        """
        Parse a conventional commit message and determine version bump type.

        Args:
            commit_message (str): Commit message to parse.

        Returns:
            str: 'major', 'minor', 'patch', or None.
        """
        try:
            # Normalize commit message
            message = commit_message.lower().strip()

            # Check for BREAKING CHANGE
            if "breaking change" in message:
                return "major"

            # Parse commit type
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
        except Exception:
            return None

    def _validate_pyproject(self, pyproject_data, pyproject_path):
        """
        Validate the pyproject.toml file for required fields.

        Args:
            pyproject_data (dict): Parsed pyproject.toml data.
            pyproject_path (str): Path to the pyproject.toml file.

        Raises:
            ValueError: If required fields are missing.
        """
        required_fields = [
            pyproject_data.get("project", {}).get("name"),
            pyproject_data.get("project", {}).get("version"),
            pyproject_data.get("tool", {})
                .get("semantic_release", {})
                .get("branches", {})
                .get("main", {})
                .get("tag_format"),
        ]
        if not all(required_fields):
            raise ValueError(f"Missing required fields in {pyproject_path}")
        return True

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
            raise

    def get_package_commits(self, package_path):
        """
        Get the list of commits affecting a specific package within the specified commit range.

        Args:
            package_path (str): Path to the package.

        Returns:
            list: A list of commit messages affecting the package.
        """
        try:
            if package_path == os.path.join(self.repo_root, "feluda"):
                cmd = [
                    "git",
                    "log",
                    f"{self.prev_commit}^..{self.current_commit}",
                    "--pretty=format:%s",
                    "--full-history",
                    "--",
                    "feluda/",
                    "pyproject.toml",
                    ":!operators/*"
                ]
            else:
                relative_path = os.path.relpath(package_path, self.repo_root)
                cmd = [
                    "git",
                    "log",
                    f"{self.prev_commit}^..{self.current_commit}",
                    "--pretty=format:%s",
                    "--full-history",
                    "--",
                    f"{relative_path}/"
                ]

            result = subprocess.run(
                cmd, cwd=self.repo_root, capture_output=True, text=True, check=True
            )

            package_commits = result.stdout.splitlines()
            return package_commits
        except subprocess.CalledProcessError:
            return []

    def determine_package_bump(self, package_path):
        """
        Determine the version bump type for a specific package.

        Args:
            package_path (str): Relative path to the package.

        Returns:
            str or None: Version bump type ('major', 'minor', 'patch') or None.
        """
        try:
            package_commits = self.get_package_commits(package_path)

            if not package_commits:
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
        except Exception:
            return None

    def _get_tag_format(self, package_info):
        """
        Get the tag format for a package from its pyproject.toml.

        Args:
            package_info (dict): A dictionary containing the package's pyproject data.

        Returns:
            str: The tag format string (e.g., "v{version}").

        Raises:
            ValueError: If the tag format is not found in pyproject.toml.
        """
        try:
            pyproject_data = package_info["pyproject_data"]
            tool = pyproject_data.get("tool", {})
            tag_format = (
                tool.get("semantic_release", {})
                .get("branches", {})
                .get("main", {})
                .get("tag_format")
            )
            if not tag_format:
                raise ValueError("tag_format not found in pyproject.toml")
            return tag_format
        except KeyError as e:
            raise ValueError(f"Missing key in pyproject.toml: {e}")

    def tag_exists(self, package_info, new_version):
        """
        Check if a Git tag exists for the package version.

        Args:
            package_info (dict): Package metadata.
            new_version (str): The new version to check.

        Returns:
            bool: True if the tag exists, False otherwise.
        """
        project_name = package_info["pyproject_data"]["project"]["name"]
        tag_format = self._get_tag_format(package_info)

        tag_name = tag_format.format(name=project_name, version=new_version)

        cmd = ["git", "tag", "--list"]
        result = subprocess.run(cmd, cwd=self.repo_root, capture_output=True, text=True, check=True)

        existing_tags = result.stdout.splitlines()
        return tag_name in existing_tags

    def create_tag(self, package_info, new_version):
        """
        Create a Git tag for the updated package version.

        Args:
            package_info (dict): Package metadata.
            new_version (str): The new version to tag.
        """
        project_name = package_info["pyproject_data"]["project"]["name"]
        tag_format = self._get_tag_format(package_info)

        tag_name = tag_format.format(name=project_name, version=new_version)

        existing_tags = subprocess.run(
            ["git", "tag", "--list"], cwd=self.repo_root, capture_output=True, text=True, check=True
        ).stdout.splitlines()

        if tag_name in existing_tags:
            return

        cmd = ["git", "tag", tag_name]
        subprocess.run(cmd, cwd=self.repo_root, check=True)

    def update_package_versions(self):
        """
        Update versions for packages with changes and create Git tags.

        Returns:
            dict: A dictionary mapping package names to their updated version information.
        """
        updated_versions = {}

        for package_name, package_info in self.packages.items():
            try:
                package_commits = self.get_package_commits(package_info["package_path"])

                if not package_commits:
                    continue

                bump_type = self.determine_package_bump(package_info["package_path"])
                if not bump_type:
                    continue

                current_version = package_info.get("current_version", "0.0.0")
                new_version = self._bump_version(current_version, bump_type)

                while self.tag_exists(package_info, new_version):
                    new_version = self._bump_version(new_version, "patch")

                package_info["current_version"] = new_version
                package_info["pyproject_data"]["project"]["version"] = new_version

                with open(package_info["pyproject_path"], "w", encoding="utf-8") as f:
                    tomlkit.dump(package_info["pyproject_data"], f)

                self.create_tag(package_info, new_version)

                updated_versions[package_name] = {
                    "old_version": current_version,
                    "new_version": new_version,
                    "bump_type": bump_type
                }

            except Exception:
                pass

        return updated_versions


# Main script execution
if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)

    repo_root = os.getcwd()
    prev_commit = sys.argv[1]
    current_commit = sys.argv[2]

    try:
        version_manager = PackageVersionManager(repo_root, prev_commit, current_commit)
        updated_versions = version_manager.update_package_versions()

        if updated_versions:
            for package, info in updated_versions.items():
                print(
                    f"{package}: {info['old_version']} -> {info['new_version']} ({info['bump_type']} bump)"
                )
        else:
            print("No packages required version updates.")

    except Exception:
        sys.exit(1)
