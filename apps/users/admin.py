"""
User admin configuration
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'company', 'role', 'status', 'is_active']
    list_filter = ['role', 'status', 'is_active', 'is_staff', 'company']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'avatar')}),
        ('Company & Role', {'fields': ('company', 'role', 'status', 'manager')}),
        ('Assignments', {'fields': ('assigned_projects', 'territories')}),
        ('Performance', {'fields': ('performance_metrics', 'sales_target')}),
        ('Settings', {'fields': ('settings', 'signature', 'calendar_url', 'social_media')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'company', 'role'),
        }),
    )

