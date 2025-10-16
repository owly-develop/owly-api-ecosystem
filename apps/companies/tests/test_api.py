"""
Integration tests for Company API endpoints
"""
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.integration
class TestCompanyAPI:
    """Test Company API endpoints"""
    
    def test_list_companies_authenticated(self, authenticated_client, company):
        """Test listing companies as authenticated user"""
        url = reverse('company-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == company.name
    
    def test_list_companies_unauthenticated(self, api_client):
        """Test listing companies without authentication fails"""
        url = reverse('company-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_company_detail(self, authenticated_client, company):
        """Test getting company details"""
        url = reverse('company-detail', kwargs={'pk': company.id})
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == company.name
        assert response.data['plan'] == 'professional'
    
    def test_tenant_isolation(self, authenticated_client, another_company):
        """Test users can't see other companies"""
        url = reverse('company-detail', kwargs={'pk': another_company.id})
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_company_stats(self, admin_client, company, admin_user):
        """Test company stats endpoint"""
        url = reverse('company-stats', kwargs={'pk': company.id})
        response = admin_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'users' in response.data
        assert 'projects' in response.data
        assert response.data['users'] >= 1
    
    def test_upgrade_plan_as_admin(self, admin_client, company):
        """Test upgrading company plan"""
        url = reverse('company-upgrade-plan', kwargs={'pk': company.id})
        response = admin_client.post(url, {'plan': 'enterprise'})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['plan'] == 'enterprise'
        assert response.data['max_users'] == 999
    
    def test_upgrade_plan_as_sales_fails(self, authenticated_client, company):
        """Test sales user cannot upgrade plan"""
        url = reverse('company-upgrade-plan', kwargs={'pk': company.id})
        response = authenticated_client.post(url, {'plan': 'enterprise'})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

