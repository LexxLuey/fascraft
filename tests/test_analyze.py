"""Tests for the analyze command functionality."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import typer

from fascraft.commands.analyze import (
    analyze_project,
    analyze_project_structure,
    display_analysis_results,
    provide_recommendations,
    is_fastapi_project,
    analyze_config_directory,
    analyze_main_py,
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
        assert "Consider converting to domain-driven architecture" in analysis["suggestions"]


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
        main_py.write_text("""
from fastapi import FastAPI
from customers import routers as customer_routers
from products import routers as product_routers

app = FastAPI()
app.include_router(customer_routers.router, prefix="/api/v1/customers")
app.include_router(product_routers.router, prefix="/api/v1/products")
""")
        
        analysis = analyze_main_py(main_py)
        
        assert analysis["has_fastapi_import"] is True
        assert analysis["has_router_includes"] is True
        assert analysis["router_count"] == 2

    def test_analyze_main_py_basic(self, tmp_path):
        """Test analysis of basic main.py."""
        main_py = tmp_path / "main.py"
        main_py.write_text("""
from fastapi import FastAPI

app = FastAPI()
""")
        
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
            "structure": {
                "config": {
                    "has_settings": True,
                    "has_database": True
                }
            },
            "modules": ["customers", "products"],
            "config_files": ["fascraft.toml", ".env"],
            "suggestions": ["Convert to domain-driven architecture"],
            "missing_components": []  # Add missing key
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
            "structure": {}  # Add empty structure to avoid KeyError
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
        with patch("fascraft.commands.analyze.analyze_project_structure") as mock_analyze:
            with patch("fascraft.commands.analyze.display_analysis_results") as mock_display:
                with patch("fascraft.commands.analyze.provide_recommendations") as mock_recommend:
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
