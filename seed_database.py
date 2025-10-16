#!/usr/bin/env python
"""
Script to seed database with realistic mock data
Genera múltiples empresas, proyectos, leads, unidades, etc.
"""
import os
import django
import random
from decimal import Decimal
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'owly_crm.settings')
django.setup()

from django.utils import timezone
from faker import Faker
from apps.companies.models import Company
from apps.users.models import User
from apps.projects.models import Project, Unit
from apps.leads.models import Lead
from apps.quotes.models import Quote
from apps.activities.models import Activity
from django.contrib.contenttypes.models import ContentType

fake = Faker(['es_MX', 'en_US'])

# Configuración
NUM_COMPANIES = 3
USERS_PER_COMPANY = 8
PROJECTS_PER_COMPANY = 4
UNITS_PER_PROJECT = 50
LEADS_PER_COMPANY = 100
QUOTES_PER_COMPANY = 40
ACTIVITIES_PER_LEAD = 5

# Datos realistas para proyectos inmobiliarios
PROJECT_NAMES = [
    "Torres del Mar", "Villas del Sol", "Residencias Paraíso",
    "Ocean View Towers", "Sunset Residences", "Green Valley Condos",
    "Marina Bay Apartments", "Sky View Penthouses", "Palm Beach Villas",
    "Crystal Lake Homes", "Mountain View Estates", "Riverside Commons"
]

CITIES = [
    ("Miami", "FL"), ("Fort Lauderdale", "FL"), ("West Palm Beach", "FL"),
    ("Tampa", "FL"), ("Orlando", "FL"), ("Jacksonville", "FL"),
    ("Coral Gables", "FL"), ("Boca Raton", "FL")
]

AMENITIES = [
    "Piscina", "Gimnasio", "Seguridad 24/7", "Estacionamiento",
    "Salón de eventos", "Área de juegos", "BBQ area", "Pet park",
    "Business center", "Yoga studio", "Spa", "Rooftop terrace"
]

UNIT_TYPES = ["Studio", "1BR/1BA", "2BR/2BA", "3BR/2BA", "3BR/3BA", "Penthouse"]

def create_companies():
    """Crear empresas"""
    print("\n" + "="*60)
    print("🏢 Creando empresas...")
    print("="*60)
    
    companies = []
    company_names = [
        "Desarrollos Inmobiliarios Premium",
        "Constructora Horizonte Real Estate",
        "Inversiones Urbanas del Sur"
    ]
    
    plans = ['professional', 'enterprise', 'starter']
    
    for i, name in enumerate(company_names):
        company = Company.objects.create(
            name=name,
            slug=f"{name.lower().replace(' ', '-')}-{i}",
            legal_name=f"{name} S.A. de C.V.",
            tax_id=fake.bothify(text='??-#######'),
            industry='Real Estate Development',
            email=f"contact@company{i+1}.com",
            phone=fake.phone_number(),
            website=f"https://www.company{i+1}.com",
            address=fake.street_address(),
            city=random.choice(CITIES)[0],
            state="FL",
            country="USA",
            postal_code=fake.zipcode(),
            plan=plans[i],
            status='active',
            max_users=50 if plans[i] == 'professional' else 999,
            max_projects=100 if plans[i] == 'professional' else 999,
            max_leads=25000 if plans[i] == 'professional' else 999999,
            primary_color=random.choice(['#3B82F6', '#10B981', '#F59E0B', '#EF4444']),
            timezone='America/New_York',
            currency='USD'
        )
        companies.append(company)
        print(f"  ✓ {company.name} ({company.plan})")
    
    print(f"\n✅ Creadas {len(companies)} empresas")
    return companies


def create_users(companies):
    """Crear usuarios para cada empresa"""
    print("\n" + "="*60)
    print("👥 Creando usuarios...")
    print("="*60)
    
    all_users = []
    roles = ['admin', 'manager', 'sales', 'sales', 'sales', 'marketing', 'support', 'sales']
    
    for company in companies:
        print(f"\n  Empresa: {company.name}")
        company_users = []
        
        for i in range(USERS_PER_COMPANY):
            role = roles[i]
            first_name = fake.first_name()
            last_name = fake.last_name()
            
            user = User.objects.create_user(
                email=f"{first_name.lower()}.{last_name.lower()}@{company.slug}.com",
                password='demo123',
                first_name=first_name,
                last_name=last_name,
                phone=fake.phone_number(),
                company=company,
                role=role,
                status='active',
                territories=[fake.city(), fake.city()],
                settings={
                    'language': 'es',
                    'timezone': 'America/New_York',
                    'notifications': {
                        'email': True,
                        'push': True
                    }
                }
            )
            company_users.append(user)
            all_users.append(user)
            print(f"    ✓ {user.full_name} ({role})")
        
    print(f"\n✅ Creados {len(all_users)} usuarios")
    return all_users


def create_projects(companies):
    """Crear proyectos para cada empresa"""
    print("\n" + "="*60)
    print("🏗️ Creando proyectos...")
    print("="*60)
    
    all_projects = []
    project_types = ['residential', 'commercial', 'mixed_use']
    statuses = ['active', 'active', 'active', 'pre_launch']
    project_counter = 0  # Contador global para nombres únicos
    
    for company in companies:
        print(f"\n  Empresa: {company.name}")
        company_users = User.objects.filter(company=company)
        
        for i in range(PROJECTS_PER_COMPANY):
            city, state = random.choice(CITIES)
            project_type = random.choice(project_types)
            status = statuses[i]
            project_counter += 1
            
            total_units = random.randint(30, 120)
            sold = random.randint(0, int(total_units * 0.6))
            reserved = random.randint(0, int((total_units - sold) * 0.2))
            available = total_units - sold - reserved
            
            price_from = random.randint(200000, 400000)
            price_to = price_from + random.randint(200000, 600000)
            
            # Preparar media items
            media_items = [
                {
                    'type': 'image',
                    'reference': f'gallery_{j}',
                    'url': f"https://picsum.photos/seed/{fake.uuid4()}/800/600"
                }
                for j in range(5)
            ]
            
            project = Project.objects.create(
                company=company,
                name=f"{random.choice(PROJECT_NAMES)} {city} #{project_counter}",
                code=f"{city[:3].upper()}-{fake.bothify(text='##??').upper()}",
                developer=company.legal_name,
                type=project_type,
                status=status,
                description=fake.paragraph(nb_sentences=5),
                tagline=fake.catch_phrase(),
                address=fake.street_address(),
                city=city,
                state=state,
                country="USA",
                postal_code=fake.zipcode(),
                latitude=Decimal(str(fake.latitude())),
                longitude=Decimal(str(fake.longitude())),
                neighborhood=fake.city_suffix(),
                total_units=total_units,
                available_units=available,
                sold_units=sold,
                reserved_units=reserved,
                price_from=Decimal(price_from),
                price_to=Decimal(price_to),
                currency='USD',
                amenities=random.sample(AMENITIES, k=random.randint(6, 10)),
                features=['Smart Home Ready', 'Energy Efficient', 'Modern Design'],
                launch_date=fake.date_between(start_date='-1y', end_date='today'),
                delivery_date=fake.date_between(start_date='today', end_date='+2y'),
                construction_progress=random.randint(40, 95) if status == 'active' else random.randint(0, 30),
                main_image=f"https://picsum.photos/seed/{fake.uuid4()}/800/600",
                media_items=media_items,
                featured=i == 0,  # Primer proyecto es featured
                tags=['nuevo', 'destacado'] if i == 0 else ['disponible'],
                project_manager=random.choice(company_users),
                view_count=random.randint(100, 5000),
                lead_count=random.randint(20, 200),
                quote_count=random.randint(10, 100)
            )
            all_projects.append(project)
            print(f"    ✓ {project.name} - {total_units} unidades ({available} disponibles)")
    
    print(f"\n✅ Creados {len(all_projects)} proyectos")
    return all_projects


def create_units(projects):
    """Crear unidades para cada proyecto"""
    print("\n" + "="*60)
    print("🏠 Creando unidades...")
    print("="*60)
    
    all_units = []
    orientations = ['North', 'South', 'East', 'West']
    view_types = ['Ocean View', 'City View', 'Garden View', 'Mountain View']
    
    for project in projects:
        print(f"\n  Proyecto: {project.name}")
        
        total_to_create = min(project.total_units, UNITS_PER_PROJECT)
        
        for i in range(total_to_create):
            unit_type = random.choice(UNIT_TYPES)
            floor = random.randint(1, 20)
            
            # Bedrooms based on type
            bedrooms_map = {
                'Studio': 0,
                '1BR/1BA': 1,
                '2BR/2BA': 2,
                '3BR/2BA': 3,
                '3BR/3BA': 3,
                'Penthouse': 3
            }
            bedrooms = bedrooms_map.get(unit_type, 2)
            bathrooms = Decimal('1.0') if bedrooms <= 1 else Decimal('2.0')
            
            # Area
            area_sqm = Decimal(str(random.randint(50, 150) + random.random()))
            
            # Price based on floor and type
            base_price = float(project.price_from)
            floor_bonus = floor * 2000
            type_bonus = 50000 if 'Penthouse' in unit_type else 0
            price = Decimal(base_price + floor_bonus + type_bonus)
            
            # Status
            if i < project.sold_units:
                unit_status = 'sold'
            elif i < project.sold_units + project.reserved_units:
                unit_status = 'reserved'
            else:
                unit_status = 'available'
            
            unit = Unit.objects.create(
                company=project.company,
                project=project,
                unit_number=f"{i+1:04d}",  # Formato único: 0001, 0002, etc.
                unit_type=unit_type,
                floor=floor,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                area_sqm=area_sqm,
                terrace_sqm=Decimal(str(random.randint(0, 30))),
                price=price,
                currency='USD',
                status=unit_status,
                orientation=random.choice(orientations),
                view_type=random.choice(view_types),
                features=['Balcony', 'Walk-in Closet', 'Modern Kitchen'],
                floor_plan_image=f"https://picsum.photos/seed/{fake.uuid4()}/600/400",
                sold_to=fake.name() if unit_status == 'sold' else '',
                sold_date=timezone.now() - timedelta(days=random.randint(1, 365)) if unit_status == 'sold' else None
            )
            all_units.append(unit)
        
        print(f"    ✓ Creadas {total_to_create} unidades")
    
    print(f"\n✅ Creadas {len(all_units)} unidades en total")
    return all_units


def create_leads(companies):
    """Crear leads para cada empresa"""
    print("\n" + "="*60)
    print("👥 Creando leads...")
    print("="*60)
    
    all_leads = []
    sources = ['website', 'facebook', 'instagram', 'whatsapp', 'referral', 'cold_call']
    statuses = ['new', 'contacted', 'qualified', 'proposal', 'negotiation', 'closed_won', 'closed_lost']
    priorities = ['low', 'medium', 'high', 'urgent']
    
    for company in companies:
        print(f"\n  Empresa: {company.name}")
        company_users = list(User.objects.filter(company=company, role='sales'))
        company_projects = list(Project.objects.filter(company=company))
        
        for i in range(LEADS_PER_COMPANY):
            status = random.choices(
                statuses,
                weights=[25, 20, 15, 12, 10, 10, 8]  # Más nuevos que cerrados
            )[0]
            
            priority = random.choices(
                priorities,
                weights=[20, 40, 30, 10]  # Mayoría medium/high
            )[0]
            
            created_date = timezone.now() - timedelta(days=random.randint(0, 180))
            
            lead = Lead.objects.create(
                company=company,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=fake.phone_number(),
                company_name=fake.company() if random.random() > 0.7 else '',
                position=fake.job() if random.random() > 0.7 else '',
                status=status,
                priority=priority,
                source=random.choice(sources),
                source_detail=f"Campaign {fake.bothify(text='##??').upper()}",
                lead_score=random.randint(20, 95),
                ai_close_probability=random.randint(15, 90),
                assigned_to=random.choice(company_users) if company_users else None,
                assigned_date=created_date + timedelta(hours=random.randint(1, 24)),
                last_contact_date=created_date + timedelta(days=random.randint(1, 30)) if status != 'new' else None,
                interaction_count=random.randint(0, 15),
                next_follow_up_date=timezone.now() + timedelta(days=random.randint(1, 14)) if status in ['contacted', 'qualified'] else None,
                budget_min=Decimal(random.randint(150000, 400000)),
                budget_max=Decimal(random.randint(400000, 800000)),
                budget_currency='USD',
                financing=random.random() > 0.3,
                notes=fake.paragraph() if random.random() > 0.5 else '',
                tags=['hot' if priority == 'urgent' else 'normal'],
                converted_to_customer=status == 'closed_won',
                conversion_date=timezone.now() - timedelta(days=random.randint(1, 30)) if status == 'closed_won' else None,
                consent_given=True,
                marketing_opt_in=random.random() > 0.3,
                created_at=created_date
            )
            
            # Agregar proyectos de interés
            if company_projects and random.random() > 0.5:
                interested = random.sample(company_projects, k=min(2, len(company_projects)))
                lead.interested_projects.set(interested)
            
            all_leads.append(lead)
        
        print(f"    ✓ Creados {LEADS_PER_COMPANY} leads")
    
    print(f"\n✅ Creados {len(all_leads)} leads en total")
    return all_leads


def create_quotes(companies):
    """Crear cotizaciones"""
    print("\n" + "="*60)
    print("💰 Creando cotizaciones...")
    print("="*60)
    
    all_quotes = []
    statuses = ['draft', 'sent', 'viewed', 'accepted', 'rejected']
    
    for company in companies:
        print(f"\n  Empresa: {company.name}")
        
        company_leads = list(Lead.objects.filter(
            company=company,
            status__in=['qualified', 'proposal', 'negotiation', 'closed_won']
        ))
        company_projects = list(Project.objects.filter(company=company))
        company_users = list(User.objects.filter(company=company, role__in=['sales', 'manager']))
        
        if not company_leads or not company_projects:
            continue
        
        for i in range(min(QUOTES_PER_COMPANY, len(company_leads))):
            lead = company_leads[i]
            project = random.choice(company_projects)
            units = list(Unit.objects.filter(project=project, status__in=['available', 'reserved'])[:10])
            
            if not units:
                continue
            
            unit = random.choice(units)
            unit_price = unit.price
            discount_pct = Decimal(random.choice([0, 3, 5, 7, 10]))
            
            quote_status = random.choices(
                statuses,
                weights=[10, 25, 20, 30, 15]
            )[0]
            
            created_date = timezone.now() - timedelta(days=random.randint(1, 90))
            
            quote = Quote.objects.create(
                company=company,
                lead=lead,
                project=project,
                unit=unit,
                unit_price=unit_price,
                discount_percentage=discount_pct,
                discount_amount=unit_price * (discount_pct / 100),
                tax_percentage=Decimal('7.0'),
                status=quote_status,
                valid_until=timezone.now() + timedelta(days=30),
                created_by=random.choice(company_users) if company_users else None,
                financing_offered=random.random() > 0.5,
                financing_terms={
                    'down_payment_percentage': 20,
                    'monthly_payment': 1850,
                    'term_months': 240
                } if random.random() > 0.5 else {},
                notes=fake.paragraph() if random.random() > 0.7 else '',
                created_at=created_date
            )
            
            # Set dates based on status
            if quote_status in ['sent', 'viewed', 'accepted', 'rejected']:
                quote.sent_date = created_date + timedelta(hours=2)
            
            if quote_status in ['viewed', 'accepted', 'rejected']:
                quote.viewed_date = created_date + timedelta(hours=random.randint(3, 50))
            
            if quote_status == 'accepted' and quote.viewed_date:
                quote.accepted_date = quote.viewed_date + timedelta(hours=random.randint(1, 72))
            
            if quote_status == 'rejected' and quote.viewed_date:
                quote.rejected_date = quote.viewed_date + timedelta(hours=random.randint(1, 72))
            
            quote.save()
            
            all_quotes.append(quote)
        
        print(f"    ✓ Creadas cotizaciones")
    
    print(f"\n✅ Creadas {len(all_quotes)} cotizaciones en total")
    return all_quotes


def create_activities(leads):
    """Crear actividades para leads"""
    print("\n" + "="*60)
    print("📋 Creando actividades...")
    print("="*60)
    
    all_activities = []
    activity_types = ['call', 'email', 'meeting', 'note', 'task']
    
    lead_content_type = ContentType.objects.get_for_model(Lead)
    
    # Solo crear para algunos leads (no todos)
    sample_leads = random.sample(list(leads), k=min(200, len(leads)))
    
    for lead in sample_leads:
        num_activities = random.randint(1, ACTIVITIES_PER_LEAD)
        
        for i in range(num_activities):
            activity_type = random.choice(activity_types)
            created_date = lead.created_at + timedelta(days=random.randint(0, 30))
            
            titles = {
                'call': [
                    'Llamada de seguimiento',
                    'Primera llamada',
                    'Llamada para confirmar cita',
                    'Seguimiento post-cotización'
                ],
                'email': [
                    'Envío de brochure',
                    'Envío de cotización',
                    'Email de seguimiento',
                    'Información del proyecto'
                ],
                'meeting': [
                    'Reunión en oficina',
                    'Visita al proyecto',
                    'Firma de contrato',
                    'Presentación de opciones'
                ],
                'note': [
                    'Nota de seguimiento',
                    'Comentario interno',
                    'Actualización de status'
                ],
                'task': [
                    'Pendiente: Enviar documentos',
                    'Preparar cotización',
                    'Coordinar visita'
                ]
            }
            
            activity = Activity.objects.create(
                company=lead.company,
                activity_type=activity_type,
                title=random.choice(titles[activity_type]),
                description=fake.paragraph() if random.random() > 0.5 else '',
                user=lead.assigned_to if lead.assigned_to else User.objects.filter(company=lead.company).first(),
                content_type=lead_content_type,
                object_id=lead.id,
                status='completed',
                completed_date=created_date,
                duration_minutes=random.randint(5, 60) if activity_type in ['call', 'meeting'] else None,
                created_at=created_date
            )
            all_activities.append(activity)
    
    print(f"✅ Creadas {len(all_activities)} actividades")
    return all_activities


def print_summary(companies, users, projects, units, leads, quotes, activities):
    """Imprimir resumen final"""
    print("\n" + "="*60)
    print("📊 RESUMEN FINAL")
    print("="*60)
    print(f"""
🏢 Empresas creadas:        {len(companies)}
👥 Usuarios creados:        {len(users)}
🏗️ Proyectos creados:       {len(projects)}
🏠 Unidades creadas:        {len(units)}
👤 Leads creados:           {len(leads)}
💰 Cotizaciones creadas:    {len(quotes)}
📋 Actividades creadas:     {len(activities)}

Por empresa:
""")
    
    for company in companies:
        comp_users = User.objects.filter(company=company).count()
        comp_projects = Project.objects.filter(company=company).count()
        comp_units = Unit.objects.filter(company=company).count()
        comp_leads = Lead.objects.filter(company=company).count()
        comp_quotes = Quote.objects.filter(company=company).count()
        
        print(f"""
  📊 {company.name}:
     • Usuarios: {comp_users}
     • Proyectos: {comp_projects}
     • Unidades: {comp_units}
     • Leads: {comp_leads}
     • Cotizaciones: {comp_quotes}
""")
    
    print("="*60)
    print("✅ BASE DE DATOS POBLADA EXITOSAMENTE!")
    print("="*60)
    print(f"""
🌐 Accede al admin:
   http://localhost:8000/admin/

👤 Credenciales:
   Email: admin@owlycrm.com
   Password: admin123

💡 También puedes usar cualquier usuario creado:
   Email: [nombre].[apellido]@[empresa].com
   Password: demo123

🎯 Próximos pasos:
   1. Explora el admin
   2. Ve los datos en las diferentes empresas
   3. Prueba filtros y búsquedas
   4. Revisa la API en /api/docs/
""")


def main():
    """Script principal"""
    import sys
    
    print("\n" + "="*60)
    print("🎲 OWLY CRM - SEED DATABASE")
    print("Generando datos de prueba realistas...")
    print("="*60)
    
    # Verificar si ya hay datos
    if Company.objects.exists():
        print("\n⚠️  ADVERTENCIA: Ya existen empresas en la base de datos")
        # Check for --force flag
        if '--force' not in sys.argv:
            print("💡 Usa --force para continuar de todos modos")
            print("   Ejemplo: python seed_database.py --force")
            print("❌ Cancelado - usa --force para agregar más datos")
            return
        else:
            print("✅ Flag --force detectado, continuando...")
    
    # Crear datos
    companies = create_companies()
    users = create_users(companies)
    projects = create_projects(companies)
    units = create_units(projects)
    leads = create_leads(companies)
    quotes = create_quotes(companies)
    activities = create_activities(leads)
    
    # Resumen
    print_summary(companies, users, projects, units, leads, quotes, activities)


if __name__ == '__main__':
    main()

