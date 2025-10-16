"""
Tests for authentication endpoints
"""
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.integration
class TestAuthentication:
    """Test authentication flow"""
    
    def test_login_success(self, api_client, sales_user):
        """Test successful login"""
        url = reverse('token_obtain_pair')
        data = {
            'email': 'sales@test.com',
            'password': 'testpass123'
        }
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_login_invalid_credentials(self, api_client):
        """Test login with invalid credentials"""
        url = reverse('token_obtain_pair')
        data = {
            'email': 'invalid@test.com',
            'password': 'wrongpassword'
        }
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_token_refresh(self, api_client, sales_user):
        """Test token refresh"""
        # First login
        login_url = reverse('token_obtain_pair')
        login_data = {
            'email': 'sales@test.com',
            'password': 'testpass123'
        }
        login_response = api_client.post(login_url, login_data)
        refresh_token = login_response.data['refresh']
        
        # Then refresh
        refresh_url = reverse('token_refresh')
        refresh_data = {'refresh': refresh_token}
        response = api_client.post(refresh_url, refresh_data)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
    
    def test_get_profile(self, authenticated_client, sales_user):
        """Test getting user profile"""
        url = reverse('user-profile')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == sales_user.email
        assert response.data['full_name'] == sales_user.full_name
    
    def test_change_password(self, authenticated_client):
        """Test changing password"""
        url = reverse('user-change-password')
        data = {
            'old_password': 'testpass123',
            'new_password': 'newpass123',
            'new_password_confirm': 'newpass123'
        }
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data

