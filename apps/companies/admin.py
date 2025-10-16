"""
Company admin configuration
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'slug', 'plan_badge', 'status_badge',
        'users_display', 'projects_display',
        'email', 'created_at'
    ]
    list_filter = ['plan', 'status', 'industry', 'created_at']
    search_fields = ['name', 'slug', 'email', 'legal_name', 'tax_id']
    readonly_fields = ['id', 'slug', 'created_at', 'updated_at', 'user_count', 'project_count']
    list_per_page = 50
    actions = ['activate_companies', 'suspend_companies', 'upgrade_to_professional']
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('id', 'slug'),
                ('name', 'legal_name'),
                ('tax_id', 'industry')
            )
        }),
        ('Contact Information', {
            'fields': (
                ('email', 'phone'),
                'website'
            )
        }),
        ('Address', {
            'fields': (
                'address',
                ('city', 'state'),
                ('country', 'postal_code')
            )
        }),
        ('Subscription', {
            'fields': (
                ('plan', 'status'),
                ('trial_ends_at', 'subscription_ends_at')
            )
        }),
        ('Limits', {
            'fields': (
                ('max_users', 'max_projects'),
                ('max_leads', 'max_storage_gb')
            )
        }),
        ('Branding & Settings', {
            'fields': (
                'logo',
                'primary_color',
                ('timezone', 'currency'),
                'features'
            )
        }),
        ('Stats', {
            'fields': ('user_count', 'project_count'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def plan_badge(self, obj):
        colors = {
            'free': '#6c757d',
            'starter': '#17a2b8',
            'professional': '#007bff',
            'enterprise': '#28a745'
        }
        color = colors.get(obj.plan, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_plan_display().upper()
        )
    plan_badge.short_description = 'Plan'
    plan_badge.admin_order_field = 'plan'
    
    def status_badge(self, obj):
        colors = {
            'active': '#28a745',
            'suspended': '#dc3545',
            'trial': '#ffc107',
            'cancelled': '#6c757d'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def users_display(self, obj):
        count = obj.get_user_count()
        max_users = obj.max_users
        percentage = (count / max_users * 100) if max_users > 0 else 0
        
        color = '#28a745' if percentage < 80 else '#ffc107' if percentage < 100 else '#dc3545'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}/{}</span>',
            color,
            count,
            max_users
        )
    users_display.short_description = 'Users'
    
    def projects_display(self, obj):
        count = obj.get_project_count()
        max_projects = obj.max_projects
        percentage = (count / max_projects * 100) if max_projects > 0 else 0
        
        color = '#28a745' if percentage < 80 else '#ffc107' if percentage < 100 else '#dc3545'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}/{}</span>',
            color,
            count,
            max_projects
        )
    projects_display.short_description = 'Projects'
    
    def user_count(self, obj):
        return obj.get_user_count()
    user_count.short_description = 'Total Users'
    
    def project_count(self, obj):
        return obj.get_project_count()
    project_count.short_description = 'Total Projects'
    
    def activate_companies(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} companies activated.')
    activate_companies.short_description = 'Activate selected companies'
    
    def suspend_companies(self, request, queryset):
        updated = queryset.update(status='suspended')
        self.message_user(request, f'{updated} companies suspended.')
    suspend_companies.short_description = 'Suspend selected companies'
    
    def upgrade_to_professional(self, request, queryset):
        updated = queryset.update(
            plan='professional',
            max_users=50,
            max_projects=100,
            max_leads=25000,
            max_storage_gb=100
        )
        self.message_user(request, f'{updated} companies upgraded to Professional plan.')
    upgrade_to_professional.short_description = 'Upgrade to Professional plan'

