"""
Quote admin configuration
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Quote, QuoteTemplate


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = [
        'quote_number_link', 'lead_link', 'project_link',
        'status_badge', 'total_display', 'created_by',
        'sent_date', 'created_at'
    ]
    list_filter = ['status', 'company', 'project', 'created_at', 'sent_date']
    search_fields = [
        'quote_number',
        'lead__first_name', 'lead__last_name', 'lead__email',
        'project__name', 'project__code'
    ]
    readonly_fields = [
        'id', 'quote_number', 'subtotal', 'tax_amount', 'total',
        'created_at', 'updated_at'
    ]
    date_hierarchy = 'created_at'
    list_per_page = 50
    actions = ['mark_as_sent', 'mark_as_accepted', 'export_quotes']
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('quote_number', 'company'),
                ('lead', 'project', 'unit'),
                ('status', 'created_by')
            )
        }),
        ('Pricing', {
            'fields': (
                'unit_price',
                ('discount_percentage', 'discount_amount'),
                'subtotal',
                ('tax_percentage', 'tax_amount'),
                ('total', 'currency')
            )
        }),
        ('Financing', {
            'fields': ('financing_offered', 'financing_terms'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': (
                'valid_until',
                ('sent_date', 'viewed_date'),
                ('accepted_date', 'rejected_date')
            )
        }),
        ('Additional Information', {
            'fields': ('additional_items', 'notes', 'terms_and_conditions'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def quote_number_link(self, obj):
        url = reverse('admin:quotes_quote_change', args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, obj.quote_number)
    quote_number_link.short_description = 'Quote #'
    quote_number_link.admin_order_field = 'quote_number'
    
    def lead_link(self, obj):
        url = reverse('admin:leads_lead_change', args=[obj.lead.id])
        return format_html('<a href="{}">{}</a>', url, obj.lead.full_name)
    lead_link.short_description = 'Lead'
    
    def project_link(self, obj):
        url = reverse('admin:projects_project_change', args=[obj.project.id])
        return format_html('<a href="{}">{}</a>', url, obj.project.name)
    project_link.short_description = 'Project'
    
    def status_badge(self, obj):
        colors = {
            'draft': '#6c757d',
            'sent': '#17a2b8',
            'viewed': '#007bff',
            'accepted': '#28a745',
            'rejected': '#dc3545',
            'expired': '#6c757d'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def total_display(self, obj):
        total_formatted = f"${float(obj.total):,.2f}"
        return f"{obj.currency} {total_formatted}"
    total_display.short_description = 'Total'
    total_display.admin_order_field = 'total'
    
    def mark_as_sent(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status='draft').update(
            status='sent',
            sent_date=timezone.now()
        )
        self.message_user(request, f'{updated} quotes marked as sent.')
    mark_as_sent.short_description = 'Mark selected as Sent'
    
    def mark_as_accepted(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(
            status='accepted',
            accepted_date=timezone.now()
        )
        self.message_user(request, f'{updated} quotes marked as accepted.')
    mark_as_accepted.short_description = 'Mark selected as Accepted'
    
    def export_quotes(self, request, queryset):
        self.message_user(request, f'Export functionality coming soon for {queryset.count()} quotes.')
    export_quotes.short_description = 'Export selected quotes'


@admin.register(QuoteTemplate)
class QuoteTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'is_active', 'default_validity_days', 'created_at']
    list_filter = ['is_active', 'company', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('name', 'company'),
                'description',
                'is_active'
            )
        }),
        ('Template Content', {
            'fields': ('content',),
            'classes': ('wide',)
        }),
        ('Default Settings', {
            'fields': (
                'default_terms',
                'default_validity_days'
            )
        }),
        ('Metadata', {
            'fields': ('metadata', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

