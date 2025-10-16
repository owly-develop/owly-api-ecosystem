# Environment Configuration Guide

## Create Your .env File

Before starting the application, you need to create a `.env` file in the root directory.

### Option 1: Use the Example File

```bash
cp .env.example .env
```

### Option 2: Create Manually

Create a `.env` file with the following content:

```bash
# Django Settings
SECRET_KEY=django-insecure-local-dev-key-change-in-production-1234567890
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database
DATABASE_URL=postgresql://owly_user:owly_secure_password_2024@db:5432/owly_crm

# Redis
REDIS_URL=redis://redis:6379/0

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# AWS Settings (leave empty for local development)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=us-east-1
USE_S3=False

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Sentry (optional)
SENTRY_DSN=

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# Application Settings
DEFAULT_FROM_EMAIL=noreply@owlycrm.com
ADMIN_EMAIL=admin@owlycrm.com
```

## Local Development (Default)

The default values above are configured for local development with Docker Compose.

**No changes needed!** Just create the file and start the services.

## Production Configuration

For production deployment (AWS), update these values:

### 1. Security
```bash
SECRET_KEY=generate-a-strong-random-key-use-python-secrets
DEBUG=False
ALLOWED_HOSTS=api.yourdomain.com,*.amazonaws.com
```

Generate a secure SECRET_KEY:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Database (AWS RDS)
```bash
DATABASE_URL=postgresql://username:password@your-rds-host.region.rds.amazonaws.com:5432/owly_crm
```

### 3. Redis (AWS ElastiCache)
```bash
REDIS_URL=redis://your-elasticache-host.region.cache.amazonaws.com:6379/0
CELERY_BROKER_URL=redis://your-elasticache-host.region.cache.amazonaws.com:6379/0
CELERY_RESULT_BACKEND=redis://your-elasticache-host.region.cache.amazonaws.com:6379/0
```

### 4. CORS (Your Frontend URLs)
```bash
CORS_ALLOWED_ORIGINS=https://app.yourdomain.com,https://yourdomain.com
```

### 5. AWS S3 (Media Storage)
```bash
USE_S3=True
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=owly-crm-media-prod
AWS_S3_REGION_NAME=us-east-1
```

### 6. Email (AWS SES or SMTP)
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-ses-smtp-username
EMAIL_HOST_PASSWORD=your-ses-smtp-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### 7. Monitoring (Sentry)
```bash
SENTRY_DSN=https://your-key@sentry.io/project-id
```

## Environment Variable Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| SECRET_KEY | Django secret key | - | ✅ Yes |
| DEBUG | Debug mode | True | ✅ Yes |
| ALLOWED_HOSTS | Allowed hosts | localhost | ✅ Yes |
| DATABASE_URL | PostgreSQL connection string | - | ✅ Yes |
| REDIS_URL | Redis connection string | - | ✅ Yes |
| CELERY_BROKER_URL | Celery broker URL | - | ✅ Yes |
| CORS_ALLOWED_ORIGINS | Frontend URLs | - | ✅ Yes |
| USE_S3 | Enable S3 storage | False | ❌ No |
| AWS_ACCESS_KEY_ID | AWS access key | - | ⚠️ If USE_S3=True |
| AWS_SECRET_ACCESS_KEY | AWS secret key | - | ⚠️ If USE_S3=True |
| AWS_STORAGE_BUCKET_NAME | S3 bucket name | - | ⚠️ If USE_S3=True |
| EMAIL_HOST | SMTP host | - | ❌ No |
| EMAIL_HOST_USER | SMTP username | - | ❌ No |
| EMAIL_HOST_PASSWORD | SMTP password | - | ❌ No |
| SENTRY_DSN | Sentry DSN for error tracking | - | ❌ No |

## Verify Configuration

After creating your `.env` file, verify it's correctly configured:

```bash
# Start services
docker-compose up -d

# Check if environment variables are loaded
docker-compose exec web python -c "import os; print('DEBUG:', os.getenv('DEBUG'))"

# Check database connection
docker-compose exec web python manage.py check --database default

# Check all settings
docker-compose exec web python manage.py check
```

## Security Best Practices

### For Production:

1. ✅ **Never commit `.env` files** to version control
2. ✅ **Use AWS Secrets Manager** or Parameter Store for sensitive data
3. ✅ **Generate a new SECRET_KEY** for each environment
4. ✅ **Set DEBUG=False** in production
5. ✅ **Use HTTPS** and configure ALLOWED_HOSTS properly
6. ✅ **Enable Sentry** for error monitoring
7. ✅ **Use strong database passwords**
8. ✅ **Restrict CORS_ALLOWED_ORIGINS** to your actual domains

### For Development:

1. ✅ **Use different credentials** than production
2. ✅ **Keep DEBUG=True** for better error messages
3. ✅ **Use EMAIL_BACKEND=console** to view emails in logs
4. ✅ **Don't use real email/SMS services**

## Troubleshooting

### "OperationalError: could not connect to server"
- Database URL is incorrect
- PostgreSQL container is not running
- Wait a few seconds for PostgreSQL to start

### "Connection refused" (Redis)
- Redis URL is incorrect
- Redis container is not running

### "ImproperlyConfigured: The SECRET_KEY setting must not be empty"
- `.env` file doesn't exist
- SECRET_KEY is not set in `.env`

### "CORS error" in frontend
- Add your frontend URL to CORS_ALLOWED_ORIGINS
- Use exact URL including protocol (http:// or https://)

---

**Ready to start? Run: `make setup` or see [QUICKSTART.md](QUICKSTART.md)**

