#!/usr/bin/env python
"""
Script to assign a company to the admin user
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'owly_crm.settings')
django.setup()

from apps.users.models import User
from apps.companies.models import Company

# Get admin user
admin = User.objects.get(email='admin@owlycrm.com')

# Get first company or create one if none exists
company = Company.objects.first()

if not company:
    print("⚠️  No hay empresas en la base de datos")
    print("💡 Ejecuta primero: python seed_database.py")
else:
    admin.company = company
    admin.save()
    print(f"✅ Usuario admin asignado a la empresa: {company.name}")
    print(f"   - Email: {admin.email}")
    print(f"   - Empresa: {company.name}")
    print(f"   - ID Empresa: {company.id}")
    print(f"\n💡 Ahora el admin puede acceder a los recursos de esta empresa")

