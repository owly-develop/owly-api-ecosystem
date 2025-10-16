"""
Advanced filters for Leads
"""
import django_filters
from django.db.models import Q
from .models import Lead


class LeadFilter(django_filters.FilterSet):
    """
    Advanced filter for leads with multiple options
    """
    # Date range filters
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    last_contact_after = django_filters.DateTimeFilter(field_name='last_contact_date', lookup_expr='gte')
    last_contact_before = django_filters.DateTimeFilter(field_name='last_contact_date', lookup_expr='lte')
    
    # Score range filters
    score_min = django_filters.NumberFilter(field_name='lead_score', lookup_expr='gte')
    score_max = django_filters.NumberFilter(field_name='lead_score', lookup_expr='lte')
    ai_probability_min = django_filters.NumberFilter(field_name='ai_close_probability', lookup_expr='gte')
    ai_probability_max = django_filters.NumberFilter(field_name='ai_close_probability', lookup_expr='lte')
    
    # Budget range filters
    budget_min = django_filters.NumberFilter(field_name='budget_min', lookup_expr='gte')
    budget_max = django_filters.NumberFilter(field_name='budget_max', lookup_expr='lte')
    
    # Multiple choice filters
    status_in = django_filters.MultipleChoiceFilter(
        field_name='status',
        choices=Lead.STATUS_CHOICES,
        lookup_expr='in'
    )
    priority_in = django_filters.MultipleChoiceFilter(
        field_name='priority',
        choices=Lead.PRIORITY_CHOICES,
        lookup_expr='in'
    )
    source_in = django_filters.MultipleChoiceFilter(
        field_name='source',
        choices=Lead.SOURCE_CHOICES,
        lookup_expr='in'
    )
    
    # Boolean filters
    has_follow_up = django_filters.BooleanFilter(method='filter_has_follow_up')
    requires_attention = django_filters.BooleanFilter(method='filter_requires_attention')
    
    # Advanced search
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Lead
        fields = [
            'status', 'priority', 'source', 'assigned_to',
            'converted_to_customer', 'consent_given', 'marketing_opt_in'
        ]
    
    def filter_has_follow_up(self, queryset, name, value):
        """Filter leads with or without follow-up date"""
        if value:
            return queryset.filter(next_follow_up_date__isnull=False)
        return queryset.filter(next_follow_up_date__isnull=True)
    
    def filter_requires_attention(self, queryset, name, value):
        """Filter leads that require attention (high priority, no recent contact)"""
        from django.utils import timezone
        from datetime import timedelta
        
        if value:
            week_ago = timezone.now() - timedelta(days=7)
            return queryset.filter(
                Q(priority__in=['high', 'urgent']) |
                Q(last_contact_date__lt=week_ago) |
                Q(last_contact_date__isnull=True)
            ).exclude(status__in=['closed_won', 'closed_lost'])
        return queryset
    
    def filter_search(self, queryset, name, value):
        """Advanced search across multiple fields"""
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value) |
            Q(phone__icontains=value) |
            Q(company_name__icontains=value) |
            Q(lead_number__icontains=value) |
            Q(notes__icontains=value)
        )

