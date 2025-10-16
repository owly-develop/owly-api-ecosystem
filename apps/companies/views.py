"""
Company views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.core.permissions import IsAdminUser, IsManagerOrAdmin
from .models import Company
from .serializers import (
    CompanySerializer,
    CompanyCreateSerializer,
    CompanyUpdateSerializer
)


class CompanyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing companies
    """
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CompanyCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CompanyUpdateSerializer
        return CompanySerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions
        """
        user = self.request.user
        if user.is_superuser:
            return Company.objects.all()
        elif hasattr(user, 'company'):
            return Company.objects.filter(id=user.company.id)
        return Company.objects.none()
    
    @action(detail=True, methods=['get'], permission_classes=[IsManagerOrAdmin])
    def stats(self, request, pk=None):
        """
        Get company statistics
        """
        company = self.get_object()
        stats = {
            'users': company.get_user_count(),
            'projects': company.get_project_count(),
            'max_users': company.max_users,
            'max_projects': company.max_projects,
            'plan': company.plan,
            'status': company.status,
            'can_add_user': company.can_add_user(),
            'can_add_project': company.can_add_project(),
        }
        return Response(stats)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def upgrade_plan(self, request, pk=None):
        """
        Upgrade company plan
        """
        company = self.get_object()
        new_plan = request.data.get('plan')
        
        if new_plan not in dict(Company.PLAN_CHOICES):
            return Response(
                {'error': 'Invalid plan'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        company.plan = new_plan
        # Update limits based on plan
        plan_limits = {
            'free': {'users': 5, 'projects': 10, 'leads': 1000, 'storage': 5},
            'starter': {'users': 10, 'projects': 25, 'leads': 5000, 'storage': 20},
            'professional': {'users': 50, 'projects': 100, 'leads': 25000, 'storage': 100},
            'enterprise': {'users': 999, 'projects': 999, 'leads': 999999, 'storage': 500},
        }
        limits = plan_limits.get(new_plan, plan_limits['free'])
        company.max_users = limits['users']
        company.max_projects = limits['projects']
        company.max_leads = limits['leads']
        company.max_storage_gb = limits['storage']
        company.save()
        
        serializer = self.get_serializer(company)
        return Response(serializer.data)

