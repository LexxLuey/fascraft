#!/bin/bash
# FasCraft Test Runner for Unix/Linux/macOS

echo "🚀 FasCraft Test Runner for Unix/Linux/macOS"
echo "=============================================="

# Initialize status variables
all_passed=true
basic_tests_passed=false
coverage_passed=false
linting_passed=false
formatting_passed=false
import_sorting_passed=false
cli_passed=false
security_passed=false

echo ""
echo "🔍 Checking Python environment..."
python3 --version >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Python available"
    PYTHON_CMD="python3"
elif python --version >/dev/null 2>&1; then
    echo "✅ Python available"
    PYTHON_CMD="python"
else
    echo "❌ Python not available"
    all_passed=false
fi

poetry run pytest --version >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Pytest available"
else
    echo "❌ Pytest not available"
    all_passed=false
fi

echo ""
echo "📊 Running full test suite with coverage..."
poetry run pytest --cov=fascraft --cov-report=term-missing
if [ $? -eq 0 ]; then
    echo "✅ Coverage tests passed"
    coverage_passed=true
else
    echo "❌ Coverage tests failed"
    all_passed=false
fi

echo ""
echo "🔍 Running linting..."
poetry run ruff check .
if [ $? -eq 0 ]; then
    echo "✅ Linting passed"
    linting_passed=true
else
    echo "❌ Linting failed"
    all_passed=false
fi

echo ""
echo "🎨 Checking code formatting..."
poetry run black --check .
if [ $? -eq 0 ]; then
    echo "✅ Code formatting passed"
    formatting_passed=true
else
    echo "❌ Code formatting failed"
    all_passed=false
fi

echo ""
echo "📦 Checking import sorting..."
poetry run isort --check-only .
if [ $? -eq 0 ]; then
    echo "✅ Import sorting passed"
    import_sorting_passed=true
else
    echo "❌ Import sorting failed"
    all_passed=false
fi

echo ""
echo "🖥️ Testing CLI functionality..."
poetry run fascraft --help
if [ $? -eq 0 ]; then
    echo "✅ CLI functionality passed"
    cli_passed=true
else
    echo "❌ CLI functionality failed"
    echo "Error code: $?"
    all_passed=false
fi

echo ""
echo "🔒 Running security scan..."
poetry run bandit -r fascraft/ -f txt >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Security scan passed"
    security_passed=true
else
    echo "❌ Security scan failed"
    all_passed=false
fi

echo ""
echo "=============================================="
echo "📊 TEST SUMMARY"
echo "=============================================="
echo "Test Coverage:         $coverage_passed"
echo "Linting (Ruff):        $linting_passed"
echo "Code Formatting:       $formatting_passed"
echo "Import Sorting:        $import_sorting_passed"
echo "CLI Functionality:     $cli_passed"
echo "Security Scanning:     $security_passed"
echo "=============================================="

if [ "$all_passed" = true ]; then
    echo "🎉 All tests passed successfully!"
    echo "✅ FasCraft is production ready!"
else
    echo "⚠️  Some tests failed. Check the output above for details."
    echo "💡 You can still use FasCraft, but some features may not work correctly."
fi

echo ""
echo "✅ All tests completed!"
