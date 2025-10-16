"""
Unit tests for Lead models
"""
import pytest
from apps.leads.models import Lead


@pytest.mark.unit
class TestLeadModel:
    """Test Lead model"""
    
    def test_create_lead(self, company):
        """Test creating a lead"""
        lead = Lead.objects.create(
            company=company,
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='+1234567890',
            status='new',
            priority='medium',
            source='website'
        )
        
        assert lead.first_name == 'John'
        assert lead.full_name == 'John Doe'
        assert lead.lead_number.startswith('LEAD-')
    
    def test_lead_number_auto_generation(self, company):
        """Test lead number is auto-generated"""
        lead1 = Lead.objects.create(
            company=company,
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            phone='+1234567891',
            status='new'
        )
        
        lead2 = Lead.objects.create(
            company=company,
            first_name='Bob',
            last_name='Johnson',
            email='bob@example.com',
            phone='+1234567892',
            status='new'
        )
        
        assert lead1.lead_number != lead2.lead_number
        assert 'LEAD-' in lead1.lead_number
        assert 'LEAD-' in lead2.lead_number
    
    def test_lead_full_name_property(self, company):
        """Test full_name property"""
        lead = Lead.objects.create(
            company=company,
            first_name='Alice',
            last_name='Williams',
            email='alice@example.com',
            phone='+1234567893'
        )
        
        assert lead.full_name == 'Alice Williams'

