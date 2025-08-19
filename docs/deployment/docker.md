# 🐳 Docker Integration

FasCraft now includes comprehensive Docker support for all generated FastAPI projects, making it easy to containerize and deploy your applications.

## ✨ **Features**

### **Automatic Docker Generation**
- **Multi-stage Dockerfiles** with development and production targets
- **Docker Compose** with database, Redis, and other services
- **Security best practices** (non-root user, minimal base images)
- **Health checks** and proper signal handling
- **Optimized layer caching** for faster builds

### **Service Stack**
- **PostgreSQL 15** with health checks and initialization
- **Redis 7** for caching and session storage
- **pgAdmin** for database management (development only)
- **Custom networks** for service isolation

## 🚀 **Usage**

### **New Projects (Automatic)**
When you create a new project with `fascraft new`, Docker support is automatically included:

```bash
# Create new project with Docker support
fascraft new my-api
cd my-api

# Build and run with Docker
docker-compose up --build
```

### **Existing Projects**
Add Docker support to existing projects:

```bash
# Add Docker support to existing project
fascraft dockerize /path/to/existing-project

# Or use force to overwrite existing files
fascraft dockerize /path/to/existing-project --force
```

## 🏗️ **Generated Files**

### **Dockerfile**
- **Multi-stage build** with development and production targets
- **Security-focused** with non-root user and minimal base images
- **Health checks** for container monitoring
- **Optimized caching** for faster builds

### **docker-compose.yml**
- **Development environment** with hot-reload and volume mounts
- **Production profile** for optimized deployment
- **Database services** with health checks and persistence
- **Service dependencies** and networking

### **.dockerignore**
- **Optimized builds** by excluding unnecessary files
- **Security-focused** by excluding sensitive files
- **Performance** by reducing build context size

### **Database Initialization**
- **Automatic database creation** on first run
- **Extension installation** (UUID, encryption)
- **Health check tables** for monitoring
- **Permission setup** for database access

## 🔧 **Commands**

### **Development Mode**
```bash
# Start development environment
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f
```

### **Production Mode**
```bash
# Start production environment
docker-compose --profile production up --build

# Run in background
docker-compose --profile production up -d --build
```

### **Service Management**
```bash
# Stop all services
docker-compose down

# Remove volumes (database data)
docker-compose down -v

# Restart specific service
docker-compose restart my-api
```

## 🌐 **Service Endpoints**

### **Application**
- **Main API**: http://localhost:8000
- **Health Check**: http://localhost:8000/api/v1/health
- **API Docs**: http://localhost:8000/docs

### **Database Services**
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **pgAdmin**: http://localhost:5050 (development only)

## 🔒 **Security Features**

### **Container Security**
- **Non-root user** for application execution
- **Minimal base images** to reduce attack surface
- **Health checks** for monitoring container status
- **Signal handling** for graceful shutdowns

### **Network Security**
- **Isolated networks** for service communication
- **Port exposure** only for necessary services
- **Service dependencies** to prevent unauthorized access

## 📊 **Performance Optimizations**

### **Build Optimizations**
- **Multi-stage builds** to reduce final image size
- **Layer caching** for faster rebuilds
- **Dependency optimization** for smaller images
- **Build context optimization** with .dockerignore

### **Runtime Optimizations**
- **Health checks** for better orchestration
- **Resource limits** for predictable performance
- **Volume mounts** for development efficiency
- **Service discovery** for dynamic scaling

## 🚀 **Deployment Scenarios**

### **Development**
```bash
# Local development with hot-reload
docker-compose up --build

# Access services
curl http://localhost:8000/api/v1/health
```

### **Testing**
```bash
# Run tests in container
docker-compose run --rm my-api pytest

# Run with coverage
docker-compose run --rm my-api pytest --cov=.
```

### **Production**
```bash
# Production deployment
docker-compose --profile production up -d --build

# Monitor services
docker-compose --profile production ps
```

## 🔧 **Customization**

### **Environment Variables**
```bash
# Override database settings
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
ENVIRONMENT=production
```

### **Service Configuration**
```yaml
# Customize PostgreSQL
postgres:
  environment:
    POSTGRES_PASSWORD: my-secure-password
    POSTGRES_DB: my-database
```

### **Port Mapping**
```yaml
# Custom port mapping
ports:
  - "8080:8000"  # Map host port 8080 to container port 8000
```

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Port Already in Use**
```bash
# Check what's using the port
lsof -i :8000

# Use different ports in docker-compose.yml
ports:
  - "8001:8000"
```

#### **Database Connection Issues**
```bash
# Check database service status
docker-compose ps postgres

# View database logs
docker-compose logs postgres

# Restart database service
docker-compose restart postgres
```

#### **Build Failures**
```bash
# Clean build cache
docker-compose build --no-cache

# Check Dockerfile syntax
docker build -t test .

# Verify template rendering
fascraft dockerize --force
```

### **Debug Commands**
```bash
# Enter running container
docker-compose exec my-api bash

# View container logs
docker-compose logs -f my-api

# Check container health
docker-compose ps
```

## 📚 **Next Steps**

### **CI/CD Integration**
- **GitHub Actions** for automated testing and deployment
- **GitLab CI** for continuous integration
- **Docker registry** for image management

### **Production Deployment**
- **Kubernetes manifests** for orchestration
- **Cloud deployment** scripts for major providers
- **Monitoring and logging** integration

### **Advanced Features**
- **Service mesh** integration
- **Load balancing** configuration
- **Auto-scaling** policies

---

**FasCraft Docker Integration** - Making containerization simple and secure! 🐳
