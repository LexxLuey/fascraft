"""Tests for enhanced error handling in the new.py command."""

from unittest.mock import MagicMock, patch

import pytest

from fascraft.commands.new import (
    create_backup_directory,
    create_minimal_structure,
    create_project_with_graceful_degradation,
    create_project_with_rollback,
    render_essential_templates,
    render_project_templates_with_progress,
    render_single_template,
    rollback_project_creation,
    validate_generated_project,
)
from fascraft.exceptions import (
    CorruptedTemplateError,
    FileSystemError,
    TemplateError,
    TemplateNotFoundError,
    TemplateRenderError,
)


class TestCreateProjectWithRollback:
    """Test the create_project_with_rollback function."""

    @patch("fascraft.commands.new.validate_file_system_writable")
    @patch("fascraft.commands.new.validate_disk_space")
    @patch("fascraft.commands.new.create_project_structure")
    @patch("fascraft.commands.new.render_project_templates_with_progress")
    @patch("fascraft.commands.new.validate_generated_project")
    def test_create_project_with_rollback_success(
        self,
        mock_validate_gen,
        mock_render,
        mock_create_structure,
        mock_validate_disk,
        mock_validate_fs,
        tmp_path,
    ):
        """Test successful project creation with rollback capability."""
        project_path = tmp_path / "test_project"
        project_name = "test_project"

        # Should not raise an exception
        create_project_with_rollback(project_path, project_name)

        # Verify all validation and creation steps were called
        mock_validate_fs.assert_called_once_with(project_path.parent)
        mock_validate_disk.assert_called_once_with(
            project_path.parent, required_space_mb=20
        )
        mock_create_structure.assert_called_once_with(project_path, project_name)
        mock_render.assert_called_once_with(project_path, project_name)
        mock_validate_gen.assert_called_once_with(project_path)

    @patch("fascraft.commands.new.validate_file_system_writable")
    @patch("fascraft.commands.new.validate_disk_space")
    @patch("fascraft.commands.new.create_project_structure")
    @patch("fascraft.commands.new.rollback_project_creation")
    def test_create_project_with_rollback_failure(
        self,
        mock_rollback,
        mock_create_structure,
        mock_validate_disk,
        mock_validate_fs,
        tmp_path,
    ):
        """Test project creation failure triggers rollback."""
        project_path = tmp_path / "test_project"
        project_name = "test_project"

        # Mock structure creation failure
        mock_create_structure.side_effect = FileSystemError("Structure creation failed")

        with pytest.raises(FileSystemError):
            create_project_with_rollback(project_path, project_name)

        # Verify rollback was called
        mock_rollback.assert_called_once_with(project_path, None, [])

    @patch("fascraft.commands.new.validate_file_system_writable")
    @patch("fascraft.commands.new.validate_disk_space")
    @patch("fascraft.commands.new.create_project_structure")
    @patch("fascraft.commands.new.render_project_templates_with_progress")
    @patch("fascraft.commands.new.rollback_project_creation")
    def test_create_project_with_rollback_template_failure(
        self,
        mock_rollback,
        mock_render,
        mock_create_structure,
        mock_validate_disk,
        mock_validate_fs,
        tmp_path,
    ):
        """Test template rendering failure is handled gracefully with fallback."""
        project_path = tmp_path / "test_project"
        project_name = "test_project"

        # Mock template rendering failure
        mock_render.side_effect = TemplateError("Template rendering failed")

        # Template errors are now caught and handled gracefully, so no exception should be raised
        # The function should complete successfully with fallback to essential templates
        create_project_with_rollback(project_path, project_name)

        # Verify rollback was NOT called since template failure is handled gracefully
        mock_rollback.assert_not_called()


class TestCreateBackupDirectory:
    """Test the create_backup_directory function."""

    @patch("shutil.copytree")
    @patch("fascraft.commands.new.datetime")
    def test_create_backup_directory_success(
        self, mock_datetime, mock_copytree, tmp_path
    ):
        """Test successful backup directory creation."""
        # Mock datetime
        mock_datetime.now.return_value.strftime.return_value = "20231201_143022"

        source_path = tmp_path / "existing_project"
        source_path.mkdir()
        (source_path / "file.txt").write_text("test content")

        result = create_backup_directory(source_path)

        # Verify backup was created
        assert result is not None
        assert "backup_20231201_143022" in str(result)
        mock_copytree.assert_called_once()

    @patch("shutil.copytree")
    @patch("fascraft.commands.new.datetime")
    def test_create_backup_directory_failure(
        self, mock_datetime, mock_copytree, tmp_path
    ):
        """Test backup directory creation failure."""
        # Mock datetime
        mock_datetime.now.return_value.strftime.return_value = "20231201_143022"

        # Mock shutil failure
        mock_copytree.side_effect = OSError("Backup failed")

        source_path = tmp_path / "existing_project"
        source_path.mkdir()

        result = create_backup_directory(source_path)

        # Verify backup creation failed gracefully
        assert result is None


class TestRollbackProjectCreation:
    """Test the rollback_project_creation function."""

    @patch("shutil.copytree")
    @patch("shutil.rmtree")
    def test_rollback_project_creation_with_backup(
        self, mock_rmtree, mock_copytree, tmp_path
    ):
        """Test rollback with available backup."""
        project_path = tmp_path / "failed_project"
        backup_path = tmp_path / "backup_project"

        # Create mock project and backup
        project_path.mkdir()
        (project_path / "file.txt").write_text("failed content")
        backup_path.mkdir()
        (backup_path / "file.txt").write_text("backup content")

        rollback_project_creation(project_path, backup_path, ["structure", "templates"])

        # Verify rollback operations
        mock_rmtree.assert_called_once_with(project_path)
        mock_copytree.assert_called_once_with(backup_path, project_path)

    @patch("shutil.copytree")
    @patch("shutil.rmtree")
    def test_rollback_project_creation_no_backup(
        self, mock_rmtree, mock_copytree, tmp_path
    ):
        """Test rollback without backup."""
        project_path = tmp_path / "failed_project"
        project_path.mkdir()
        (project_path / "file.txt").write_text("failed content")

        rollback_project_creation(project_path, None, ["structure"])

        # Verify only removal was attempted
        mock_rmtree.assert_called_once_with(project_path)
        mock_copytree.assert_not_called()

    @patch("shutil.copytree")
    @patch("shutil.rmtree")
    def test_rollback_project_creation_rollback_failure(
        self, mock_rmtree, mock_copytree, tmp_path
    ):
        """Test rollback failure handling."""
        project_path = tmp_path / "failed_project"
        backup_path = tmp_path / "backup_project"

        # Mock rollback failure
        mock_rmtree.side_effect = OSError("Rollback failed")

        # Should not raise exception, just log warning
        rollback_project_creation(project_path, backup_path, ["structure"])


class TestCreateProjectWithGracefulDegradation:
    """Test the create_project_with_graceful_degradation function."""

    @patch("fascraft.commands.new.create_project_structure")
    @patch("fascraft.commands.new.render_project_templates_with_progress")
    @patch("fascraft.commands.new.display_partial_success_warnings")
    def test_create_project_with_graceful_degradation_success(
        self,
        mock_display_warnings,
        mock_render,
        mock_create_structure,
        tmp_path,
    ):
        """Test successful project creation with graceful degradation."""
        project_path = tmp_path / "test_project"
        project_name = "test_project"

        create_project_with_graceful_degradation(project_path, project_name)

        # Verify all steps were called
        mock_create_structure.assert_called_once_with(project_path, project_name)
        mock_render.assert_called_once_with(project_path, project_name)
        mock_display_warnings.assert_not_called()  # No warnings

    @patch("fascraft.commands.new.create_project_structure")
    @patch("fascraft.commands.new.create_minimal_structure")
    @patch("fascraft.commands.new.render_project_templates_with_progress")
    @patch("fascraft.commands.new.render_essential_templates")
    @patch("fascraft.commands.new.display_partial_success_warnings")
    @patch("fascraft.commands.new.rollback_project_creation")
    def test_create_project_with_graceful_degradation_partial_failure(
        self,
        mock_rollback,
        mock_display_warnings,
        mock_render_essential,
        mock_render_full,
        mock_create_minimal,
        mock_create_structure,
        tmp_path,
    ):
        """Test partial failure with graceful degradation."""
        project_path = tmp_path / "test_project"
        project_name = "test_project"

        # Mock structure creation failure
        mock_create_structure.side_effect = FileSystemError("Structure failed")

        create_project_with_graceful_degradation(project_path, project_name)

        # Verify graceful degradation
        mock_create_minimal.assert_called_once_with(project_path, project_name)
        mock_render_full.assert_called_once_with(project_path, project_name)
        mock_display_warnings.assert_called_once()

    @patch("fascraft.commands.new.create_project_structure")
    @patch("fascraft.commands.new.create_minimal_structure")
    @patch("fascraft.commands.new.rollback_project_creation")
    def test_create_project_with_graceful_degradation_complete_failure(
        self,
        mock_rollback,
        mock_create_minimal,
        mock_create_structure,
        tmp_path,
    ):
        """Test complete failure triggers rollback."""
        project_path = tmp_path / "test_project"
        project_name = "test_project"

        # Mock both structure creation and minimal structure failure
        mock_create_structure.side_effect = FileSystemError("Structure failed")
        mock_create_minimal.side_effect = FileSystemError("Minimal structure failed")

        with pytest.raises(FileSystemError):
            create_project_with_graceful_degradation(project_path, project_name)

        # Verify rollback was called
        mock_rollback.assert_called_once_with(project_path, None, [])


class TestCreateMinimalStructure:
    """Test the create_minimal_structure function."""

    def test_create_minimal_structure_success(self, tmp_path):
        """Test successful minimal structure creation."""
        project_path = tmp_path / "test_project"

        create_minimal_structure(project_path, "test_project")

        # Verify minimal structure was created
        assert (project_path / "main.py").parent.exists()

    @patch("pathlib.Path.mkdir")
    def test_create_minimal_structure_failure(self, mock_mkdir, tmp_path):
        """Test minimal structure creation failure."""
        project_path = tmp_path / "test_project"

        # Mock mkdir failure
        mock_mkdir.side_effect = OSError("Permission denied")

        with pytest.raises(FileSystemError) as exc_info:
            create_minimal_structure(project_path, "test_project")

        assert "Failed to create even minimal structure" in str(exc_info.value)


class TestRenderEssentialTemplates:
    """Test the render_essential_templates function."""

    @patch("fascraft.commands.new.render_single_template")
    def test_render_essential_templates_success(self, mock_render_single, tmp_path):
        """Test successful essential template rendering."""
        project_path = tmp_path / "test_project"
        project_name = "test_project"

        render_essential_templates(project_path, project_name)

        # Verify essential templates were rendered (8 templates total)
        assert mock_render_single.call_count == 8
        mock_render_single.assert_any_call(
            project_path, project_name, "main.py.jinja2", "main.py"
        )
        mock_render_single.assert_any_call(
            project_path, project_name, "pyproject.toml.jinja2", "pyproject.toml"
        )
        mock_render_single.assert_any_call(
            project_path, project_name, "requirements.txt.jinja2", "requirements.txt"
        )
        mock_render_single.assert_any_call(
            project_path, project_name, "__init__.py.jinja2", "__init__.py"
        )
        mock_render_single.assert_any_call(
            project_path,
            project_name,
            "config/__init__.py.jinja2",
            "config/__init__.py",
        )
        mock_render_single.assert_any_call(
            project_path,
            project_name,
            "config/settings.py.jinja2",
            "config/settings.py",
        )
        mock_render_single.assert_any_call(
            project_path,
            project_name,
            "routers/__init__.py.jinja2",
            "routers/__init__.py",
        )
        mock_render_single.assert_any_call(
            project_path, project_name, "routers/base.py.jinja2", "routers/base.py"
        )

    @patch("fascraft.commands.new.render_single_template")
    def test_render_essential_templates_partial_failure(
        self, mock_render_single, tmp_path
    ):
        """Test partial failure in essential template rendering."""
        project_path = tmp_path / "test_project"
        project_name = "test_project"

        # Mock partial template failures (8 templates total)
        mock_render_single.side_effect = [
            None,  # main.py.jinja2 succeeds
            None,  # pyproject.toml.jinja2 succeeds
            None,  # requirements.txt.jinja2 succeeds
            None,  # __init__.py.jinja2 succeeds
            None,  # config/__init__.py.jinja2 succeeds
            TemplateError("config/settings.py.jinja2 failed"),  # This one fails
            None,  # routers/__init__.py.jinja2 succeeds
            None,  # routers/base.py.jinja2 succeeds
        ]

        # Should not raise exception, just log warning
        render_essential_templates(project_path, project_name)


class TestValidateGeneratedProject:
    """Test the validate_generated_project function."""

    def test_validate_generated_project_success(self, tmp_path):
        """Test successful project validation."""
        project_path = tmp_path / "test_project"
        project_path.mkdir()

        # Create essential files
        (project_path / "main.py").write_text("FastAPI app")
        (project_path / "pyproject.toml").write_text("Project config")

        # Should not raise exception
        validate_generated_project(project_path)

    def test_validate_generated_project_missing_file(self, tmp_path):
        """Test project validation with missing essential file."""
        project_path = tmp_path / "test_project"
        project_path.mkdir()

        # Only create one essential file
        (project_path / "main.py").write_text("FastAPI app")

        with pytest.raises(TemplateError) as exc_info:
            validate_generated_project(project_path)

        assert "Essential file pyproject.toml was not generated" in str(exc_info.value)

    def test_validate_generated_project_empty_file(self, tmp_path):
        """Test project validation with empty essential file."""
        project_path = tmp_path / "test_project"
        project_path.mkdir()

        # Create empty essential files
        (project_path / "main.py").write_text("")
        (project_path / "pyproject.toml").write_text("Project config")

        with pytest.raises(TemplateError) as exc_info:
            validate_generated_project(project_path)

        assert "Generated file main.py is empty" in str(exc_info.value)


class TestRenderProjectTemplatesWithProgress:
    """Test the render_project_templates_with_progress function."""

    @patch("fascraft.commands.new.render_single_template")
    @patch("fascraft.commands.new.Progress")
    def test_render_project_templates_with_progress_success(
        self, mock_progress_class, mock_render_single, tmp_path
    ):
        """Test successful template rendering with progress."""
        # Mock progress bar
        mock_progress = MagicMock()
        mock_progress_class.return_value.__enter__.return_value = mock_progress

        project_path = tmp_path / "test_project"
        project_name = "test_project"

        render_project_templates_with_progress(project_path, project_name)

        # Verify progress was tracked
        mock_progress.add_task.assert_called_once()
        assert mock_render_single.call_count == 18  # Number of templates

    @patch("fascraft.commands.new.render_single_template")
    @patch("fascraft.commands.new.Progress")
    def test_render_project_templates_with_progress_failure(
        self, mock_progress_class, mock_render_single, tmp_path
    ):
        """Test template rendering failure with progress."""
        # Mock progress bar
        mock_progress = MagicMock()
        mock_progress_class.return_value.__enter__.return_value = mock_progress

        project_path = tmp_path / "test_project"
        project_name = "test_project"

        # Mock template rendering failure
        mock_render_single.side_effect = TemplateError("Template failed")

        with pytest.raises(TemplateRenderError):
            render_project_templates_with_progress(project_path, project_name)

        # Verify progress was stopped
        mock_progress.stop.assert_called_once()


class TestRenderSingleTemplate:
    """Test the render_single_template function."""

    @patch("fascraft.commands.new.Environment")
    def test_render_single_template_success(self, mock_env_class, tmp_path):
        """Test successful single template rendering."""
        # Mock Jinja2 environment
        mock_env = MagicMock()
        mock_template = MagicMock()
        mock_env.get_template.return_value = mock_template
        mock_template.render.return_value = "Rendered content"
        mock_env_class.return_value = mock_env

        project_path = tmp_path / "test_project"
        project_name = "test_project"

        render_single_template(project_path, project_name, "main.py.jinja2", "main.py")

        # Verify template was rendered
        mock_template.render.assert_called_once_with(
            project_name=project_name, author_name="Lutor Iyornumbe"
        )

    @patch("fascraft.commands.new.Environment")
    def test_render_single_template_not_found(self, mock_env_class, tmp_path):
        """Test template not found error."""
        # Mock template not found error
        mock_env = MagicMock()
        mock_env.get_template.side_effect = FileNotFoundError(
            "No such file or directory"
        )
        mock_env_class.return_value = mock_env

        project_path = tmp_path / "test_project"
        project_name = "test_project"

        with pytest.raises(TemplateNotFoundError) as exc_info:
            render_single_template(
                project_path, project_name, "missing.jinja2", "missing.py"
            )

        assert "Template not found" in str(exc_info.value)

    @patch("fascraft.commands.new.Environment")
    def test_render_single_template_corrupted(self, mock_env_class, tmp_path):
        """Test corrupted template error."""
        # Mock template syntax error
        mock_env = MagicMock()
        mock_env.get_template.side_effect = Exception("Template syntax error")
        mock_env_class.return_value = mock_env

        project_path = tmp_path / "test_project"
        project_name = "test_project"

        with pytest.raises(CorruptedTemplateError) as exc_info:
            render_single_template(
                project_path, project_name, "corrupted.jinja2", "corrupted.py"
            )

        assert "Template syntax error" in str(exc_info.value)
