"""
Quote serializers
"""
from rest_framework import serializers
from .models import Quote, QuoteTemplate


class QuoteSerializer(serializers.ModelSerializer):
    """Serializer for Quote model"""
    lead_name = serializers.CharField(source='lead.full_name', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    unit_number = serializers.CharField(source='unit.unit_number', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = Quote
        fields = '__all__'
        read_only_fields = [
            'id', 'company', 'quote_number', 'subtotal', 'tax_amount', 'total',
            'sent_date', 'viewed_date', 'accepted_date', 'rejected_date',
            'created_at', 'updated_at'
        ]


class QuoteTemplateSerializer(serializers.ModelSerializer):
    """Serializer for QuoteTemplate model"""
    class Meta:
        model = QuoteTemplate
        fields = '__all__'
        read_only_fields = ['id', 'company', 'created_at', 'updated_at']

