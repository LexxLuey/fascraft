"""Tests for the enhanced analyze command with documentation integration."""

import json

from fascraft.commands.analyze import (
    analyze_api_docs_quality,
    analyze_changelog_quality,
    analyze_readme_quality,
    extract_version_info,
    generate_doc_suggestions,
    is_semantic_version,
)


class TestDocumentationQualityAnalysis:
    """Test documentation quality analysis functionality."""

    def test_analyze_readme_quality_basic(self, tmp_path):
        """Test README quality analysis with basic content."""
        readme_file = tmp_path / "README.md"
        readme_file.write_text(
            "# Test Project\n\n## Installation\n```bash\npip install test\n```"
        )

        score = analyze_readme_quality(readme_file)
        assert score >= 30
        assert score <= 100

    def test_analyze_changelog_quality_comprehensive(self, tmp_path):
        """Test changelog quality analysis with comprehensive content."""
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
        changelog_file = tmp_path / "CHANGELOG.md"
        changelog_file.write_text(changelog_content)

        score = analyze_changelog_quality(changelog_file)
        assert score == 100

    def test_analyze_api_docs_quality_with_openapi(self, tmp_path):
        """Test API documentation quality analysis with OpenAPI spec."""
        openapi_content = {
            "openapi": "3.0.0",
            "info": {"title": "Test API", "version": "1.0.0"},
            "paths": {"/health": {"get": {"summary": "Health check"}}},
            "components": {"schemas": {"HealthResponse": {"type": "object"}}},
        }

        openapi_file = tmp_path / "openapi.json"
        openapi_file.write_text(json.dumps(openapi_content))

        score = analyze_api_docs_quality(tmp_path)
        assert score == 100


class TestVersionInformationExtraction:
    """Test version information extraction functionality."""

    def test_extract_version_info_from_pyproject(self, tmp_path):
        """Test version extraction from pyproject.toml."""
        pyproject_content = """[tool.poetry]
name = "test-project"
version = "1.2.3"
description = "Test project"
"""
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(pyproject_content)

        version_info = extract_version_info(tmp_path)
        assert version_info["pyproject_version"] == "1.2.3"
        assert version_info["latest_version"] == "1.2.3"

    def test_extract_version_info_consistency(self, tmp_path):
        """Test version consistency checking."""
        pyproject_content = """[tool.poetry]
version = "1.0.0"
"""
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(pyproject_content)

        readme_content = """# Test Project
Version: 2.0.0
"""
        readme_file = tmp_path / "README.md"
        readme_file.write_text(readme_content)

        version_info = extract_version_info(tmp_path)
        assert version_info["version_consistency"] is False
        assert version_info["latest_version"] == "2.0.0"


class TestSemanticVersionValidation:
    """Test semantic version validation functionality."""

    def test_valid_semantic_versions(self):
        """Test valid semantic version strings."""
        valid_versions = ["1.0.0", "2.1.3", "1.0.0-alpha", "1.0.0+20130313144700"]

        for version in valid_versions:
            assert is_semantic_version(version), f"Version {version} should be valid"

    def test_invalid_semantic_versions(self):
        """Test invalid semantic version strings."""
        invalid_versions = ["1.0", "1.0.0.0", "v1.0.0"]

        for version in invalid_versions:
            assert not is_semantic_version(
                version
            ), f"Version {version} should be invalid"


class TestDocumentationSuggestions:
    """Test documentation improvement suggestions generation."""

    def test_generate_doc_suggestions_missing_readme(self):
        """Test suggestions when README is missing."""
        doc_analysis = {
            "has_readme": False,
            "has_changelog": True,
            "has_api_docs": True,
            "has_project_docs": False,
            "has_module_docs": False,
            "docs_directory": False,
            "readme_quality": 0,
            "changelog_quality": 90,
            "api_docs_quality": 85,
            "version_info": {"version_consistency": True},
        }

        suggestions = generate_doc_suggestions(doc_analysis)
        assert "Create a comprehensive README.md file" in suggestions

    def test_generate_doc_suggestions_no_issues(self):
        """Test suggestions when documentation is comprehensive."""
        doc_analysis = {
            "has_readme": True,
            "has_changelog": True,
            "has_api_docs": True,
            "has_project_docs": True,
            "has_module_docs": True,
            "docs_directory": True,
            "readme_quality": 95,
            "changelog_quality": 95,
            "api_docs_quality": 95,
            "version_info": {"version_consistency": True},
        }

        suggestions = generate_doc_suggestions(doc_analysis)
        assert len(suggestions) == 0
