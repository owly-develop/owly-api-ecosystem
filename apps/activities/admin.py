"""
Activity admin configuration
"""
from django.contrib import admin
from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'activity_type', 'status', 'user', 'company', 'created_at']
    list_filter = ['activity_type', 'status', 'company', 'user']
    search_fields = ['title', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']

