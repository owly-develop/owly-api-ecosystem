"""
Activity views
"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.permissions import IsTenantUser
from .models import Activity
from .serializers import ActivitySerializer


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for managing activities"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated, IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['activity_type', 'status', 'user']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'scheduled_date', 'completed_date']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Activity.objects.all()
        if hasattr(user, 'company'):
            queryset = Activity.objects.filter(company=user.company)
            # Regular users can only see their own activities
            if not user.is_manager:
                queryset = queryset.filter(user=user)
            return queryset
        return Activity.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.company,
            user=self.request.user
        )

