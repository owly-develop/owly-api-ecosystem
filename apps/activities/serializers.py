"""
Activity serializers
"""
from rest_framework import serializers
from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ['id', 'company', 'created_at', 'updated_at']

