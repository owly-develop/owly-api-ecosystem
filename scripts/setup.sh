#!/bin/bash

# OWLY CRM API - Initial Setup Script

set -e

echo "🚀 OWLY CRM API - Initial Setup"
echo "================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration before continuing!"
    exit 1
fi

echo "🐳 Starting Docker containers..."
docker-compose up -d

echo "⏳ Waiting for database to be ready..."
sleep 10

echo "📦 Running migrations..."
docker-compose exec -T web python manage.py migrate

echo "📊 Creating initial data..."
docker-compose exec -T web python manage.py shell << EOF
from apps.companies.models import Company
from apps.users.models import User

# Create demo company
if not Company.objects.filter(slug='demo-company').exists():
    company = Company.objects.create(
        name='Demo Company',
        slug='demo-company',
        email='demo@owlycrm.com',
        plan='professional',
        status='active'
    )
    print(f'✅ Created demo company: {company.name}')
    
    # Create admin user
    if not User.objects.filter(email='admin@owlycrm.com').exists():
        user = User.objects.create_superuser(
            email='admin@owlycrm.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            company=company
        )
        print(f'✅ Created admin user: {user.email}')
else:
    print('ℹ️  Demo company already exists')
EOF

echo ""
echo "✅ Setup Complete!"
echo "===================="
echo ""
echo "🌐 API: http://localhost:8000/api/"
echo "👤 Admin: http://localhost:8000/admin/"
echo "📚 Docs: http://localhost:8000/api/docs/"
echo ""
echo "🔑 Login Credentials:"
echo "   Email: admin@owlycrm.com"
echo "   Password: admin123"
echo ""
echo "⚠️  Remember to change the default password!"

