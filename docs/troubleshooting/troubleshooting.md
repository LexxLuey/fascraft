# FasCraft Troubleshooting Guide

This guide helps you resolve common issues when using FasCraft. If you can't find a solution here, please check our [GitHub Issues](https://github.com/LexxLuey/fascraft/issues) or join our [Discord Community](https://discord.gg/fascraft).

## 🚨 **Critical Issues**

### **Project Creation Fails Completely**

#### **Error: "Permission denied" or "Access denied"**
```bash
❌ Error: Permission denied when creating project directory
```

**Causes:**
- Insufficient file system permissions
- Antivirus software blocking operations
- Windows User Account Control (UAC) restrictions

**Solutions:**
1. **Run as Administrator** (Windows):
   ```bash
   # Right-click PowerShell/Command Prompt → "Run as Administrator"
   poetry run fascraft new my-project
   ```

2. **Check Directory Permissions**:
   ```bash
   # Verify you have write access
   ls -la /target/directory
   # Windows: dir /target/directory
   ```

3. **Use Different Location**:
   ```bash
   # Try creating in your home directory
   poetry run fascraft new my-project --path ~/
   ```

#### **Error: "No space left on device"**
```bash
❌ Error: Insufficient disk space
```

**Solutions:**
1. **Check Available Space**:
   ```bash
   # Linux/Mac
   df -h
   
   # Windows
   dir C:\
   ```

2. **Free Up Space**:
   - Remove unnecessary files
   - Clear temporary directories
   - Empty trash/recycle bin

3. **Use Different Drive** (Windows):
   ```bash
   poetry run fascraft new my-project --path D:\projects\
   ```

### **Template Rendering Errors**

#### **Error: "Template rendering failed"**
```bash
❌ Template rendering failed: 'matrix' is undefined
```

**Causes:**
- Jinja2 template syntax errors
- Missing template variables
- Corrupted template files

**Solutions:**
1. **Reinstall FasCraft**:
   ```bash
   pip uninstall fascraft
   pip install fascraft --upgrade
   ```

2. **Clear Template Cache**:
   ```bash
   # Remove any cached templates
   rm -rf ~/.fascraft/templates/
   ```

3. **Check Template Files**:
   ```bash
   # Verify template integrity
   poetry run fascraft list-templates
   ```

## 🔧 **Common Issues**

### **Import Errors**

#### **Error: "No module named fascraft"**
```bash
ModuleNotFoundError: No module named 'fascraft'
```

**Solutions:**
1. **Install FasCraft**:
   ```bash
   pip install fascraft
   ```

2. **Use Poetry** (Recommended):
   ```bash
   poetry install
   poetry run fascraft new my-project
   ```

3. **Check Virtual Environment**:
   ```bash
   # Activate virtual environment
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

#### **Error: "No module named fascraft.__main__"**
```bash
ModuleNotFoundError: No module named 'fascraft.__main__'
```

**Solutions:**
1. **Use Poetry Script**:
   ```bash
   poetry run fascraft new my-project
   ```

2. **Check pyproject.toml**:
   ```toml
   [tool.poetry.scripts]
   fascraft = "fascraft.main:app"
   ```

### **Project Generation Issues**

#### **Error: "Module not found after generation"**
```bash
❌ Module 'users' not found
```

**Solutions:**
1. **Check Module Directory**:
   ```bash
   ls -la users/
   # Verify __init__.py exists
   ```

2. **Regenerate Module**:
   ```bash
   poetry run fascraft generate user --force
   ```

3. **Check Import Paths**:
   ```python
   # In main.py, ensure correct import
   from users.routers import router as users_router
   ```

#### **Error: "Database model errors"**
```bash
❌ Table 'users' doesn't exist
```

**Solutions:**
1. **Initialize Database**:
   ```bash
   # Create tables
   python -c "from config.database import init_db; init_db()"
   ```

2. **Run Migrations**:
   ```bash
   # If using Alembic
   alembic upgrade head
   ```

3. **Check Model Imports**:
   ```python
   # In config/database.py
   from users.models import UserModel  # Add this line
   ```

### **Docker Issues**

#### **Error: "Docker build failed"**
```bash
❌ Failed to build Docker image
```

**Solutions:**
1. **Check Docker Installation**:
   ```bash
   docker --version
   docker-compose --version
   ```

2. **Verify Dockerfile**:
   ```bash
   # Check if Dockerfile exists
   ls -la Dockerfile
   ```

3. **Build Manually**:
   ```bash
   docker build -t my-project .
   ```

#### **Error: "Port already in use"**
```bash
❌ Port 8000 is already in use
```

**Solutions:**
1. **Change Port**:
   ```bash
   # In main.py
   uvicorn.run(app, host="0.0.0.0", port=8001)
   ```

2. **Stop Conflicting Service**:
   ```bash
   # Find process using port 8000
   netstat -ano | findstr :8000  # Windows
   lsof -i :8000                 # Linux/Mac
   ```

3. **Use Different Port in Docker**:
   ```yaml
   # docker-compose.yml
   ports:
     - "8001:8000"
   ```

## 🐛 **Development Issues**

### **Testing Problems**

#### **Error: "pytest not found"**
```bash
❌ Command 'pytest' not found
```

**Solutions:**
1. **Install Development Dependencies**:
   ```bash
   pip install -r requirements.dev.txt
   ```

2. **Use Poetry**:
   ```bash
   poetry install --with dev
   poetry run pytest
   ```

3. **Install Pytest Directly**:
   ```bash
   pip install pytest pytest-cov
   ```

#### **Error: "Import errors in tests"**
```bash
❌ ModuleNotFoundError in test files
```

**Solutions:**
1. **Check PYTHONPATH**:
   ```bash
   # Add project root to Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. **Run Tests from Project Root**:
   ```bash
   cd /path/to/project
   python -m pytest
   ```

3. **Use Test Configuration**:
   ```python
   # In pytest.ini or pyproject.toml
   [tool.pytest.ini_options]
   pythonpath = ["."]
   ```

### **Code Quality Issues**

#### **Error: "Black formatting failed"**
```bash
❌ Black formatting check failed
```

**Solutions:**
1. **Format Code**:
   ```bash
   black .
   ```

2. **Check Black Version**:
   ```bash
   black --version
   pip install --upgrade black
   ```

3. **Ignore Specific Files**:
   ```python
   # In pyproject.toml
   [tool.black]
   exclude = '''
   /(
       migrations
     | .git
     | __pycache__
   )/
   '''
   ```

#### **Error: "Ruff linting failed"**
```bash
❌ Ruff check failed
```

**Solutions:**
1. **Fix Linting Issues**:
   ```bash
   ruff check --fix .
   ```

2. **Update Ruff**:
   ```bash
   pip install --upgrade ruff
   ```

3. **Configure Ruff**:
   ```python
   # In pyproject.toml
   [tool.ruff]
   line-length = 88
   target-version = "py39"
   ```

## 🌐 **Environment Issues**

### **Python Version Problems**

#### **Error: "Python version not supported"**
```bash
❌ Python 3.8 not supported
```

**Solutions:**
1. **Check Python Version**:
   ```bash
   python --version
   python3 --version
   ```

2. **Upgrade Python**:
   - Install Python 3.10+ from [python.org](https://python.org)
   - Use pyenv for version management

3. **Use Virtual Environment**:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

### **Dependency Conflicts**

#### **Error: "Dependency conflict"**
```bash
❌ Conflict between package versions
```

**Solutions:**
1. **Update Dependencies**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Use Poetry**:
   ```bash
   poetry update
   poetry install
   ```

3. **Check Compatibility**:
   ```bash
   pip check
   ```

## 🚀 **Performance Issues**

### **Slow Project Creation**

#### **Issue: "Project creation takes too long"**
```bash
⏱️ Project creation is slow
```

**Solutions:**
1. **Check Disk Performance**:
   - Use SSD instead of HDD
   - Ensure sufficient free space

2. **Optimize Network**:
   - Use local templates if available
   - Check internet connection

3. **Reduce Template Complexity**:
   - Use minimal templates for testing
   - Disable unnecessary features

### **Memory Issues**

#### **Error: "Out of memory"**
```bash
❌ MemoryError during template rendering
```

**Solutions:**
1. **Increase Memory**:
   - Close other applications
   - Restart terminal/IDE

2. **Use Smaller Templates**:
   - Generate projects one at a time
   - Avoid very large template files

3. **Check System Resources**:
   ```bash
   # Monitor memory usage
   top
   htop
   ```

## 🔍 **Debugging Tips**

### **Enable Verbose Logging**

```bash
# Set debug environment variable
export FASCRAFT_DEBUG=1
poetry run fascraft new my-project

# Or use Python logging
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python -c "import logging; logging.basicConfig(level=logging.DEBUG); from fascraft.commands.new import create_new_project"
```

### **Check Configuration**

```bash
# Verify FasCraft configuration
poetry run fascraft config show

# Check template locations
poetry run fascraft list-templates
```

### **Validate Project Structure**

```bash
# Analyze generated project
cd my-project
poetry run fascraft analyze

# Check for missing files
find . -name "*.py" -type f
```

## 📞 **Getting Help**

### **Self-Service Resources**

1. **Documentation**: Check our [comprehensive guides](docs/)
2. **Examples**: Review [example projects](../examples/)
3. **GitHub Issues**: Search [existing issues](https://github.com/LexxLuey/fascraft/issues)

### **Community Support**

1. **GitHub Discussions**: [Join the conversation](https://github.com/LexxLuey/fascraft/discussions)
2. **Discord Server**: [Get real-time help](https://discord.gg/fascraft)
3. **Stack Overflow**: Tag questions with `fascraft`

### **Reporting Issues**

When reporting issues, please include:

1. **Environment Details**:
   - Operating System and version
   - Python version
   - FasCraft version
   - Installation method

2. **Error Information**:
   - Complete error message
   - Steps to reproduce
   - Expected vs actual behavior

3. **System Information**:
   - Available disk space
   - Memory usage
   - Network connectivity

### **Issue Templates**

Use our [GitHub issue templates](https://github.com/LexxLuey/fascraft/issues/new/choose) for:
- 🐛 Bug reports
- 💡 Feature requests
- 📚 Documentation improvements
- ❓ Questions and support

## 🎯 **Prevention Tips**

### **Best Practices**

1. **Always use virtual environments**
2. **Keep dependencies updated**
3. **Test in clean environments**
4. **Backup important projects**
5. **Use version control (Git)**

### **Regular Maintenance**

1. **Update FasCraft monthly**
2. **Clean up old projects**
3. **Monitor disk space**
4. **Check for security updates**

---

**Still having issues?** Don't hesitate to reach out! Our community is here to help you succeed with FasCraft. 🚀

- **GitHub Issues**: [Report bugs](https://github.com/LexxLuey/fascraft/issues)
- **Discord**: [Get help](https://discord.gg/fascraft)
- **Documentation**: [Learn more](docs/)
