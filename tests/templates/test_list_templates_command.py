"""Unit tests for the list_templates command functionality."""

from unittest.mock import patch

import pytest
import typer

from fascraft.commands.list_templates import list_templates
from fascraft.template_registry import TemplateMetadata


class TestListTemplatesCommand:
    """Test the list_templates command function directly."""

    def test_list_templates_basic_functionality(self):
        """Test that list_templates function works with basic parameters."""
        # Mock the console to capture output
        with patch("fascraft.commands.list_templates.console") as mock_console:
            # Mock the template registry
            with patch(
                "fascraft.commands.list_templates.template_registry"
            ) as mock_registry:
                # Create mock templates
                mock_templates = [
                    TemplateMetadata(
                        name="basic",
                        display_name="Basic CRUD",
                        description="Simple CRUD operations",
                        complexity="basic",
                        category="crud",
                        dependencies=["sqlalchemy"],
                        template_path=None,
                        preview_available=True,
                    ),
                    TemplateMetadata(
                        name="crud",
                        display_name="Advanced CRUD",
                        description="Enhanced CRUD features",
                        complexity="intermediate",
                        category="crud",
                        dependencies=["sqlalchemy", "pydantic"],
                        template_path=None,
                        preview_available=True,
                    ),
                ]

                mock_registry.list_templates.return_value = mock_templates
                mock_registry.get_template_categories.return_value = [
                    "crud",
                    "api_first",
                ]

                # Call the function directly with explicit parameters
                list_templates(category=None, verbose=False)

                # Verify console.print was called for the table
                mock_console.print.assert_called()

                # Verify registry methods were called
                mock_registry.list_templates.assert_called_once_with(category=None)
                mock_registry.get_template_categories.assert_called_once()

    def test_list_templates_with_category_filter(self):
        """Test that list_templates function works with category filtering."""
        with patch("fascraft.commands.list_templates.console"):
            with patch(
                "fascraft.commands.list_templates.template_registry"
            ) as mock_registry:
                # Mock filtered templates
                mock_templates = [
                    TemplateMetadata(
                        name="api_first",
                        display_name="API-First",
                        description="API-centric design",
                        complexity="intermediate",
                        category="api_first",
                        dependencies=["fastapi"],
                        template_path=None,
                        preview_available=True,
                    )
                ]

                mock_registry.list_templates.return_value = mock_templates

                # Call with category filter
                list_templates(category="api_first", verbose=False)

                # Verify category filter was applied
                mock_registry.list_templates.assert_called_once_with(
                    category="api_first"
                )

    def test_list_templates_with_verbose_flag(self):
        """Test that list_templates function works with verbose output."""
        with patch("fascraft.commands.list_templates.console") as mock_console:
            with patch(
                "fascraft.commands.list_templates.template_registry"
            ) as mock_registry:
                mock_templates = [
                    TemplateMetadata(
                        name="basic",
                        display_name="Basic CRUD",
                        description="Simple CRUD operations",
                        complexity="basic",
                        category="crud",
                        dependencies=["sqlalchemy"],
                        template_path=None,
                        preview_available=True,
                    )
                ]

                mock_registry.list_templates.return_value = mock_templates
                mock_registry.get_template_categories.return_value = ["crud"]

                # Call with verbose flag
                list_templates(category=None, verbose=True)

                # Verify verbose output was generated
                mock_console.print.assert_called()
                # Should have more console.print calls due to verbose panels
                assert mock_console.print.call_count > 1

    def test_list_templates_no_templates_found(self):
        """Test that list_templates handles empty template lists gracefully."""
        with patch("fascraft.commands.list_templates.console") as mock_console:
            with patch(
                "fascraft.commands.list_templates.template_registry"
            ) as mock_registry:
                # Mock empty template list
                mock_registry.list_templates.return_value = []

                # Call the function
                list_templates(category=None, verbose=False)

                # Verify appropriate message was displayed
                mock_console.print.assert_called()
                # Check that the error message was shown
                calls = mock_console.print.call_args_list
                error_call = any(
                    "No templates available" in str(call) for call in calls
                )
                assert error_call

    def test_list_templates_with_category_no_results(self):
        """Test that list_templates handles category filtering with no results."""
        with patch("fascraft.commands.list_templates.console") as mock_console:
            with patch(
                "fascraft.commands.list_templates.template_registry"
            ) as mock_registry:
                # Mock empty filtered results
                mock_registry.list_templates.return_value = []

                # Call with category filter
                list_templates(category="nonexistent", verbose=False)

                # Verify appropriate message was displayed
                mock_console.print.assert_called()
                calls = mock_console.print.call_args_list
                error_call = any(
                    "No templates found in category" in str(call) for call in calls
                )
                assert error_call

    def test_list_templates_exception_handling(self):
        """Test that list_templates handles exceptions gracefully."""
        with patch("fascraft.commands.list_templates.console") as mock_console:
            with patch(
                "fascraft.commands.list_templates.template_registry"
            ) as mock_registry:
                # Mock registry to raise an exception
                mock_registry.list_templates.side_effect = Exception("Registry error")

                # Call the function and expect it to raise typer.Exit
                with pytest.raises(typer.Exit):
                    list_templates(category=None, verbose=False)

                # Verify error message was displayed
                mock_console.print.assert_called()
                calls = mock_console.print.call_args_list
                error_call = any(
                    "Failed to list templates" in str(call) for call in calls
                )
                assert error_call

    def test_list_templates_complexity_coloring(self):
        """Test that list_templates applies correct complexity coloring."""
        with patch("fascraft.commands.list_templates.console") as mock_console:
            with patch(
                "fascraft.commands.list_templates.template_registry"
            ) as mock_registry:
                # Mock templates with different complexities
                mock_templates = [
                    TemplateMetadata(
                        name="basic",
                        display_name="Basic",
                        description="Basic template",
                        complexity="basic",
                        category="test",
                        dependencies=[],
                        template_path=None,
                        preview_available=True,
                    ),
                    TemplateMetadata(
                        name="intermediate",
                        display_name="Intermediate",
                        description="Intermediate template",
                        complexity="intermediate",
                        category="test",
                        dependencies=[],
                        template_path=None,
                        preview_available=True,
                    ),
                    TemplateMetadata(
                        name="advanced",
                        display_name="Advanced",
                        description="Advanced template",
                        complexity="advanced",
                        category="test",
                        dependencies=[],
                        template_path=None,
                        preview_available=True,
                    ),
                ]

                mock_registry.list_templates.return_value = mock_templates
                mock_registry.get_template_categories.return_value = ["test"]

                # Call the function
                list_templates(category=None, verbose=False)

                # Verify console.print was called (table generation)
                mock_console.print.assert_called()

    def test_list_templates_usage_instructions(self):
        """Test that list_templates displays usage instructions."""
        with patch("fascraft.commands.list_templates.console") as mock_console:
            with patch(
                "fascraft.commands.list_templates.template_registry"
            ) as mock_registry:
                mock_templates = [
                    TemplateMetadata(
                        name="basic",
                        display_name="Basic CRUD",
                        description="Simple CRUD operations",
                        complexity="basic",
                        category="crud",
                        dependencies=["sqlalchemy"],
                        template_path=None,
                        preview_available=True,
                    )
                ]

                mock_registry.list_templates.return_value = mock_templates
                mock_registry.get_template_categories.return_value = ["crud"]

                # Call the function
                list_templates(category=None, verbose=False)

                # Verify usage instructions were displayed
                mock_console.print.assert_called()
                calls = mock_console.print.call_args_list
                usage_call = any("fascraft generate" in str(call) for call in calls)
                assert usage_call

    def test_list_templates_template_selection_tips(self):
        """Test that list_templates displays template selection tips."""
        with patch("fascraft.commands.list_templates.console") as mock_console:
            with patch(
                "fascraft.commands.list_templates.template_registry"
            ) as mock_registry:
                mock_templates = [
                    TemplateMetadata(
                        name="basic",
                        display_name="Basic CRUD",
                        description="Simple CRUD operations",
                        complexity="basic",
                        category="crud",
                        dependencies=["sqlalchemy"],
                        template_path=None,
                        preview_available=True,
                    )
                ]

                mock_registry.list_templates.return_value = mock_templates
                mock_registry.get_template_categories.return_value = ["crud"]

                # Call the function
                list_templates(category=None, verbose=False)

                # Verify template selection tips were displayed
                mock_console.print.assert_called()
                calls = mock_console.print.call_args_list
                tips_call = any(
                    "Template Selection Tips" in str(call) for call in calls
                )
                assert tips_call
