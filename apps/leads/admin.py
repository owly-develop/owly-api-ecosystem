"""
Lead admin configuration
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Lead


class LeadStatusFilter(admin.SimpleListFilter):
    """Custom filter for lead status with counts"""
    title = 'status'
    parameter_name = 'status'
    
    def lookups(self, request, model_admin):
        return Lead.STATUS_CHOICES
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


class LeadScoreFilter(admin.SimpleListFilter):
    """Filter leads by score range"""
    title = 'lead score'
    parameter_name = 'score_range'
    
    def lookups(self, request, model_admin):
        return (
            ('high', 'High (70-100)'),
            ('medium', 'Medium (40-69)'),
            ('low', 'Low (0-39)'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'high':
            return queryset.filter(lead_score__gte=70)
        if self.value() == 'medium':
            return queryset.filter(lead_score__gte=40, lead_score__lt=70)
        if self.value() == 'low':
            return queryset.filter(lead_score__lt=40)
        return queryset


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = [
        'lead_number_link', 'full_name_display', 'email', 'phone',
        'status_badge', 'priority_badge', 'source',
        'lead_score_display', 'ai_close_probability',
        'assigned_to', 'created_at_display'
    ]
    list_filter = [
        LeadStatusFilter,
        'priority',
        'source',
        LeadScoreFilter,
        'company',
        'assigned_to',
        'converted_to_customer',
        'consent_given',
        'created_at'
    ]
    search_fields = [
        'lead_number', 'first_name', 'last_name',
        'email', 'phone', 'company_name', 'notes'
    ]
    readonly_fields = [
        'id', 'lead_number', 'created_at', 'updated_at',
        'quote_count', 'total_quote_value', 'last_quote_date',
        'interaction_count'
    ]
    date_hierarchy = 'created_at'
    list_per_page = 50
    list_select_related = ['company', 'assigned_to']
    
    # Bulk actions
    actions = [
        'mark_as_contacted',
        'mark_as_qualified',
        'mark_as_high_priority',
        'assign_to_me',
        'export_selected_leads'
    ]
    
    fieldsets = (
        ('Identification', {
            'fields': ('id', 'lead_number', 'company')
        }),
        ('Personal Information', {
            'fields': (
                ('first_name', 'last_name'),
                ('email', 'phone'),
                ('alternate_phone', 'company_name'),
                'position'
            )
        }),
        ('Status & Priority', {
            'fields': (
                ('status', 'priority'),
                ('source', 'source_detail'),
                ('lead_score', 'ai_close_probability')
            )
        }),
        ('AI Insights', {
            'fields': ('ai_insights', 'conversion_factors'),
            'classes': ('collapse',)
        }),
        ('Assignment', {
            'fields': (
                'assigned_to',
                ('assigned_date', 'assigned_by')
            )
        }),
        ('Interaction Tracking', {
            'fields': (
                ('last_contact_date', 'last_interaction_date'),
                ('interaction_count', 'next_follow_up_date')
            )
        }),
        ('Budget & Preferences', {
            'fields': (
                ('budget_min', 'budget_max', 'budget_currency'),
                ('financing', 'down_payment_percentage'),
                'preferences'
            ),
            'classes': ('collapse',)
        }),
        ('Interests', {
            'fields': ('interested_projects', 'interested_units'),
            'classes': ('collapse',)
        }),
        ('Quotes', {
            'fields': (
                ('quote_count', 'total_quote_value'),
                'last_quote_date'
            ),
            'classes': ('collapse',)
        }),
        ('Notes & Tags', {
            'fields': ('notes', 'tags'),
            'classes': ('wide',)
        }),
        ('Conversion', {
            'fields': (
                ('converted_to_customer', 'customer_id'),
                'conversion_date'
            ),
            'classes': ('collapse',)
        }),
        ('Privacy & Consent', {
            'fields': (
                ('consent_given', 'consent_date'),
                'marketing_opt_in'
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'is_deleted'),
            'classes': ('collapse',)
        })
    )
    
    # Custom display methods
    def lead_number_link(self, obj):
        url = reverse('admin:leads_lead_change', args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, obj.lead_number)
    lead_number_link.short_description = 'Lead #'
    lead_number_link.admin_order_field = 'lead_number'
    
    def full_name_display(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name_display.short_description = 'Name'
    full_name_display.admin_order_field = 'first_name'
    
    def status_badge(self, obj):
        colors = {
            'new': '#17a2b8',
            'contacted': '#6c757d',
            'qualified': '#007bff',
            'proposal': '#fd7e14',
            'negotiation': '#ffc107',
            'closed_won': '#28a745',
            'closed_lost': '#dc3545',
            'nurturing': '#6f42c1'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def priority_badge(self, obj):
        colors = {
            'low': '#6c757d',
            'medium': '#17a2b8',
            'high': '#fd7e14',
            'urgent': '#dc3545'
        }
        color = colors.get(obj.priority, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'
    priority_badge.admin_order_field = 'priority'
    
    def lead_score_display(self, obj):
        if obj.lead_score >= 70:
            color = '#28a745'  # Green
        elif obj.lead_score >= 40:
            color = '#ffc107'  # Yellow
        else:
            color = '#dc3545'  # Red
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.lead_score
        )
    lead_score_display.short_description = 'Score'
    lead_score_display.admin_order_field = 'lead_score'
    
    def created_at_display(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at_display.short_description = 'Created'
    created_at_display.admin_order_field = 'created_at'
    
    # Bulk actions
    def mark_as_contacted(self, request, queryset):
        updated = queryset.update(
            status='contacted',
            last_contact_date=timezone.now()
        )
        self.message_user(request, f'{updated} leads marked as contacted.')
    mark_as_contacted.short_description = 'Mark selected as Contacted'
    
    def mark_as_qualified(self, request, queryset):
        updated = queryset.update(status='qualified')
        self.message_user(request, f'{updated} leads marked as qualified.')
    mark_as_qualified.short_description = 'Mark selected as Qualified'
    
    def mark_as_high_priority(self, request, queryset):
        updated = queryset.update(priority='high')
        self.message_user(request, f'{updated} leads marked as high priority.')
    mark_as_high_priority.short_description = 'Mark selected as High Priority'
    
    def assign_to_me(self, request, queryset):
        updated = queryset.update(
            assigned_to=request.user,
            assigned_date=timezone.now(),
            assigned_by=request.user
        )
        self.message_user(request, f'{updated} leads assigned to you.')
    assign_to_me.short_description = 'Assign selected to me'
    
    def export_selected_leads(self, request, queryset):
        # This would export to CSV - placeholder for now
        self.message_user(request, f'Export functionality coming soon for {queryset.count()} leads.')
    export_selected_leads.short_description = 'Export selected leads to CSV'

