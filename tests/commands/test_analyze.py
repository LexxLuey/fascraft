"""Tests for the analyze command functionality."""

from unittest.mock import patch

import pytest
import typer

from fascraft.commands.analyze import (
    analyze_changelog_quality,
    analyze_config_directory,
    analyze_documentation_quality,
    analyze_main_py,
    analyze_project,
    analyze_project_structure,
    analyze_readme_quality,
    display_analysis_results,
    extract_version_info,
    is_fastapi_project,
    provide_recommendations,
)


class TestIsFastApiProject:
    """Test the is_fastapi_project function."""

    def test_is_fastapi_project_valid_main_py(self, tmp_path):
        """Test that a valid FastAPI project with main.py is correctly identified."""
        # Create main.py with FastAPI content
        main_py = tmp_path / "main.py"
        main_py.write_text("from fastapi import FastAPI\napp = FastAPI()")

        assert is_fastapi_project(tmp_path) is True

    def test_is_fastapi_project_valid_pyproject_toml(self, tmp_path):
        """Test that a valid FastAPI project with pyproject.toml is correctly identified."""
        # Create pyproject.toml with FastAPI dependency
        pyproject_toml = tmp_path / "pyproject.toml"
        pyproject_toml.write_text("[tool.poetry.dependencies]\nfastapi = '^0.104.0'")

        assert is_fastapi_project(tmp_path) is True

    def test_is_fastapi_project_invalid(self, tmp_path):
        """Test that an invalid project is not identified as FastAPI."""
        # Create empty directory
        assert is_fastapi_project(tmp_path) is False

        # Create main.py without FastAPI
        main_py = tmp_path / "main.py"
        main_py.write_text("print('Hello World')")
        assert is_fastapi_project(tmp_path) is False


class TestAnalyzeProjectStructure:
    """Test the analyze_project_structure function."""

    def test_analyze_project_structure_basic(self, tmp_path):
        """Test basic project structure analysis."""
        # Create a basic project structure
        (tmp_path / "config").mkdir()
        (tmp_path / "config" / "settings.py").write_text("# settings")
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")

        analysis = analyze_project_structure(tmp_path)

        assert analysis["project_name"] == tmp_path.name
        assert "config" in analysis["structure"]
        assert analysis["structure"]["config"]["has_settings"] is True

    def test_analyze_project_structure_with_modules(self, tmp_path):
        """Test project structure analysis with domain modules."""
        # Create domain modules
        customers_dir = tmp_path / "customers"
        customers_dir.mkdir()
        (customers_dir / "__init__.py").write_text("")
        (customers_dir / "models.py").write_text("# models")

        products_dir = tmp_path / "products"
        products_dir.mkdir()
        (products_dir / "__init__.py").write_text("")
        (products_dir / "models.py").write_text("# models")

        analysis = analyze_project_structure(tmp_path)

        assert "customers" in analysis["modules"]
        assert "products" in analysis["modules"]
        assert len(analysis["modules"]) == 2

    def test_analyze_project_structure_flat_structure(self, tmp_path):
        """Test detection of flat structure projects."""
        # Create flat structure indicators
        (tmp_path / "models").mkdir()
        (tmp_path / "schemas").mkdir()
        (tmp_path / "routers").mkdir()

        analysis = analyze_project_structure(tmp_path)

        assert analysis["structure"].get("flat_structure") is True
        assert (
            "Consider converting to domain-driven architecture"
            in analysis["suggestions"]
        )


class TestAnalyzeConfigDirectory:
    """Test the analyze_config_directory function."""

    def test_analyze_config_directory_complete(self, tmp_path):
        """Test analysis of complete config directory."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        (config_dir / "settings.py").write_text("# settings")
        (config_dir / "database.py").write_text("# database")
        (config_dir / "exceptions.py").write_text("# exceptions")
        (config_dir / "middleware.py").write_text("# middleware")

        analysis = analyze_config_directory(config_dir)

        assert analysis["has_settings"] is True
        assert analysis["has_database"] is True
        assert "exceptions.py" in analysis["files"]
        assert "middleware.py" in analysis["files"]

    def test_analyze_config_directory_partial(self, tmp_path):
        """Test analysis of partial config directory."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        (config_dir / "settings.py").write_text("# settings")
        (config_dir / "database.py").write_text("# database")

        analysis = analyze_config_directory(config_dir)

        assert analysis["has_settings"] is True
        assert analysis["has_database"] is True
        assert "exceptions.py" not in analysis["files"]
        assert "middleware.py" not in analysis["files"]


class TestAnalyzeMainPy:
    """Test the analyze_main_py function."""

    def test_analyze_main_py_with_routers(self, tmp_path):
        """Test analysis of main.py with router includes."""
        main_py = tmp_path / "main.py"
        main_py.write_text(
            """
from fastapi import FastAPI
from customers import routers as customer_routers
from products import routers as product_routers

app = FastAPI()
app.include_router(customer_routers.router, prefix="/api/v1/customers")
app.include_router(product_routers.router, prefix="/api/v1/products")
"""
        )

        analysis = analyze_main_py(main_py)

        assert analysis["has_fastapi_import"] is True
        assert analysis["has_router_includes"] is True
        assert analysis["router_count"] == 2

    def test_analyze_main_py_basic(self, tmp_path):
        """Test analysis of basic main.py."""
        main_py = tmp_path / "main.py"
        main_py.write_text(
            """
from fastapi import FastAPI

app = FastAPI()
"""
        )

        analysis = analyze_main_py(main_py)

        assert analysis["has_fastapi_import"] is True
        assert analysis["has_router_includes"] is False
        assert analysis["router_count"] == 0


class TestDisplayAnalysisResults:
    """Test the display_analysis_results function."""

    @patch("fascraft.commands.analyze.console.print")
    def test_display_analysis_results(self, mock_print, tmp_path):
        """Test that analysis results are displayed correctly."""
        analysis = {
            "project_name": "test-project",
            "structure": {"config": {"has_settings": True, "has_database": True}},
            "modules": ["customers", "products"],
            "config_files": ["fascraft.toml", ".env"],
            "suggestions": ["Convert to domain-driven architecture"],
            "missing_components": [],  # Add missing key
        }

        display_analysis_results(analysis)

        # Verify that console.print was called multiple times
        assert mock_print.call_count > 0


class TestProvideRecommendations:
    """Test the provide_recommendations function."""

    @patch("fascraft.commands.analyze.console.print")
    def test_provide_recommendations(self, mock_print, tmp_path):
        """Test that recommendations are provided correctly."""
        analysis = {
            "suggestions": ["Convert to domain-driven architecture"],
            "missing_components": ["config/settings.py"],
            "modules": ["customers"],
            "config_files": ["fascraft.toml"],
            "structure": {},  # Add empty structure to avoid KeyError
        }

        provide_recommendations(analysis)

        # Verify that console.print was called
        assert mock_print.call_count > 0


class TestAnalyzeProject:
    """Test the analyze_project function."""

    def test_analyze_project_success(self, tmp_path):
        """Test successful project analysis."""
        # Create a valid FastAPI project
        main_py = tmp_path / "main.py"
        main_py.write_text("from fastapi import FastAPI\napp = FastAPI()")

        # Mock the analysis functions to avoid complex logic
        with patch(
            "fascraft.commands.analyze.analyze_project_structure"
        ) as mock_analyze:
            with patch(
                "fascraft.commands.analyze.display_analysis_results"
            ) as mock_display:
                with patch(
                    "fascraft.commands.analyze.provide_recommendations"
                ) as mock_recommend:
                    mock_analyze.return_value = {"project_name": "test"}

                    analyze_project(str(tmp_path))

                    mock_analyze.assert_called_once()
                    mock_display.assert_called_once()
                    mock_recommend.assert_called_once()

    def test_analyze_project_invalid_path(self):
        """Test analysis with invalid path."""
        with pytest.raises(typer.Exit) as exc_info:
            analyze_project("/nonexistent/path")

        # Check that it's an exit exception
        exception = exc_info.value
        assert isinstance(exception, typer.Exit)

    def test_analyze_project_not_fastapi(self, tmp_path):
        """Test analysis of non-FastAPI project."""
        # Create a non-FastAPI project
        main_py = tmp_path / "main.py"
        main_py.write_text("print('Hello World')")

        with pytest.raises(typer.Exit) as exc_info:
            analyze_project(str(tmp_path))

        # Check that it's an exit exception
        exception = exc_info.value
        assert isinstance(exception, typer.Exit)


class TestDocumentationAnalysis:
    """Test the documentation analysis functionality."""

    def test_analyze_readme_quality(self, tmp_path):
        """Test README quality analysis."""
        readme_file = tmp_path / "README.md"
        readme_content = """# Test Project

## Installation
```bash
pip install test
```

## API Endpoints
- GET /health
"""
        readme_file.write_text(readme_content)

        score = analyze_readme_quality(readme_file)
        assert score >= 40  # Should have title, sections, code blocks, and API info
        assert score <= 100

    def test_analyze_changelog_quality(self, tmp_path):
        """Test changelog quality analysis."""
        changelog_file = tmp_path / "CHANGELOG.md"
        changelog_content = """# Changelog

## [1.0.0] - 2024-01-01

### Added
- Initial release

### Changed
- Updated dependencies

### Fixed
- Bug fixes

### Security
- Security updates
"""
        changelog_file.write_text(changelog_content)

        score = analyze_changelog_quality(changelog_file)
        assert score == 100  # Should have all categories

    def test_extract_version_info(self, tmp_path):
        """Test version information extraction."""
        # Create pyproject.toml
        pyproject_content = """[tool.poetry]
name = "test-project"
version = "1.2.3"
"""
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(pyproject_content)

        # Create README with version
        readme_content = """# Test Project
Version: 1.2.3
"""
        readme_file = tmp_path / "README.md"
        readme_file.write_text(readme_content)

        version_info = extract_version_info(tmp_path)
        assert version_info["pyproject_version"] == "1.2.3"
        assert version_info["readme_version"] == "1.2.3"
        assert version_info["version_consistency"] is True
        assert version_info["latest_version"] == "1.2.3"

    def test_analyze_documentation_quality_integration(self, tmp_path):
        """Test integration of documentation quality analysis."""
        # Create project structure
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")
        (tmp_path / "README.md").write_text("# Test Project\n\n## Installation")
        (tmp_path / "CHANGELOG.md").write_text("## [1.0.0]\n\n### Added\n- Feature")

        doc_analysis = analyze_documentation_quality(tmp_path)

        assert doc_analysis["has_readme"] is True
        assert doc_analysis["has_changelog"] is True
        assert doc_analysis["readme_quality"] > 0
        assert doc_analysis["changelog_quality"] > 0
        assert "API Documentation" in doc_analysis["missing_docs"]
