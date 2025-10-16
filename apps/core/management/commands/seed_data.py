"""
Django management command to seed database
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from decimal import Decimal
from datetime import timedelta

fake = Faker(['es_MX', 'en_US'])


class Command(BaseCommand):
    help = 'Seed database with realistic mock data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--companies',
            type=int,
            default=3,
            help='Number of companies to create'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('🗑️ Limpiando base de datos...'))
            self.clear_data()
        
        self.stdout.write(self.style.SUCCESS('\n🎲 Iniciando seed...'))
        
        companies = self.create_companies(options['companies'])
        users = self.create_users(companies)
        projects = self.create_projects(companies)
        units = self.create_units(projects)
        leads = self.create_leads(companies)
        quotes = self.create_quotes(companies)
        activities = self.create_activities(leads)
        
        self.print_summary(companies, users, projects, units, leads, quotes, activities)

    def clear_data(self):
        """Clear all data"""
        from apps.companies.models import Company
        
        # Deleting companies will cascade delete everything
        deleted = Company.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Datos eliminados'))

    def create_companies(self, num):
        """Create companies"""
        from apps.companies.models import Company
        
        self.stdout.write('\n🏢 Creando empresas...')
        
        companies = []
        names = [
            "Desarrollos Inmobiliarios Premium",
            "Constructora Horizonte Real Estate",
            "Inversiones Urbanas del Sur",
            "Grupo Inmobiliario Elite",
            "Propiedades del Caribe"
        ]
        
        plans = ['professional', 'enterprise', 'starter']
        
        for i in range(num):
            company = Company.objects.create(
                name=names[i] if i < len(names) else f"Empresa {i+1}",
                slug=f"company-{i+1}",
                email=f"contact@company{i+1}.com",
                plan=plans[i % len(plans)],
                status='active',
                city=fake.city(),
                state="FL",
                country="USA"
            )
            companies.append(company)
            self.stdout.write(f'  ✓ {company.name}')
        
        return companies

    def create_users(self, companies):
        """Create users"""
        from apps.users.models import User
        
        self.stdout.write('\n👥 Creando usuarios...')
        
        all_users = []
        roles = ['admin', 'manager', 'sales', 'sales', 'sales', 'marketing', 'support', 'sales']
        
        for company in companies:
            for i, role in enumerate(roles):
                first_name = fake.first_name()
                last_name = fake.last_name()
                
                user = User.objects.create_user(
                    email=f"{first_name.lower()}.{last_name.lower()}{i}@{company.slug}.com",
                    password='demo123',
                    first_name=first_name,
                    last_name=last_name,
                    company=company,
                    role=role,
                    status='active'
                )
                all_users.append(user)
        
        self.stdout.write(f'  ✓ Creados {len(all_users)} usuarios')
        return all_users

    def create_projects(self, companies):
        """Create projects"""
        from apps.projects.models import Project
        from apps.users.models import User
        
        self.stdout.write('\n🏗️ Creando proyectos...')
        
        all_projects = []
        cities = ["Miami", "Tampa", "Orlando"]
        
        for company in companies:
            for i in range(4):
                city = random.choice(cities)
                total_units = random.randint(30, 100)
                sold = random.randint(5, int(total_units * 0.4))
                reserved = random.randint(0, int(total_units * 0.1))
                available = total_units - sold - reserved
                
                import uuid
                code_suffix = str(uuid.uuid4())[:6].upper()
                project = Project.objects.create(
                    company=company,
                    name=f"Proyecto {city} {i+1}",
                    code=f"{city[:3].upper()}-{code_suffix}",
                    description=fake.paragraph(),
                    address=fake.street_address(),
                    city=city,
                    state="FL",
                    country="USA",
                    postal_code=fake.zipcode(),
                    total_units=total_units,
                    available_units=available,
                    sold_units=sold,
                    reserved_units=reserved,
                    price_from=Decimal(random.randint(200000, 400000)),
                    price_to=Decimal(random.randint(400000, 800000)),
                    status='active',
                    type='residential'
                )
                all_projects.append(project)
        
        self.stdout.write(f'  ✓ Creados {len(all_projects)} proyectos')
        return all_projects

    def create_units(self, projects):
        """Create units"""
        from apps.projects.models import Unit
        
        self.stdout.write('\n🏠 Creando unidades...')
        
        all_units = []
        
        for project in projects:
            for i in range(min(30, project.total_units)):
                unit = Unit.objects.create(
                    company=project.company,
                    project=project,
                    unit_number=f"{i+1:04d}",
                    unit_type=random.choice(['1BR', '2BR', '3BR']),
                    floor=random.randint(1, 15),
                    bedrooms=random.randint(1, 3),
                    bathrooms=Decimal('2.0'),
                    area_sqm=Decimal(random.randint(60, 120)),
                    price=Decimal(random.randint(250000, 600000)),
                    status='available' if i >= project.sold_units else 'sold'
                )
                all_units.append(unit)
        
        self.stdout.write(f'  ✓ Creadas {len(all_units)} unidades')
        return all_units

    def create_leads(self, companies):
        """Create leads"""
        from apps.leads.models import Lead
        from apps.users.models import User
        
        self.stdout.write('\n👥 Creando leads...')
        
        all_leads = []
        
        for company in companies:
            sales_users = list(User.objects.filter(company=company, role='sales'))
            
            for i in range(100):
                lead = Lead.objects.create(
                    company=company,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.email(),
                    phone=fake.phone_number(),
                    status=random.choice(['new', 'contacted', 'qualified', 'proposal']),
                    priority=random.choice(['low', 'medium', 'high']),
                    source=random.choice(['website', 'facebook', 'instagram', 'referral']),
                    lead_score=random.randint(30, 95),
                    assigned_to=random.choice(sales_users) if sales_users else None
                )
                all_leads.append(lead)
        
        self.stdout.write(f'  ✓ Creados {len(all_leads)} leads')
        return all_leads

    def create_quotes(self, companies):
        """Create quotes"""
        from apps.quotes.models import Quote
        from apps.leads.models import Lead
        from apps.projects.models import Project, Unit
        from apps.users.models import User
        
        self.stdout.write('\n💰 Creando cotizaciones...')
        
        all_quotes = []
        
        for company in companies:
            leads = list(Lead.objects.filter(company=company, status='qualified')[:20])
            projects = list(Project.objects.filter(company=company))
            users = list(User.objects.filter(company=company, role='sales'))
            
            for lead in leads:
                if not projects:
                    continue
                    
                project = random.choice(projects)
                units = list(Unit.objects.filter(project=project, status='available')[:5])
                
                if not units:
                    continue
                
                unit = random.choice(units)
                
                quote = Quote.objects.create(
                    company=company,
                    lead=lead,
                    project=project,
                    unit=unit,
                    unit_price=unit.price,
                    discount_percentage=Decimal('5'),
                    tax_percentage=Decimal('7'),
                    status='sent',
                    valid_until=timezone.now() + timedelta(days=30),
                    created_by=random.choice(users) if users else None
                )
                all_quotes.append(quote)
        
        self.stdout.write(f'  ✓ Creadas {len(all_quotes)} cotizaciones')
        return all_quotes

    def create_activities(self, leads):
        """Create activities"""
        from apps.activities.models import Activity
        from apps.leads.models import Lead
        from django.contrib.contenttypes.models import ContentType
        
        self.stdout.write('\n📋 Creando actividades...')
        
        all_activities = []
        lead_ct = ContentType.objects.get_for_model(Lead)
        
        for lead in random.sample(list(leads), min(100, len(leads))):
            if not lead.assigned_to:
                continue
                
            activity = Activity.objects.create(
                company=lead.company,
                activity_type='call',
                title='Llamada de seguimiento',
                description=fake.paragraph(),
                user=lead.assigned_to,
                content_type=lead_ct,
                object_id=lead.id,
                status='completed',
                completed_date=timezone.now()
            )
            all_activities.append(activity)
        
        self.stdout.write(f'  ✓ Creadas {len(all_activities)} actividades')
        return all_activities

    def print_summary(self, companies, users, projects, units, leads, quotes, activities):
        """Print summary"""
        self.stdout.write(self.style.SUCCESS(f"""
\n{'='*60}
📊 RESUMEN FINAL
{'='*60}

🏢 Empresas:        {len(companies)}
👥 Usuarios:        {len(users)}
🏗️ Proyectos:       {len(projects)}
🏠 Unidades:        {len(units)}
👤 Leads:           {len(leads)}
💰 Cotizaciones:    {len(quotes)}
📋 Actividades:     {len(activities)}

{'='*60}
✅ BASE DE DATOS POBLADA!
{'='*60}

🌐 Admin: http://localhost:8000/admin/
👤 Email: admin@owlycrm.com
🔑 Pass: admin123

💡 También: [nombre].[apellido][número]@company-1.com / demo123
"""))

