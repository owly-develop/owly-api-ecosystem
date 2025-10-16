"""
Multi-tenant isolation tests
"""
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.integration
class TestMultiTenantIsolation:
    """Test that multi-tenant data isolation works correctly"""
    
    def test_leads_isolated_by_company(self, api_client, company, another_company):
        """Test leads are isolated by company"""
        from apps.users.models import User
        from apps.leads.models import Lead
        
        # Create users
        user1 = User.objects.create_user(
            email='user1@company1.com',
            password='test123',
            first_name='User1',
            last_name='Test',
            company=company
        )
        
        user2 = User.objects.create_user(
            email='user2@company2.com',
            password='test123',
            first_name='User2',
            last_name='Test',
            company=another_company
        )
        
        # Create leads
        lead1 = Lead.objects.create(
            company=company,
            first_name='Lead1',
            last_name='CompanyA',
            email='lead1@test.com',
            phone='+1111111111',
            assigned_to=user1
        )
        
        lead2 = Lead.objects.create(
            company=another_company,
            first_name='Lead2',
            last_name='CompanyB',
            email='lead2@test.com',
            phone='+2222222222',
            assigned_to=user2
        )
        
        # Login as user1
        login_url = reverse('token_obtain_pair')
        login_response = api_client.post(
            login_url,
            {'email': 'user1@company1.com', 'password': 'test123'}
        )
        token1 = login_response.data['access']
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token1}')
        
        # List leads - should only see lead1
        leads_url = reverse('lead-list')
        response = api_client.get(leads_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['id'] == str(lead1.id)
        
        # Try to access lead2 directly - should fail
        lead2_url = reverse('lead-detail', kwargs={'pk': lead2.id})
        response = api_client.get(lead2_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_projects_isolated_by_company(self, api_client, company, another_company):
        """Test projects are isolated by company"""
        from apps.users.models import User
        from apps.projects.models import Project
        
        # Create users
        user1 = User.objects.create_user(
            email='user1@company1.com',
            password='test123',
            first_name='User1',
            last_name='Test',
            company=company
        )
        
        # Create projects
        project1 = Project.objects.create(
            company=company,
            name='Project Company A',
            code='PCA-2024',
            description='Test',
            address='123 St',
            city='Miami',
            state='FL',
            country='USA',
            postal_code='33101',
            total_units=50,
            price_from=200000,
            price_to=400000
        )
        
        project2 = Project.objects.create(
            company=another_company,
            name='Project Company B',
            code='PCB-2024',
            description='Test',
            address='456 St',
            city='Miami',
            state='FL',
            country='USA',
            postal_code='33102',
            total_units=30,
            price_from=300000,
            price_to=500000
        )
        
        # Login as user1
        login_url = reverse('token_obtain_pair')
        login_response = api_client.post(
            login_url,
            {'email': 'user1@company1.com', 'password': 'test123'}
        )
        token = login_response.data['access']
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # List projects - should only see project1
        projects_url = reverse('project-list')
        response = api_client.get(projects_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == 'Project Company A'
    
    def test_cannot_create_lead_for_another_company(self, authenticated_client, another_company):
        """Test user cannot create lead for another company"""
        url = reverse('lead-list')
        data = {
            'company': str(another_company.id),  # Try to set another company
            'first_name': 'Hacker',
            'last_name': 'Attempt',
            'email': 'hacker@test.com',
            'phone': '+9999999999'
        }
        response = authenticated_client.post(url, data, format='json')
        
        # Should create but with user's company, not the one in data
        if response.status_code == status.HTTP_201_CREATED:
            # Verify it used the authenticated user's company
            from apps.leads.models import Lead
            lead = Lead.objects.get(id=response.data['id'])
            assert lead.company != another_company
            assert lead.company == authenticated_client.handler._force_user.company

