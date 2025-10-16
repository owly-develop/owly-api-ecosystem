"""
Integration tests for Quote API endpoints
"""
import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from apps.quotes.models import Quote
from apps.leads.models import Lead
from apps.projects.models import Project, Unit
from decimal import Decimal


@pytest.mark.integration
class TestQuoteAPI:
    """Test Quote API endpoints"""
    
    @pytest.fixture
    def project_and_unit(self, company):
        """Create project and unit for testing"""
        project = Project.objects.create(
            company=company,
            name='Test Project',
            code='TP-2024',
            description='Test',
            address='123 St',
            city='Miami',
            state='FL',
            country='USA',
            postal_code='33101',
            total_units=10,
            price_from=100000,
            price_to=200000
        )
        
        unit = Unit.objects.create(
            company=company,
            project=project,
            unit_number='301',
            unit_type='2BR',
            floor=3,
            bedrooms=2,
            bathrooms=Decimal('2.0'),
            area_sqm=Decimal('85.0'),
            price=Decimal('150000')
        )
        
        return project, unit
    
    def test_create_quote(self, authenticated_client, company, sales_user, project_and_unit):
        """Test creating a quote"""
        project, unit = project_and_unit
        
        lead = Lead.objects.create(
            company=company,
            first_name='Test',
            last_name='Lead',
            email='test@lead.com',
            phone='+1234567897',
            assigned_to=sales_user
        )
        
        url = reverse('quote-list')
        data = {
            'lead': str(lead.id),
            'project': str(project.id),
            'unit': str(unit.id),
            'unit_price': '150000',
            'discount_percentage': '5',
            'tax_percentage': '7',
            'valid_until': (timezone.now() + timedelta(days=30)).isoformat()
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['quote_number'].startswith('QT-')
        # Check calculations
        assert float(response.data['discount_amount']) == 7500.0  # 5% of 150000
        assert float(response.data['subtotal']) == 142500.0
    
    def test_send_quote(self, authenticated_client, company, sales_user, project_and_unit):
        """Test sending a quote"""
        project, unit = project_and_unit
        
        lead = Lead.objects.create(
            company=company,
            first_name='Test',
            last_name='Lead',
            email='test@lead.com',
            phone='+1234567898',
            assigned_to=sales_user
        )
        
        quote = Quote.objects.create(
            company=company,
            lead=lead,
            project=project,
            unit=unit,
            unit_price=Decimal('150000'),
            status='draft',
            valid_until=timezone.now() + timedelta(days=30),
            created_by=sales_user
        )
        
        url = reverse('quote-send', kwargs={'pk': quote.id})
        response = authenticated_client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'sent'
        assert response.data['sent_date'] is not None
    
    def test_accept_quote(self, authenticated_client, company, sales_user, project_and_unit):
        """Test accepting a quote"""
        project, unit = project_and_unit
        
        lead = Lead.objects.create(
            company=company,
            first_name='Test',
            last_name='Lead',
            email='test@lead.com',
            phone='+1234567899',
            assigned_to=sales_user
        )
        
        quote = Quote.objects.create(
            company=company,
            lead=lead,
            project=project,
            unit=unit,
            unit_price=Decimal('150000'),
            status='sent',
            valid_until=timezone.now() + timedelta(days=30),
            created_by=sales_user
        )
        
        url = reverse('quote-accept', kwargs={'pk': quote.id})
        response = authenticated_client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'accepted'
        assert response.data['accepted_date'] is not None

