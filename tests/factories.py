"""
Factory Boy factories for creating test data
"""
import factory
from factory.django import DjangoModelFactory
from faker import Faker
from decimal import Decimal
from django.utils import timezone

fake = Faker()


class CompanyFactory(DjangoModelFactory):
    """Factory for creating Company instances"""
    
    class Meta:
        model = 'companies.Company'
    
    name = factory.Faker('company')
    slug = factory.LazyAttribute(lambda obj: obj.name.lower().replace(' ', '-'))
    email = factory.Faker('email')
    plan = factory.Iterator(['free', 'starter', 'professional', 'enterprise'])
    status = 'active'
    max_users = 50
    max_projects = 100
    max_leads = 10000


class UserFactory(DjangoModelFactory):
    """Factory for creating User instances"""
    
    class Meta:
        model = 'users.User'
    
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = factory.Iterator(['admin', 'manager', 'sales', 'marketing'])
    status = 'active'
    company = factory.SubFactory(CompanyFactory)
    
    @factory.post_generation
    def password(obj, create, extracted):
        if create:
            obj.set_password(extracted or 'testpass123')
            obj.save()


class ProjectFactory(DjangoModelFactory):
    """Factory for creating Project instances"""
    
    class Meta:
        model = 'projects.Project'
    
    company = factory.SubFactory(CompanyFactory)
    name = factory.Faker('catch_phrase')
    code = factory.Sequence(lambda n: f'PROJ-2024-{n:03d}')
    type = factory.Iterator(['residential', 'commercial', 'mixed_use'])
    status = factory.Iterator(['planning', 'active', 'sold_out'])
    description = factory.Faker('paragraph')
    address = factory.Faker('street_address')
    city = factory.Faker('city')
    state = factory.Faker('state_abbr')
    country = 'USA'
    postal_code = factory.Faker('zipcode')
    total_units = factory.Faker('random_int', min=10, max=200)
    available_units = factory.LazyAttribute(lambda obj: obj.total_units // 2)
    price_from = Decimal('200000')
    price_to = Decimal('500000')


class UnitFactory(DjangoModelFactory):
    """Factory for creating Unit instances"""
    
    class Meta:
        model = 'projects.Unit'
    
    company = factory.LazyAttribute(lambda obj: obj.project.company)
    project = factory.SubFactory(ProjectFactory)
    unit_number = factory.Sequence(lambda n: f'{n:04d}')
    unit_type = factory.Iterator(['Studio', '1BR', '2BR', '3BR', 'Penthouse'])
    floor = factory.Faker('random_int', min=1, max=20)
    bedrooms = factory.Iterator([0, 1, 2, 3, 4])
    bathrooms = factory.Iterator([Decimal('1.0'), Decimal('1.5'), Decimal('2.0'), Decimal('2.5')])
    area_sqm = factory.Faker('pydecimal', left_digits=3, right_digits=2, min_value=50, max_value=200)
    price = factory.Faker('pydecimal', left_digits=6, right_digits=2, min_value=150000, max_value=800000)
    status = 'available'


class LeadFactory(DjangoModelFactory):
    """Factory for creating Lead instances"""
    
    class Meta:
        model = 'leads.Lead'
    
    company = factory.SubFactory(CompanyFactory)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    status = factory.Iterator(['new', 'contacted', 'qualified', 'proposal'])
    priority = factory.Iterator(['low', 'medium', 'high', 'urgent'])
    source = factory.Iterator(['website', 'facebook', 'instagram', 'referral'])
    lead_score = factory.Faker('random_int', min=0, max=100)
    ai_close_probability = factory.Faker('random_int', min=0, max=100)


class QuoteFactory(DjangoModelFactory):
    """Factory for creating Quote instances"""
    
    class Meta:
        model = 'quotes.Quote'
    
    company = factory.LazyAttribute(lambda obj: obj.lead.company)
    lead = factory.SubFactory(LeadFactory)
    project = factory.SubFactory(ProjectFactory)
    unit = factory.SubFactory(UnitFactory)
    unit_price = Decimal('350000')
    discount_percentage = Decimal('5')
    tax_percentage = Decimal('7')
    status = 'draft'
    valid_until = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=30))

