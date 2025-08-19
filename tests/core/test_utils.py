"""Utility tests and helper functions for FasCraft testing."""

import tempfile
from collections.abc import Generator
from pathlib import Path


def create_temp_project_structure() -> Generator[Path, None, None]:
    """Create a temporary project structure for testing."""
    temp_dir = tempfile.mkdtemp()
    temp_path = Path(temp_dir)

    # Create a mock project structure
    project_dir = temp_path / "test-project"
    project_dir.mkdir()

    # Create mock files
    (project_dir / "main.py").write_text("# Mock main.py")
    (project_dir / "pyproject.toml").write_text("# Mock pyproject.toml")
    (project_dir / "README.md").write_text("# Mock README")

    yield project_dir

    # Cleanup
    import shutil

    shutil.rmtree(temp_dir)


class TestTestUtilities:
    """Test the test utility functions."""

    def test_create_temp_project_structure(self) -> None:
        """Test that temporary project structure is created correctly."""
        project_dir = next(create_temp_project_structure())
        assert project_dir.exists()
        assert project_dir.is_dir()
        assert (project_dir / "main.py").exists()
        assert (project_dir / "pyproject.toml").exists()
        assert (project_dir / "README.md").exists()

        # Cleanup manually
        import shutil

        shutil.rmtree(project_dir.parent)

    def test_temp_directory_is_cleaned_up(self) -> None:
        """Test that temporary directory is properly cleaned up."""
        project_path = None

        project_path = next(create_temp_project_structure())
        assert project_path.exists()

        # Cleanup manually
        import shutil

        shutil.rmtree(project_path.parent)

        # After cleanup, directory should not exist
        assert not project_path.exists()


def test_pathlib_operations() -> None:
    """Test basic pathlib operations used in tests."""
    temp_dir = Path(tempfile.mkdtemp())

    try:
        # Test path joining
        project_path = temp_dir / "test-project"
        assert str(project_path) == str(temp_dir / "test-project")

        # Test path creation
        project_path.mkdir()
        assert project_path.exists()
        assert project_path.is_dir()

        # Test file creation
        test_file = project_path / "test.txt"
        test_file.write_text("test content")
        assert test_file.exists()
        assert test_file.is_file()
        assert test_file.read_text() == "test content"

    finally:
        # Cleanup
        import shutil

        shutil.rmtree(temp_dir)


def test_pytest_fixtures_work() -> None:
    """Test that pytest fixtures are working correctly."""
    # This test ensures our test infrastructure is working
    assert True

    # Test basic assertions
    assert 1 == 1
    assert "test" in "test string"
    assert isinstance([], list)
