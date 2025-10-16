"""
Middleware for multi-tenant support
"""
from django.utils.deprecation import MiddlewareMixin
from apps.companies.models import Company


class TenantMiddleware(MiddlewareMixin):
    """
    Middleware to automatically set the current tenant based on the authenticated user
    """
    def process_request(self, request):
        if request.user.is_authenticated:
            # Set the current company from the user's profile
            if hasattr(request.user, 'company'):
                request.company = request.user.company
            else:
                request.company = None
        else:
            request.company = None

