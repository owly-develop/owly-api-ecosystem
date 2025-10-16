"""
Custom permissions for multi-tenant access control
"""
from rest_framework import permissions


class IsTenantUser(permissions.BasePermission):
    """
    Permission to ensure users can only access data from their own company
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'company')
    
    def has_object_permission(self, request, view, obj):
        # Check if object has a company attribute
        if hasattr(obj, 'company'):
            return obj.company == request.user.company
        return True


class IsAdminUser(permissions.BasePermission):
    """
    Permission for admin users only
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class IsManagerOrAdmin(permissions.BasePermission):
    """
    Permission for manager or admin users
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['admin', 'manager']
        )

