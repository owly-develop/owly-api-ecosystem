#!/usr/bin/env python
"""
Script para asociar el admin a una empresa y crear una empresa demo
Ejecutar con: docker-compose exec web python fix_admin_company.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'owly_crm.settings')
django.setup()

from apps.users.models import User
from apps.companies.models import Company

try:
    # Buscar o crear empresa demo
    company, created = Company.objects.get_or_create(
        slug='owly-demo',
        defaults={
            'name': 'Owly Demo Company',
            'legal_name': 'Owly Demo Company S.A.S.',
            'industry': 'real_estate',
            'plan': 'enterprise',
            'status': 'active',
            'email': 'demo@owly.com',
            'phone': '+57 300 123 4567',
            'address': 'Calle 100 #15-20, Bogotá',
            'city': 'Bogotá',
            'state': 'Cundinamarca',
            'country': 'Colombia',
            'currency': 'COP',
            'max_users': 100,
            'max_projects': 100,
            'max_leads': 10000,
        }
    )
    
    if created:
        print(f"✅ Empresa creada: {company.name}")
    else:
        print(f"✅ Empresa encontrada: {company.name}")
    
    # Asociar el admin a la empresa
    admin = User.objects.get(email='admin@owly.com')
    
    if not admin.company:
        admin.company = company
        admin.save()
        print(f"✅ Usuario {admin.email} asociado a {company.name}")
    else:
        print(f"✅ Usuario {admin.email} ya estaba asociado a {admin.company.name}")
    
    print("\n" + "="*50)
    print("INFORMACIÓN DE ACCESO:")
    print("="*50)
    print(f"Email: admin@owly.com")
    print(f"Password: OwlyAdmin2024!")
    print(f"Empresa: {company.name}")
    print(f"ID Empresa: {company.id}")
    print("="*50)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

