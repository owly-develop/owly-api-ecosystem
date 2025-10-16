#!/usr/bin/env python
"""
Script to create a superuser programmatically
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'owly_crm.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

email = 'admin@owlycrm.com'
password = 'admin123'
first_name = 'Admin'
last_name = 'User'

if not User.objects.filter(email=email).exists():
    user = User.objects.create_superuser(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    print(f'✅ Superuser created successfully!')
    print(f'   Email: {email}')
    print(f'   Password: {password}')
    print(f'   ⚠️  Remember to change the password!')
else:
    print(f'ℹ️  Superuser with email {email} already exists.')

