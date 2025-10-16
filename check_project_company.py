#!/usr/bin/env python
"""
Script to check which company a project belongs to
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'owly_crm.settings')
django.setup()

from apps.projects.models import Project
from apps.companies.models import Company

project_id = '3cf587c2-126e-46be-bf40-fe3bce9dfa92'

try:
    project = Project.objects.get(id=project_id)
    print(f"\n📊 INFORMACIÓN DEL PROYECTO:\n")
    print(f"Nombre: {project.name}")
    print(f"Código: {project.code}")
    print(f"Empresa: {project.company.name}")
    print(f"ID Empresa: {project.company.id}")
    print(f"\n" + "="*60)
    
    print(f"\n🏢 TODAS LAS EMPRESAS Y SUS PROYECTOS:\n")
    for company in Company.objects.all():
        projects = Project.objects.filter(company=company)
        print(f"\n{company.name} (ID: {company.id})")
        print(f"  Total proyectos: {projects.count()}")
        for p in projects[:3]:  # Mostrar primeros 3
            print(f"    • {p.name} - ID: {p.id}")
            
except Project.DoesNotExist:
    print(f"⚠️  Proyecto con ID {project_id} no existe")

