"""Integration tests for the FasCraft CLI."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from fascraft.main import app


class TestCLIIntegration:
    """Test CLI integration and command registration."""

    def test_hello_command(self, cli_runner: CliRunner) -> None:
        """Test the hello command."""
        result = cli_runner.invoke(app, ["hello"])
        assert result.exit_code == 0
        assert "Hello World!" in result.stdout
        assert "Welcome to FasCraft!" in result.stdout

    def test_hello_command_with_name(self, cli_runner: CliRunner) -> None:
        """Test the hello command with custom name."""
        result = cli_runner.invoke(app, ["hello", "Alice"])
        assert result.exit_code == 0
        assert "Hello Alice!" in result.stdout
        assert "Welcome to FasCraft!" in result.stdout

    def test_version_command(self, cli_runner: CliRunner) -> None:
        """Test the version command."""
        result = cli_runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "FasCraft version" in result.stdout

    def test_new_command_help(self, cli_runner: CliRunner) -> None:
        """Test the new command help."""
        result = cli_runner.invoke(app, ["new", "--help"])
        assert result.exit_code == 0
        assert "Generates a new FastAPI project" in result.stdout

    def test_generate_command_help(self, cli_runner: CliRunner) -> None:
        """Test the generate command help."""
        result = cli_runner.invoke(app, ["generate", "--help"])
        assert result.exit_code == 0
        assert "Generates a new domain module in an existing FastAPI project" in result.stdout

    def test_list_command_help(self, cli_runner: CliRunner) -> None:
        """Test the list command help."""
        result = cli_runner.invoke(app, ["list", "--help"])
        assert result.exit_code == 0
        assert "Lists all existing domain modules in a FastAPI project" in result.stdout

    def test_remove_command_help(self, cli_runner: CliRunner) -> None:
        """Test the remove command help."""
        result = cli_runner.invoke(app, ["remove", "--help"])
        assert result.exit_code == 0
        assert "Removes a domain module from a FastAPI project" in result.stdout

    def test_update_command_help(self, cli_runner: CliRunner) -> None:
        """Test the update command help."""
        result = cli_runner.invoke(app, ["update", "--help"])
        assert result.exit_code == 0
        assert "Updates an existing domain module with the latest templates" in result.stdout

    def test_main_help(self, cli_runner: CliRunner) -> None:
        """Test the main help command."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "FasCraft CLI for generating modular FastAPI projects" in result.stdout
        assert "new" in result.stdout
        assert "generate" in result.stdout
        assert "list" in result.stdout
        assert "remove" in result.stdout
        assert "update" in result.stdout
        assert "hello" in result.stdout
        assert "version" in result.stdout

    def test_invalid_command(self, cli_runner: CliRunner) -> None:
        """Test invalid command handling."""
        result = cli_runner.invoke(app, ["invalid-command"])
        assert result.exit_code != 0

    def test_new_command_validation(self, cli_runner: CliRunner, temp_dir) -> None:
        """Test new command with validation."""
        project_name = "test-project"
        result = cli_runner.invoke(app, ["new", project_name, "--path", str(temp_dir)])
        assert result.exit_code == 0
        assert "Successfully created new project" in result.stdout
        assert project_name in result.stdout

    def test_generate_command_validation(self, cli_runner: CliRunner, temp_dir) -> None:
        """Test generate command with validation."""
        # First create a project
        project_name = "test-project"
        cli_runner.invoke(app, ["new", project_name, "--path", str(temp_dir)])
        
        # Then try to generate a module
        module_name = "users"
        result = cli_runner.invoke(app, ["generate", module_name, "--path", str(temp_dir / project_name)])
        assert result.exit_code == 0
        assert "Successfully generated domain module" in result.stdout
        assert module_name in result.stdout

    def test_list_command_validation(self, cli_runner: CliRunner, temp_dir) -> None:
        """Test list command with validation."""
        # First create a project
        project_name = "test-project"
        cli_runner.invoke(app, ["new", project_name, "--path", str(temp_dir)])
        
        # Then try to list modules
        result = cli_runner.invoke(app, ["list", "--path", str(temp_dir / project_name)])
        assert result.exit_code == 0
        assert "No domain modules found" in result.stdout

    def test_list_command_with_modules(self, cli_runner: CliRunner, temp_dir) -> None:
        """Test list command when modules exist."""
        # First create a project
        project_name = "test-project"
        cli_runner.invoke(app, ["new", project_name, "--path", str(temp_dir)])
        
        # Generate a module
        module_name = "users"
        cli_runner.invoke(app, ["generate", module_name, "--path", str(temp_dir / project_name)])
        
        # Then list modules
        result = cli_runner.invoke(app, ["list", "--path", str(temp_dir / project_name)])
        assert result.exit_code == 0
        assert "Found 1 domain module(s)" in result.stdout
        assert module_name in result.stdout

    def test_remove_command_validation(self, cli_runner: CliRunner, temp_dir) -> None:
        """Test remove command with validation."""
        # First create a project
        project_name = "test-project"
        cli_runner.invoke(app, ["new", project_name, "--path", str(temp_dir)])
        
        # Generate a module
        module_name = "users"
        cli_runner.invoke(app, ["generate", module_name, "--path", str(temp_dir / project_name)])
        
        # Then try to remove the module (with force to avoid interactive prompt)
        result = cli_runner.invoke(app, ["remove", module_name, "--path", str(temp_dir / project_name), "--force"])
        assert result.exit_code == 0
        assert "Successfully removed module" in result.stdout
        assert module_name in result.stdout

    def test_update_command_validation(self, cli_runner: CliRunner, temp_dir) -> None:
        """Test update command with validation."""
        # First create a project
        project_name = "test-project"
        cli_runner.invoke(app, ["new", project_name, "--path", str(temp_dir)])
        
        # Generate a module
        module_name = "users"
        cli_runner.invoke(app, ["generate", module_name, "--path", str(temp_dir / project_name)])
        
        # Then try to update the module (with force to avoid interactive prompt)
        result = cli_runner.invoke(app, ["update", module_name, "--path", str(temp_dir / project_name), "--force"])
        assert result.exit_code == 0
        assert "Successfully updated module" in result.stdout
        assert module_name in result.stdout
