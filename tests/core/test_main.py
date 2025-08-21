"""Tests for the main CLI module."""

from unittest.mock import patch

from typer.testing import CliRunner

from fascraft.main import app, hello, version


class TestMainCLI:
    """Test the main CLI functionality."""

    def test_hello_command_default(self):
        """Test hello command with default name."""
        runner = CliRunner()
        result = runner.invoke(app, ["hello"])
        assert result.exit_code == 0
        assert "Hello World!" in result.stdout
        assert "Welcome to FasCraft!" in result.stdout

    def test_hello_command_custom_name(self):
        """Test hello command with custom name."""
        runner = CliRunner()
        result = runner.invoke(app, ["hello", "Alice"])
        assert result.exit_code == 0
        assert "Hello Alice!" in result.stdout
        assert "Welcome to FasCraft!" in result.stdout

    def test_version_command(self):
        """Test version command."""
        runner = CliRunner()
        with patch("fascraft.version.get_version", return_value="9.9.9"):
            result = runner.invoke(app, ["version"])
            assert result.exit_code == 0
            assert "Fascraft version 9.9.9" in result.stdout

    def test_main_app_help(self):
        """Test main app help command."""
        runner = CliRunner()
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "FasCraft CLI for generating modular FastAPI projects" in result.stdout

    def test_main_app_commands_listed(self):
        """Test that all main commands are listed in help."""
        runner = CliRunner()
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0

        # Check that core commands are listed
        assert "new" in result.stdout
        assert "generate" in result.stdout
        assert "list" in result.stdout
        assert "remove" in result.stdout
        assert "update" in result.stdout
        assert "analyze" in result.stdout
        assert "migrate" in result.stdout

    def test_main_app_invalid_command(self):
        """Test main app with invalid command."""
        runner = CliRunner()
        result = runner.invoke(app, ["invalid-command"])
        assert result.exit_code != 0

    def test_hello_function_direct_call(self):
        """Test hello function directly."""
        with patch("fascraft.main.console.print") as mock_print:
            hello("TestUser")
            # Verify console.print was called (we can't easily test the exact output)
            assert mock_print.called

    def test_version_function_direct_call(self):
        """Test version function directly."""
        with patch("fascraft.version.get_version", return_value="1.0.0"):
            with patch("fascraft.main.console.print") as mock_print:
                version()
                # Verify console.print was called
                assert mock_print.called
