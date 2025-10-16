"""
Unit tests for Project models
"""
import pytest
from apps.projects.models import Project, Unit
from decimal import Decimal


@pytest.mark.unit
class TestProjectModel:
    """Test Project model"""
    
    def test_create_project(self, company):
        """Test creating a project"""
        project = Project.objects.create(
            company=company,
            name='Test Project',
            code='TP-2024',
            type='residential',
            status='active',
            description='Test description',
            address='123 Test St',
            city='Miami',
            state='FL',
            country='USA',
            postal_code='33101',
            total_units=100,
            available_units=50,
            sold_units=30,
            reserved_units=20,
            price_from=250000,
            price_to=500000
        )
        
        assert project.name == 'Test Project'
        assert project.code == 'TP-2024'
        # (30 sold + 20 reserved) / 100 = 50%
        assert project.occupancy_rate == 50.0
    
    def test_occupancy_rate_calculation(self, company):
        """Test occupancy rate calculation"""
        project = Project.objects.create(
            company=company,
            name='Test',
            code='T-2',
            description='Test',
            address='123 St',
            city='Miami',
            state='FL',
            country='USA',
            postal_code='33102',
            total_units=100,
            available_units=30,
            sold_units=60,
            reserved_units=10,
            price_from=100000,
            price_to=200000
        )
        
        # (60 sold + 10 reserved) / 100 total = 70%
        assert project.occupancy_rate == 70.0


@pytest.mark.unit
class TestUnitModel:
    """Test Unit model"""
    
    def test_create_unit(self, company):
        """Test creating a unit"""
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
        
        unit = Unit.objects.create(
            company=company,
            project=project,
            unit_number='101',
            unit_type='2BR',
            floor=1,
            bedrooms=2,
            bathrooms=Decimal('2.0'),
            area_sqm=Decimal('85.5'),
            price=Decimal('150000')
        )
        
        assert unit.unit_number == '101'
        assert unit.project == project
        assert unit.price_per_sqm is not None
    
    def test_price_per_sqm_calculation(self, company):
        """Test price per sqm is calculated automatically"""
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
            area_sqm=Decimal('100.0'),
            price=Decimal('200000')
        )
        
        # 200000 / 100 = 2000
        assert float(unit.price_per_sqm) == 2000.0

