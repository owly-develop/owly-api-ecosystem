# OWLY CRM API - Django REST Framework

Multi-tenant CRM API built with Django REST Framework, PostgreSQL, Redis, and Celery. Dockerized and ready for AWS deployment.

## 🚀 Features

- **Multi-tenant Architecture**: One database, multiple companies with data isolation
- **Complete CRM**: Companies, Users, Projects, Units, Leads, Quotes, Activities
- **JWT Authentication**: Secure token-based authentication
- **RESTful API**: Full CRUD operations with filtering, search, and pagination
- **Real-time Analytics**: Dashboard statistics and sales funnel
- **Async Tasks**: Celery for background jobs
- **API Documentation**: Auto-generated with drf-spectacular (Swagger/OpenAPI)
- **Production Ready**: Docker, AWS S3, Redis caching, error tracking

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 16
- Redis 7

## 🛠️ Installation & Setup

### 1. Clone and Setup

```bash
cd owly-api-django
```

### 2. Create Environment File

```bash
cp .env.example .env
```

Edit `.env` with your settings.

### 3. Run with Docker Compose

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Redis cache
- Django web server
- Celery worker
- Celery beat scheduler

### 4. Run Migrations

```bash
docker-compose exec web python manage.py migrate
```

### 5. Create Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### 6. Access the Application

- **API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/docs/
- **Health Check**: http://localhost:8000/api/health/

## 📚 API Endpoints

### Authentication
```
POST   /api/auth/login/          - Login (get JWT tokens)
POST   /api/auth/refresh/        - Refresh access token
POST   /api/auth/verify/         - Verify token
GET    /api/auth/users/profile/  - Get current user profile
POST   /api/auth/users/change_password/ - Change password
```

### Companies
```
GET    /api/companies/           - List companies
POST   /api/companies/           - Create company
GET    /api/companies/{id}/      - Get company details
PUT    /api/companies/{id}/      - Update company
GET    /api/companies/{id}/stats/ - Get company statistics
POST   /api/companies/{id}/upgrade_plan/ - Upgrade plan
```

### Projects
```
GET    /api/projects/            - List projects
POST   /api/projects/            - Create project
GET    /api/projects/{id}/       - Get project details
PUT    /api/projects/{id}/       - Update project
GET    /api/projects/{id}/units/ - Get project units
GET    /api/projects/{id}/stats/ - Get project statistics
```

### Units
```
GET    /api/projects/units/      - List units
POST   /api/projects/units/      - Create unit
GET    /api/projects/units/{id}/ - Get unit details
PUT    /api/projects/units/{id}/ - Update unit
```

### Leads
```
GET    /api/leads/               - List leads
POST   /api/leads/               - Create lead
GET    /api/leads/{id}/          - Get lead details
PUT    /api/leads/{id}/          - Update lead
POST   /api/leads/{id}/assign/   - Assign lead to user
POST   /api/leads/{id}/change_status/ - Change lead status
POST   /api/leads/{id}/update_score/ - Update lead score
GET    /api/leads/stats/         - Get lead statistics
```

### Quotes
```
GET    /api/quotes/              - List quotes
POST   /api/quotes/              - Create quote
GET    /api/quotes/{id}/         - Get quote details
PUT    /api/quotes/{id}/         - Update quote
POST   /api/quotes/{id}/send/    - Send quote to lead
POST   /api/quotes/{id}/accept/  - Accept quote
POST   /api/quotes/{id}/reject/  - Reject quote
```

### Activities
```
GET    /api/activities/          - List activities
POST   /api/activities/          - Create activity
GET    /api/activities/{id}/     - Get activity details
PUT    /api/activities/{id}/     - Update activity
```

### Analytics
```
GET    /api/analytics/dashboard/ - Dashboard statistics
GET    /api/analytics/leads/     - Lead analytics
GET    /api/analytics/sales-funnel/ - Sales funnel data
```

## 🏗️ Project Structure

```
owly-api-django/
├── apps/
│   ├── core/           # Base models, middleware, permissions
│   ├── companies/      # Multi-tenant company management
│   ├── users/          # Custom user model & authentication
│   ├── projects/       # Real estate projects & units
│   ├── leads/          # Lead/prospect management
│   ├── quotes/         # Quote/proposal system
│   ├── activities/     # Activity tracking
│   └── analytics/      # Analytics & reporting
├── owly_crm/
│   ├── settings.py     # Django settings
│   ├── urls.py         # Main URL configuration
│   ├── wsgi.py         # WSGI application
│   └── celery.py       # Celery configuration
├── docker-compose.yml  # Docker services definition
├── Dockerfile          # Docker image configuration
├── requirements.txt    # Python dependencies
└── manage.py          # Django management script
```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Use Token
```bash
curl -X GET http://localhost:8000/api/leads/ \
  -H "Authorization: Bearer <access_token>"
```

## 🗄️ Database Models

### Core Models
- **Company**: Multi-tenant organization
- **User**: Custom user with role-based permissions
- **Project**: Real estate project
- **Unit**: Individual property unit
- **Lead**: Sales lead/prospect
- **Quote**: Quote/proposal
- **Activity**: Activity tracking
- **QuoteTemplate**: Reusable quote templates

### Key Features
- UUIDs for all primary keys
- Soft delete support
- Automatic timestamps
- JSON fields for flexible data
- Tenant isolation
- Full-text search

## 🔧 Development

### Run Tests
```bash
docker-compose exec web python manage.py test
```

### Create Migration
```bash
docker-compose exec web python manage.py makemigrations
```

### Apply Migrations
```bash
docker-compose exec web python manage.py migrate
```

### Shell Access
```bash
docker-compose exec web python manage.py shell
```

### View Logs
```bash
docker-compose logs -f web
docker-compose logs -f celery
```

## 🚀 AWS Deployment

### 1. Prepare Environment Variables

Set these in your AWS environment:
```
SECRET_KEY=<your-secret-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,*.amazonaws.com
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
USE_S3=True
AWS_ACCESS_KEY_ID=<your-key>
AWS_SECRET_ACCESS_KEY=<your-secret>
AWS_STORAGE_BUCKET_NAME=<your-bucket>
```

### 2. Setup AWS RDS (PostgreSQL)
- Create PostgreSQL 16 instance
- Configure security groups
- Note connection details

### 3. Setup AWS ElastiCache (Redis)
- Create Redis cluster
- Configure security groups
- Note connection endpoint

### 4. Setup AWS S3
- Create S3 bucket for media files
- Configure CORS
- Set bucket policy

### 5. Deploy with ECS/Fargate or EC2
- Build and push Docker image to ECR
- Create ECS task definition
- Deploy service with load balancer

### 6. Run Migrations
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/api/health/
```

Response:
```json
{
  "status": "healthy",
  "database": "connected",
  "cache": "connected"
}
```

### Sentry Integration
Set `SENTRY_DSN` in environment variables for error tracking.

## 🔒 Security

- JWT token authentication
- Password hashing with Django's PBKDF2
- CORS protection
- Rate limiting (add if needed)
- SQL injection protection (Django ORM)
- XSS protection
- CSRF protection

## 📝 License

Proprietary - All rights reserved

## 👥 Support

For support and questions, contact: admin@owlycrm.com

---

**Built with ❤️ for OWLY CRM**

