"""Additional tests for CI/CD module to improve coverage."""

from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from fascraft.commands.ci_cd import (
    check_existing_ci_cd_files,
    create_environment_configs,
    display_setup_instructions,
    display_success_message,
    render_ci_cd_template,
    setup_ci_cd_environments,
    setup_pre_commit_hooks,
)


class TestCICDCoverage:
    """Test CI/CD module functions to improve coverage."""

    def test_check_existing_ci_cd_files_github(self):
        """Test checking existing CI/CD files for GitHub."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.glob", return_value=[Path("workflow.yml")]):
                result = check_existing_ci_cd_files(Path("."), "github")
                assert isinstance(result, list)

    def test_check_existing_ci_cd_files_gitlab(self):
        """Test checking existing CI/CD files for GitLab."""
        with patch("pathlib.Path.exists", return_value=True):
            result = check_existing_ci_cd_files(Path("."), "gitlab")
            assert isinstance(result, list)

    def test_check_existing_ci_cd_files_both(self):
        """Test checking existing CI/CD files for both platforms."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.glob", return_value=[Path("workflow.yml")]):
                result = check_existing_ci_cd_files(Path("."), "both")
                assert isinstance(result, list)

    def test_check_existing_ci_cd_files_no_files(self):
        """Test checking existing CI/CD files when none exist."""
        with patch("pathlib.Path.exists", return_value=False):
            result = check_existing_ci_cd_files(Path("."), "github")
            assert result == []

    def test_render_ci_cd_template(self):
        """Test CI/CD template rendering."""
        with patch("jinja2.Environment") as mock_env:
            mock_template = mock_env.return_value.get_template.return_value
            mock_template.render.return_value = "rendered content"

            with patch("builtins.open", mock_open()):
                with patch("pathlib.Path.mkdir"):
                    render_ci_cd_template(
                        mock_env,
                        Path("."),
                        "test-project",
                        "template.jinja2",
                        "output.txt",
                    )
                    # Should not raise error

    def test_display_success_message(self):
        """Test success message display."""
        with patch("fascraft.commands.ci_cd.console.print") as mock_print:
            display_success_message(Path("."), "github")
            assert mock_print.called

    def test_setup_ci_cd_environments(self):
        """Test CI/CD environment setup."""
        with patch("pathlib.Path.mkdir"):
            setup_ci_cd_environments(Path("."))
            # Should not raise error

    def test_create_environment_configs(self):
        """Test environment configuration creation."""
        with patch("builtins.open", mock_open()):
            create_environment_configs(Path("."))
            # Should not raise error

    def test_setup_pre_commit_hooks(self):
        """Test pre-commit hooks setup."""
        with patch("builtins.open", mock_open()):
            setup_pre_commit_hooks(Path("."))
            # Should not raise error

    def test_display_setup_instructions(self):
        """Test setup instructions display."""
        with patch("fascraft.commands.ci_cd.console.print") as mock_print:
            display_setup_instructions(Path("."))
            assert mock_print.called

    def test_check_existing_ci_cd_files_with_pre_commit(self):
        """Test checking existing CI/CD files including pre-commit config."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.glob", return_value=[Path("workflow.yml")]):
                result = check_existing_ci_cd_files(Path("."), "github")
                assert isinstance(result, list)

    def test_check_existing_ci_cd_files_github_workflows(self):
        """Test checking GitHub workflows specifically."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch(
                "pathlib.Path.glob", return_value=[Path("test.yml"), Path("deploy.yml")]
            ):
                result = check_existing_ci_cd_files(Path("."), "github")
                assert len(result) > 0
                # Check that GitHub workflow files are included
                github_files = [f for f in result if ".github/workflows/" in f]
                assert len(github_files) == 2
                assert ".github/workflows/test.yml" in result
                assert ".github/workflows/deploy.yml" in result

    def test_check_existing_ci_cd_files_gitlab_ci(self):
        """Test checking GitLab CI file specifically."""
        with patch("pathlib.Path.exists", return_value=True):
            result = check_existing_ci_cd_files(Path("."), "gitlab")
            assert isinstance(result, list)

    def test_check_existing_ci_cd_files_both_platforms(self):
        """Test checking both GitHub and GitLab files."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.glob", return_value=[Path("workflow.yml")]):
                result = check_existing_ci_cd_files(Path("."), "both")
                assert isinstance(result, list)

    def test_render_ci_cd_template_with_context(self):
        """Test CI/CD template rendering with context data."""
        with patch("jinja2.Environment") as mock_env:
            mock_template = mock_env.return_value.get_template.return_value
            mock_template.render.return_value = "Hello World"

            with patch("builtins.open", mock_open()):
                with patch("pathlib.Path.mkdir"):
                    render_ci_cd_template(
                        mock_env,
                        Path("."),
                        "test-project",
                        "greeting.jinja2",
                        "output.txt",
                    )
                    # Should not raise error

    def test_display_success_message_different_platforms(self):
        """Test success message display for different platforms."""
        with patch("fascraft.commands.ci_cd.console.print") as mock_print:
            display_success_message(Path("."), "gitlab")
            assert mock_print.called

            mock_print.reset_mock()
            display_success_message(Path("."), "both")
            assert mock_print.called

    def test_check_existing_ci_cd_files_no_github_dir(self):
        """Test when GitHub workflows directory doesn't exist."""
        with patch("pathlib.Path.exists", return_value=False):
            result = check_existing_ci_cd_files(Path("."), "github")
            assert result == []

    def test_check_existing_ci_cd_files_gitlab_exists(self):
        """Test when GitLab CI file exists."""
        # Simple mock - just return True for all exists calls
        with patch("pathlib.Path.exists", return_value=True):
            result = check_existing_ci_cd_files(Path("."), "gitlab")
            assert ".gitlab-ci.yml" in result

    def test_check_existing_ci_cd_files_pre_commit_exists(self):
        """Test when pre-commit config exists."""
        with patch(
            "pathlib.Path.exists", side_effect=[False, False, True]
        ):  # github_dir, gitlab_file, pre_commit
            result = check_existing_ci_cd_files(Path("."), "both")
            assert ".pre-commit-config.yaml" in result

    def test_check_existing_ci_cd_files_platform_specific(self):
        """Test platform-specific file checking."""
        # Test GitHub only
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.glob", return_value=[Path("ci.yml")]):
                result = check_existing_ci_cd_files(Path("."), "github")
                assert ".github/workflows/ci.yml" in result

        # Test GitLab only
        with patch("pathlib.Path.exists", return_value=True):
            result = check_existing_ci_cd_files(Path("."), "gitlab")
            assert ".gitlab-ci.yml" in result

    def test_check_existing_ci_cd_files_edge_cases(self):
        """Test edge cases for file checking."""
        # Test with no files at all
        with patch("pathlib.Path.exists", return_value=False):
            result = check_existing_ci_cd_files(Path("."), "both")
            assert result == []

        # Test with empty GitHub workflows directory
        with patch("pathlib.Path.exists", return_value=False):
            with patch("pathlib.Path.glob", return_value=[]):
                result = check_existing_ci_cd_files(Path("."), "github")
                assert result == []

    def test_check_existing_ci_cd_files_comprehensive_scenarios(self):
        """Test comprehensive scenarios for different platform combinations."""
        # Test both platforms with all files existing
        with patch("pathlib.Path.exists", return_value=True):
            with patch(
                "pathlib.Path.glob", return_value=[Path("ci.yml"), Path("deploy.yml")]
            ):
                result = check_existing_ci_cd_files(Path("."), "both")
                assert len(result) > 0

        # Test GitHub platform with pre-commit
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.glob", return_value=[Path("test.yml")]):
                result = check_existing_ci_cd_files(Path("."), "github")
                assert len(result) > 0

    def test_check_existing_ci_cd_files_error_handling(self):
        """Test error handling in file checking."""
        # Test with invalid platform - should only check pre-commit since platform is invalid
        with patch("pathlib.Path.exists", return_value=False):
            result = check_existing_ci_cd_files(Path("."), "invalid_platform")
            assert result == []

        # Test with None project_path
        with pytest.raises(TypeError):
            check_existing_ci_cd_files(None, "github")
