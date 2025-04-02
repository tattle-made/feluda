import tempfile
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

# Import the script functions to test
from scripts.toml_dependencies_update_script import (
    find_pyproject_files,
    load_lock_file,
    update_dependencies_list,
    update_dependency_version,
    update_pyproject_versions,
)


class TestPyprojectFileFinder(unittest.TestCase):
    """Test the find_pyproject_files function."""

    def setUp(self):
        # Create temporary directory structure for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)

        # Create some test pyproject.toml files
        (self.test_dir / "pyproject.toml").touch()
        (self.test_dir / "project1").mkdir()
        (self.test_dir / "project1" / "pyproject.toml").touch()
        (self.test_dir / "project2").mkdir()
        (self.test_dir / "project2" / "pyproject.toml").touch()

        # Create ignored directories with pyproject files
        (self.test_dir / ".venv").mkdir()
        (self.test_dir / ".venv" / "pyproject.toml").touch()
        (self.test_dir / "dist").mkdir()
        (self.test_dir / "dist" / "pyproject.toml").touch()
        (self.test_dir / "__pycache__").mkdir()
        (self.test_dir / "__pycache__" / "pyproject.toml").touch()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_find_pyproject_files(self):
        """Test that pyproject.toml files are found correctly."""
        files = find_pyproject_files(self.test_dir)

        # Should find 3 files (root, project1, project2)
        self.assertEqual(len(files), 3)

        # Check that the files are the ones we expect
        file_paths = [str(f) for f in files]
        self.assertTrue(str(self.test_dir / "pyproject.toml") in file_paths)
        self.assertTrue(
            str(self.test_dir / "project1" / "pyproject.toml") in file_paths
        )
        self.assertTrue(
            str(self.test_dir / "project2" / "pyproject.toml") in file_paths
        )

        # Check that ignored directories are not included
        self.assertFalse(str(self.test_dir / ".venv" / "pyproject.toml") in file_paths)
        self.assertFalse(str(self.test_dir / "dist" / "pyproject.toml") in file_paths)
        self.assertFalse(
            str(self.test_dir / "__pycache__" / "pyproject.toml") in file_paths
        )


class TestLockFileParser(unittest.TestCase):
    """Test the load_lock_file function."""

    def test_parse_valid_toml(self):
        """Test parsing a valid TOML lock file."""
        mock_lock_content = """
        [[package]]
        name = "requests"
        version = "2.28.1"

        [[package]]
        name = "pytest"
        version = "7.1.3"
        """

        with patch("builtins.open", mock_open(read_data=mock_lock_content)):
            result = load_lock_file("fake_path.lock")

        self.assertEqual(len(result), 2)
        self.assertEqual(result["requests"], "2.28.1")
        self.assertEqual(result["pytest"], "7.1.3")

    def test_parse_malformed_toml_fallback(self):
        """Test fallback regex parsing for malformed TOML."""
        # This is intentionally malformed TOML but with valid package info for regex to find
        mock_lock_content = """
        [[package]]
        name = "requests"
        version = "2.28.1"
        broken syntax here

        [[package]]
        name = "pytest"
        version = "7.1.3"
        """

        # Mock tomlkit.parse to raise an exception to trigger fallback
        with patch("tomlkit.parse", side_effect=Exception("TOML parse error")):
            with patch("builtins.open", mock_open(read_data=mock_lock_content)):
                result = load_lock_file("fake_path.lock")

        self.assertEqual(len(result), 2)
        self.assertEqual(result["requests"], "2.28.1")
        self.assertEqual(result["pytest"], "7.1.3")

    def test_empty_lock_file(self):
        """Test handling an empty lock file."""
        with patch("builtins.open", mock_open(read_data="")):
            result = load_lock_file("fake_path.lock")

        self.assertEqual(len(result), 0)


class TestDependencyUpdates(unittest.TestCase):
    """Test the dependency update functions."""

    def setUp(self):
        self.package_versions = {
            "requests": "2.28.1",
            "pytest": "7.1.3",
            "numpy": "1.23.3",
            "pandas": "1.5.0",
        }

    def test_update_dependency_no_constraint(self):
        """Test updating a dependency with no version constraint."""
        result = update_dependency_version("requests", self.package_versions)
        self.assertEqual(result, "requests>=2.28.1")

    def test_update_dependency_with_constraint(self):
        """Test updating a dependency with an existing constraint."""
        result = update_dependency_version("requests>=2.26.0", self.package_versions)
        self.assertEqual(result, "requests>=2.28.1")

    def test_update_dependency_equals_constraint(self):
        """Test updating a dependency with an equals constraint."""
        result = update_dependency_version("requests==2.26.0", self.package_versions)
        self.assertEqual(result, "requests==2.28.1")

    def test_update_nonexistent_package(self):
        """Test handling a package not in the versions dictionary."""
        result = update_dependency_version("nonexistent>=1.0.0", self.package_versions)
        self.assertEqual(result, "nonexistent>=1.0.0")

    def test_update_dependencies_list(self):
        """Test updating a list of dependencies."""
        dependencies = [
            "requests>=2.26.0",
            "pytest==7.0.0",
            "nonexistent>=1.0.0",
            "numpy",
        ]

        updated = update_dependencies_list(dependencies, self.package_versions)

        self.assertEqual(updated, 3)  # 3 packages should be updated
        self.assertEqual(dependencies[0], "requests>=2.28.1")
        self.assertEqual(dependencies[1], "pytest==7.1.3")
        self.assertEqual(dependencies[2], "nonexistent>=1.0.0")  # Unchanged
        self.assertEqual(dependencies[3], "numpy>=1.23.3")


class TestPyprojectUpdates(unittest.TestCase):
    """Test updating full pyproject.toml files."""

    def setUp(self):
        self.package_versions = {
            "requests": "2.28.1",
            "pytest": "7.1.3",
            "numpy": "1.23.3",
            "pandas": "1.5.0",
        }

        self.pyproject_content = """
        [project]
        name = "test-project"
        version = "0.1.0"
        dependencies = [
            "requests>=2.26.0",
            "numpy"
        ]

        [project.optional-dependencies]
        test = [
            "pytest==7.0.0"
        ]
        dev = [
            "pandas>=1.4.0",
            "nonexistent>=1.0.0"
        ]
        """

    @patch("builtins.open")
    def test_update_pyproject_versions(self, mock_open_func):
        """Test updating versions in a pyproject.toml file."""
        # Setup mock for file reading
        mock_file = mock_open_func.return_value.__enter__.return_value
        mock_file.read.return_value = self.pyproject_content

        # Execute function
        result = update_pyproject_versions("fake_path.toml", self.package_versions)

        # Check results
        self.assertEqual(result, 4)

        # Check the file was written with updated content
        mock_open_func.assert_called_with("fake_path.toml", "w", encoding="utf-8")

        # Get the written content
        written_calls = mock_file.write.call_args_list
        self.assertEqual(len(written_calls), 1)

        # Convert to string for easier assertions
        written_content = written_calls[0][0][0]

        # Check that dependencies were updated correctly
        self.assertIn('"requests>=2.28.1"', written_content)
        self.assertIn('"numpy>=1.23.3"', written_content)
        self.assertIn('"pytest==7.1.3"', written_content)
        self.assertIn('"pandas>=1.5.0"', written_content)
        self.assertIn('"nonexistent>=1.0.0"', written_content)  # Unchanged

    @patch("builtins.open")
    def test_no_dependencies_to_update(self, mock_open_func):
        """Test handling a file with no dependencies to update."""
        # Setup mock for reading a file with no updateable dependencies
        no_deps_content = """
        [project]
        name = "test-project"
        version = "0.1.0"
        """
        mock_file = mock_open_func.return_value.__enter__.return_value
        mock_file.read.return_value = no_deps_content

        # Execute function
        result = update_pyproject_versions("fake_path.toml", self.package_versions)

        # Check results
        self.assertEqual(result, 0)
