# Database Migration Guide

Learn how to manage database schema changes in your FasCraft projects using Alembic. This guide covers migration setup, creating and applying migrations, and best practices for database evolution.

## 🚀 Overview

Database migrations allow you to:
- **Version control your database schema** alongside your code
- **Safely evolve your database** as your application grows
- **Collaborate with team members** on schema changes
- **Deploy database changes** consistently across environments
- **Rollback changes** when needed

## 📋 Prerequisites

### Install Alembic
```bash
# Install alembic
pip install alembic

# Or add to requirements.txt
echo "alembic>=1.12.0" >> requirements.txt
```

### Database Setup
Ensure your database configuration is working:
```python
# config/database.py should be properly configured
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Your database engine and session setup
```

## 🏗️ Initial Setup

### Initialize Alembic
```bash
# Navigate to your project root
cd my-project

# Initialize alembic
alembic init alembic
```

This creates:
```
alembic/
├── env.py              # Migration environment configuration
├── script.py.mako      # Migration template
├── README              # Alembic documentation
└── versions/           # Migration files directory
alembic.ini            # Alembic configuration file
```

### Configure `alembic.ini`
```ini
# alembic.ini
[alembic]
# Path to migration scripts
script_location = alembic

# Database connection string
sqlalchemy.url = sqlite:///./app.db

# Template used to generate migration files
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(rev)s_%%(slug)s

# Logging configuration
loggers = alembic, sqlalchemy
```

### Configure `alembic/env.py`
```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

# Import your models and configuration
from config.database import Base
from config.settings import get_settings

# Import all models to register them with Base.metadata
from users.models import UserModel  # Add your models here
from products.models import ProductModel
from orders.models import OrderModel

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Update the config section to use your database URL
settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.database_url)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## 🔄 Creating Migrations

### Auto-Generate Migration
```bash
# Generate migration from model changes
alembic revision --autogenerate -m "Add user table"

# Generate migration for specific changes
alembic revision --autogenerate -m "Add email field to users"
```

### Manual Migration
```bash
# Create empty migration
alembic revision -m "Custom migration"
```

Then edit the generated file:
```python
# alembic/versions/20231201_120000_add_user_table.py
"""Add user table

Revision ID: 20231201_120000
Revises: 
Create Date: 2023-12-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '20231201_120000'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

def downgrade() -> None:
    # Drop users table
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
```

## 🚀 Applying Migrations

### Apply All Pending Migrations
```bash
# Apply all migrations up to the latest
alembic upgrade head

# Apply specific migration
alembic upgrade 20231201_120000

# Apply one migration forward
alembic upgrade +1
```

### Check Migration Status
```bash
# Check current migration
alembic current

# Check migration history
alembic history

# Check migration history with details
alembic history --verbose

# Check what migrations are pending
alembic show head
```

## 🔄 Rolling Back Migrations

### Rollback Migrations
```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific migration
alembic downgrade 20231201_120000

# Rollback to beginning
alembic downgrade base

# Rollback to previous migration
alembic downgrade -1
```

### Rollback Examples
```bash
# Rollback the last migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade 20231201_120000

# Rollback all migrations
alembic downgrade base
```

## 🎯 Common Migration Scenarios

### Adding a New Table
```bash
# 1. Create the model in your module
# users/models.py
class UserModel(Base):
    __tablename__ = "users"
    # ... model definition

# 2. Generate migration
alembic revision --autogenerate -m "Add users table"

# 3. Apply migration
alembic upgrade head
```

### Adding a New Column
```bash
# 1. Modify the model
# users/models.py
class UserModel(Base):
    __tablename__ = "users"
    # ... existing columns
    phone = Column(String(20), nullable=True)  # New column

# 2. Generate migration
alembic revision --autogenerate -m "Add phone to users"

# 3. Apply migration
alembic upgrade head
```

### Modifying Column Type
```python
# alembic/versions/20231201_130000_modify_username_length.py
def upgrade() -> None:
    # Modify column type
    op.alter_column('users', 'username',
        existing_type=sa.String(length=50),
        type_=sa.String(length=100),
        existing_nullable=False)

def downgrade() -> None:
    # Revert column type
    op.alter_column('users', 'username',
        existing_type=sa.String(length=100),
        type_=sa.String(length=50),
        existing_nullable=False)
```

### Adding Indexes
```python
# alembic/versions/20231201_140000_add_user_indexes.py
def upgrade() -> None:
    # Add index on created_at for sorting
    op.create_index('ix_users_created_at', 'users', ['created_at'])

def downgrade() -> None:
    # Remove index
    op.drop_index('ix_users_created_at', table_name='users')
```

### Adding Foreign Keys
```python
# alembic/versions/20231201_150000_add_user_orders.py
def upgrade() -> None:
    # Add foreign key column
    op.add_column('orders', sa.Column('user_id', sa.Integer(), nullable=True))
    
    # Add foreign key constraint
    op.create_foreign_key('fk_orders_user_id', 'orders', 'users', ['user_id'], ['id'])

def downgrade() -> None:
    # Remove foreign key constraint
    op.drop_constraint('fk_orders_user_id', 'orders', type_='foreignkey')
    
    # Remove column
    op.drop_column('orders', 'user_id')
```

## 🔧 Advanced Migration Features

### Data Migrations
```python
# alembic/versions/20231201_160000_populate_default_values.py
def upgrade() -> None:
    # Get connection
    connection = op.get_bind()
    
    # Update existing records
    connection.execute(
        "UPDATE users SET is_active = true WHERE is_active IS NULL"
    )

def downgrade() -> None:
    # Revert changes if needed
    connection = op.get_bind()
    connection.execute(
        "UPDATE users SET is_active = NULL WHERE is_active = true"
    )
```

### Conditional Migrations
```python
# alembic/versions/20231201_170000_conditional_migration.py
def upgrade() -> None:
    # Check if column exists before adding
    inspector = inspect(op.get_bind())
    columns = [c['name'] for c in inspector.get_columns('users')]
    
    if 'avatar_url' not in columns:
        op.add_column('users', sa.Column('avatar_url', sa.String(255), nullable=True))

def downgrade() -> None:
    # Remove column if it exists
    inspector = inspect(op.get_bind())
    columns = [c['name'] for c in inspector.get_columns('users')]
    
    if 'avatar_url' in columns:
        op.drop_column('users', 'avatar_url')
```

### Environment-Specific Migrations
```python
# alembic/versions/20231201_180000_env_specific.py
import os

def upgrade() -> None:
    environment = os.getenv('ENVIRONMENT', 'development')
    
    if environment == 'production':
        # Production-specific changes
        op.execute("CREATE INDEX CONCURRENTLY ix_users_email_prod ON users(email)")
    else:
        # Development changes
        op.create_index('ix_users_email_dev', 'users', ['email'])

def downgrade() -> None:
    environment = os.getenv('ENVIRONMENT', 'development')
    
    if environment == 'production':
        op.execute("DROP INDEX CONCURRENTLY ix_users_email_prod")
    else:
        op.drop_index('ix_users_email_dev', table_name='users')
```

## 🧪 Testing Migrations

### Test Migration Process
```bash
# 1. Create test database
sqlite3 test.db ".databases"

# 2. Update alembic.ini for testing
# sqlalchemy.url = sqlite:///./test.db

# 3. Run migrations
alembic upgrade head

# 4. Verify schema
sqlite3 test.db ".schema"

# 5. Test rollback
alembic downgrade -1
```

### Migration Testing Script
```python
# tests/test_migrations.py
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
import tempfile
import os

def test_migration_upgrade_downgrade():
    """Test that migrations can be applied and rolled back."""
    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        # Create alembic config for testing
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
        
        # Run migrations
        command.upgrade(alembic_cfg, "head")
        
        # Verify tables exist
        engine = create_engine(f"sqlite:///{db_path}")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result]
            assert "users" in tables
        
        # Test rollback
        command.downgrade(alembic_cfg, "base")
        
        # Verify tables removed
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result]
            assert "users" not in tables
            
    finally:
        # Clean up
        os.unlink(db_path)
```

## 🚀 Deployment Workflow

### Development Workflow
```bash
# 1. Make model changes
# Edit your models (e.g., users/models.py)

# 2. Generate migration
alembic revision --autogenerate -m "Description of changes"

# 3. Review generated migration
# Check alembic/versions/xxx_migration.py

# 4. Apply migration
alembic upgrade head

# 5. Test your changes
pytest
```

### Production Deployment
```bash
# 1. Backup database (important!)
pg_dump mydb > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. Deploy code with migrations
git pull origin main

# 3. Run migrations
alembic upgrade head

# 4. Verify deployment
alembic current
```

### CI/CD Integration
```yaml
# .github/workflows/deploy.yml
- name: Run Database Migrations
  run: |
    # Install dependencies
    pip install -r requirements.txt
    
    # Run migrations
    alembic upgrade head
    
    # Verify migration status
    alembic current
```

## 🎯 Best Practices

### Migration Naming
- Use descriptive names: `add_user_table`, `modify_email_field`
- Include date prefix: `20231201_120000_add_user_table`
- Be specific about what changes

### Migration Safety
- **Always backup** before running migrations in production
- **Test migrations** in development/staging first
- **Review auto-generated migrations** before applying
- **Use transactions** when possible
- **Plan rollback strategy** for complex migrations

### Code Organization
- Keep migrations in version control
- Document complex migrations
- Use consistent naming conventions
- Group related changes in single migration

### Performance Considerations
- **Large tables**: Use `CONCURRENTLY` for PostgreSQL indexes
- **Data migrations**: Process in batches for large datasets
- **Downtime**: Plan maintenance windows for schema changes
- **Testing**: Test migration performance on production-like data

## 🔍 Troubleshooting

### Common Issues

**Migration conflicts:**
```bash
# Check migration history
alembic history --verbose

# Check current state
alembic current

# Resolve conflicts manually
# Edit migration files or reset database
```

**Model import errors:**
```bash
# Verify model imports in env.py
python -c "from users.models import UserModel; print('OK')"

# Check Python path
python -c "import sys; print(sys.path)"
```

**Database connection issues:**
```bash
# Test database connection
python -c "from config.database import engine; print('OK')"

# Check database URL
echo $DATABASE_URL
```

**Migration not found:**
```bash
# Check migration files
ls -la alembic/versions/

# Verify migration ID
alembic show head
```

## 📚 Next Steps

After setting up migrations:

1. **Create initial migration** for existing models
2. **Set up CI/CD pipeline** for automatic migrations
3. **Document migration procedures** for your team
4. **Create migration templates** for common changes
5. **Set up monitoring** for migration status

## 🎉 Success Checklist

- [ ] Alembic initialized and configured
- [ ] Models properly imported in env.py
- [ ] First migration created and applied
- [ ] Migration workflow tested
- [ ] Rollback procedures verified
- [ ] CI/CD integration configured
- [ ] Team procedures documented

---

**Your database migrations are now properly configured! 🚀**

The migration system provides a safe and reliable way to evolve your database schema. Use auto-generation for simple changes, manual migrations for complex scenarios, and always test your migrations before applying them to production.
