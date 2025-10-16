"""
End-to-end tests for complete user flows
"""
import pytest
from django.urls import reverse
from rest_framework import status
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta


@pytest.mark.e2e
@pytest.mark.django_db
class TestCompleteSalesFlow:
    """Test complete sales flow from lead to closed deal"""
    
    def test_complete_sales_cycle(self, api_client, company):
        """
        Test complete flow:
        1. Create company
        2. Create user
        3. Login
        4. Create project
        5. Create unit
        6. Create lead
        7. Create quote
        8. Send quote
        9. Accept quote
        10. Reserve unit
        11. Mark as sold
        """
        from apps.users.models import User
        from apps.projects.models import Project, Unit
        from apps.leads.models import Lead
        from apps.quotes.models import Quote
        
        # 1. Company already created via fixture
        assert company.name == 'Test Company'
        
        # 2. Create user
        user = User.objects.create_user(
            email='sales@test.com',
            password='testpass123',
            first_name='Sales',
            last_name='Rep',
            company=company,
            role='sales'
        )
        
        # 3. Login
        login_url = reverse('token_obtain_pair')
        login_data = {'email': 'sales@test.com', 'password': 'testpass123'}
        login_response = api_client.post(login_url, login_data)
        
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.data['access']
        
        # Set auth header
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # 4. Create project
        project_url = reverse('project-list')
        project_data = {
            'name': 'Sunset Towers',
            'code': 'ST-2024',
            'type': 'residential',
            'status': 'active',
            'description': 'Luxury apartments',
            'address': '100 Ocean Dr',
            'city': 'Miami Beach',
            'state': 'FL',
            'country': 'USA',
            'postal_code': '33139',
            'total_units': 50,
            'available_units': 30,
            'price_from': 300000,
            'price_to': 700000
        }
        project_response = api_client.post(project_url, project_data, format='json')
        assert project_response.status_code == status.HTTP_201_CREATED
        project_id = project_response.data['id']
        
        # 5. Create unit
        unit_url = reverse('unit-list')
        unit_data = {
            'project': project_id,
            'unit_number': '1205',
            'unit_type': '2BR/2BA',
            'floor': 12,
            'bedrooms': 2,
            'bathrooms': '2.0',
            'area_sqm': '95.5',
            'price': '450000',
            'status': 'available'
        }
        unit_response = api_client.post(unit_url, unit_data, format='json')
        assert unit_response.status_code == status.HTTP_201_CREATED
        unit_id = unit_response.data['id']
        
        # 6. Create lead
        lead_url = reverse('lead-list')
        lead_data = {
            'first_name': 'Maria',
            'last_name': 'Gonzalez',
            'email': 'maria@test.com',
            'phone': '+13055551234',
            'source': 'website',
            'priority': 'high'
        }
        lead_response = api_client.post(lead_url, lead_data, format='json')
        assert lead_response.status_code == status.HTTP_201_CREATED
        lead_id = lead_response.data['id']
        
        # 7. Create quote
        quote_url = reverse('quote-list')
        quote_data = {
            'lead': lead_id,
            'project': project_id,
            'unit': unit_id,
            'unit_price': '450000',
            'discount_percentage': '5',
            'tax_percentage': '7',
            'valid_until': (timezone.now() + timedelta(days=30)).isoformat()
        }
        quote_response = api_client.post(quote_url, quote_data, format='json')
        assert quote_response.status_code == status.HTTP_201_CREATED
        quote_id = quote_response.data['id']
        assert quote_response.data['status'] == 'draft'
        
        # 8. Send quote
        send_url = reverse('quote-send', kwargs={'pk': quote_id})
        send_response = api_client.post(send_url)
        assert send_response.status_code == status.HTTP_200_OK
        assert send_response.data['status'] == 'sent'
        
        # 9. Accept quote
        accept_url = reverse('quote-accept', kwargs={'pk': quote_id})
        accept_response = api_client.post(accept_url)
        assert accept_response.status_code == status.HTTP_200_OK
        assert accept_response.data['status'] == 'accepted'
        
        # 10. Reserve unit
        reserve_url = reverse('unit-reserve', kwargs={'pk': unit_id})
        reserve_data = {'lead_id': lead_id}
        reserve_response = api_client.post(reserve_url, reserve_data, format='json')
        assert reserve_response.status_code == status.HTTP_200_OK
        assert reserve_response.data['status'] == 'reserved'
        
        # 11. Mark as sold
        sold_url = reverse('unit-mark-as-sold', kwargs={'pk': unit_id})
        sold_data = {'sold_to': 'Maria Gonzalez - Contract #2024-001'}
        sold_response = api_client.post(sold_url, sold_data, format='json')
        assert sold_response.status_code == status.HTTP_200_OK
        assert sold_response.data['status'] == 'sold'
        
        # Verify final state
        final_lead_url = reverse('lead-detail', kwargs={'pk': lead_id})
        final_lead = api_client.get(final_lead_url)
        # Lead should still exist and be trackable


@pytest.mark.e2e
class TestMultiTenantIsolation:
    """Test that multi-tenant isolation works correctly"""
    
    def test_company_data_isolation(self, api_client, company, another_company):
        """Test that companies cannot see each other's data"""
        from apps.users.models import User
        from apps.leads.models import Lead
        
        # Create users for both companies
        user1 = User.objects.create_user(
            email='user1@company1.com',
            password='test123',
            first_name='User',
            last_name='One',
            company=company
        )
        
        user2 = User.objects.create_user(
            email='user2@company2.com',
            password='test123',
            first_name='User',
            last_name='Two',
            company=another_company
        )
        
        # Create lead for company 1
        lead1 = Lead.objects.create(
            company=company,
            first_name='Lead',
            last_name='One',
            email='lead1@test.com',
            phone='+1111111111',
            assigned_to=user1
        )
        
        # Create lead for company 2
        lead2 = Lead.objects.create(
            company=another_company,
            first_name='Lead',
            last_name='Two',
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
        
        # User1 should see only lead1
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token1}')
        leads_url = reverse('lead-list')
        response = api_client.get(leads_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['id'] == str(lead1.id)
        
        # User1 should NOT be able to access lead2
        lead2_url = reverse('lead-detail', kwargs={'pk': lead2.id})
        response = api_client.get(lead2_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        # Login as user2
        login_response = api_client.post(
            login_url,
            {'email': 'user2@company2.com', 'password': 'test123'}
        )
        token2 = login_response.data['access']
        
        # User2 should see only lead2
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token2}')
        response = api_client.get(leads_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['id'] == str(lead2.id)


@pytest.mark.e2e
class TestAnalyticsDashboard:
    """Test analytics dashboard with real data"""
    
    def test_dashboard_with_data(self, authenticated_client, company, sales_user):
        """Test dashboard returns correct statistics"""
        from apps.leads.models import Lead
        from apps.projects.models import Project
        
        # Create test data
        # 5 leads in different statuses
        for i in range(5):
            Lead.objects.create(
                company=company,
                first_name=f'Lead{i}',
                last_name='Test',
                email=f'lead{i}@test.com',
                phone=f'+111111{i}{i}{i}{i}',
                assigned_to=sales_user,
                status='new' if i < 2 else 'qualified'
            )
        
        # 2 projects
        for i in range(2):
            Project.objects.create(
                company=company,
                name=f'Project {i}',
                code=f'P{i}-2024',
                description='Test',
                address='123 St',
                city='Miami',
                state='FL',
                country='USA',
                postal_code='33101',
                total_units=50,
                available_units=30,
                price_from=200000,
                price_to=400000,
                status='active'
            )
        
        url = reverse('dashboard-stats')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['leads']['total'] == 5
        assert response.data['projects']['total'] == 2
        assert response.data['projects']['active'] == 2

