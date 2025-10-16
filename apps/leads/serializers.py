"""
Lead serializers
"""
from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    """Serializer for Lead model"""
    full_name = serializers.CharField(read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    interested_projects_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Lead
        fields = '__all__'
        read_only_fields = [
            'id', 'company', 'lead_number', 'created_at', 'updated_at',
            'quote_count', 'total_quote_value', 'last_quote_date'
        ]
    
    def get_interested_projects_data(self, obj):
        return [{'id': str(p.id), 'name': p.name} for p in obj.interested_projects.all()]


class LeadListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for lead lists"""
    full_name = serializers.CharField(read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    
    class Meta:
        model = Lead
        fields = [
            'id', 'lead_number', 'first_name', 'last_name', 'full_name',
            'email', 'phone', 'status', 'priority', 'source',
            'lead_score', 'ai_close_probability', 'assigned_to', 'assigned_to_name',
            'last_contact_date', 'next_follow_up_date', 'created_at'
        ]


class LeadCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new lead"""
    class Meta:
        model = Lead
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'alternate_phone',
            'company_name', 'position', 'source', 'source_detail',
            'priority', 'assigned_to', 'interested_projects', 'interested_units',
            'budget_min', 'budget_max', 'budget_currency', 'financing',
            'preferences', 'notes', 'tags', 'consent_given', 'marketing_opt_in'
        ]

