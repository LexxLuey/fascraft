"""Tests for the testing utilities module."""

import json
import time
from pathlib import Path

import pytest

from fascraft.testing_utils import (
    DatabaseFixtureGenerator,
    MockDataGenerator,
    TestConfig,
    TestCoverageReporter,
    TestPerformanceMonitor,
    TestUtilities,
    create_test_config,
    create_test_utilities,
    generate_mock_data,
)


class TestTestConfig:
    """Test the TestConfig class."""

    def test_test_config_defaults(self):
        """Test TestConfig default values."""
        config = TestConfig()

        assert config.database_url == "sqlite:///:memory:"
        assert config.test_timeout == 30
        assert config.coverage_enabled is True
        assert config.mock_data_enabled is True
        assert config.coverage_report_formats == ["term", "html", "xml"]

    def test_test_config_custom_values(self):
        """Test TestConfig with custom values."""
        config = TestConfig(
            database_url="postgresql://test:test@localhost/test",
            test_timeout=60,
            coverage_enabled=False,
        )

        assert config.database_url == "postgresql://test:test@localhost/test"
        assert config.test_timeout == 60
        assert config.coverage_enabled is False


class TestDatabaseFixtureGenerator:
    """Test the DatabaseFixtureGenerator class."""

    def test_create_test_database(self):
        """Test creating test database configuration."""
        config = TestConfig()
        generator = DatabaseFixtureGenerator(config)

        db_config = generator.create_test_database("test_module")

        assert db_config["database_url"] == "sqlite:///:memory:"
        assert db_config["echo"] is False
        assert db_config["pool_pre_ping"] is True
        assert "check_same_thread" in db_config["connect_args"]

    def test_create_test_session(self):
        """Test creating test session configuration."""
        config = TestConfig()
        generator = DatabaseFixtureGenerator(config)

        session_config = generator.create_test_session("test_module")

        assert session_config["autocommit"] is False
        assert session_config["autoflush"] is False
        assert session_config["expire_on_commit"] is False

    def test_create_test_engine(self):
        """Test creating test engine configuration."""
        config = TestConfig()
        generator = DatabaseFixtureGenerator(config)

        engine_config = generator.create_test_engine("test_module")

        assert engine_config["poolclass"] == "StaticPool"
        assert engine_config["pool_size"] == 1
        assert engine_config["max_overflow"] == 0


class TestMockDataGenerator:
    """Test the MockDataGenerator class."""

    def test_generate_user_data_single(self):
        """Test generating single user data."""
        config = TestConfig()
        generator = MockDataGenerator(config)

        user_data = generator.generate_user_data(1)

        assert isinstance(user_data, dict)
        assert user_data["username"] == "testuser"
        assert user_data["email"] == "test@example.com"
        assert user_data["is_active"] is True

    def test_generate_user_data_multiple(self):
        """Test generating multiple user data."""
        config = TestConfig()
        generator = MockDataGenerator(config)

        users_data = generator.generate_user_data(3)

        assert isinstance(users_data, list)
        assert len(users_data) == 3
        assert users_data[0]["username"] == "testuser1"
        assert users_data[1]["username"] == "testuser2"
        assert users_data[2]["username"] == "testuser3"

    def test_generate_product_data_single(self):
        """Test generating single product data."""
        config = TestConfig()
        generator = MockDataGenerator(config)

        product_data = generator.generate_product_data(1)

        assert isinstance(product_data, dict)
        assert product_data["name"] == "Test Product"
        assert product_data["price"] == 99.99
        assert product_data["category"] == "electronics"

    def test_generate_order_data_single(self):
        """Test generating single order data."""
        config = TestConfig()
        generator = MockDataGenerator(config)

        order_data = generator.generate_order_data(1)

        assert isinstance(order_data, dict)
        assert order_data["user_id"] == 1
        assert order_data["total_amount"] == 99.99
        assert order_data["status"] == "pending"

    def test_generate_custom_data(self):
        """Test generating custom data with template."""
        config = TestConfig()
        generator = MockDataGenerator(config)

        template = {
            "name": "Item {index}",
            "description": "Description for item {index}",
            "created_at": "{timestamp}",
        }

        custom_data = generator.generate_custom_data(template, 2)

        assert isinstance(custom_data, list)
        assert len(custom_data) == 2
        assert custom_data[0]["name"] == "Item 1"
        assert custom_data[1]["name"] == "Item 2"


class TestTestCoverageReporter:
    """Test the TestCoverageReporter class."""

    def test_start_coverage(self):
        """Test starting coverage measurement."""
        config = TestConfig()
        reporter = TestCoverageReporter(config)

        reporter.start_coverage("test_module")

        assert "test_module" in reporter.coverage_data
        assert reporter.coverage_data["test_module"]["start_time"] is not None

    def test_stop_coverage(self):
        """Test stopping coverage measurement."""
        config = TestConfig()
        reporter = TestCoverageReporter(config)

        reporter.start_coverage("test_module")
        time.sleep(0.1)  # Small delay to ensure different timestamps
        result = reporter.stop_coverage("test_module")

        assert result["module"] == "test_module"
        assert result["lines_percentage"] == 85.0
        assert result["branches_percentage"] == 80.0

    def test_get_coverage_summary(self):
        """Test getting coverage summary."""
        config = TestConfig()
        reporter = TestCoverageReporter(config)

        # Add some coverage data
        reporter.coverage_data["module1"] = {
            "lines_covered": 80,
            "lines_total": 100,
            "branches_covered": 15,
            "branches_total": 20,
        }
        reporter.coverage_data["module2"] = {
            "lines_covered": 90,
            "lines_total": 100,
            "branches_covered": 18,
            "branches_total": 20,
        }

        summary = reporter.get_coverage_summary()

        assert summary["modules_tested"] == 2
        assert summary["total_lines_covered"] == 170
        assert summary["total_lines"] == 200
        assert summary["overall_line_coverage"] == 85.0


class TestTestPerformanceMonitor:
    """Test the TestPerformanceMonitor class."""

    def test_start_test(self):
        """Test starting test monitoring."""
        monitor = TestPerformanceMonitor()

        monitor.start_test("test_function")

        assert "test_function" in monitor.performance_data
        assert monitor.performance_data["test_function"]["start_time"] is not None

    def test_stop_test(self):
        """Test stopping test monitoring."""
        monitor = TestPerformanceMonitor()

        monitor.start_test("test_function")
        time.sleep(0.1)  # Small delay
        result = monitor.stop_test("test_function")

        assert result["test_name"] == "test_function"
        assert result["duration"] > 0

    def test_get_performance_summary(self):
        """Test getting performance summary."""
        monitor = TestPerformanceMonitor()

        # Add some performance data
        monitor.performance_data["test1"] = {"duration": 1.0}
        monitor.performance_data["test2"] = {"duration": 2.0}

        summary = monitor.get_performance_summary()

        assert summary["total_tests"] == 2
        assert summary["total_duration"] == 3.0
        assert summary["average_duration"] == 1.5
        assert summary["slowest_test"] == "test2"
        assert summary["fastest_test"] == "test1"


class TestTestUtilities:
    """Test the TestUtilities class."""

    def test_create_test_environment(self):
        """Test creating test environment."""
        config = TestConfig()
        utils = TestUtilities(config)

        env = utils.create_test_environment("test_module")

        assert "database" in env
        assert "session" in env
        assert "engine" in env
        assert "mock_data" in env
        assert len(env["mock_data"]["users"]) == 5

    def test_start_test_session(self):
        """Test starting test session."""
        config = TestConfig()
        utils = TestUtilities(config)

        utils.start_test_session("test_module::test_function")

        # Verify coverage and performance monitoring started
        assert "test_module" in utils.coverage_reporter.coverage_data
        assert (
            "test_module::test_function" in utils.performance_monitor.performance_data
        )

    def test_end_test_session(self):
        """Test ending test session."""
        config = TestConfig()
        utils = TestUtilities(config)

        utils.start_test_session("test_module::test_function")
        time.sleep(0.1)
        result = utils.end_test_session("test_module::test_function")

        assert result["test_name"] == "test_module::test_function"
        assert "coverage" in result
        assert "performance" in result

    def test_generate_test_report(self, tmp_path):
        """Test generating test report."""
        config = TestConfig()
        utils = TestUtilities(config)

        # Add some test data
        utils.start_test_session("test_module::test_function")
        utils.end_test_session("test_module::test_function")

        report_file = utils.generate_test_report(str(tmp_path))

        assert Path(report_file).exists()

        # Verify report content
        with open(report_file) as f:
            report_data = json.load(f)

        assert "coverage_summary" in report_data
        assert "performance_summary" in report_data
        assert "generated_at" in report_data


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_create_test_utilities(self):
        """Test create_test_utilities function."""
        utils = create_test_utilities()

        assert isinstance(utils, TestUtilities)
        assert utils.config.database_url == "sqlite:///:memory:"

    def test_create_test_utilities_custom_config(self):
        """Test create_test_utilities with custom config."""
        config = TestConfig(database_url="custom://url")
        utils = create_test_utilities(config)

        assert utils.config.database_url == "custom://url"

    def test_generate_mock_data(self):
        """Test generate_mock_data function."""
        user_data = generate_mock_data("user", 1)

        assert isinstance(user_data, dict)
        assert user_data["username"] == "testuser"

    def test_generate_mock_data_invalid_type(self):
        """Test generate_mock_data with invalid type."""
        with pytest.raises(ValueError, match="Unknown data type: invalid"):
            generate_mock_data("invalid", 1)

    def test_create_test_config(self):
        """Test create_test_config function."""
        config = create_test_config(database_url="custom://url", test_timeout=60)

        assert config.database_url == "custom://url"
        assert config.test_timeout == 60
        assert config.coverage_enabled is True  # Default value
