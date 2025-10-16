"""
Tests for advanced filters
"""
import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework import status


@pytest.mark.integration
class TestLeadFilters:
    """Test lead filtering capabilities"""
    
    def test_filter_by_score_range(self, authenticated_client, company, sales_user):
        """Test filtering leads by score range"""
        from apps.leads.models import Lead
        
        # Create leads with different scores
        Lead.objects.create(
            company=company,
            first_name='Low',
            last_name='Score',
            email='low@test.com',
            phone='+1111111111',
            lead_score=30,
            assigned_to=sales_user
        )
        
        Lead.objects.create(
            company=company,
            first_name='High',
            last_name='Score',
            email='high@test.com',
            phone='+2222222222',
            lead_score=85,
            assigned_to=sales_user
        )
        
        # Filter for high scores
        url = reverse('lead-list')
        response = authenticated_client.get(f'{url}?score_min=70')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['lead_score'] >= 70
    
    def test_filter_by_multiple_statuses(self, authenticated_client, company, sales_user):
        """Test filtering by multiple statuses"""
        from apps.leads.models import Lead
        
        Lead.objects.create(
            company=company,
            first_name='New',
            last_name='Lead',
            email='new@test.com',
            phone='+3333333333',
            status='new',
            assigned_to=sales_user
        )
        
        Lead.objects.create(
            company=company,
            first_name='Qualified',
            last_name='Lead',
            email='qualified@test.com',
            phone='+4444444444',
            status='qualified',
            assigned_to=sales_user
        )
        
        Lead.objects.create(
            company=company,
            first_name='Closed',
            last_name='Lead',
            email='closed@test.com',
            phone='+5555555555',
            status='closed_won',
            assigned_to=sales_user
        )
        
        # Filter for new and qualified only
        url = reverse('lead-list')
        response = authenticated_client.get(f'{url}?status_in=new,qualified')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2
    
    def test_filter_by_date_range(self, authenticated_client, company, sales_user):
        """Test filtering by creation date"""
        from apps.leads.models import Lead
        from freezegun import freeze_time
        
        # Create lead 10 days ago
        with freeze_time(timezone.now() - timedelta(days=10)):
            Lead.objects.create(
                company=company,
                first_name='Old',
                last_name='Lead',
                email='old@test.com',
                phone='+6666666666',
                assigned_to=sales_user
            )
        
        # Create lead today
        Lead.objects.create(
            company=company,
            first_name='Recent',
            last_name='Lead',
            email='recent@test.com',
            phone='+7777777777',
            assigned_to=sales_user
        )
        
        # Filter for leads created in last 7 days
        url = reverse('lead-list')
        date_filter = (timezone.now() - timedelta(days=7)).isoformat()
        response = authenticated_client.get(f'{url}?created_after={date_filter}')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

