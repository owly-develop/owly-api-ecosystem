"""
Unit tests for Company models
"""
import pytest
from apps.companies.models import Company


@pytest.mark.unit
class TestCompanyModel:
    """Test Company model"""
    
    def test_create_company(self, db):
        """Test creating a company"""
        company = Company.objects.create(
            name='Test Company',
            slug='test-company',
            email='test@company.com',
            plan='professional',
            status='active'
        )
        
        assert company.name == 'Test Company'
        assert company.slug == 'test-company'
        assert company.is_active is True
        assert company.is_trial is False
    
    def test_company_user_count(self, company, admin_user, sales_user):
        """Test user count method"""
        assert company.get_user_count() == 2
    
    def test_company_can_add_user(self, company):
        """Test can_add_user method"""
        company.max_users = 5
        company.save()
        
        # Create 4 users
        from apps.users.models import User
        for i in range(4):
            User.objects.create_user(
                email=f'user{i}@test.com',
                password='test123',
                first_name=f'User{i}',
                last_name='Test',
                company=company
            )
        
        assert company.can_add_user() is True
        
        # Create 5th user (at limit)
        User.objects.create_user(
            email='user5@test.com',
            password='test123',
            first_name='User5',
            last_name='Test',
            company=company
        )
        
        assert company.can_add_user() is False
    
    def test_company_string_representation(self, company):
        """Test __str__ method"""
        assert str(company) == 'Test Company'

