# 🚀 Deployment Integration

FasCraft now includes comprehensive deployment automation for all generated FastAPI projects, providing production-ready deployment scripts, infrastructure-as-code templates, and monitoring configurations.

## ✨ **Features**

### **Multi-Platform Deployment Support**
- **AWS ECS** - Container orchestration with Fargate
- **Kubernetes** - Production-grade container orchestration
- **Terraform** - Infrastructure-as-code automation
- **Monitoring** - Prometheus, Grafana, and logging setup

### **Production Automation**
- **Deployment Scripts** - Automated deployment and rollback
- **Infrastructure Templates** - Reproducible infrastructure
- **Health Checks** - Automated health monitoring
- **Scaling** - Auto-scaling configurations
- **Security** - IAM roles, security groups, and secrets management

## 🚀 **Usage**

### **Generate Deployment Files**
```bash
# Generate AWS ECS deployment files
fascraft deploy generate --platform aws

# Generate Kubernetes deployment files
fascraft deploy generate --platform kubernetes

# Generate Terraform infrastructure files
fascraft deploy generate --platform terraform

# Generate all deployment platforms
fascraft deploy generate --platform all

# Force overwrite existing files
fascraft deploy generate --platform aws --force
```

### **Setup Monitoring**
```bash
# Setup monitoring and logging configuration
fascraft deploy setup-monitoring
```

## 🏗️ **Generated Deployment Files**

### **AWS ECS Deployment**

#### **ECS Deployment Script (`deploy/aws/ecs-deploy.sh`)**
- **Automated deployment** to AWS ECS Fargate
- **Docker image building** and ECR push
- **Cluster and service creation** with proper networking
- **Health checks** and service stability monitoring
- **Rollback capability** to previous deployments
- **Environment-specific** configurations

#### **Features:**
- Multi-stage deployment process
- Automatic ECR repository creation
- Load balancer configuration
- Security group management
- CloudWatch logging integration
- Health check endpoints

### **Kubernetes Deployment**

#### **Kubernetes Manifests (`deploy/kubernetes/deployment.yaml`)**
- **Production-ready deployment** with 3 replicas
- **Service and ingress** configuration
- **Resource limits** and requests
- **Health checks** (liveness and readiness probes)
- **Horizontal Pod Autoscaler** (HPA)
- **RBAC** and service account setup

#### **Components:**
- Deployment with rolling updates
- Service for internal communication
- Ingress for external access
- ConfigMap for configuration
- Secrets for sensitive data
- HPA for auto-scaling

### **Terraform Infrastructure**

#### **Infrastructure Code (`deploy/terraform/main.tf`)**
- **Complete VPC** with public/private subnets
- **ECS cluster** with Fargate support
- **Application Load Balancer** (ALB)
- **Security groups** and IAM roles
- **ECR repository** for container images
- **CloudWatch** logging and monitoring

#### **Resources:**
- VPC with internet gateway
- Public and private subnets
- ECS cluster and service
- Load balancer and target groups
- IAM roles and policies
- SSM parameters for secrets

### **Monitoring and Logging**

#### **Prometheus Configuration (`deploy/monitoring/prometheus.yml`)**
- **Application metrics** collection
- **Infrastructure monitoring** (CPU, memory, disk)
- **Service discovery** for dynamic targets
- **Recording rules** for common metrics
- **Remote storage** integration
- **Alerting** configuration

#### **Monitoring Targets:**
- FastAPI application metrics
- Container and host metrics
- Database and Redis metrics
- Load balancer metrics
- Blackbox endpoint monitoring

#### **Logging Configuration (`config/logging.yml`)**
- **Structured logging** with JSON format
- **Log rotation** with size limits
- **Multiple handlers** (console, file, error)
- **Configurable log levels** per component
- **Centralized log management**

## 🔧 **Commands**

### **Generate Deployment Files**
```bash
# Generate AWS deployment
fascraft deploy generate --platform aws

# Generate Kubernetes deployment
fascraft deploy generate --platform kubernetes

# Generate Terraform infrastructure
fascraft deploy generate --platform terraform

# Generate all platforms
fascraft deploy generate --platform all

# Force overwrite existing files
fascraft deploy generate --platform aws --force
```

### **Setup Monitoring**
```bash
# Setup monitoring configuration
fascraft deploy setup-monitoring

# Setup for specific project
fascraft deploy setup-monitoring --path /path/to/project
```

## 🌐 **Platform-Specific Features**

### **AWS ECS Deployment**

#### **Deployment Process**
```bash
# Deploy to ECS
./deploy/aws/ecs-deploy.sh deploy

# Rollback deployment
./deploy/aws/ecs-deploy.sh rollback

# Health check
./deploy/aws/ecs-deploy.sh health-check
```

#### **Environment Variables**
```bash
export AWS_REGION=us-east-1
export AWS_ACCOUNT_ID=123456789012
export IMAGE_TAG=latest
export ECR_REPOSITORY=my-api
export SUBNET_IDS=subnet-123,subnet-456
export SECURITY_GROUP_IDS=sg-123,sg-456
export SERVICE_URL=https://my-api.example.com
```

#### **Features**
- **Fargate** serverless compute
- **Auto-scaling** based on CPU/memory
- **Load balancer** with health checks
- **CloudWatch** metrics and logs
- **IAM roles** for security
- **VPC networking** with security groups

### **Kubernetes Deployment**

#### **Deployment Commands**
```bash
# Apply all manifests
kubectl apply -f deploy/kubernetes/

# Check deployment status
kubectl get pods -l app=my-api

# View logs
kubectl logs -l app=my-api

# Scale deployment
kubectl scale deployment my-api-deployment --replicas=5
```

#### **Features**
- **Rolling updates** with zero downtime
- **Resource management** with limits
- **Health checks** and readiness probes
- **Auto-scaling** with HPA
- **Ingress** with SSL termination
- **RBAC** and security policies

### **Terraform Infrastructure**

#### **Deployment Commands**
```bash
# Initialize Terraform
cd deploy/terraform
terraform init

# Plan deployment
terraform plan

# Apply infrastructure
terraform apply

# Destroy infrastructure
terraform destroy
```

#### **Features**
- **Infrastructure-as-code** for reproducibility
- **State management** with S3 backend
- **Variable configuration** for environments
- **Output values** for integration
- **Resource tagging** for cost management
- **Security best practices**

## 📊 **Monitoring and Observability**

### **Prometheus Metrics**
- **HTTP metrics**: requests, duration, errors
- **Application metrics**: custom business logic
- **System metrics**: CPU, memory, disk usage
- **Container metrics**: resource utilization
- **Database metrics**: connection pools, queries

### **Grafana Dashboards**
- **Application overview** with key metrics
- **Infrastructure monitoring** with system stats
- **Business metrics** and KPIs
- **Alerting** and notification rules
- **Custom dashboards** for teams

### **Logging Strategy**
- **Structured logging** in JSON format
- **Centralized collection** with aggregation
- **Log levels** for different environments
- **Rotation policies** for storage management
- **Search and analysis** capabilities

## 🔒 **Security Features**

### **AWS Security**
- **IAM roles** with least privilege
- **Security groups** for network isolation
- **VPC networking** with private subnets
- **Secrets management** with SSM parameters
- **Encryption** at rest and in transit

### **Kubernetes Security**
- **RBAC** with service accounts
- **Network policies** for pod isolation
- **Secrets** for sensitive data
- **Pod security** standards
- **TLS termination** at ingress

### **Infrastructure Security**
- **Private subnets** for application instances
- **Security groups** for traffic control
- **IAM policies** for resource access
- **Encryption** for data storage
- **Audit logging** for compliance

## 🚀 **Deployment Scenarios**

### **Development Environment**
```bash
# Generate development deployment
fascraft deploy generate --platform aws

# Deploy with development config
./deploy/aws/ecs-deploy.sh deploy
```

### **Staging Environment**
```bash
# Generate staging deployment
fascraft deploy generate --platform kubernetes

# Deploy to staging cluster
kubectl apply -f deploy/kubernetes/
```

### **Production Environment**
```bash
# Generate production infrastructure
fascraft deploy generate --platform terraform

# Deploy production infrastructure
cd deploy/terraform
terraform apply
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

### **Resource Configuration**
```yaml
# Kubernetes resource limits
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"

# AWS ECS task definition
cpu: 256
memory: 512
```

### **Scaling Configuration**
```yaml
# Kubernetes HPA
minReplicas: 2
maxReplicas: 10
targetCPUUtilizationPercentage: 70

# AWS ECS auto-scaling
minCapacity: 2
maxCapacity: 10
targetTrackingScalingPolicy:
  targetValue: 70.0
```

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Deployment Failures**
```bash
# Check deployment status
kubectl describe deployment my-api-deployment

# View pod logs
kubectl logs -l app=my-api

# Check service endpoints
kubectl get endpoints my-api-service
```

#### **Infrastructure Issues**
```bash
# Check Terraform state
terraform show

# Validate configuration
terraform validate

# Check AWS resources
aws ecs describe-services --cluster my-api-cluster
```

#### **Monitoring Issues**
```bash
# Check Prometheus targets
curl http://prometheus:9090/api/v1/targets

# Verify metrics endpoint
curl http://my-api:8000/metrics

# Check log files
tail -f logs/app.log
```

### **Debug Commands**
```bash
# Check deployment files
ls -la deploy/

# Verify template rendering
cat deploy/kubernetes/deployment.yaml

# Test health endpoints
curl -f http://localhost:8000/api/v1/health

# Check resource usage
kubectl top pods
```

## 📚 **Next Steps**

### **Advanced Deployment Features**
- **Multi-region** deployment strategies
- **Blue-green** and canary deployments
- **Infrastructure testing** with Terratest
- **GitOps** integration with ArgoCD
- **Chaos engineering** with Chaos Monkey

### **Integration Enhancements**
- **Slack notifications** for deployments
- **JIRA integration** for issue tracking
- **Cost optimization** with AWS Cost Explorer
- **Performance testing** with K6
- **Security scanning** with Trivy

### **Monitoring Enhancements**
- **Distributed tracing** with Jaeger
- **APM integration** with New Relic
- **Custom dashboards** for business metrics
- **Alerting rules** for SLOs
- **Log correlation** with trace IDs

---

**FasCraft Deployment Integration** - Making production deployment simple and powerful! 🚀
