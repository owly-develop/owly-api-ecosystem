"""
Integration tests for Project API endpoints
"""
import pytest
from django.urls import reverse
from rest_framework import status
from apps.projects.models import Project, Unit
from decimal import Decimal


@pytest.mark.integration
class TestProjectAPI:
    """Test Project API endpoints"""
    
    def test_list_projects(self, authenticated_client, company):
        """Test listing projects"""
        Project.objects.create(
            company=company,
            name='Test Project',
            code='TP-2024',
            description='Test',
            address='123 St',
            city='Miami',
            state='FL',
            country='USA',
            postal_code='33101',
            total_units=100,
            price_from=250000,
            price_to=500000
        )
        
        url = reverse('project-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
    
    def test_create_project(self, authenticated_client):
        """Test creating a project"""
        url = reverse('project-list')
        data = {
            'name': 'New Project',
            'code': 'NP-2024',
            'type': 'residential',
            'status': 'planning',
            'description': 'New test project',
            'address': '456 Main St',
            'city': 'Miami',
            'state': 'FL',
            'country': 'USA',
            'postal_code': '33102',
            'total_units': 50,
            'price_from': 300000,
            'price_to': 600000
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Project'
    
    def test_get_project_stats(self, authenticated_client, company):
        """Test project stats endpoint"""
        project = Project.objects.create(
            company=company,
            name='Stats Project',
            code='SP-2024',
            description='Test',
            address='789 St',
            city='Miami',
            state='FL',
            country='USA',
            postal_code='33103',
            total_units=100,
            available_units=60,
            sold_units=30,
            reserved_units=10,
            price_from=250000,
            price_to=500000
        )
        
        url = reverse('project-stats', kwargs={'pk': project.id})
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['total_units'] == 100
        assert response.data['occupancy_rate'] == 40.0
    
    def test_featured_projects(self, authenticated_client, company):
        """Test getting featured projects"""
        Project.objects.create(
            company=company,
            name='Featured Project',
            code='FP-2024',
            description='Test',
            address='111 St',
            city='Miami',
            state='FL',
            country='USA',
            postal_code='33104',
            total_units=50,
            price_from=300000,
            price_to=600000,
            status='active',
            featured=True
        )
        
        url = reverse('project-featured')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
        assert response.data[0]['featured'] is True


@pytest.mark.integration
class TestUnitAPI:
    """Test Unit API endpoints"""
    
    def test_list_units(self, authenticated_client, company):
        """Test listing units"""
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
        
        Unit.objects.create(
            company=company,
            project=project,
            unit_number='101',
            unit_type='2BR',
            floor=1,
            bedrooms=2,
            bathrooms=Decimal('2.0'),
            area_sqm=Decimal('85.0'),
            price=Decimal('150000')
        )
        
        url = reverse('unit-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
    
    def test_reserve_unit(self, authenticated_client, company, sales_user):
        """Test reserving a unit for a lead"""
        from apps.leads.models import Lead
        
        project = Project.objects.create(
            company=company,
            name='Test',
            code='T-1',
            description='Test',
            address='123 St',
            city='Miami',
            state='FL',
            country='USA',
            postal_code='33101',
            total_units=10,
            available_units=5,
            price_from=100000,
            price_to=200000
        )
        
        unit = Unit.objects.create(
            company=company,
            project=project,
            unit_number='201',
            unit_type='2BR',
            floor=2,
            bedrooms=2,
            bathrooms=Decimal('2.0'),
            area_sqm=Decimal('90.0'),
            price=Decimal('180000'),
            status='available'
        )
        
        lead = Lead.objects.create(
            company=company,
            first_name='Test',
            last_name='Lead',
            email='test@lead.com',
            phone='+1234567896',
            assigned_to=sales_user
        )
        
        url = reverse('unit-reserve', kwargs={'pk': unit.id})
        data = {'lead_id': str(lead.id)}
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'reserved'
        
        # Verify project counts updated
        project.refresh_from_db()
        assert project.available_units == 4
        assert project.reserved_units == 1

