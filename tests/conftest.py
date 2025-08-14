"""Pytest configuration and fixtures for FastForge tests."""

import tempfile
from pathlib import Path
from typing import Generator

import pytest
from typer.testing import CliRunner


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide a CLI runner for testing Typer commands."""
    return CliRunner()


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_project_name() -> str:
    """Provide a sample project name for testing."""
    return "test-api"


@pytest.fixture
def expected_files() -> list[str]:
    """Provide list of expected files in generated project."""
    return [
        "__init__.py", 
        "main.py", 
        "pyproject.toml", 
        "README.md",
        "config/__init__.py",
        "config/settings.py",
        "config/database.py",
        "config/exceptions.py",
        "config/middleware.py"
    ]
