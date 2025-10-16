"""
Core views and health check
"""
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.db import connection
from django.core.cache import cache
from apps.core.permissions import IsManagerOrAdmin
from .models import ScheduledTask
from .serializers import (
    ScheduledTaskSerializer,
    ScheduledTaskCreateSerializer,
    TaskTemplateSerializer
)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for monitoring
    """
    health_status = {
        'status': 'healthy',
        'database': 'unknown',
        'cache': 'unknown',
    }
    
    # Check database
    try:
        connection.ensure_connection()
        health_status['database'] = 'connected'
    except Exception as e:
        health_status['database'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # Check cache
    try:
        cache.set('health_check', 'ok', 10)
        if cache.get('health_check') == 'ok':
            health_status['cache'] = 'connected'
        else:
            health_status['cache'] = 'error'
            health_status['status'] = 'unhealthy'
    except Exception as e:
        health_status['cache'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    status_code = status.HTTP_200_OK if health_status['status'] == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return Response(health_status, status=status_code)


class ScheduledTaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing scheduled tasks
    User-friendly API for non-technical users
    """
    queryset = ScheduledTask.objects.all()
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ScheduledTaskCreateSerializer
        return ScheduledTaskSerializer
    
    def get_queryset(self):
        """Filter by company"""
        user = self.request.user
        if user.is_superuser:
            return ScheduledTask.objects.all()
        if hasattr(user, 'company'):
            return ScheduledTask.objects.filter(company=user.company)
        return ScheduledTask.objects.none()
    
    def perform_create(self, serializer):
        """Set company and created_by"""
        serializer.save(
            company=self.request.user.company,
            created_by=self.request.user
        )
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a task"""
        task = self.get_object()
        task.is_active = True
        task.save()
        
        serializer = self.get_serializer(task)
        return Response({
            'message': f'Tarea "{task.name}" activada',
            'task': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a task"""
        task = self.get_object()
        task.is_active = False
        task.save()
        
        serializer = self.get_serializer(task)
        return Response({
            'message': f'Tarea "{task.name}" pausada',
            'task': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def run_now(self, request, pk=None):
        """Execute task immediately"""
        task = self.get_object()
        
        try:
            from celery import current_app
            result = current_app.send_task(task.task_name)
            
            return Response({
                'message': f'Tarea "{task.name}" ejecutada',
                'task_id': result.id,
                'status': 'sent'
            })
        except Exception as e:
            return Response({
                'error': f'Error ejecutando tarea: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def templates(self, request):
        """Get pre-configured task templates"""
        templates = [
            {
                'id': 'followup-reminders',
                'name': 'Recordatorios de Follow-ups',
                'description': 'Envía emails a vendedores recordándoles sus follow-ups del día',
                'category': 'followups',
                'task_name': 'apps.leads.tasks.send_followup_reminders',
                'recommended_frequency': 'daily',
                'recommended_hour': 8,
                'why_useful': 'Los vendedores nunca olvidan llamar a sus clientes'
            },
            {
                'id': 'calculate-scores',
                'name': 'Calcular Scores de Leads',
                'description': 'Recalcula automáticamente el score de todos los leads activos',
                'category': 'leads',
                'task_name': 'apps.leads.tasks.calculate_lead_scores',
                'recommended_frequency': 'daily',
                'recommended_hour': 2,
                'why_useful': 'Scores siempre actualizados para priorizar mejor'
            },
        ]
        
        serializer = TaskTemplateSerializer(templates, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get tasks grouped by category"""
        queryset = self.get_queryset()
        
        categories = {}
        for choice in ScheduledTask.CATEGORY_CHOICES:
            category_code, category_name = choice
            tasks = queryset.filter(category=category_code)
            categories[category_code] = {
                'name': category_name,
                'count': tasks.count(),
                'active_count': tasks.filter(is_active=True).count(),
                'tasks': ScheduledTaskSerializer(tasks, many=True).data
            }
        
        return Response(categories)
