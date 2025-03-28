import unittest
import os
from unittest.mock import patch, mock_open, MagicMock
from semantic_release_workflow import PackageVersionManager


class TestPackageVersionManager(unittest.TestCase):

    @patch("os.path.exists", return_value=True)
    def setUp(self, mock_exists):
        """Set up a mock environment for testing."""
        self.repo_root = os.getcwd()  # Use actual test directory
        self.prev_commit = "abc123"
        self.current_commit = "def456"
        self.manager = PackageVersionManager(self.repo_root, self.prev_commit, self.current_commit)

    def test_discover_packages(self):
        """Test package discovery."""
        # Mock the file system and pyproject.toml contents
        with patch("os.path.exists") as mock_exists, \
             patch("os.path.isdir") as mock_isdir, \
             patch("glob.glob") as mock_glob, \
             patch("builtins.open", mock_open(read_data="""
                [project]
                name = "test_pkg"
                version = "1.0.0"

                [tool.semantic_release.branches.main]
                tag_format = "v{version}"
             """)) as mock_file:

            # Setup mock responses
            def exists_side_effect(path):
                if "pyproject.toml" in path:
                    return True
                if path.endswith("operators"):
                    return True
                return False

            mock_exists.side_effect = exists_side_effect
            mock_isdir.return_value = True
            mock_glob.return_value = [os.path.join("operators", "test_pkg", "pyproject.toml")]

            packages = self.manager._discover_packages()
            self.assertIn("operators/test_pkg", packages)
            self.assertEqual(packages["operators/test_pkg"]["current_version"], "1.0.0")

    @patch("semantic_release_workflow.subprocess.run")
    @patch("semantic_release_workflow.PackageVersionManager._get_tag_format", return_value="v{version}")
    def test_tag_exists(self, mock_get_tag_format, mock_subprocess):
        """Test if a tag exists."""
        mock_subprocess.return_value = MagicMock(stdout="v1.2.3\nv1.2.4\n")
        package_info = {
            "pyproject_data": {
                "project": {"name": "pkg1"},
                "tool": {"semantic_release": {"branches": {"main": {"tag_format": "v{version}"}}}},
            },
            "current_version": "1.2.3",
        }
        self.assertTrue(self.manager.tag_exists(package_info, "1.2.3"))

    def test_bump_version(self):
        """Test bumping a version."""
        # Test major bump
        self.assertEqual(self.manager._bump_version("1.2.3", "major"), "2.0.0")
        # Test minor bump
        self.assertEqual(self.manager._bump_version("1.2.3", "minor"), "1.3.0")
        # Test patch bump
        self.assertEqual(self.manager._bump_version("1.2.3", "patch"), "1.2.4")
        # Test no bump
        self.assertEqual(self.manager._bump_version("1.2.3", None), "1.2.3")

    def test_parse_conventional_commit(self):
        """Test commit message parsing."""
        # Test feature commit
        self.assertEqual(self.manager._parse_conventional_commit("feat: new feature"), "minor")
        # Test fix commit
        self.assertEqual(self.manager._parse_conventional_commit("fix: bug fix"), "patch")
        # Test breaking change
        self.assertEqual(self.manager._parse_conventional_commit("feat!: breaking change"), "major")
        # Test chore commit
        self.assertEqual(self.manager._parse_conventional_commit("chore: update deps"), "patch")
        # Test invalid commit
        self.assertEqual(self.manager._parse_conventional_commit("random message"), "patch")
        # Test empty commit
        self.assertIsNone(self.manager._parse_conventional_commit(""))

    @patch("semantic_release_workflow.subprocess.run")
    def test_get_package_commits(self, mock_run):
        """Test getting commits for a package."""
        mock_run.return_value = MagicMock(stdout="feat: new feature\nfix: bug fix\n")
        commits = self.manager.get_package_commits("some/package/path")
        self.assertEqual(len(commits), 2)
        self.assertIn("feat: new feature", commits)
        self.assertIn("fix: bug fix", commits)


if __name__ == "__main__":
    unittest.main()