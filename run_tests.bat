@echo off
setlocal enabledelayedexpansion

echo 🚀 FasCraft Test Runner for Windows
echo ======================================

set "all_passed=true"
set "basic_tests_passed=false"
set "coverage_passed=false"
set "linting_passed=false"
set "formatting_passed=false"
set "import_sorting_passed=false"
set "cli_passed=false"
set "security_passed=false"

echo.
echo 🔍 Checking Python environment...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python available
) else (
    echo ❌ Python not available
    set "all_passed=false"
)

poetry run pytest --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Pytest available
) else (
    echo ❌ Pytest not available
    set "all_passed=false"
)

echo.
echo 📊 Running full test suite with coverage...
poetry run pytest --cov=fascraft --cov-report=term-missing
if %errorlevel% equ 0 (
    echo ✅ Coverage tests passed
    set "coverage_passed=true"
) else (
    echo ❌ Coverage tests failed
    set "all_passed=false"
)

echo.
echo 🔍 Running linting...
poetry run ruff check .
if %errorlevel% equ 0 (
    echo ✅ Linting passed
    set "linting_passed=true"
) else (
    echo ❌ Linting failed
    set "all_passed=false"
)

echo.
echo 🎨 Checking code formatting...
poetry run black --check .
if %errorlevel% equ 0 (
    echo ✅ Code formatting passed
    set "formatting_passed=true"
) else (
    echo ❌ Code formatting failed
    set "all_passed=false"
)

echo.
echo 📦 Checking import sorting...
poetry run isort --check-only .
if %errorlevel% equ 0 (
    echo ✅ Import sorting passed
    set "import_sorting_passed=true"
) else (
    echo ❌ Import sorting failed
    set "all_passed=false"
)

echo.
echo 🖥️ Testing CLI functionality...
poetry run fascraft --help
if %errorlevel% equ 0 (
    echo ✅ CLI functionality passed
    set "cli_passed=true"
) else (
    echo ❌ CLI functionality failed
    echo Error code: %errorlevel%
    set "all_passed=false"
)

echo.
echo 🔒 Running security scan...
poetry run bandit -r fascraft/ -f txt >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Security scan passed
    set "security_passed=true"
) else (
    echo ❌ Security scan failed
    set "all_passed=false"
)

echo.
echo ======================================
echo 📊 TEST SUMMARY
echo ======================================
echo Test Coverage:         !coverage_passed!
echo Linting (Ruff):        !linting_passed!
echo Code Formatting:       !formatting_passed!
echo Import Sorting:        !import_sorting_passed!
echo CLI Functionality:     !cli_passed!
echo Security Scanning:     !security_passed!
echo ======================================

if "!all_passed!"=="true" (
    echo 🎉 All tests passed successfully!
    echo ✅ FasCraft is production ready!
) else (
    echo ⚠️  Some tests failed. Check the output above for details.
    echo 💡 You can still use FasCraft, but some features may not work correctly.
)

echo.
echo ✅ All tests completed!
pause