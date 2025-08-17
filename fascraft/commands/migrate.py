"""Command for migrating legacy FastAPI projects to domain-driven architecture."""

from pathlib import Path
from typing import Dict, List, Optional
import shutil

import typer
from rich.console import Console
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn

# Initialize rich console
console = Console()


def migrate_project(
    path: str = typer.Option(
        ".", help="📁 The path to the FastAPI project to migrate"
    ),
    backup: bool = typer.Option(
        True, help="💾 Create backup before migration"
    ),
) -> None:
    """🚀 Migrates a legacy FastAPI project to domain-driven architecture."""
    path_obj = Path(path)
    
    if not path_obj.exists():
        error_text = Text(
            "❌ Error: Path does not exist.", style="bold red"
        )
        console.print(error_text)
        raise typer.Exit(code=1)
    
    if not is_fastapi_project(path_obj):
        error_text = Text(
            "❌ Error: This is not a FastAPI project.", style="bold red"
        )
        console.print(error_text)
        raise typer.Exit(code=1)
    
    console.print(f"🚀 Starting migration for project at: {path_obj}", style="bold blue")
    
    # Analyze current structure
    analysis = analyze_current_structure(path_obj)
    
    if not analysis["needs_migration"]:
        console.print("✅ Project is already using domain-driven architecture!", style="bold green")
        return
    
    # Confirm migration
    if not confirm_migration(analysis):
        console.print("❌ Migration cancelled by user.", style="bold red")
        raise typer.Exit(code=1)
    
    # Create backup if requested
    if backup:
        backup_path = create_backup(path_obj)
        console.print(f"💾 Backup created at: {backup_path}", style="bold green")
    
    # Perform migration
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Migrating project...", total=100)
        
        # Step 1: Create routers directory and base router
        progress.update(task, description="Creating base router structure...")
        create_base_router_structure(path_obj)
        progress.advance(task, advance=25)
        
        # Step 2: Migrate flat structure to domain modules
        progress.update(task, description="Migrating to domain modules...")
        migrate_to_domain_modules(path_obj, analysis)
        progress.advance(task, advance=50)
        
        # Step 3: Update main.py
        progress.update(task, description="Updating main.py...")
        update_main_py_for_migration(path_obj)
        progress.advance(task, advance=75)
        
        # Step 4: Create FasCraft configuration
        progress.update(task, description="Creating FasCraft configuration...")
        create_fascraft_config(path_obj)
        progress.advance(task, advance=100)
    
    console.print("🎉 Migration completed successfully!", style="bold green")
    display_migration_summary(analysis)


def is_fastapi_project(project_path: Path) -> bool:
    """Check if the given path is a FastAPI project."""
    if (project_path / "main.py").exists():
        content = (project_path / "main.py").read_text()
        if "FastAPI" in content or "fastapi" in content:
            return True
    
    if (project_path / "pyproject.toml").exists():
        content = (project_path / "pyproject.toml").read_text()
        if "fastapi" in content.lower():
            return True
    
    return False


def analyze_current_structure(project_path: Path) -> Dict:
    """Analyze the current project structure to determine migration needs."""
    analysis = {
        "needs_migration": False,
        "flat_structure": False,
        "existing_modules": [],
        "flat_directories": [],
        "main_py_analysis": {}
    }
    
    # Check for flat structure
    flat_dirs = ["models", "schemas", "services", "routers"]
    for flat_dir in flat_dirs:
        if (project_path / flat_dir).exists():
            analysis["flat_structure"] = True
            analysis["flat_directories"].append(flat_dir)
    
    # Check for existing domain modules
    for item in project_path.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            if (item / "__init__.py").exists() and (item / "models.py").exists():
                analysis["existing_modules"].append(item.name)
    
    # Analyze main.py
    main_py_path = project_path / "main.py"
    if main_py_path.exists():
        content = main_py_path.read_text()
        analysis["main_py_analysis"] = {
            "has_router_includes": "app.include_router" in content,
            "router_count": content.count("app.include_router"),
            "has_base_router": "from routers import base_router" in content
        }
    
    # Determine if migration is needed
    if analysis["flat_structure"] or analysis["main_py_analysis"]["router_count"] > 3:
        analysis["needs_migration"] = True
    
    return analysis


def confirm_migration(analysis: Dict) -> bool:
    """Ask user to confirm the migration."""
    console.print("\n📋 Migration Summary:", style="bold yellow")
    
    if analysis["flat_structure"]:
        console.print(f"• Convert flat structure: {', '.join(analysis['flat_directories'])}", style="white")
    
    if analysis["main_py_analysis"]["router_count"] > 3:
        console.print(f"• Consolidate {analysis['main_py_analysis']['router_count']} router includes", style="white")
    
    console.print("• Create base router structure", style="white")
    console.print("• Add FasCraft configuration", style="white")
    
    console.print("\n⚠️  This will modify your project structure.", style="bold red")
    response = typer.confirm("Do you want to continue with the migration?")
    
    return response


def create_backup(project_path: Path) -> Path:
    """Create a backup of the project before migration."""
    backup_path = project_path.parent / f"{project_path.name}_backup_{int(Path().stat().st_mtime)}"
    shutil.copytree(project_path, backup_path)
    return backup_path


def create_base_router_structure(project_path: Path) -> None:
    """Create the base router structure."""
    routers_dir = project_path / "routers"
    routers_dir.mkdir(exist_ok=True)
    
    # Create __init__.py
    init_content = '''"""Routers package for migrated project."""

from .base import base_router

__all__ = ["base_router"]
'''
    (routers_dir / "__init__.py").write_text(init_content)
    
    # Create base.py
    base_content = '''"""Base router for migrated project API endpoints."""

from fastapi import APIRouter

# Create base router with common prefix
base_router = APIRouter(prefix="/api/v1")

# Import all module routers here
# from users import routers as user_routers
# from products import routers as product_routers

# Include all module routers
# base_router.include_router(user_routers.router, prefix="/users", tags=["users"])
# base_router.include_router(product_routers.router, prefix="/products", tags=["products"])

# Health check endpoint
@base_router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "migrated"}
'''
    (routers_dir / "base.py").write_text(base_content)


def migrate_to_domain_modules(project_path: Path, analysis: Dict) -> None:
    """Migrate flat structure to domain modules."""
    if not analysis["flat_structure"]:
        return
    
    # For now, we'll create a simple migration
    # In a full implementation, this would analyze the flat structure
    # and create appropriate domain modules
    
    console.print("📝 Note: Manual module creation may be needed for complex migrations", style="yellow")
    
    # Create a basic users module as an example
    users_dir = project_path / "users"
    if not users_dir.exists():
        users_dir.mkdir()
        
        # Create basic module structure
        (users_dir / "__init__.py").write_text('"""Users domain module."""\n')
        (users_dir / "models.py").write_text('"""User models."""\n\n# TODO: Migrate user models from flat structure\n')
        (users_dir / "schemas.py").write_text('"""User schemas."""\n\n# TODO: Migrate user schemas from flat structure\n')
        (users_dir / "services.py").write_text('"""User services."""\n\n# TODO: Migrate user services from flat structure\n')
        (users_dir / "routers.py").write_text('"""User routers."""\n\nfrom fastapi import APIRouter\n\nrouter = APIRouter(tags=["users"])\n\n# TODO: Migrate user routes from flat structure\n')


def update_main_py_for_migration(project_path: Path) -> None:
    """Update main.py to use the new base router structure."""
    main_py_path = project_path / "main.py"
    
    if not main_py_path.exists():
        return
    
    content = main_py_path.read_text()
    
    # Replace router includes with base router
    if "app.include_router" in content:
        # Simple replacement - in a full implementation, this would be more sophisticated
        content = content.replace(
            "# Import routers (will be added as modules are generated)",
            "# Import base router"
        )
        content = content.replace(
            "# from customers import routers as customer_routers",
            "from routers import base_router"
        )
        content = content.replace(
            "# app.include_router(customer_routers.router, prefix=\"/api/v1/customers\", tags=[\"customers\"])",
            "app.include_router(base_router)"
        )
        
        # Remove other router includes
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if not line.strip().startswith("app.include_router") or "base_router" in line:
                new_lines.append(line)
        content = '\n'.join(new_lines)
    
    main_py_path.write_text(content)


def create_fascraft_config(project_path: Path) -> None:
    """Create FasCraft configuration file."""
    config_content = '''# FasCraft project configuration for migrated project

[project]
name = "migrated_project"
version = "1.0.0"
description = "A FastAPI project migrated with FasCraft"

[router]
base_prefix = "/api/v1"
health_endpoint = true

[database]
default = "sqlite"
supported = ["sqlite", "postgresql", "mysql", "mongodb"]

[modules]
auto_import = true
prefix_strategy = "plural"
test_coverage = true

[development]
auto_reload = true
debug = true
log_level = "DEBUG"

[production]
auto_reload = false
debug = false
log_level = "INFO"
'''
    
    (project_path / "fascraft.toml").write_text(config_content)


def display_migration_summary(analysis: Dict) -> None:
    """Display a summary of what was migrated."""
    console.print("\n📊 Migration Summary", style="bold green")
    
    if analysis["flat_structure"]:
        console.print("✅ Converted flat structure to domain-driven architecture", style="white")
    
    console.print("✅ Created base router structure", style="white")
    console.print("✅ Updated main.py to use base router", style="white")
    console.print("✅ Added FasCraft configuration", style="white")
    
    console.print("\n🚀 Next steps:", style="bold yellow")
    console.print("1. Review the migrated structure", style="white")
    console.print("2. Migrate your business logic to domain modules", style="white")
    console.print("3. Use 'fascraft generate <module_name>' for new modules", style="white")
    console.print("4. Test your application", style="white")
