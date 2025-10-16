"""
Advanced filters for Projects
"""
import django_filters
from .models import Project, Unit


class ProjectFilter(django_filters.FilterSet):
    """Advanced filter for projects"""
    # Price range
    price_min = django_filters.NumberFilter(field_name='price_from', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price_to', lookup_expr='lte')
    
    # Date range
    launch_after = django_filters.DateFilter(field_name='launch_date', lookup_expr='gte')
    launch_before = django_filters.DateFilter(field_name='launch_date', lookup_expr='lte')
    delivery_after = django_filters.DateFilter(field_name='delivery_date', lookup_expr='gte')
    delivery_before = django_filters.DateFilter(field_name='delivery_date', lookup_expr='lte')
    
    # Units
    available_units_min = django_filters.NumberFilter(field_name='available_units', lookup_expr='gte')
    total_units_min = django_filters.NumberFilter(field_name='total_units', lookup_expr='gte')
    total_units_max = django_filters.NumberFilter(field_name='total_units', lookup_expr='lte')
    
    # Construction
    construction_progress_min = django_filters.NumberFilter(field_name='construction_progress', lookup_expr='gte')
    
    class Meta:
        model = Project
        fields = ['status', 'type', 'city', 'state', 'country', 'featured']


class UnitFilter(django_filters.FilterSet):
    """Advanced filter for units"""
    # Price range
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    # Area range
    area_min = django_filters.NumberFilter(field_name='area_sqm', lookup_expr='gte')
    area_max = django_filters.NumberFilter(field_name='area_sqm', lookup_expr='lte')
    
    # Rooms
    bedrooms_min = django_filters.NumberFilter(field_name='bedrooms', lookup_expr='gte')
    bedrooms_max = django_filters.NumberFilter(field_name='bedrooms', lookup_expr='lte')
    bathrooms_min = django_filters.NumberFilter(field_name='bathrooms', lookup_expr='gte')
    
    # Floor
    floor_min = django_filters.NumberFilter(field_name='floor', lookup_expr='gte')
    floor_max = django_filters.NumberFilter(field_name='floor', lookup_expr='lte')
    
    class Meta:
        model = Unit
        fields = ['project', 'status', 'unit_type', 'floor', 'bedrooms', 'orientation']

