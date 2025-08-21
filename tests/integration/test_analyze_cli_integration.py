"""Tests for the CLI integration of the enhanced analyze command."""

from unittest.mock import patch

import fascraft.commands.analyze as analyze_module


class TestAnalyzeCLIIntegration:
    """Test the CLI integration of the analyze command."""

    def test_analyze_project_docs_only_option(self, tmp_path):
        """Test the --docs-only option for documentation-only analysis."""
        # Create a valid FastAPI project
        main_py = tmp_path / "main.py"
        main_py.write_text("from fastapi import FastAPI\napp = FastAPI()")

        # Create some documentation files
        readme_file = tmp_path / "README.md"
        readme_file.write_text("# Test Project\n\n## Installation")

        # Mock the documentation analysis function
        with patch(
            "fascraft.commands.analyze.analyze_documentation_quality"
        ) as mock_doc_analysis:
            with patch(
                "fascraft.commands.analyze.display_documentation_analysis"
            ) as mock_display:
                with patch("fascraft.commands.analyze.console.print") as mock_console:
                    mock_doc_analysis.return_value = {
                        "has_readme": True,
                        "has_changelog": False,
                        "has_api_docs": False,
                        "has_project_docs": False,
                        "has_module_docs": False,
                        "docs_directory": False,
                        "readme_quality": 70,
                        "changelog_quality": 0,
                        "api_docs_quality": 0,
                        "missing_docs": ["CHANGELOG.md", "API Documentation"],
                        "doc_suggestions": ["Add a CHANGELOG.md file"],
                        "version_info": {"version_consistency": True},
                    }

                    # Call with docs_only=True
                    analyze_module.analyze_project(
                        path=str(tmp_path), docs_only=True, version_report=False
                    )

                    # Verify documentation analysis was called
                    mock_doc_analysis.assert_called_once_with(tmp_path)
                    mock_display.assert_called_once()
                    mock_console.assert_called()

    def test_analyze_project_version_report_option(self, tmp_path):
        """Test the --version-report option for version consistency analysis."""
        # Create a valid FastAPI project
        main_py = tmp_path / "main.py"
        main_py.write_text("from fastapi import FastAPI\napp = FastAPI()")

        # Mock the version report function
        with patch(
            "fascraft.commands.analyze.generate_documentation_version_report"
        ) as mock_version_report:
            with patch(
                "fascraft.commands.analyze.display_version_report"
            ) as mock_display:
                with patch("fascraft.commands.analyze.console.print") as mock_console:
                    mock_version_report.return_value = {
                        "timestamp": "2024-01-01T00:00:00",
                        "project_path": str(tmp_path),
                        "version_sources": {
                            "pyproject.toml": "1.0.0",
                            "README.md": "1.0.0",
                        },
                        "consistency_issues": [],
                        "recommendations": [],
                    }

                    # Call with version_report=True
                    analyze_module.analyze_project(
                        path=str(tmp_path), docs_only=False, version_report=True
                    )

                    # Verify version report was called
                    mock_version_report.assert_called_once_with(tmp_path)
                    mock_display.assert_called_once()
                    mock_console.assert_called()

    def test_analyze_project_full_analysis_with_docs(self, tmp_path):
        """Test full project analysis including documentation analysis."""
        # Create a valid FastAPI project
        main_py = tmp_path / "main.py"
        main_py.write_text("from fastapi import FastAPI\napp = FastAPI()")

        # Mock all the analysis functions
        with patch(
            "fascraft.commands.analyze.analyze_project_structure"
        ) as mock_structure:
            with patch(
                "fascraft.commands.analyze.display_analysis_results"
            ) as mock_display:
                with patch(
                    "fascraft.commands.analyze.provide_recommendations"
                ) as mock_recommend:
                    mock_structure.return_value = {
                        "project_name": "test",
                        "structure": {},
                        "modules": [],
                        "routers": [],
                        "config_files": [],
                        "missing_components": [],
                        "suggestions": [],
                        "main_py": {},
                        "documentation": {
                            "has_readme": True,
                            "has_changelog": False,
                            "has_api_docs": False,
                            "has_project_docs": False,
                            "has_module_docs": False,
                            "docs_directory": False,
                            "readme_quality": 70,
                            "changelog_quality": 0,
                            "api_docs_quality": 0,
                            "missing_docs": [],
                            "doc_suggestions": ["Add a CHANGELOG.md file"],
                            "version_info": {"version_consistency": True},
                        },
                    }

                    # Call without any special options (full analysis)
                    analyze_module.analyze_project(
                        path=str(tmp_path), docs_only=False, version_report=False
                    )

                    # Verify all analysis functions were called
                    mock_structure.assert_called_once_with(tmp_path)
                    mock_display.assert_called_once()
                    mock_recommend.assert_called_once()

    def test_analyze_project_option_priority(self, tmp_path):
        """Test that version_report takes priority over docs_only."""
        # Create a valid FastAPI project
        main_py = tmp_path / "main.py"
        main_py.write_text("from fastapi import FastAPI\napp = FastAPI()")

        # Mock the version report function
        with patch(
            "fascraft.commands.analyze.generate_documentation_version_report"
        ) as mock_version_report:
            with patch(
                "fascraft.commands.analyze.analyze_documentation_quality"
            ) as mock_doc_analysis:
                mock_version_report.return_value = {
                    "timestamp": "2024-01-01T00:00:00",
                    "project_path": str(tmp_path),
                    "version_sources": {},
                    "consistency_issues": [],
                    "recommendations": [],
                }

                # Call with both options - version_report should take priority
                analyze_module.analyze_project(
                    path=str(tmp_path), docs_only=True, version_report=True
                )

                # Verify only version report was called
                mock_version_report.assert_called_once_with(tmp_path)
                mock_doc_analysis.assert_not_called()
