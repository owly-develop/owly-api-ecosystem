"""
User views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from apps.core.permissions import IsManagerOrAdmin, IsTenantUser
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsTenantUser]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action == 'profile':
            return UserProfileSerializer
        return UserSerializer
    
    def get_queryset(self):
        """
        Filter users based on company and permissions
        """
        user = self.request.user
        queryset = User.objects.all()
        
        if user.is_superuser:
            return queryset
        
        # Filter by company
        if hasattr(user, 'company') and user.company:
            queryset = queryset.filter(company=user.company)
        else:
            return User.objects.none()
        
        # Managers can see their team
        if user.is_manager:
            return queryset
        
        # Regular users can only see themselves
        return queryset.filter(id=user.id)
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def profile(self, request):
        """
        Get or update current user profile
        """
        user = request.user
        
        if request.method == 'GET':
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """
        Change user password
        """
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get('old_password')):
                return Response(
                    {'old_password': ['Wrong password']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password
            user.set_password(serializer.data.get('new_password'))
            user.save()
            
            return Response({'message': 'Password changed successfully'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], permission_classes=[IsManagerOrAdmin])
    def performance(self, request, pk=None):
        """
        Get user performance metrics
        """
        user = self.get_object()
        # This would be calculated by a celery task periodically
        return Response(user.performance_metrics)
    
    @action(detail=True, methods=['post'], permission_classes=[IsManagerOrAdmin])
    def deactivate(self, request, pk=None):
        """
        Deactivate a user
        """
        user = self.get_object()
        user.status = 'inactive'
        user.is_active = False
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsManagerOrAdmin])
    def activate(self, request, pk=None):
        """
        Activate a user
        """
        user = self.get_object()
        user.status = 'active'
        user.is_active = True
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

