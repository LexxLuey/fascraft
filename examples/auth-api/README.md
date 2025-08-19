# Authentication API Example

A secure authentication system demonstrating JWT tokens, user management, role-based access control, and security best practices with FasCraft.

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Poetry (recommended) or pip
- Docker (optional)

### Step-by-Step Setup

1. **Navigate to the project directory:**
   ```bash
   cd examples/auth-api
   ```

2. **Install dependencies:**
   ```bash
   # Using Poetry (recommended)
   poetry install
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   # Using Poetry
   poetry run python main.py
   
   # Or directly
   python main.py
   ```

4. **Access the API:**
   - **API Base URL:** http://localhost:8000
   - **Interactive Docs:** http://localhost:8000/docs
   - **ReDoc Documentation:** http://localhost:8000/redoc

## 📁 Project Structure (DDA Approach)

```
auth-api/
├── config/                 # Configuration management
│   ├── __init__.py
│   ├── settings.py         # App settings and environment
│   ├── database.py         # Database configuration
│   ├── exceptions.py       # Custom exception handling
│   └── middleware.py       # Custom middleware
├── routers/                # Router structure
│   ├── __init__.py
│   └── base.py            # Base router for module management
├── .github/                # CI/CD workflows
│   └── workflows/
│       ├── ci.yml         # GitHub Actions CI pipeline
│       └── dependency-update.yml
├── main.py                 # FastAPI application with authentication logic
├── requirements.txt        # Production dependencies
├── requirements.dev.txt    # Development dependencies
├── requirements.prod.txt   # Production dependencies
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-service orchestration
├── fascraft.toml          # FasCraft project configuration
└── README.md              # This file
```

## 🔧 FasCraft Features Demonstrated

### 1. **Project Generation**
- ✅ **Clean DDA Structure** - No unnecessary MVC folders
- ✅ **Essential Configuration** - Settings, database, middleware
- ✅ **Router Foundation** - Base router for module management

### 2. **Security Implementation**
- ✅ **JWT Authentication** - Secure token-based authentication
- ✅ **Password Hashing** - SHA-256 password security
- ✅ **Role-Based Access Control** - Admin and user roles
- ✅ **Token Management** - Access and refresh tokens

### 3. **User Management**
- ✅ **User Registration** - Secure user creation
- ✅ **User Login** - Authentication with token generation
- ✅ **User Profiles** - Current user information
- ✅ **Admin Functions** - User management capabilities

### 4. **API Security**
- ✅ **Protected Endpoints** - JWT token validation
- ✅ **Role Verification** - Admin-only access control
- ✅ **Error Handling** - Secure error responses
- ✅ **Input Validation** - Data sanitization

### 5. **CI/CD Integration**
- ✅ **GitHub Actions** - Automated testing and deployment
- ✅ **Dependency Updates** - Automated security updates
- ✅ **Code Quality** - Linting, testing, security scanning

## 🎯 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login (returns JWT token)
- `POST /api/auth/refresh` - Refresh access token

### User Management
- `GET /api/auth/me` - Get current user info (requires token)
- `GET /api/auth/users` - List all users (admin only, requires token)

### System
- `GET /` - Welcome message and status
- `GET /api/v1/health` - Health check (via base router)

## 🔐 Sample Users

The API comes with pre-loaded sample users:

### Admin User
- **Username:** `admin`
- **Password:** `admin123`
- **Role:** `admin`
- **Access:** Full system access

### Regular User
- **Username:** `user1`
- **Password:** `user123`
- **Role:** `user`
- **Access:** Limited access

## 🚀 Next Steps with FasCraft

### Add New Modules
```bash
# Generate a profile module
fascraft generate profile

# Generate a permissions module
fascraft generate permissions

# Generate a audit module
fascraft generate audit
```

### Analyze Project
```bash
# Get insights on your project structure
fascraft analyze

# Check dependencies
fascraft dependencies list
```

### Testing
   ```bash
# Install development dependencies
pip install -r requirements.dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=.
```

## 🐳 Docker Deployment

### Development
   ```bash
docker-compose up --build
   ```

### Production
   ```bash
docker-compose --profile production up --build
   ```

## 🔍 API Usage Examples

### 1. Register a New User
   ```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=newuser&email=newuser@example.com&password=securepass123"
```

### 2. Login and Get Token
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "role": "admin"
  }
}
```

### 3. Access Protected Endpoint
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### 4. Admin: List All Users
```bash
curl -X GET "http://localhost:8000/api/auth/users" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### 5. Refresh Token
```bash
curl -X POST "http://localhost:8000/api/auth/refresh" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

## 🔒 Security Features

### JWT Configuration
- **Algorithm:** HS256
- **Token Expiry:** 30 minutes
- **Refresh Capability:** Yes
- **Secret Key:** Configurable (change in production)

### Password Security
- **Hashing:** SHA-256
- **Salt:** Built into hash
- **Storage:** Hashed only (never plain text)

### Access Control
- **Role-Based:** Admin and User roles
- **Endpoint Protection:** JWT token validation
- **Admin Functions:** Restricted to admin users

## 🔍 Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Change port in main.py
   uvicorn.run(app, host="0.0.0.0", port=8001)
   ```

2. **Import errors:**
   ```bash
   # Ensure dependencies are installed
   pip install -r requirements.txt
   ```

3. **Authentication errors:**
   - Check token format: `Bearer <token>`
   - Verify token hasn't expired
   - Ensure correct username/password

4. **Permission errors:**
   - Verify user role (admin vs user)
   - Check if endpoint requires admin access
   - Ensure token is valid

## 📚 Learning Path

This example demonstrates:
1. **Security Fundamentals** - JWT authentication
2. **User Management** - Registration, login, profiles
3. **Access Control** - Role-based permissions
4. **API Security** - Protected endpoints
5. **FasCraft DDA** - Clean architecture principles

## 🚨 Production Security Notes

### Before Deployment
1. **Change JWT Secret Key** - Use environment variable
2. **Use HTTPS** - Never send tokens over HTTP
3. **Implement Rate Limiting** - Prevent brute force attacks
4. **Add CORS Policy** - Restrict allowed origins
5. **Use Strong Passwords** - Enforce password policies

### Security Best Practices
- Store JWT secret in environment variables
- Implement token blacklisting for logout
- Add request rate limiting
- Use HTTPS in production
- Regular security audits

## 🎉 Success!

Your Authentication API is now running and demonstrates:
- ✅ **Security Implementation** - JWT authentication system
- ✅ **User Management** - Registration, login, profiles
- ✅ **Access Control** - Role-based permissions
- ✅ **FasCraft Integration** - Ready for scaling

**Next:** Explore the Database API to see ORM integration, or start building your own secure application!