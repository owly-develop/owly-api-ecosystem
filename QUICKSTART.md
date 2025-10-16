# 🚀 Quick Start Guide

Get the OWLY CRM API up and running in 5 minutes!

## Prerequisites

- Docker Desktop installed
- Docker Compose installed

## Start in 3 Steps

### 1. Start Services
```bash
docker-compose up -d
```

This starts:
- PostgreSQL database
- Redis cache
- Django API server
- Celery worker
- Celery beat scheduler

### 2. Run Migrations
```bash
docker-compose exec web python manage.py migrate
```

### 3. Create Superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

Enter:
- Email: `admin@owlycrm.com`
- Password: `admin123` (or your choice)
- First name: `Admin`
- Last name: `User`

## Access the Application

| Service | URL |
|---------|-----|
| 🌐 API | http://localhost:8000/api/ |
| 👤 Admin Panel | http://localhost:8000/admin/ |
| 📚 API Documentation | http://localhost:8000/api/docs/ |
| ❤️ Health Check | http://localhost:8000/api/health/ |

## Test the API

### 1. Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@owlycrm.com",
    "password": "admin123"
  }'
```

You'll get:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 2. Get Profile
```bash
curl -X GET http://localhost:8000/api/auth/users/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. Create a Company
```bash
curl -X POST http://localhost:8000/api/companies/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Real Estate Company",
    "email": "contact@mycompany.com",
    "plan": "professional"
  }'
```

### 4. Create a Lead
```bash
curl -X POST http://localhost:8000/api/leads/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "source": "website",
    "priority": "high"
  }'
```

## Useful Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f celery
```

### Django Shell
```bash
docker-compose exec web python manage.py shell
```

### Create Test Data
```bash
docker-compose exec web python manage.py shell << EOF
from apps.companies.models import Company
from apps.users.models import User
from apps.projects.models import Project

# Create demo company
company = Company.objects.create(
    name='Demo Real Estate',
    slug='demo-real-estate',
    email='demo@realestate.com',
    plan='professional'
)

# Create demo project
project = Project.objects.create(
    company=company,
    name='Sunset Towers',
    code='ST-2024',
    type='residential',
    status='active',
    description='Luxury residential project',
    address='123 Main St',
    city='Miami',
    state='Florida',
    country='USA',
    postal_code='33101',
    total_units=50,
    available_units=30,
    price_from=250000,
    price_to=750000,
    currency='USD'
)

print(f'Created company: {company.name}')
print(f'Created project: {project.name}')
EOF
```

### Stop Services
```bash
docker-compose down
```

### Stop and Remove All Data
```bash
docker-compose down -v
```

## API Endpoints Quick Reference

### Authentication
- `POST /api/auth/login/` - Login
- `POST /api/auth/refresh/` - Refresh token
- `GET /api/auth/users/profile/` - Get profile

### Companies
- `GET /api/companies/` - List companies
- `POST /api/companies/` - Create company
- `GET /api/companies/{id}/` - Get company

### Projects
- `GET /api/projects/` - List projects
- `POST /api/projects/` - Create project
- `GET /api/projects/{id}/` - Get project

### Leads
- `GET /api/leads/` - List leads
- `POST /api/leads/` - Create lead
- `GET /api/leads/stats/` - Get statistics

### Quotes
- `GET /api/quotes/` - List quotes
- `POST /api/quotes/` - Create quote
- `POST /api/quotes/{id}/send/` - Send quote

### Analytics
- `GET /api/analytics/dashboard/` - Dashboard stats
- `GET /api/analytics/leads/` - Lead analytics
- `GET /api/analytics/sales-funnel/` - Sales funnel

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, edit `docker-compose.yml`:
```yaml
web:
  ports:
    - "8001:8000"  # Change to 8001 or any available port
```

### Database Connection Error
Wait a few seconds for PostgreSQL to fully start:
```bash
docker-compose logs db
```

### Reset Everything
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## Next Steps

1. ✅ Read the full [README.md](README.md)
2. ✅ Check [DEPLOYMENT.md](DEPLOYMENT.md) for AWS deployment
3. ✅ Explore API documentation at http://localhost:8000/api/docs/
4. ✅ Start building your frontend!

## Need Help?

- 📖 Documentation: http://localhost:8000/api/docs/
- 💬 Support: admin@owlycrm.com

---

**Happy coding! 🎉**

