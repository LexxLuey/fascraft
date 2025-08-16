# FasCraft Publishing Guide 🚀

This guide covers the complete process of publishing FasCraft to PyPI, including version management, building packages, and deployment.

## **📋 Pre-Publication Checklist**

Before publishing, ensure you have:

- ✅ **PyPI Account**: Username and password for [PyPI](https://pypi.org)
- ✅ **TestPyPI Account**: Username and password for [TestPyPI](https://test.pypi.org)
- ✅ **Poetry Configuration**: Poetry configured with your PyPI credentials
- ✅ **Clean Working Directory**: No uncommitted changes
- ✅ **All Tests Passing**: `poetry run pytest` succeeds
- ✅ **Version Consistency**: All version references updated

## **🔢 Version Management**

### **1. Poetry Version Commands**

FasCraft uses semantic versioning (MAJOR.MINOR.PATCH). Poetry provides powerful version management:

```bash
# Check current version
poetry version

# Update to specific version
poetry version 0.3.1

# Bump versions automatically
poetry version patch    # 0.3.0 → 0.3.1
poetry version minor    # 0.3.0 → 0.4.0
poetry version major    # 0.3.0 → 1.0.0

# Get version string only (useful for scripts)
poetry version -s
```

**What Poetry does automatically:**
- ✅ Updates `pyproject.toml` version
- ✅ Updates `poetry.lock` if needed
- ✅ Provides version validation

**What you need to do manually:**
- 📝 Update version in `fascraft/__init__.py`
- 📝 Update version in `fascraft/main.py`

### **2. Update Python File Versions**

After using `poetry version`, you'll need to manually update version references in your Python files:

1. **`fascraft/__init__.py`**
```python
__version__ = "0.3.1"  # Update this line
```

2. **`fascraft/main.py`**
```python
version_text.append("0.3.1", style="bold green")  # Update this line
```

**Pro Tip:** You can use search and replace in your editor to quickly update all version references.

## **🏗️ Building Packages**

### **1. Clean Previous Builds**

```bash
# Remove old distribution files
rm -rf dist/
rm -rf build/
rm -rf *.egg-info/

# Clean Poetry cache (optional)
poetry cache clear . --all
```

### **2. Build Distribution Packages**

```bash
# Build using Poetry (recommended)
poetry build

# Verify build output
ls -la dist/
# Should show:
# - fascraft-0.3.1.tar.gz (source distribution)
# - fascraft-0.3.1-py3-none-any.whl (wheel distribution)
```

### **3. Verify Package Contents**

```bash
# Check wheel contents
unzip -l dist/fascraft-0.3.1-py3-none-any.whl

# Check source distribution
tar -tzf dist/fascraft-0.3.1.tar.gz | head -20
```

### **4. Test Package Locally**

```bash
# Install from wheel locally
pip install dist/fascraft-0.3.1-py3-none-any.whl

# Test CLI functionality
fascraft --help
fascraft version

# Uninstall test installation
pip uninstall fascraft -y
```

## **📤 Publishing to PyPI**

### **1. Configure Poetry Credentials**

```bash
# Configure PyPI credentials
poetry config pypi-token.pypi YOUR_PYPI_TOKEN
poetry config pypi-token.testpypi YOUR_TESTPYPI_TOKEN

# Or use username/password (less secure)
poetry config pypi-token.pypi ""
poetry config http-basic.pypi YOUR_USERNAME YOUR_PASSWORD
poetry config http-basic.testpypi YOUR_USERNAME YOUR_PASSWORD
```

### **2. Test on TestPyPI**

```bash
# Publish to TestPyPI first
poetry publish --repository testpypi

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ fascraft
fascraft version

# Uninstall test version
pip uninstall fascraft -y
```

### **3. Publish to Production PyPI**

```bash
# Publish to main PyPI
poetry publish

# Verify publication
pip install fascraft
fascraft version
```

## **🔍 Post-Publication Verification**

### **1. Check PyPI Listing**

- Visit [https://pypi.org/project/fascraft/](https://pypi.org/project/fascraft/)
- Verify version number and description
- Check download statistics

### **2. Test Installation**

```bash
# Test in clean environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate
pip install fascraft
fascraft --help
fascraft version
deactivate
rm -rf test_env
```

### **3. Update Documentation**

- Update PyPI badges in README.md
- Update installation instructions if needed
- Update CHANGELOG.md with release notes

## **🚨 Troubleshooting**

### **Common Issues**

1. **Authentication Errors**
```bash
# Clear Poetry cache and reconfigure
poetry cache clear pypi --all
poetry config pypi-token.pypi YOUR_TOKEN
```

2. **Version Already Exists**
```bash
# Check current version on PyPI
pip index versions fascraft

# Update version number and rebuild
poetry version patch    # or use specific version
poetry build
poetry publish
```

3. **Build Failures**
```bash
# Check Poetry configuration
poetry check

# Verify pyproject.toml syntax
poetry validate

# Clean and rebuild
rm -rf dist/ build/
poetry build
```

### **Rollback Procedure**

If you need to remove a published version:

```bash
# Note: PyPI doesn't allow version deletion
# You can only yank (mark as broken)
pip install twine
twine delete --username YOUR_USERNAME fascraft 0.3.1

# Or mark as broken
twine yank --username YOUR_USERNAME fascraft 0.3.1
```

## **📚 Release Workflow Summary**

```bash
# 1. Update version using Poetry
poetry version patch    # or: poetry version 0.3.1
poetry version          # verify the new version

# 2. Update Python file versions manually
# Edit fascraft/__init__.py and fascraft/main.py

# 3. Commit changes
git add .
git commit -m "Release version $(poetry version -s)"
git tag v$(poetry version -s)
git push origin main --tags

# 4. Build packages
poetry build

# 5. Test locally
pip install dist/fascraft-$(poetry version -s)-py3-none-any.whl
fascraft version
pip uninstall fascraft -y

# 6. Publish to TestPyPI
poetry publish --repository testpypi

# 7. Test from TestPyPI
pip install --index-url https://test.pypi.org/simple/ fascraft
fascraft version
pip uninstall fascraft -y

# 8. Publish to PyPI
poetry publish

# 9. Verify publication
pip install fascraft
fascraft version
```

## **🎯 Best Practices**

- **Always test on TestPyPI first** before publishing to production
- **Use Poetry's version commands** for consistent version management
- **Use semantic versioning** consistently (MAJOR.MINOR.PATCH)
- **Keep build artifacts** in version control (dist/ directory)
- **Document breaking changes** in CHANGELOG.md
- **Test installation** in clean environments
- **Monitor PyPI statistics** after release

## **📖 Quick Reference: Poetry Version Commands**

```bash
# Version Management
poetry version                    # Show current version
poetry version -s                # Show version string only
poetry version patch             # Bump patch version (0.3.0 → 0.3.1)
poetry version minor             # Bump minor version (0.3.0 → 0.4.0)
poetry version major             # Bump major version (0.3.0 → 1.0.0)
poetry version 1.2.3            # Set specific version

# Publishing
poetry build                     # Build distribution packages
poetry publish                   # Publish to PyPI
poetry publish --repository testpypi  # Publish to TestPyPI

# Configuration
poetry config pypi-token.pypi YOUR_TOKEN     # Set PyPI token
poetry config pypi-token.testpypi YOUR_TOKEN # Set TestPyPI token
```

## **🔗 Useful Resources**

- [Python Packaging User Guide](https://packaging.python.org/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [PyPI Help](https://pypi.org/help/)
- [TestPyPI Help](https://test.pypi.org/help/)

---

**Happy Publishing! 🚀**

FasCraft is ready to make its mark on the Python ecosystem!