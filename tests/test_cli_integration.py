"""Integration tests for the FastForge CLI."""

from pathlib import Path

from typer.testing import CliRunner

from fastforge.main import app


class TestCLIIntegration:
    """Test CLI integration and command execution."""

    def test_cli_app_has_new_command(self) -> None:
        """Test that the CLI app has the new command registered."""
        runner = CliRunner()
        result = runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "new" in result.output
        assert "Generates a new FastAPI project" in result.output

    def test_cli_app_has_version_command(self) -> None:
        """Test that the CLI app has the version command."""
        runner = CliRunner()
        result = runner.invoke(app, ["version"])

        assert result.exit_code == 0
        assert "FastForge version" in result.output

    def test_cli_app_has_hello_command(self) -> None:
        """Test that the CLI app has the hello command."""
        runner = CliRunner()
        result = runner.invoke(app, ["hello", "--name", "TestUser"])

        assert result.exit_code == 0
        assert "Hello TestUser! Welcome to FastForge!" in result.output

    def test_new_command_via_cli(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test new command execution through CLI."""
        runner = CliRunner()

        with runner.isolated_filesystem(temp_dir):
            result = runner.invoke(app, ["new", sample_project_name])

            assert result.exit_code == 0
            assert "Successfully created new project" in result.output
            assert sample_project_name in result.output
            assert "poetry install" in result.output

    def test_new_command_with_path_option(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test new command with custom path option."""
        runner = CliRunner()
        custom_path = temp_dir / "custom-location"

        with runner.isolated_filesystem(temp_dir):
            result = runner.invoke(
                app, ["new", sample_project_name, "--path", str(custom_path)]
            )

            assert result.exit_code == 0
            assert "Successfully created new project" in result.output

            # Verify project was created in custom location
            project_path = custom_path / sample_project_name
            assert project_path.exists()
            assert (project_path / "main.py").exists()

    def test_new_command_error_existing_directory(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test new command error when directory already exists."""
        runner = CliRunner()

        with runner.isolated_filesystem(temp_dir):
            # Create project first time
            result1 = runner.invoke(app, ["new", sample_project_name])
            assert result1.exit_code == 0

            # Try to create again - should fail
            result2 = runner.invoke(app, ["new", sample_project_name])
            assert result2.exit_code == 1
            assert "already exists" in result2.output

    def test_new_command_help(self) -> None:
        """Test new command help output."""
        runner = CliRunner()
        result = runner.invoke(app, ["new", "--help"])

        assert result.exit_code == 0
        assert "PROJECT_NAME" in result.output
        assert "--path" in result.output
        assert "Generates a new FastAPI project" in result.output

    def test_cli_app_help(self) -> None:
        """Test main CLI app help output."""
        runner = CliRunner()
        result = runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "FastForge CLI for generating modular FastAPI projects" in result.output
        assert "new" in result.output
        assert "version" in result.output
        assert "hello" in result.output

    def test_cli_new_command_executes_successfully(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that CLI new command executes successfully."""
        runner = CliRunner()

        with runner.isolated_filesystem(temp_dir):
            result = runner.invoke(app, ["new", sample_project_name])

            assert result.exit_code == 0
            assert "Successfully created new project" in result.output
            assert sample_project_name in result.output

    def test_new_command_creates_all_required_files(
        self, temp_dir: Path, sample_project_name: str, expected_files: list[str]
    ) -> None:
        """Test that CLI new command creates all required files."""
        runner = CliRunner()

        with runner.isolated_filesystem(temp_dir):
            result = runner.invoke(app, ["new", sample_project_name])

            assert result.exit_code == 0

            # Verify all expected files were created
            project_path = Path(sample_project_name)
            for expected_file in expected_files:
                file_path = project_path / expected_file
                assert (
                    file_path.exists()
                ), f"Expected file {expected_file} was not created"
                assert file_path.is_file()

    def test_new_command_with_invalid_project_name(self) -> None:
        """Test new command with invalid project name."""
        runner = CliRunner()

        # Test with empty project name
        result = runner.invoke(app, ["new", ""])
        assert result.exit_code != 0

        # Test with whitespace-only project name
        result = runner.invoke(app, ["new", "   "])
        assert result.exit_code != 0
