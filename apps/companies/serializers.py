"""
Company serializers
"""
from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer for Company model
    """
    user_count = serializers.SerializerMethodField()
    project_count = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'slug', 'legal_name', 'tax_id', 'industry',
            'email', 'phone', 'website',
            'address', 'city', 'state', 'country', 'postal_code',
            'plan', 'status', 'trial_ends_at', 'subscription_ends_at',
            'max_users', 'max_projects', 'max_leads', 'max_storage_gb',
            'logo', 'primary_color', 'timezone', 'currency',
            'features', 'metadata',
            'user_count', 'project_count', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
    
    def get_user_count(self, obj):
        return obj.get_user_count()
    
    def get_project_count(self, obj):
        return obj.get_project_count()


class CompanyCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new company
    """
    class Meta:
        model = Company
        fields = [
            'name', 'legal_name', 'email', 'phone', 'website',
            'address', 'city', 'state', 'country', 'postal_code',
            'industry', 'plan'
        ]
    
    def create(self, validated_data):
        # Generate slug from name
        from django.utils.text import slugify
        import uuid
        slug = slugify(validated_data['name'])
        # Ensure uniqueness
        if Company.objects.filter(slug=slug).exists():
            slug = f"{slug}-{uuid.uuid4().hex[:6]}"
        validated_data['slug'] = slug
        return super().create(validated_data)


class CompanyUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating company details
    """
    class Meta:
        model = Company
        fields = [
            'name', 'legal_name', 'tax_id', 'industry',
            'email', 'phone', 'website',
            'address', 'city', 'state', 'country', 'postal_code',
            'logo', 'primary_color', 'timezone', 'currency',
            'features', 'metadata'
        ]

