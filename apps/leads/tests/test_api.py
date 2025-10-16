"""
Integration tests for Lead API endpoints
"""
import pytest
from django.urls import reverse
from rest_framework import status
from apps.leads.models import Lead


@pytest.mark.integration
class TestLeadAPI:
    """Test Lead API endpoints"""
    
    def test_list_leads(self, authenticated_client, company, sales_user):
        """Test listing leads"""
        # Create test leads
        Lead.objects.create(
            company=company,
            first_name='John',
            last_name='Doe',
            email='john@test.com',
            phone='+1234567890',
            assigned_to=sales_user
        )
        
        url = reverse('lead-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
    
    def test_create_lead(self, authenticated_client):
        """Test creating a lead"""
        url = reverse('lead-list')
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@test.com',
            'phone': '+1234567891',
            'source': 'website',
            'priority': 'high'
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['first_name'] == 'Jane'
        assert response.data['lead_number'].startswith('LEAD-')
    
    def test_tenant_isolation_leads(self, authenticated_client, another_company):
        """Test users can only see their company's leads"""
        # Create lead in another company
        lead = Lead.objects.create(
            company=another_company,
            first_name='Other',
            last_name='Company',
            email='other@test.com',
            phone='+1234567892'
        )
        
        # Try to access
        url = reverse('lead-detail', kwargs={'pk': lead.id})
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_assign_lead(self, manager_client, company, sales_user):
        """Test assigning lead to user"""
        lead = Lead.objects.create(
            company=company,
            first_name='Test',
            last_name='Lead',
            email='test@lead.com',
            phone='+1234567893'
        )
        
        url = reverse('lead-assign', kwargs={'pk': lead.id})
        data = {'user_id': str(sales_user.id)}
        response = manager_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['assigned_to'] == str(sales_user.id)
    
    def test_change_status(self, authenticated_client, company, sales_user):
        """Test changing lead status"""
        lead = Lead.objects.create(
            company=company,
            first_name='Test',
            last_name='Lead',
            email='test@lead.com',
            phone='+1234567894',
            assigned_to=sales_user,
            status='new'
        )
        
        url = reverse('lead-change-status', kwargs={'pk': lead.id})
        data = {'status': 'contacted'}
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'contacted'
    
    def test_add_note(self, authenticated_client, company, sales_user):
        """Test adding note to lead"""
        lead = Lead.objects.create(
            company=company,
            first_name='Test',
            last_name='Lead',
            email='test@lead.com',
            phone='+1234567895',
            assigned_to=sales_user
        )
        
        url = reverse('lead-add-note', kwargs={'pk': lead.id})
        data = {'note': 'This is a test note'}
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'This is a test note' in response.data['notes']
    
    def test_bulk_assign(self, manager_client, company, sales_user):
        """Test bulk assigning leads"""
        # Create multiple leads
        lead1 = Lead.objects.create(
            company=company,
            first_name='Lead1',
            last_name='Test',
            email='lead1@test.com',
            phone='+1111111111'
        )
        lead2 = Lead.objects.create(
            company=company,
            first_name='Lead2',
            last_name='Test',
            email='lead2@test.com',
            phone='+2222222222'
        )
        
        url = reverse('lead-bulk-assign')
        data = {
            'lead_ids': [str(lead1.id), str(lead2.id)],
            'user_id': str(sales_user.id)
        }
        response = manager_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['updated_count'] == 2
    
    def test_hot_leads(self, authenticated_client, company, sales_user):
        """Test getting hot leads"""
        # Create high priority lead
        Lead.objects.create(
            company=company,
            first_name='Hot',
            last_name='Lead',
            email='hot@test.com',
            phone='+3333333333',
            priority='high',
            lead_score=85,
            assigned_to=sales_user
        )
        
        url = reverse('lead-hot-leads')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
    
    def test_lead_stats(self, authenticated_client, company, sales_user):
        """Test lead statistics endpoint"""
        # Create some leads
        for i in range(3):
            Lead.objects.create(
                company=company,
                first_name=f'Lead{i}',
                last_name='Test',
                email=f'lead{i}@test.com',
                phone=f'+111111{i}{i}{i}{i}',
                assigned_to=sales_user,
                status='new' if i % 2 == 0 else 'contacted'
            )
        
        url = reverse('lead-stats')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'total' in response.data
        assert 'by_status' in response.data
        assert response.data['total'] >= 3

