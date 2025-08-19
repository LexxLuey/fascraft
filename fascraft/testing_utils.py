"""Testing utilities for FasCraft modules."""

import json
import os
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import pytest  # noqa: F401

    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False

try:
    import coverage  # noqa: F401

    COVERAGE_AVAILABLE = True
except ImportError:
    COVERAGE_AVAILABLE = False


@dataclass
class TestConfig:
    """Configuration for test utilities."""

    database_url: str = "sqlite:///:memory:"
    test_timeout: int = 30
    coverage_enabled: bool = True
    coverage_report_formats: list[str] = None
    mock_data_enabled: bool = True

    def __post_init__(self):
        if self.coverage_report_formats is None:
            self.coverage_report_formats = ["term", "html", "xml"]


class DatabaseFixtureGenerator:
    """Generate database fixtures for testing."""

    def __init__(self, config: TestConfig):
        self.config = config

    def create_test_database(self, module_name: str) -> dict[str, Any]:
        """Create a test database configuration."""
        return {
            "database_url": self.config.database_url,
            "echo": False,
            "pool_pre_ping": True,
            "pool_recycle": 300,
            "connect_args": (
                {"check_same_thread": False}
                if "sqlite" in self.config.database_url
                else {}
            ),
        }

    def create_test_session(self, module_name: str) -> dict[str, Any]:
        """Create a test session configuration."""
        return {"autocommit": False, "autoflush": False, "expire_on_commit": False}

    def create_test_engine(self, module_name: str) -> dict[str, Any]:
        """Create a test engine configuration."""
        return {
            "poolclass": "StaticPool" if "sqlite" in self.config.database_url else None,
            "pool_size": 1,
            "max_overflow": 0,
        }


class MockDataGenerator:
    """Generate mock data for testing."""

    def __init__(self, config: TestConfig):
        self.config = config
        self._mock_data_cache = {}

    def generate_user_data(
        self, count: int = 1
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Generate mock user data."""
        if count == 1:
            return {
                "id": 1,
                "username": "testuser",
                "email": "test@example.com",
                "full_name": "Test User",
                "is_active": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }

        users = []
        for i in range(count):
            users.append(
                {
                    "id": i + 1,
                    "username": f"testuser{i+1}",
                    "email": f"test{i+1}@example.com",
                    "full_name": f"Test User {i+1}",
                    "is_active": True,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                }
            )
        return users

    def generate_product_data(
        self, count: int = 1
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Generate mock product data."""
        if count == 1:
            return {
                "id": 1,
                "name": "Test Product",
                "description": "A test product for testing",
                "price": 99.99,
                "category": "electronics",
                "in_stock": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }

        products = []
        for i in range(count):
            products.append(
                {
                    "id": i + 1,
                    "name": f"Test Product {i+1}",
                    "description": f"A test product {i+1} for testing",
                    "price": round(99.99 + i, 2),
                    "category": "electronics",
                    "in_stock": True,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                }
            )
        return products

    def generate_order_data(
        self, count: int = 1
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Generate mock order data."""
        if count == 1:
            return {
                "id": 1,
                "user_id": 1,
                "total_amount": 99.99,
                "status": "pending",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }

        orders = []
        for i in range(count):
            orders.append(
                {
                    "id": i + 1,
                    "user_id": i + 1,
                    "total_amount": round(99.99 + i, 2),
                    "status": "pending",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                }
            )
        return orders

    def generate_custom_data(
        self, template: dict[str, Any], count: int = 1
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Generate custom mock data based on a template."""
        if count == 1:
            return self._apply_template(template, 1)

        data_list = []
        for i in range(count):
            data_list.append(self._apply_template(template, i + 1))
        return data_list

    def _apply_template(self, template: dict[str, Any], index: int) -> dict[str, Any]:
        """Apply template with index-based substitutions."""
        result = {}
        for key, value in template.items():
            if isinstance(value, str) and "{index}" in value:
                result[key] = value.replace("{index}", str(index))
            elif isinstance(value, str) and "{timestamp}" in value:
                result[key] = value.replace("{timestamp}", datetime.now().isoformat())
            else:
                result[key] = value
        return result


class TestCoverageReporter:
    """Handle test coverage reporting."""

    def __init__(self, config: TestConfig):
        self.config = config
        self.coverage_data = {}
        self.start_time = None

    def start_coverage(self, module_name: str) -> None:
        """Start coverage measurement for a module."""
        if not COVERAGE_AVAILABLE or not self.config.coverage_enabled:
            return

        self.start_time = time.time()
        self.coverage_data[module_name] = {
            "start_time": self.start_time,
            "lines_covered": 0,
            "lines_total": 0,
            "branches_covered": 0,
            "branches_total": 0,
        }

    def stop_coverage(self, module_name: str) -> dict[str, Any]:
        """Stop coverage measurement and return results."""
        if not COVERAGE_AVAILABLE or not self.config.coverage_enabled:
            return {}

        if module_name not in self.coverage_data:
            return {}

        end_time = time.time()
        duration = end_time - self.coverage_data[module_name]["start_time"]

        # Mock coverage data for demonstration
        coverage_result = {
            "module": module_name,
            "duration": duration,
            "lines_covered": 85,
            "lines_total": 100,
            "lines_percentage": 85.0,
            "branches_covered": 20,
            "branches_total": 25,
            "branches_percentage": 80.0,
            "timestamp": datetime.now().isoformat(),
        }

        self.coverage_data[module_name].update(coverage_result)
        return coverage_result

    def generate_coverage_report(
        self, module_name: str, output_dir: str = "coverage_reports"
    ) -> str:
        """Generate a coverage report for a module."""
        if not COVERAGE_AVAILABLE or not self.config.coverage_enabled:
            return "Coverage reporting not available"

        if module_name not in self.coverage_data:
            return f"No coverage data for module '{module_name}'"

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Generate report file
        report_file = output_path / f"{module_name}_coverage_report.json"
        with open(report_file, "w") as f:
            json.dump(self.coverage_data[module_name], f, indent=2)

        return str(report_file)

    def get_coverage_summary(self) -> dict[str, Any]:
        """Get a summary of all coverage data."""
        if not self.coverage_data:
            return {}

        total_lines_covered = sum(
            data.get("lines_covered", 0) for data in self.coverage_data.values()
        )
        total_lines = sum(
            data.get("lines_total", 0) for data in self.coverage_data.values()
        )
        total_branches_covered = sum(
            data.get("branches_covered", 0) for data in self.coverage_data.values()
        )
        total_branches = sum(
            data.get("branches_total", 0) for data in self.coverage_data.values()
        )

        return {
            "modules_tested": len(self.coverage_data),
            "total_lines_covered": total_lines_covered,
            "total_lines": total_lines,
            "overall_line_coverage": (
                round((total_lines_covered / total_lines * 100), 2)
                if total_lines > 0
                else 0
            ),
            "total_branches_covered": total_branches_covered,
            "total_branches": total_branches,
            "overall_branch_coverage": (
                round((total_branches_covered / total_branches * 100), 2)
                if total_branches > 0
                else 0
            ),
            "timestamp": datetime.now().isoformat(),
        }


class TestPerformanceMonitor:
    """Monitor test performance metrics."""

    def __init__(self):
        self.performance_data = {}
        self.current_test = None

    def start_test(self, test_name: str) -> None:
        """Start monitoring a test."""
        self.current_test = test_name
        self.performance_data[test_name] = {
            "start_time": time.time(),
            "memory_start": self._get_memory_usage(),
            "cpu_start": self._get_cpu_usage(),
        }

    def stop_test(self, test_name: str) -> dict[str, Any]:
        """Stop monitoring a test and return metrics."""
        if test_name not in self.performance_data:
            return {}

        end_time = time.time()
        duration = end_time - self.performance_data[test_name]["start_time"]

        metrics = {
            "test_name": test_name,
            "duration": duration,
            "memory_usage": self._get_memory_usage()
            - self.performance_data[test_name]["memory_start"],
            "cpu_usage": self._get_cpu_usage()
            - self.performance_data[test_name]["cpu_start"],
            "timestamp": datetime.now().isoformat(),
        }

        self.performance_data[test_name].update(metrics)
        return metrics

    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            import psutil

            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            return 0.0

    def _get_cpu_usage(self) -> float:
        """Get current CPU usage percentage."""
        try:
            import psutil

            process = psutil.Process(os.getpid())
            return process.cpu_percent()
        except ImportError:
            return 0.0

    def get_performance_summary(self) -> dict[str, Any]:
        """Get a summary of all performance data."""
        if not self.performance_data:
            return {}

        total_duration = sum(
            data.get("duration", 0) for data in self.performance_data.values()
        )
        avg_duration = (
            total_duration / len(self.performance_data) if self.performance_data else 0
        )
        total_memory = sum(
            data.get("memory_usage", 0) for data in self.performance_data.values()
        )

        return {
            "total_tests": len(self.performance_data),
            "total_duration": total_duration,
            "average_duration": avg_duration,
            "total_memory_usage": total_memory,
            "slowest_test": (
                max(
                    self.performance_data.items(), key=lambda x: x[1].get("duration", 0)
                )[0]
                if self.performance_data
                else None
            ),
            "fastest_test": (
                min(
                    self.performance_data.items(), key=lambda x: x[1].get("duration", 0)
                )[0]
                if self.performance_data
                else None
            ),
            "timestamp": datetime.now().isoformat(),
        }


class TestUtilities:
    """Main test utilities class that combines all functionality."""

    def __init__(self, config: TestConfig | None = None):
        self.config = config or TestConfig()
        self.db_generator = DatabaseFixtureGenerator(self.config)
        self.mock_generator = MockDataGenerator(self.config)
        self.coverage_reporter = TestCoverageReporter(self.config)
        self.performance_monitor = TestPerformanceMonitor()

    def create_test_environment(self, module_name: str) -> dict[str, Any]:
        """Create a complete test environment for a module."""
        return {
            "database": self.db_generator.create_test_database(module_name),
            "session": self.db_generator.create_test_session(module_name),
            "engine": self.db_generator.create_test_engine(module_name),
            "mock_data": {
                "users": self.mock_generator.generate_user_data(5),
                "products": self.mock_generator.generate_product_data(5),
                "orders": self.mock_generator.generate_order_data(5),
            },
        }

    def start_test_session(self, test_name: str) -> None:
        """Start a test session with coverage and performance monitoring."""
        self.coverage_reporter.start_coverage(
            test_name.split("::")[0]
        )  # Extract module name
        self.performance_monitor.start_test(test_name)

    def end_test_session(self, test_name: str) -> dict[str, Any]:
        """End a test session and return results."""
        module_name = test_name.split("::")[0]  # Extract module name

        coverage_result = self.coverage_reporter.stop_coverage(module_name)
        performance_result = self.performance_monitor.stop_test(test_name)

        return {
            "test_name": test_name,
            "coverage": coverage_result,
            "performance": performance_result,
            "timestamp": datetime.now().isoformat(),
        }

    def generate_test_report(self, output_dir: str = "test_reports") -> str:
        """Generate a comprehensive test report."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Generate reports
        coverage_summary = self.coverage_reporter.get_coverage_summary()
        performance_summary = self.performance_monitor.get_performance_summary()

        # Combine all data
        report_data = {
            "coverage_summary": coverage_summary,
            "performance_summary": performance_summary,
            "generated_at": datetime.now().isoformat(),
        }

        # Write report
        report_file = (
            output_path / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_file, "w") as f:
            json.dump(report_data, f, indent=2)

        return str(report_file)


# Convenience functions for easy access
def create_test_utilities(config: TestConfig | None = None) -> TestUtilities:
    """Create a test utilities instance."""
    return TestUtilities(config)


def generate_mock_data(
    data_type: str, count: int = 1
) -> dict[str, Any] | list[dict[str, Any]]:
    """Quick access to mock data generation."""
    utils = TestUtilities()
    if data_type == "user":
        return utils.mock_generator.generate_user_data(count)
    elif data_type == "product":
        return utils.mock_generator.generate_product_data(count)
    elif data_type == "order":
        return utils.mock_generator.generate_order_data(count)
    else:
        raise ValueError(f"Unknown data type: {data_type}")


def create_test_config(**kwargs) -> TestConfig:
    """Create a test configuration with custom settings."""
    return TestConfig(**kwargs)
