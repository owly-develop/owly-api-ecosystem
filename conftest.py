"""
Pytest configuration and fixtures
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.companies.models import Company

User = get_user_model()


@pytest.fixture
def api_client():
    """API client for testing"""
    return APIClient()


@pytest.fixture
def company(db):
    """Create a test company"""
    return Company.objects.create(
        name='Test Company',
        slug='test-company',
        email='test@company.com',
        plan='professional',
        status='active',
        max_users=50,
        max_projects=100,
        max_leads=10000
    )


@pytest.fixture
def another_company(db):
    """Create another company for multi-tenant testing"""
    return Company.objects.create(
        name='Another Company',
        slug='another-company',
        email='test@another.com',
        plan='starter',
        status='active'
    )


@pytest.fixture
def admin_user(db, company):
    """Create admin user"""
    return User.objects.create_user(
        email='admin@test.com',
        password='testpass123',
        first_name='Admin',
        last_name='User',
        role='admin',
        company=company,
        is_staff=True
    )


@pytest.fixture
def manager_user(db, company):
    """Create manager user"""
    return User.objects.create_user(
        email='manager@test.com',
        password='testpass123',
        first_name='Manager',
        last_name='User',
        role='manager',
        company=company
    )


@pytest.fixture
def sales_user(db, company):
    """Create sales user"""
    return User.objects.create_user(
        email='sales@test.com',
        password='testpass123',
        first_name='Sales',
        last_name='User',
        role='sales',
        company=company
    )


@pytest.fixture
def another_company_user(db, another_company):
    """Create user from another company"""
    return User.objects.create_user(
        email='user@another.com',
        password='testpass123',
        first_name='Other',
        last_name='User',
        role='sales',
        company=another_company
    )


@pytest.fixture
def authenticated_client(api_client, sales_user):
    """API client authenticated as sales user"""
    api_client.force_authenticate(user=sales_user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """API client authenticated as admin"""
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def manager_client(api_client, manager_user):
    """API client authenticated as manager"""
    api_client.force_authenticate(user=manager_user)
    return api_client

