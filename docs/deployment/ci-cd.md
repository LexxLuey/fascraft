# 🚀 CI/CD Integration

FasCraft now includes comprehensive CI/CD support for all generated FastAPI projects, providing automated testing, quality checks, and deployment pipelines.

## ✨ **Features**

### **Multi-Platform Support**
- **GitHub Actions** - Automated workflows for testing, linting, and deployment
- **GitLab CI** - Comprehensive pipeline configuration with stages
- **Pre-commit Hooks** - Automated code quality checks before commits
- **Cross-platform** - Support for both platforms simultaneously

### **Automated Workflows**
- **Testing** - Multi-Python version testing with coverage reporting
- **Code Quality** - Automated linting, formatting, and style checks
- **Security** - Vulnerability scanning with Bandit and Safety
- **Dependencies** - Automated updates and security monitoring
- **Deployment** - Multi-environment deployment pipelines

## 🚀 **Usage**

### **New Projects (Automatic)**
When you create a new project with `fascraft new`, CI/CD support is automatically included:

```bash
# Create new project with CI/CD support
fascraft new my-api
cd my-api

# CI/CD files are automatically generated
ls -la .github/workflows/ .gitlab-ci.yml .pre-commit-config.yaml
```

### **Existing Projects**
Add CI/CD support to existing projects:

```bash
# Add GitHub Actions CI/CD
fascraft ci-cd add-ci-cd --platform github

# Add GitLab CI/CD
fascraft ci-cd add-ci-cd --platform gitlab

# Add both platforms
fascraft ci-cd add-ci-cd --platform both

# Setup environments and configurations
fascraft ci-cd setup
```

## 🏗️ **Generated CI/CD Files**

### **GitHub Actions Workflows**

#### **Main CI/CD Pipeline (`.github/workflows/ci.yml`)**
- **Multi-Python testing** (3.10, 3.11, 3.12)
- **Code quality checks** (Black, Ruff, isort, Flake8)
- **Security scanning** (Bandit, Safety)
- **Docker building** and testing
- **Multi-environment deployment** (dev, staging, prod)

#### **Dependency Updates (`.github/workflows/dependency-update.yml`)**
- **Scheduled dependency checks** (weekly)
- **Security vulnerability monitoring**
- **Automated pull request creation**
- **Manual update triggers**

### **GitLab CI Configuration (`.gitlab-ci.yml`)**
- **Multi-stage pipeline** (test, lint, security, build, deploy)
- **Parallel testing** across Python versions
- **Docker integration** with build and test
- **Environment-specific deployments**
- **Artifact management** and reporting

### **Pre-commit Hooks (`.pre-commit-config.yaml`)**
- **Code formatting** (Black, Ruff, isort)
- **Quality checks** (Flake8, Bandit, Safety)
- **Type checking** (MyPy)
- **Documentation** (Markdown linting)
- **Shell script** validation

## 🔧 **Commands**

### **Add CI/CD Support**
```bash
# Add GitHub Actions
fascraft ci-cd add-ci-cd --platform github

# Add GitLab CI
fascraft ci-cd add-ci-cd --platform gitlab

# Add both platforms
fascraft ci-cd add-ci-cd --platform both

# Force overwrite existing files
fascraft ci-cd add-ci-cd --platform github --force
```

### **Setup and Configuration**
```bash
# Setup CI/CD environments
fascraft ci-cd setup

# Configure environment variables
fascraft ci-cd setup --path /path/to/project
```

## 🌐 **Platform-Specific Features**

### **GitHub Actions**

#### **Workflow Triggers**
```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  schedule:
    - cron: '0 9 * * 1'  # Weekly dependency checks
```

#### **Jobs and Stages**
- **test** - Multi-Python version testing with coverage
- **lint** - Code quality and style enforcement
- **security** - Vulnerability scanning and reporting
- **build** - Docker image building and testing
- **deploy** - Environment-specific deployments

#### **Environment Protection**
```yaml
deploy-prod:
  environment: production
  if: github.ref == 'refs/heads/main'
  needs: [build]
```

### **GitLab CI**

#### **Pipeline Stages**
```yaml
stages:
  - test
  - lint
  - security
  - build
  - deploy
```

#### **Matrix Testing**
```yaml
test:
  parallel:
    matrix:
      - PYTHON_VERSION: ["3.10", "3.11", "3.12"]
```

#### **Environment Management**
```yaml
deploy-prod:
  environment:
    name: production
    url: https://my-api.example.com
  when: manual
  allow_failure: false
```

## 🔒 **Security Features**

### **Automated Security Scanning**
- **Bandit** - Python security linter
- **Safety** - Dependency vulnerability checker
- **SAST integration** - GitLab security scanning
- **Artifact reporting** - Security issue tracking

### **Code Quality Enforcement**
- **Pre-commit hooks** - Prevent low-quality code commits
- **Automated formatting** - Consistent code style
- **Type checking** - Catch type-related errors
- **Documentation validation** - Ensure proper docs

## 📊 **Testing and Coverage**

### **Multi-Version Testing**
```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
```

### **Coverage Reporting**
- **XML reports** for CI/CD integration
- **HTML reports** for local viewing
- **Coverage thresholds** enforcement
- **Codecov integration** for GitHub

### **Test Types**
- **Unit tests** - Individual component testing
- **Integration tests** - Component interaction testing
- **Security tests** - Vulnerability assessment
- **Performance tests** - Load and stress testing

## 🚀 **Deployment Pipelines**

### **Environment Strategy**
- **Development** - Automatic deployment on develop branch
- **Staging** - Manual deployment on main branch
- **Production** - Manual deployment with approval

### **Deployment Triggers**
```yaml
# Development - automatic
deploy-dev:
  if: github.ref == 'refs/heads/develop'

# Staging - manual
deploy-staging:
  if: github.ref == 'refs/heads/main'
  environment: staging

# Production - manual with approval
deploy-prod:
  if: github.ref == 'refs/heads/main'
  environment: production
```

## 🔧 **Configuration and Customization**

### **Environment Variables**
```bash
# Development
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG

# Staging
ENVIRONMENT=staging
DEBUG=false
LOG_LEVEL=INFO

# Production
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
```

### **Platform-Specific Settings**
```yaml
# GitHub Actions
env:
  PYTHON_VERSION: "3.10"
  POETRY_VERSION: "1.7.0"

# GitLab CI
variables:
  PYTHON_VERSION: "3.10"
  POETRY_VERSION: "1.7.0"
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.pip-cache"
```

### **Custom Workflows**
```yaml
# Add custom steps
- name: Custom deployment step
  run: |
    echo "Deploying to custom environment"
    # Your deployment logic here
```

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Workflow Not Triggering**
```bash
# Check branch names
git branch -a

# Verify workflow file location
ls -la .github/workflows/

# Check workflow syntax
# Use GitHub's workflow validator
```

#### **Tests Failing**
```bash
# Run tests locally
poetry run pytest

# Check dependencies
poetry show --outdated

# Verify Python version
python --version
```

#### **Pre-commit Hooks Failing**
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### **Debug Commands**
```bash
# Check CI/CD file syntax
yamllint .github/workflows/*.yml
yamllint .gitlab-ci.yml

# Validate pre-commit config
pre-commit validate-config

# Test specific hooks
pre-commit run black --all-files
```

## 📚 **Next Steps**

### **Advanced CI/CD Features**
- **Kubernetes deployment** integration
- **Cloud provider** deployment scripts
- **Monitoring and alerting** setup
- **Performance testing** automation

### **Integration Enhancements**
- **Slack notifications** for deployments
- **JIRA integration** for issue tracking
- **SonarQube** for code quality metrics
- **Artifact management** and versioning

### **Security Enhancements**
- **Container scanning** with Trivy
- **Infrastructure as Code** validation
- **Compliance checking** automation
- **Secret management** integration

---

**FasCraft CI/CD Integration** - Making continuous integration and deployment simple and powerful! 🚀
