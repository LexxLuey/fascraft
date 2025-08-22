"""Tests for fascraft/templates/new_project/config/exceptions.py.jinja2."""

from pathlib import Path


class TestExceptionsTemplate:
    """Test class for exceptions.py.jinja2 template."""

    def test_exceptions_template_exists(self):
        """Test that exceptions.py.jinja2 template file exists."""
        template_path = Path(
            "fascraft/templates/new_project/config/exceptions.py.jinja2"
        )
        assert template_path.exists(), "Exceptions template file should exist"

    def test_exceptions_template_content_structure(self):
        """Test exceptions.py.jinja2 template content structure."""
        template_path = Path(
            "fascraft/templates/new_project/config/exceptions.py.jinja2"
        )
        content = template_path.read_text(encoding="utf-8")

        # Test template variables exist
        assert (
            "{{ project_name }}" in content
        ), "Template should contain project_name variable"

        # Test imports
        assert "from fastapi import HTTPException, status" in content

        # Test base exception class
        assert "class FasCraftException(HTTPException):" in content
        assert "def __init__(" in content
        assert "super().__init__(" in content

        # Test specific exception classes
        assert "class ValidationError(FasCraftException):" in content
        assert "class NotFoundError(FasCraftException):" in content
        assert "class ConflictError(FasCraftException):" in content

    def test_exceptions_template_status_codes(self):
        """Test exceptions.py.jinja2 template HTTP status code assignments."""
        template_path = Path(
            "fascraft/templates/new_project/config/exceptions.py.jinja2"
        )
        content = template_path.read_text(encoding="utf-8")

        # Test status code assignments
        assert "status.HTTP_500_INTERNAL_SERVER_ERROR" in content
        assert "status.HTTP_422_UNPROCESSABLE_ENTITY" in content
        assert "status.HTTP_404_NOT_FOUND" in content
        assert "status.HTTP_409_CONFLICT" in content

    def test_exceptions_template_inheritance(self):
        """Test exceptions.py.jinja2 template class inheritance structure."""
        template_path = Path(
            "fascraft/templates/new_project/config/exceptions.py.jinja2"
        )
        content = template_path.read_text(encoding="utf-8")

        # Test inheritance chain
        assert "class ValidationError(FasCraftException):" in content
        assert "class NotFoundError(FasCraftException):" in content
        assert "class ConflictError(FasCraftException):" in content

        # Test all inherit from FasCraftException
        assert (
            content.count("class FasCraftException") == 1
        ), "Should have one base class"
        assert (
            content.count("(FasCraftException)") == 3
        ), "Should have three child classes"

    def test_exceptions_template_method_signatures(self):
        """Test exceptions.py.jinja2 template method signatures."""
        template_path = Path(
            "fascraft/templates/new_project/config/exceptions.py.jinja2"
        )
        content = template_path.read_text(encoding="utf-8")

        # Test constructor parameters
        assert "detail: str" in content
        assert "status_code: int" in content
        assert "headers: dict" in content

        # Test method definitions
        assert "def __init__(" in content
        assert "detail=detail" in content
        assert "status_code=status_code" in content

    def test_exceptions_template_line_coverage(self):
        """Test exceptions.py.jinja2 template covers all lines including missing ones."""
        template_path = Path(
            "fascraft/templates/new_project/config/exceptions.py.jinja2"
        )
        content = template_path.read_text(encoding="utf-8")

        # Test specific missing lines from coverage report
        lines = content.split("\n")

        # Line 3: Import statement
        assert "from fastapi import HTTPException, status" in content

        # Line 15-42: Various exception classes and methods
        assert "class FasCraftException(HTTPException):" in content
        assert "def __init__(" in content
        assert "detail: str" in content
        assert "status_code: int" in content
        assert "headers: dict" in content
        assert "super().__init__(" in content
        assert "detail=detail" in content
        assert "status_code=status_code" in content
        assert "class ValidationError(FasCraftException):" in content
        assert "status.HTTP_422_UNPROCESSABLE_ENTITY" in content
        assert "class NotFoundError(FasCraftException):" in content
        assert "status.HTTP_404_NOT_FOUND" in content
        assert "class ConflictError(FasCraftException):" in content
        assert "status.HTTP_409_CONFLICT" in content

        # Verify we're testing the right content
        assert len(lines) >= 42, "Template should have at least 42 lines"
