# FasCraft Development Makefile
# Simple commands for common development tasks

.PHONY: help install test lint format clean

# Default target
help:
	@echo "FasCraft Development Commands:"
	@echo ""
	@echo "Installation:"
	@echo "  install     Install dependencies with Poetry"
	@echo "  install-dev Install development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  test        Run all tests"
	@echo "  test-verbose Run tests with verbose output"
	@echo "  test-cov    Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint        Run Ruff linter"
	@echo "  lint-fix    Run Ruff linter with auto-fix"
	@echo "  format      Format code with Ruff"
	@echo "  format-check Check code formatting"
	@echo "  all-checks  Run all code quality checks"
	@echo ""
	@echo "Development:"
	@echo "  clean       Clean up generated files and caches"
	@echo "  cli         Run FasCraft CLI"
	@echo "  cli-help    Show CLI help"

# Installation
install:
	poetry install

install-dev:
	poetry install --with dev

# Testing
test:
	poetry run pytest tests/ -v

test-verbose:
	poetry run pytest tests/ -vv

test-cov:
	poetry run pytest tests/ --cov=fascraft --cov-report=html

# Code Quality
lint:
	poetry run ruff check .

lint-fix:
	poetry run ruff check --fix .

format:
	poetry run ruff format .

format-check:
	poetry run ruff format --check .

all-checks:
	poetry run ruff check . && poetry run ruff format --check . && poetry run black --check .

# Development
clean:
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

cli:
	poetry run fascraft --help

cli-help:
	poetry run fascraft new --help
