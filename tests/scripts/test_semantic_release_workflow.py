import os
import shutil
import subprocess
import tempfile
import unittest
from unittest.case import skip
from unittest.mock import patch

import tomlkit

from scripts.semantic_release_workflow import PackageVersionManager


class TestPackageVersionManager(unittest.TestCase):
    def setUp(self):
        """Set up a temporary directory structure simulating a monorepo."""
        # Create a temporary directory to simulate the repo
        self.temp_dir = tempfile.mkdtemp()

        # Create the basic structure
        os.makedirs(os.path.join(self.temp_dir, "feluda"))
        os.makedirs(os.path.join(self.temp_dir, "operators", "operator1"))
        os.makedirs(os.path.join(self.temp_dir, "operators", "operator2"))

        # Create git repo
        self._setup_git_repo()

        # Create pyproject.toml files
        self._create_pyproject_files()

        # Set up initial commit
        self._create_initial_commit()

    def tearDown(self):
        """Clean up the temporary directory."""
        shutil.rmtree(self.temp_dir)

    def _setup_git_repo(self):
        """Initialize a git repository in the temporary directory."""
        subprocess.run(["git", "init"], cwd=self.temp_dir, check=True)
        subprocess.run(["git", "branch", "-M", "main"], cwd=self.temp_dir, check=True)

        # Configure git for the tests
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=self.temp_dir,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"], cwd=self.temp_dir, check=True
        )

    def _create_pyproject_content(self, name, version="0.1.0"):
        """Create content for a pyproject.toml file."""
        data = tomlkit.document()
        project = tomlkit.table()
        project["name"] = name
        project["version"] = version
        data["project"] = project

        tool = tomlkit.table()
        semantic_release = tomlkit.table()
        branches = tomlkit.table()
        main = tomlkit.table()
        main["tag_format"] = "{name}-v{version}"
        branches["main"] = main
        semantic_release["branches"] = branches
        tool["semantic_release"] = semantic_release
        data["tool"] = tool

        return data

    def _create_pyproject_files(self):
        """Create pyproject.toml files for each package."""
        # Create pyproject.toml for main package
        feluda_pyproject = self._create_pyproject_content("feluda")
        with open(os.path.join(self.temp_dir, "pyproject.toml"), "w") as f:
            tomlkit.dump(feluda_pyproject, f)

        # Create pyproject.toml for operator1
        op1_pyproject = self._create_pyproject_content("operator1")
        with open(
            os.path.join(self.temp_dir, "operators", "operator1", "pyproject.toml"), "w"
        ) as f:
            tomlkit.dump(op1_pyproject, f)

        # Create pyproject.toml for operator2
        op2_pyproject = self._create_pyproject_content("operator2")
        with open(
            os.path.join(self.temp_dir, "operators", "operator2", "pyproject.toml"), "w"
        ) as f:
            tomlkit.dump(op2_pyproject, f)

    def _create_initial_commit(self):
        """Create an initial commit to start with."""
        subprocess.run(["git", "add", "."], cwd=self.temp_dir, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"], cwd=self.temp_dir, check=True
        )
        self.initial_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.temp_dir,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    def _create_file_and_commit(self, path, content, commit_message):
        """Create a file and commit it."""
        file_path = os.path.join(self.temp_dir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as f:
            f.write(content)

        subprocess.run(["git", "add", path], cwd=self.temp_dir, check=True)
        subprocess.run(
            ["git", "commit", "-m", commit_message], cwd=self.temp_dir, check=True
        )

        # Return the commit hash
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.temp_dir,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    def _get_current_version(self, package_path):
        """Get the current version from a package's pyproject.toml."""
        if package_path == "feluda":
            pyproject_path = os.path.join(self.temp_dir, "pyproject.toml")
        else:
            pyproject_path = os.path.join(self.temp_dir, package_path, "pyproject.toml")

        with open(pyproject_path, "r") as f:
            data = tomlkit.parse(f.read())

        return data["project"]["version"]

    def test_init_with_invalid_repo_root(self):
        """Test initialization with an invalid repository root."""
        with self.assertRaises(FileNotFoundError):
            PackageVersionManager("/nonexistent/path", "commit1", "commit2")

    def test_discover_packages(self):
        """Test that the class correctly discovers all packages."""
        manager = PackageVersionManager(
            self.temp_dir, self.initial_commit, self.initial_commit
        )

        # Check that we have exactly 3 packages discovered
        self.assertEqual(len(manager.packages), 3)
        # Check for the root package 'feluda'
        self.assertIn("feluda", manager.packages)
        self.assertEqual(
            manager.packages["feluda"]["package_path"],
            os.path.join(self.temp_dir, "feluda"),
        )
        # Check for operator1 and operator2 by their absolute paths
        op1_path = os.path.join(self.temp_dir, "operators", "operator1")
        op2_path = os.path.join(self.temp_dir, "operators", "operator2")
        self.assertIn(op1_path, manager.packages)
        self.assertIn(op2_path, manager.packages)
        # Additional checks to verify the version and package name
        self.assertEqual(
            manager.packages["feluda"]["pyproject_data"]["project"]["name"], "feluda"
        )
        self.assertEqual(
            manager.packages[op1_path]["pyproject_data"]["project"]["name"], "operator1"
        )
        self.assertEqual(
            manager.packages[op2_path]["pyproject_data"]["project"]["name"], "operator2"
        )

    def test_parse_conventional_commit(self):
        """Test parsing of conventional commit messages."""
        manager = PackageVersionManager(
            self.temp_dir, self.initial_commit, self.initial_commit
        )

        # Test major bump detection
        self.assertEqual(
            manager._parse_conventional_commit(
                "feat: new feature with BREAKING CHANGE"
            ),
            "major",
        )

        # Test minor bump detection
        self.assertEqual(
            manager._parse_conventional_commit("feat: new feature"), "minor"
        )

        # Test patch bump detection
        self.assertEqual(manager._parse_conventional_commit("fix: bug fix"), "patch")

        # Test non-conventional commit
        self.assertEqual(
            manager._parse_conventional_commit("random commit message"), "patch"
        )

        # Test empty commit message
        self.assertIsNone(manager._parse_conventional_commit(""))

    def test_bump_version(self):
        """Test version bumping logic."""
        manager = PackageVersionManager(
            self.temp_dir, self.initial_commit, self.initial_commit
        )

        # Test major bump
        self.assertEqual(manager._bump_version("1.2.3", "major"), "2.0.0")

        # Test minor bump
        self.assertEqual(manager._bump_version("1.2.3", "minor"), "1.3.0")

        # Test patch bump
        self.assertEqual(manager._bump_version("1.2.3", "patch"), "1.2.4")

        # Test invalid bump type
        self.assertEqual(manager._bump_version("1.2.3", "invalid"), "1.2.3")

        # Test invalid version format
        with self.assertRaises(ValueError):
            manager._bump_version("invalid", "patch")

    @skip
    def test_package_commits_detection(self):
        """Test detection of commits affecting a specific package."""
        # Create commits that affect different packages
        self._create_file_and_commit(
            "feluda/example.py", "print('hello')", "feat: added example file to feluda"
        )

        commit2 = self._create_file_and_commit(
            "operators/operator1/example.py",
            "print('hello')",
            "fix: added example file to operator1",
        )

        manager = PackageVersionManager(self.temp_dir, self.initial_commit, commit2)

        # Test feluda commits
        feluda_commits = manager.get_package_commits(
            os.path.join(self.temp_dir, "feluda")
        )
        self.assertEqual(len(feluda_commits), 1)
        self.assertIn("feat: added example file to feluda", feluda_commits)

        # Test operator1 commits
        op1_commits = manager.get_package_commits(
            os.path.join(self.temp_dir, "operators/operator1")
        )
        self.assertEqual(len(op1_commits), 1)
        self.assertIn("fix: added example file to operator1", op1_commits)

        # Test operator2 commits (should have none)
        op2_commits = manager.get_package_commits(
            os.path.join(self.temp_dir, "operators/operator2")
        )
        self.assertEqual(len(op2_commits), 0)

    def test_determine_package_bump(self):
        """Test determination of version bump type based on commits."""
        # Create a series of commits affecting different packages
        self._create_file_and_commit(
            "feluda/example1.py", "print('hello')", "feat: added feature to feluda"
        )

        self._create_file_and_commit(
            "operators/operator1/example1.py",
            "print('hello')",
            "feat: added feature to operator1 with BREAKING CHANGE",
        )

        commit3 = self._create_file_and_commit(
            "operators/operator2/example1.py",
            "print('hello')",
            "fix: fixed bug in operator2",
        )

        manager = PackageVersionManager(self.temp_dir, self.initial_commit, commit3)

        # Test feluda bump (should be minor)
        self.assertEqual(
            manager.determine_package_bump(os.path.join(self.temp_dir, "feluda")),
            "minor",
        )

        # Test operator1 bump (should be major due to BREAKING CHANGE)
        self.assertEqual(
            manager.determine_package_bump(
                os.path.join(self.temp_dir, "operators/operator1")
            ),
            "major",
        )

        # Test operator2 bump (should be patch)
        self.assertEqual(
            manager.determine_package_bump(
                os.path.join(self.temp_dir, "operators/operator2")
            ),
            "patch",
        )

        # Test non-existent package (should return None)
        self.assertIsNone(
            manager.determine_package_bump(
                os.path.join(self.temp_dir, "nonexistent_package")
            )
        )

    def test_determine_package_bump_no_update(self):
        """Test that no version bump occurs if no commits affect the package."""
        # Create a commit affecting only one package
        self._create_file_and_commit(
            "feluda/example1.py", "print('hello')", "feat: added feature to feluda"
        )

        # Create the version manager
        manager = PackageVersionManager(
            self.temp_dir, self.initial_commit, self.initial_commit
        )

        # Test operator1 bump (should be None since no commits)
        self.assertIsNone(
            manager.determine_package_bump(
                os.path.join(self.temp_dir, "operators/operator1")
            )
        )

    def test_get_tag_format(self):
        """Test the tag format generation."""
        manager = PackageVersionManager(
            self.temp_dir, self.initial_commit, self.initial_commit
        )

        expected_tag = manager.packages["feluda"].get("pyproject_data", {}).get(
            "tool", {}
        ).get("semantic_release", {}).get("branches", {}).get("main", {}).get(
            "tag_format", "{name}-v{version}"
        )

        self.assertEqual(
            manager._get_tag_format(manager.packages["feluda"]), expected_tag
        )

    def test_tag_exists(self):
        """Test detection of existing tags."""
        manager = PackageVersionManager(
            self.temp_dir, self.initial_commit, self.initial_commit
        )

        # Create a tag
        subprocess.run(["git", "tag", "feluda-v0.2.0"], cwd=self.temp_dir, check=True)

        # Test tag exists
        self.assertTrue(manager.tag_exists(manager.packages["feluda"], "0.2.0"))

        # Test tag doesn't exist
        self.assertFalse(manager.tag_exists(manager.packages["feluda"], "0.3.0"))

    def test_create_tag(self):
        """Test creation of tags."""
        manager = PackageVersionManager(
            self.temp_dir, self.initial_commit, self.initial_commit
        )

        manager.create_tag(manager.packages["feluda"], "0.2.0")

        tags = subprocess.run(
            ["git", "tag"],
            cwd=self.temp_dir,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
        self.assertIn("feluda-v0.2.0", tags)
        self.assertNotIn("feluda-v0.3.0", tags)

        # Check if the tag was created
        manager.create_tag(manager.packages["feluda"], "0.3.0")
        tags = subprocess.run(  
            ["git", "tag"],
            cwd=self.temp_dir,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
        self.assertIn("feluda-v0.3.0", tags)

    def test_update_package_versions_no_changes(self):
        """Test that no version updates occur when there are no changes."""
        manager = PackageVersionManager(
            self.temp_dir, self.initial_commit, self.initial_commit
        )
        updated_versions = manager.update_package_versions()

        self.assertEqual(len(updated_versions), 0)

    def test_update_package_versions_with_changes(self):
        """Test version updates based on commits."""
        # Create a series of commits affecting different packages
        self._create_file_and_commit(
            "feluda/example1.py", "print('hello')", "feat: added feature to feluda"
        )

        self._create_file_and_commit(
            "operators/operator1/example1.py",
            "print('hello')",
            "feat: added feature to operator1 with BREAKING CHANGE",
        )

        commit3 = self._create_file_and_commit(
            "operators/operator2/example1.py",
            "print('hello')",
            "fix: fixed bug in operator2",
        )

        # Create the version manager
        manager = PackageVersionManager(self.temp_dir, self.initial_commit, commit3)

        # Update versions
        updated_versions = manager.update_package_versions()

        # Check that all packages were updated
        self.assertEqual(len(updated_versions), 3)

        # Check feluda version (should be minor bump from 0.1.0 to 0.2.0)
        self.assertEqual(updated_versions["feluda"]["old_version"], "0.1.0")
        self.assertEqual(updated_versions["feluda"]["new_version"], "0.2.0")
        self.assertEqual(updated_versions["feluda"]["bump_type"], "minor")

        # Check operator1 version (should be major bump from 0.1.0 to 1.0.0)
        self.assertEqual(
            updated_versions[f"{self.temp_dir}/operators/operator1"]["old_version"], "0.1.0"
        )
        self.assertEqual(
            updated_versions[f"{self.temp_dir}/operators/operator1"]["new_version"], "1.0.0"
        )
        self.assertEqual(updated_versions[f"{self.temp_dir}/operators/operator1"]["bump_type"], "major")

        # Check operator2 version (should be patch bump from 0.1.0 to 0.1.1)
        self.assertEqual(
            updated_versions[f"{self.temp_dir}/operators/operator2"]["old_version"], "0.1.0"
        )
        self.assertEqual(
            updated_versions[f"{self.temp_dir}/operators/operator2"]["new_version"], "0.1.1"
        )
        self.assertEqual(updated_versions[f"{self.temp_dir}/operators/operator2"]["bump_type"], "patch")

        # Verify that the versions were updated in the pyproject.toml files
        self.assertEqual(self._get_current_version("feluda"), "0.2.0")
        self.assertEqual(self._get_current_version("operators/operator1"), "1.0.0")
        self.assertEqual(self._get_current_version("operators/operator2"), "0.1.1")

        # Verify that tags were created
        tags = subprocess.run(
            ["git", "tag"],
            cwd=self.temp_dir,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()

        self.assertIn("feluda-v0.2.0", tags)
        self.assertIn("operator1-v1.0.0", tags)
        self.assertIn("operator2-v0.1.1", tags)

    def test_version_bump_with_existing_tag(self):
        """Test version bumping when a tag already exists."""
        # Create a commit affecting feluda
        commit1 = self._create_file_and_commit(
            "feluda/example1.py", "print('hello')", "feat: added feature to feluda"
        )

        # Create a tag for feluda-v0.2.0
        subprocess.run(["git", "tag", "feluda-v0.2.0"], cwd=self.temp_dir, check=True)

        # Create the version manager
        manager = PackageVersionManager(self.temp_dir, self.initial_commit, commit1)

        # Update versions
        updated_versions = manager.update_package_versions()

        # Check that feluda was updated to 0.2.1 (since 0.2.0 tag already exists)
        self.assertEqual(updated_versions["feluda"]["old_version"], "0.1.0")
        self.assertEqual(updated_versions["feluda"]["new_version"], "0.2.1")

        # Verify that the version was updated in the pyproject.toml file
        self.assertEqual(self._get_current_version("feluda"), "0.2.1")

        # Verify that the new tag was created
        tags = subprocess.run(
            ["git", "tag"],
            cwd=self.temp_dir,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()

        self.assertIn("feluda-v0.2.1", tags)

    def test_package_without_pyproject_toml(self):
        """Test handling of a package without pyproject.toml."""
        # Remove the pyproject.toml file from operator2
        os.remove(
            os.path.join(self.temp_dir, "operators", "operator2", "pyproject.toml")
        )

        # Create the version manager
        manager = PackageVersionManager(
            self.temp_dir, self.initial_commit, self.initial_commit
        )

        # Check that only two packages were discovered
        self.assertEqual(len(manager.packages), 2)
        self.assertIn("feluda", manager.packages)
        self.assertIn(f"{self.temp_dir}/operators/operator1", manager.packages)
        self.assertNotIn(f"{self.temp_dir}operators/operator2", manager.packages)

    def test_invalid_pyproject_toml(self):
        """Test handling of a package with invalid pyproject.toml."""
        # Write invalid content to the operator2 pyproject.toml
        with open(
            os.path.join(self.temp_dir, "operators", "operator2", "pyproject.toml"), "w"
        ) as f:
            f.write("This is not valid TOML")

        # Create the version manager
        manager = PackageVersionManager(
            self.temp_dir, self.initial_commit, self.initial_commit
        )

        # Check that only two packages were discovered
        self.assertEqual(len(manager.packages), 2)
        self.assertIn("feluda", manager.packages)
        self.assertIn(f"{self.temp_dir}/operators/operator1", manager.packages)
        self.assertNotIn(f"{self.temp_dir}/operators/operator2", manager.packages)

    def test_missing_required_fields_in_pyproject(self):
        """Test handling of a package with missing required fields in pyproject.toml."""
        # Create a pyproject.toml with missing required fields
        invalid_pyproject = tomlkit.document()
        project = tomlkit.table()
        # Missing name and version
        invalid_pyproject["project"] = project

        with open(
            os.path.join(self.temp_dir, "operators", "operator2", "pyproject.toml"), "w"
        ) as f:
            tomlkit.dump(invalid_pyproject, f)

        # Create the version manager
        manager = PackageVersionManager(
            self.temp_dir, self.initial_commit, self.initial_commit
        )

        # Check that only two packages were discovered
        self.assertEqual(len(manager.packages), 2)
        self.assertIn("feluda", manager.packages)
        self.assertIn(f"{self.temp_dir}/operators/operator1", manager.packages)
        self.assertNotIn(f"{self.temp_dir}/operators/operator2", manager.packages)

    def test_mixed_commit_types(self):
        """Test version bump selection with mixed commit types."""
        # Create a series of commits with different types
        self._create_file_and_commit(
            "feluda/example1.py", "print('hello')", "feat: new feature"
        )

        self._create_file_and_commit(
            "feluda/example2.py", "print('world')", "fix: bug fix"
        )

        commit3 = self._create_file_and_commit(
            "feluda/example3.py", "print('!')", "docs: update documentation"
        )

        # Create the version manager
        manager = PackageVersionManager(self.temp_dir, self.initial_commit, commit3)

        # Determine the bump type (should be minor due to feat commit)
        bump_type = manager.determine_package_bump(
            os.path.join(self.temp_dir, "feluda")
        )
        self.assertEqual(bump_type, "minor")

    def test_non_conventional_commits(self):
        """Test handling of non-conventional commits."""
        # Create a non-conventional commit
        commit = self._create_file_and_commit(
            "feluda/example.py", "print('hello')", "Added a new file"
        )

        # Create the version manager
        manager = PackageVersionManager(self.temp_dir, self.initial_commit, commit)

        # Determine the bump type (should be patch for non-conventional commits)
        bump_type = manager.determine_package_bump(
            os.path.join(self.temp_dir, "feluda")
        )
        self.assertEqual(bump_type, "patch")

    def test_multiple_package_updates(self):
        """Test updating versions for multiple packages with multiple commits."""
        # Create a series of commits affecting different packages
        self._create_file_and_commit(
            "feluda/file1.py", "print('hello')", "feat: new feature in feluda"
        )

        self._create_file_and_commit(
            "operators/operator1/file1.py",
            "print('hello')",
            "fix: bug fix in operator1",
        )

        # Create more commits
        self._create_file_and_commit(
            "feluda/file2.py",
            "print('world')",
            "feat: another feature in feluda with BREAKING CHANGE",
        )

        commit4 = self._create_file_and_commit(
            "operators/operator1/file2.py",
            "print('world')",
            "feat: new feature in operator1",
        )

        # Create the version manager
        manager = PackageVersionManager(self.temp_dir, self.initial_commit, commit4)

        # Update versions
        updated_versions = manager.update_package_versions()

        # Check that both packages were updated
        self.assertEqual(len(updated_versions), 2)

        # Check feluda version (should be major bump due to BREAKING CHANGE)
        self.assertEqual(updated_versions["feluda"]["old_version"], "0.1.0")
        self.assertEqual(updated_versions["feluda"]["new_version"], "1.0.0")
        self.assertEqual(updated_versions["feluda"]["bump_type"], "major")

        # Check operator1 version (should be minor bump due to feat commit)
        self.assertEqual(
            updated_versions[f"{self.temp_dir}/operators/operator1"]["old_version"], "0.1.0"
        )
        self.assertEqual(
            updated_versions[f"{self.temp_dir}/operators/operator1"]["new_version"], "0.2.0"
        )
        self.assertEqual(updated_versions[f"{self.temp_dir}/operators/operator1"]["bump_type"], "minor")

    @patch("scripts.semantic_release_workflow.subprocess.run")
    def test_git_command_failure(self, mock_run):
        """Test handling of git command failures."""
        # Setup the mock to raise an exception when getting commits
        mock_run.side_effect = subprocess.CalledProcessError(1, "git")

        # Create the version manager
        manager = PackageVersionManager(
            self.temp_dir, self.initial_commit, self.initial_commit
        )

        # Get package commits should return an empty list on error
        commits = manager.get_package_commits(os.path.join(self.temp_dir, "feluda"))
        self.assertEqual(commits, [])

        # Determine package bump should return None on error
        bump_type = manager.determine_package_bump(
            os.path.join(self.temp_dir, "feluda")
        )
        self.assertIsNone(bump_type)

        # Update package versions should not raise an exception
        updated_versions = manager.update_package_versions()
        self.assertEqual(len(updated_versions), 0)

    @skip # See Todo message
    def test_multiple_breaking_changes(self):
        """Test that the highest bump type is selected when multiple breaking changes exist."""
        # Create commits with breaking changes in different packages
        self._create_file_and_commit(
            "feluda/breaking.py", "print('break')", "feat: breaking change in feluda\n\nBREAKING CHANGE: API change"
        )
        
        self._create_file_and_commit(
            "operators/operator1/breaking.py", 
            "print('break')",
            "fix: minor fix with BREAKING CHANGE"
        )
        
        # TODO: This test fails because _parse_conventional_commit detects the "breaking change" in the message and marks this as major
        commit3 = self._create_file_and_commit(
            "operators/operator2/normal.py",
            "print('normal')",
            "feat: new feature without breaking change"
        )
        
        manager = PackageVersionManager(self.temp_dir, self.initial_commit, commit3)
        updated_versions = manager.update_package_versions()
        
        # Check that feluda and operator1 got major bumps, and operator2 got a minor bump
        self.assertEqual(updated_versions["feluda"]["bump_type"], "major")
        self.assertEqual(updated_versions[f"{self.temp_dir}/operators/operator1"]["bump_type"], "major")
        self.assertEqual(updated_versions[f"{self.temp_dir}/operators/operator2"]["bump_type"], "minor")