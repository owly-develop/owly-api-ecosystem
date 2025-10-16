#!/usr/bin/env python
"""
Script para establecer la contraseña del superusuario
Ejecutar con: docker-compose exec web python set_admin_password.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'owly_crm.settings')
django.setup()

from apps.users.models import User

try:
    user = User.objects.get(email='admin@owly.com')
    user.set_password('OwlyAdmin2024!')
    user.save()
    print("✅ Contraseña establecida correctamente para admin@owly.com")
    print("   Contraseña: OwlyAdmin2024!")
except User.DoesNotExist:
    print("❌ Usuario no encontrado")

