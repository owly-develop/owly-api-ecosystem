"""
Custom exception handlers
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'error': True,
            'message': str(exc),
            'status_code': response.status_code,
            'details': response.data
        }
        response.data = custom_response_data
    
    return response


class TenantAccessDenied(Exception):
    """
    Raised when a user tries to access data from another tenant
    """
    pass


class ResourceNotFound(Exception):
    """
    Raised when a requested resource is not found
    """
    pass

