"""Tests for the environment management command."""

from unittest.mock import MagicMock, patch

import pytest
import typer

from fascraft.commands.environment import (
    create,
    create_enhanced_settings,
    create_environment,
    create_environment_config_yaml,
    create_environment_file,
    create_individual_env_config,
    get_current_environment,
    get_environment_overrides,
    init,
    initialize_environment_management,
    list_environments,
    switch,
    switch_environment,
    update_main_environment_config,
    validate_environments,
    validate_single_environment,
)


class TestEnvironmentCommand:
    """Test cases for environment management command functionality."""

    def test_init_environment_management_success(self, tmp_path):
        """Test successful environment management initialization."""
        # Create a mock FastAPI project
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        (project_path / "main.py").write_text("# FastAPI app")

        with patch("fascraft.commands.environment.Environment") as mock_env:
            mock_template = MagicMock()
            mock_template.render.return_value = "env content"
            mock_env.return_value.get_template.return_value = mock_template

            initialize_environment_management(
                project_path, ["dev", "staging", "prod"], force=False
            )

            # Verify environment files were created
            assert (project_path / ".env.dev").exists()
            assert (project_path / ".env.staging").exists()
            assert (project_path / ".env.prod").exists()
            assert (
                project_path / "config" / "environments" / "environments.yml"
            ).exists()
            assert (project_path / "config" / "environments" / "dev.yml").exists()
            assert (project_path / "config" / "environments" / "staging.yml").exists()
            assert (project_path / "config" / "environments" / "prod.yml").exists()
            assert (project_path / "config" / "settings.py").exists()

    def test_create_environment_file_success(self, tmp_path):
        """Test successful environment file creation."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        mock_env = MagicMock()
        mock_template = MagicMock()
        mock_template.render.return_value = "environment content"
        mock_env.get_template.return_value = mock_template

        create_environment_file(project_path, "dev", mock_env, "test-project")

        # Verify environment file was created
        assert (project_path / ".env.dev").exists()
        assert (project_path / ".env.dev").read_text() == "environment content"

    def test_get_environment_overrides(self):
        """Test environment-specific configuration overrides."""
        # Test development environment
        dev_overrides = get_environment_overrides("development")
        assert dev_overrides["DEBUG"] == "True"
        assert dev_overrides["ENVIRONMENT"] == "development"
        assert dev_overrides["LOG_LEVEL"] == "DEBUG"

        # Test production environment
        prod_overrides = get_environment_overrides("production")
        assert prod_overrides["DEBUG"] == "False"
        assert prod_overrides["ENVIRONMENT"] == "production"
        assert prod_overrides["LOG_LEVEL"] == "WARNING"

        # Test unknown environment (should default to development)
        unknown_overrides = get_environment_overrides("unknown")
        assert unknown_overrides["DEBUG"] == "True"

    def test_create_environment_config_yaml_success(self, tmp_path):
        """Test successful environment configuration YAML creation."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        # Create the config directory structure
        config_dir = project_path / "config"
        config_dir.mkdir()
        env_config_dir = config_dir / "environments"
        env_config_dir.mkdir()

        create_environment_config_yaml(project_path, ["dev", "staging"], "test-project")

        # Verify main config was created
        main_config_file = project_path / "config" / "environments" / "environments.yml"
        assert main_config_file.exists()

        # Verify individual configs were created
        assert (project_path / "config" / "environments" / "dev.yml").exists()
        assert (project_path / "config" / "environments" / "staging.yml").exists()

    def test_create_individual_env_config_success(self, tmp_path):
        """Test successful individual environment configuration creation."""
        env_config_dir = tmp_path / "config" / "environments"
        env_config_dir.mkdir(parents=True)

        create_individual_env_config(env_config_dir, "development", "test-project")

        # Verify config file was created
        config_file = env_config_dir / "development.yml"
        assert config_file.exists()

        # Verify content structure
        import yaml

        with open(config_file) as f:
            config = yaml.safe_load(f)

        assert config["environment"] == "development"
        assert config["project"] == "test-project"
        assert config["app"]["debug"] is True
        assert config["database"]["pool_size"] == 5

    def test_create_enhanced_settings_success(self, tmp_path):
        """Test successful enhanced settings creation."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        mock_env = MagicMock()

        create_enhanced_settings(project_path, "test-project", mock_env)

        # Verify settings file was created
        settings_file = project_path / "config" / "settings.py"
        assert settings_file.exists()

        # Verify content contains expected elements
        content = settings_file.read_text()
        assert "Enhanced application settings with environment support" in content
        assert "class Settings(BaseSettings):" in content
        assert "def get_settings() -> Settings:" in content

    def test_create_environment_success(self, tmp_path):
        """Test successful environment creation."""
        # Create a mock FastAPI project
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        (project_path / "main.py").write_text("# FastAPI app")

        with patch("fascraft.commands.environment.Environment") as mock_env:
            mock_template = MagicMock()
            mock_template.render.return_value = "env content"
            mock_env.return_value.get_template.return_value = mock_template

            create_environment(project_path, "custom", "development", force=False)

            # Verify environment was created
            assert (project_path / ".env.custom").exists()
            assert (project_path / "config" / "environments" / "custom.yml").exists()

    def test_update_main_environment_config_success(self, tmp_path):
        """Test successful main environment configuration update."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        # Create existing config
        env_config_dir = project_path / "config" / "environments"
        env_config_dir.mkdir(parents=True)

        existing_config = {
            "project": "test-project",
            "default_environment": "development",
            "environments": {"dev": {"description": "Development environment"}},
        }

        import yaml

        main_config_file = env_config_dir / "environments.yml"
        with open(main_config_file, "w") as f:
            yaml.dump(existing_config, f)

        # Update with new environment
        update_main_environment_config(project_path, "staging")

        # Verify new environment was added
        with open(main_config_file) as f:
            updated_config = yaml.safe_load(f)

        assert "staging" in updated_config["environments"]
        assert (
            updated_config["environments"]["staging"]["description"]
            == "Staging environment configuration"
        )

    def test_list_environments_success(self, tmp_path):
        """Test successful environment listing."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        # Create some environment files
        (project_path / ".env.dev").write_text("ENVIRONMENT=development")
        (project_path / ".env.prod").write_text("ENVIRONMENT=production")

        # Create environment configs
        env_config_dir = project_path / "config" / "environments"
        env_config_dir.mkdir(parents=True)
        (env_config_dir / "dev.yml").write_text("environment: dev")
        (env_config_dir / "prod.yml").write_text("environment: prod")

        list_environments(project_path)

        # The function should complete without errors
        # In a real scenario, it would display a table

    def test_get_current_environment_from_env_file(self, tmp_path):
        """Test getting current environment from .env file."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        # Create .env file with environment
        env_file = project_path / ".env"
        env_file.write_text("ENVIRONMENT=staging\nDEBUG=false")

        current_env = get_current_environment(project_path)
        assert current_env == "staging"

    def test_get_current_environment_from_indicator(self, tmp_path):
        """Test getting current environment from indicator file."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        # Create environment indicator file
        indicator_file = project_path / ".current_environment"
        indicator_file.write_text("production")

        current_env = get_current_environment(project_path)
        assert current_env == "production"

    def test_switch_environment_success(self, tmp_path):
        """Test successful environment switching."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        # Create source environment file
        source_env_file = project_path / ".env.dev"
        source_env_file.write_text("ENVIRONMENT=development\nDEBUG=true")

        switch_environment(project_path, "dev")

        # Verify .env file was created
        target_env_file = project_path / ".env"
        assert target_env_file.exists()
        assert target_env_file.read_text() == "ENVIRONMENT=development\nDEBUG=true"

        # Verify indicator file was created
        indicator_file = project_path / ".current_environment"
        assert indicator_file.exists()
        assert indicator_file.read_text() == "dev"

    def test_validate_environments_success(self, tmp_path):
        """Test successful environment validation."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        # Create environment file
        env_file = project_path / ".env.dev"
        env_file.write_text("ENVIRONMENT=development\nDEBUG=true")

        # Create environment config
        env_config_dir = project_path / "config" / "environments"
        env_config_dir.mkdir(parents=True)

        import yaml

        config_file = env_config_dir / "dev.yml"
        config_content = {"environment": "dev", "app": {"name": "test"}}
        with open(config_file, "w") as f:
            yaml.dump(config_content, f)

        validate_environments(project_path)

        # The function should complete without errors
        # In a real scenario, it would display validation results

    def test_validate_single_environment_success(self, tmp_path):
        """Test successful single environment validation."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        # Create valid environment file
        env_file = project_path / ".env.dev"
        env_file.write_text("ENVIRONMENT=development\nDEBUG=true")

        # Create valid environment config
        env_config_dir = project_path / "config" / "environments"
        env_config_dir.mkdir(parents=True)

        import yaml

        config_file = env_config_dir / "dev.yml"
        config_content = {"environment": "dev"}
        with open(config_file, "w") as f:
            yaml.dump(config_content, f)

        result = validate_single_environment(project_path, "dev")
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_validate_single_environment_missing_file(self, tmp_path):
        """Test environment validation with missing file."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        result = validate_single_environment(project_path, "missing")
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert "not found" in result["errors"][0]

    def test_validate_single_environment_invalid_yaml(self, tmp_path):
        """Test environment validation with invalid YAML."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        # Create environment file
        env_file = project_path / ".env.dev"
        env_file.write_text("ENVIRONMENT=development")

        # Create invalid YAML config
        env_config_dir = project_path / "config" / "environments"
        env_config_dir.mkdir(parents=True)
        config_file = env_config_dir / "dev.yml"
        config_file.write_text("invalid: yaml: content: [unclosed")

        result = validate_single_environment(project_path, "dev")
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert "Invalid YAML" in result["errors"][0]

    def test_environment_not_fastapi_project(self, tmp_path):
        """Test environment init fails for non-FastAPI projects."""
        project_path = tmp_path / "not-fastapi"
        project_path.mkdir()
        # No main.py file

        with pytest.raises(typer.Exit) as exc_info:
            init(project_path, environments="dev", force=False)

        # Check that it's an exit exception with code 1
        assert exc_info.value.exit_code == 1

    def test_environment_project_not_exists(self, tmp_path):
        """Test environment init fails for non-existent projects."""
        project_path = tmp_path / "non-existent"

        with pytest.raises(typer.Exit) as exc_info:
            init(project_path, environments="dev", force=False)

        # Check that it's an exit exception with code 1
        assert exc_info.value.exit_code == 1

    def test_environment_invalid_environments(self, tmp_path):
        """Test environment init fails for invalid environment list."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        (project_path / "main.py").write_text("# FastAPI app")

        with pytest.raises(typer.Exit) as exc_info:
            init(project_path, environments="", force=False)

        # Check that it's an exit exception with code 1
        assert exc_info.value.exit_code == 1

    def test_environment_switch_not_found(self, tmp_path):
        """Test environment switch fails for non-existent environment."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        (project_path / "main.py").write_text("# FastAPI app")

        with pytest.raises(typer.Exit) as exc_info:
            switch(project_path, environment="missing")

        # Check that it's an exit exception with code 1
        assert exc_info.value.exit_code == 1

    def test_environment_create_invalid_template(self, tmp_path):
        """Test environment create fails for invalid template."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        (project_path / "main.py").write_text("# FastAPI app")

        with pytest.raises(typer.Exit) as exc_info:
            create(project_path, name="custom", template="invalid", force=False)

        # Check that it's an exit exception with code 1
        assert exc_info.value.exit_code == 1
