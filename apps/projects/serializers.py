"""
Project serializers
"""
from rest_framework import serializers
from .models import Project, Unit


class UnitSerializer(serializers.ModelSerializer):
    """Serializer for Unit model"""
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = Unit
        fields = '__all__'
        read_only_fields = ['id', 'company', 'created_at', 'updated_at', 'price_per_sqm']


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model"""
    units = UnitSerializer(many=True, read_only=True)
    occupancy_rate = serializers.FloatField(read_only=True)
    project_manager_name = serializers.CharField(source='project_manager.full_name', read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['id', 'company', 'created_at', 'updated_at', 'view_count', 'lead_count', 'quote_count']


class ProjectListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for project lists"""
    occupancy_rate = serializers.FloatField(read_only=True)
    available_units_count = serializers.IntegerField(source='available_units', read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'code', 'type', 'status', 'city', 'state',
            'total_units', 'available_units', 'available_units_count',
            'price_from', 'price_to', 'currency',
            'main_image', 'featured', 'occupancy_rate', 'created_at'
        ]

