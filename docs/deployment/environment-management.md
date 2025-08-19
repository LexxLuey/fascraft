# 🌍 Environment Management

FasCraft provides comprehensive environment management capabilities for FastAPI projects, allowing developers to manage multiple environment configurations efficiently and securely.

## 🚀 Overview

The environment management system in FasCraft enables you to:

- **Initialize** environment management for existing projects
- **Create** new environment configurations with predefined templates
- **Switch** between different environments seamlessly
- **Validate** environment configurations for correctness
- **List** all available environments in a project
- **Manage** environment-specific settings and configurations

## 📋 Commands

### Initialize Environment Management

Initialize environment management for an existing FastAPI project:

```bash
# Initialize with default environments (dev, staging, prod)
fascraft environment init

# Initialize with custom environments
fascraft environment init --environments "dev,staging,prod,testing"

# Force overwrite existing environment files
fascraft environment init --force
```

**Options:**
- `--path, -p`: Path to the FastAPI project (default: current directory)
- `--environments, -e`: Comma-separated list of environments to create
- `--force, -f`: Overwrite existing environment files

### Create New Environment

Create a new environment configuration:

```bash
# Create development environment
fascraft environment create --name dev --template development

# Create custom environment
fascraft environment create --name custom --template custom

# Force overwrite existing environment
fascraft environment create --name staging --template staging --force
```

**Options:**
- `--path, -p`: Path to the FastAPI project (default: current directory)
- `--name, -n`: Name of the environment to create
- `--template, -t`: Template to use (development, staging, production, custom)
- `--force, -f`: Overwrite existing environment

### List Environments

List all available environments in a project:

```bash
# List all environments
fascraft environment list-envs

# List environments in specific project
fascraft environment list-envs --path /path/to/project
```

### Switch Environment

Switch to a different environment:

```bash
# Switch to development environment
fascraft environment switch --environment dev

# Switch to production environment
fascraft environment switch --environment prod
```

**Options:**
- `--path, -p`: Path to the FastAPI project (default: current directory)
- `--environment, -e`: Environment to switch to

### Validate Environments

Validate environment configurations:

```bash
# Validate all environments
fascraft environment validate

# Validate specific environment
fascraft environment validate --environment dev

# Validate environments in specific project
fascraft environment validate --path /path/to/project
```

## 🏗️ Architecture

### File Structure

When you initialize environment management, FasCraft creates the following structure:

```
project/
├── .env.dev                 # Development environment variables
├── .env.staging            # Staging environment variables
├── .env.prod               # Production environment variables
├── .env                    # Current active environment (symlinked)
├── .current_environment    # Environment indicator file
├── config/
│   ├── settings.py         # Enhanced settings with environment support
│   └── environments/
│       ├── environments.yml # Main environment configuration
│       ├── dev.yml         # Development environment config
│       ├── staging.yml     # Staging environment config
│       └── prod.yml        # Production environment config
```

### Environment Templates

FasCraft provides predefined environment templates:

#### Development Template
```bash
DEBUG=True
ENVIRONMENT=development
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///./app_dev.db
REDIS_URI=redis://localhost:6379/1
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

#### Staging Template
```bash
DEBUG=False
ENVIRONMENT=staging
LOG_LEVEL=INFO
DATABASE_URL=postgresql://staging_user:staging_pass@staging_db:5432/staging_db
REDIS_URI=redis://staging_redis:6379/0
CORS_ORIGINS=["https://staging.example.com"]
```

#### Production Template
```bash
DEBUG=False
ENVIRONMENT=production
LOG_LEVEL=WARNING
DATABASE_URL=postgresql://prod_user:prod_pass@prod_db:5432/prod_db
REDIS_URI=redis://prod_redis:6379/0
CORS_ORIGINS=["https://example.com"]
```

#### Testing Template
```bash
DEBUG=False
ENVIRONMENT=testing
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///./test.db
REDIS_URI=redis://localhost:6379/2
CORS_ORIGINS=["http://localhost:3000"]
```

## ⚙️ Configuration

### Environment Configuration Files

Each environment has a YAML configuration file that defines:

```yaml
environment: development
project: my-api
app:
  name: my-api
  version: 0.1.0
  debug: true
  host: 0.0.0.0
  port: 8000
database:
  url: sqlite:///./my-api_dev.db
  pool_size: 5
  max_overflow: 10
redis:
  url: redis://localhost:6379/1
  pool_size: 5
logging:
  level: DEBUG
  format: detailed
security:
  secret_key: your-dev-secret-key-here
  access_token_expire_minutes: 30
```

### Enhanced Settings

FasCraft creates an enhanced `settings.py` file with environment support:

```python
from fascraft.commands.environment import get_settings, get_environment

# Get current environment
current_env = get_environment()

# Get environment-specific settings
settings = get_settings()

# Check environment type
if settings.is_development():
    print("Running in development mode")
elif settings.is_production():
    print("Running in production mode")
```

## 🔄 Environment Switching

### How It Works

1. **Source Environment**: FasCraft reads from `.env.{environment}` file
2. **Target Environment**: Creates/updates `.env` file with source content
3. **Indicator**: Creates `.current_environment` file for tracking

### Example Workflow

```bash
# 1. Initialize environment management
fascraft environment init --environments "dev,staging,prod"

# 2. Switch to development
fascraft environment switch --environment dev

# 3. Verify current environment
fascraft environment list-envs

# 4. Switch to production
fascraft environment switch --environment prod

# 5. Validate production environment
fascraft environment validate --environment prod
```

## ✅ Validation

### What Gets Validated

- **Environment Files**: Existence and format of `.env.{environment}` files
- **YAML Configs**: Syntax and structure of environment configuration files
- **File Format**: Proper key-value pairs in environment files
- **Dependencies**: Required configuration files and directories

### Validation Results

```bash
✅ Environment Validation Results

✅ dev
  ⚠️ Environment config dev.yml not found

✅ staging
  ✅ All validations passed

❌ prod
  ❌ Invalid YAML in prod.yml: while parsing a block mapping
```

## 🚀 Use Cases

### Development Workflow

```bash
# Start development
fascraft environment switch --environment dev

# Run application
uvicorn main:app --reload

# Switch to staging for testing
fascraft environment switch --environment staging

# Deploy to staging
docker-compose up --build
```

### CI/CD Integration

```bash
# In CI/CD pipeline
if [ "$ENVIRONMENT" = "staging" ]; then
    fascraft environment switch --environment staging
elif [ "$ENVIRONMENT" = "production" ]; then
    fascraft environment switch --environment prod
fi

# Run application with environment-specific config
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Team Collaboration

```bash
# Developer A: Switch to development
fascraft environment switch --environment dev

# Developer B: Switch to staging
fascraft environment switch --environment staging

# Both can work on the same project with different configs
```

## 🔧 Customization

### Custom Environment Templates

Create custom environment configurations:

```bash
# Create custom environment
fascraft environment create --name custom --template custom

# Edit the generated files
# .env.custom - Environment variables
# config/environments/custom.yml - Configuration
```

### Environment-Specific Overrides

Modify environment configurations:

```yaml
# config/environments/custom.yml
environment: custom
app:
  debug: false
  port: 9000
database:
  url: postgresql://custom_user:custom_pass@custom_db:5432/custom_db
  pool_size: 15
```

### Advanced Configuration

Extend the enhanced settings for custom needs:

```python
# config/settings.py
class Settings(BaseSettings):
    # Add custom fields
    custom_setting: str = "default_value"
    api_rate_limit: int = 100
    
    # Environment-specific logic
    @property
    def is_custom_environment(self) -> bool:
        return self.environment == "custom"
```

## 🐛 Troubleshooting

### Common Issues

#### Environment Not Found
```bash
❌ Error: Environment 'missing' not found
💡 Solution: Run 'fascraft environment list-envs' to see available environments
```

#### Invalid YAML Configuration
```bash
❌ Error: Invalid YAML in dev.yml: while parsing a block mapping
💡 Solution: Check YAML syntax in config/environments/dev.yml
```

#### Template Rendering Errors
```bash
❌ Error: Failed to create enhanced settings
💡 Solution: Ensure project has proper FastAPI structure with main.py
```

### Debug Commands

```bash
# Check current environment
cat .current_environment

# View environment file content
cat .env

# Validate specific environment
fascraft environment validate --environment dev

# List all environment files
ls -la .env.*
ls -la config/environments/
```

### Recovery Steps

1. **Backup**: Always backup your environment files before major changes
2. **Validation**: Use `fascraft environment validate` to check configurations
3. **Reset**: Use `--force` flag to recreate environment files if needed
4. **Manual Fix**: Edit YAML files directly if automatic fixes fail

## 📚 Best Practices

### Environment Naming

- Use descriptive names: `dev`, `staging`, `prod`, `testing`
- Avoid special characters and spaces
- Use lowercase for consistency

### Configuration Management

- Keep sensitive data in environment variables, not in YAML files
- Use different database names for each environment
- Implement proper logging levels per environment
- Set appropriate CORS policies for each environment

### Security Considerations

- Never commit `.env` files to version control
- Use strong, unique secrets for each environment
- Implement proper access controls for production environments
- Regular rotation of secrets and credentials

### Version Control

```bash
# .gitignore additions
.env
.env.local
.env.*.local

# Commit environment templates
!.env.sample
!config/environments/
```

## 🔮 Future Enhancements

### Planned Features

- **Secrets Management**: Integration with external secret management systems
- **Feature Flags**: Environment-specific feature toggles
- **Configuration Encryption**: Encrypted environment configurations
- **Environment Cloning**: Copy and modify existing environments
- **Health Checks**: Environment-specific health check configurations

### Integration Possibilities

- **Kubernetes**: Native Kubernetes secret management
- **AWS**: AWS Systems Manager Parameter Store integration
- **Azure**: Azure Key Vault integration
- **GCP**: Google Secret Manager integration
- **HashiCorp Vault**: Vault integration for secrets

## 📖 Examples

### Complete Workflow Example

```bash
# 1. Navigate to your FastAPI project
cd my-fastapi-project

# 2. Initialize environment management
fascraft environment init --environments "dev,staging,prod"

# 3. Switch to development
fascraft environment switch --environment dev

# 4. Start development server
uvicorn main:app --reload

# 5. Create custom environment for testing
fascraft environment create --name testing --template custom

# 6. Switch to testing
fascraft environment switch --environment testing

# 7. Validate all environments
fascraft environment validate

# 8. List all environments
fascraft environment list-envs
```

### Docker Integration

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

# Install FasCraft
RUN pip install fascraft

# Initialize environment management
RUN fascraft environment init --environments "dev,staging,prod"

# Set default environment
ENV ENVIRONMENT=production

# Switch to production environment
RUN fascraft environment switch --environment prod

# Install dependencies and run
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### CI/CD Pipeline Example

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main, develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install FasCraft
        run: pip install fascraft
      
      - name: Setup Environment
        run: |
          if [ "${{ github.ref }}" = "refs/heads/develop" ]; then
            fascraft environment switch --environment staging
          elif [ "${{ github.ref }}" = "refs/heads/main" ]; then
            fascraft environment switch --environment prod
          fi
      
      - name: Deploy
        run: |
          # Your deployment logic here
          echo "Deploying to $ENVIRONMENT environment"
```

## 🤝 Contributing

### Development Setup

```bash
# Clone the repository
git clone https://github.com/your-org/fascraft.git

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/commands/test_environment.py -v

# Run linting
ruff check fascraft/commands/environment.py
```

### Testing

```bash
# Run environment management tests
pytest tests/commands/test_environment.py::TestEnvironmentCommand -v

# Run specific test
pytest tests/commands/test_environment.py::TestEnvironmentCommand::test_init_environment_management_success -v

# Run with coverage
pytest tests/commands/test_environment.py --cov=fascraft.commands.environment --cov-report=html
```

## 📄 License

This documentation is part of the FasCraft project and is licensed under the same terms as the project itself.

## 🆘 Support

### Getting Help

- **Documentation**: Check this guide and other FasCraft documentation
- **Issues**: Report bugs and feature requests on GitHub
- **Discussions**: Join community discussions for help and ideas
- **Examples**: Review the examples and use cases in this guide

### Community Resources

- **GitHub Repository**: [FasCraft GitHub](https://github.com/your-org/fascraft)
- **Documentation**: [FasCraft Docs](https://fascraft.readthedocs.io)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/fascraft/discussions)
- **Issues**: [GitHub Issues](https://github.com/your-org/fascraft/issues)
