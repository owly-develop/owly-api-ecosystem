"""
Lead views
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q, Count, Avg, Max, Min
from datetime import timedelta
from apps.core.permissions import IsTenantUser, IsManagerOrAdmin
from .models import Lead
from .serializers import LeadSerializer, LeadListSerializer, LeadCreateSerializer
from .filters import LeadFilter


class LeadViewSet(viewsets.ModelViewSet):
    """ViewSet for managing leads"""
    queryset = Lead.objects.all()
    permission_classes = [IsAuthenticated, IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = LeadFilter
    search_fields = ['lead_number', 'first_name', 'last_name', 'email', 'phone', 'company_name']
    ordering_fields = ['created_at', 'lead_score', 'ai_close_probability', 'last_contact_date', 'updated_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return LeadListSerializer
        elif self.action == 'create':
            return LeadCreateSerializer
        return LeadSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.filter(is_deleted=False)
        
        if user.is_superuser:
            return queryset
        
        if hasattr(user, 'company'):
            queryset = queryset.filter(company=user.company)
        else:
            return Lead.objects.none()
        
        # Filter by assigned user if not admin/manager
        if not user.is_manager:
            queryset = queryset.filter(assigned_to=user)
        
        return queryset
    
    def perform_create(self, serializer):
        lead = serializer.save(company=self.request.user.company)
        # Auto-assign if not assigned
        if not lead.assigned_to:
            lead.assigned_to = self.request.user
            lead.assigned_date = timezone.now()
            lead.assigned_by = self.request.user
            lead.save()
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """Assign lead to a user"""
        lead = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            from apps.users.models import User
            user = User.objects.get(id=user_id, company=request.user.company)
            lead.assigned_to = user
            lead.assigned_date = timezone.now()
            lead.assigned_by = request.user
            lead.save()
            
            serializer = self.get_serializer(lead)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Change lead status"""
        lead = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Lead.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        lead.status = new_status
        lead.save()
        
        serializer = self.get_serializer(lead)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_score(self, request, pk=None):
        """Update lead score"""
        lead = self.get_object()
        score = request.data.get('score', 0)
        
        if not isinstance(score, int) or score < 0 or score > 100:
            return Response(
                {'error': 'Score must be between 0 and 100'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        lead.lead_score = score
        lead.save()
        
        serializer = self.get_serializer(lead)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get lead statistics"""
        queryset = self.get_queryset()
        
        stats = {
            'total': queryset.count(),
            'by_status': {},
            'by_priority': {},
            'by_source': {},
            'avg_lead_score': 0,
            'avg_close_probability': 0,
        }
        
        # Count by status
        for status_code, _ in Lead.STATUS_CHOICES:
            stats['by_status'][status_code] = queryset.filter(status=status_code).count()
        
        # Count by priority
        for priority_code, _ in Lead.PRIORITY_CHOICES:
            stats['by_priority'][priority_code] = queryset.filter(priority=priority_code).count()
        
        # Count by source
        for source_code, _ in Lead.SOURCE_CHOICES:
            stats['by_source'][source_code] = queryset.filter(source=source_code).count()
        
        # Calculate averages
        if queryset.count() > 0:
            averages = queryset.aggregate(
                avg_score=Avg('lead_score'),
                avg_probability=Avg('ai_close_probability')
            )
            stats['avg_lead_score'] = round(averages['avg_score'] or 0, 2)
            stats['avg_close_probability'] = round(averages['avg_probability'] or 0, 2)
        
        return Response(stats)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsManagerOrAdmin])
    def bulk_assign(self, request):
        """Bulk assign leads to users"""
        lead_ids = request.data.get('lead_ids', [])
        user_id = request.data.get('user_id')
        
        if not lead_ids or not user_id:
            return Response(
                {'error': 'lead_ids and user_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from apps.users.models import User
            user = User.objects.get(id=user_id, company=request.user.company)
            
            leads = self.get_queryset().filter(id__in=lead_ids)
            updated_count = leads.update(
                assigned_to=user,
                assigned_date=timezone.now(),
                assigned_by=request.user
            )
            
            return Response({
                'message': f'{updated_count} leads assigned successfully',
                'updated_count': updated_count
            })
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsManagerOrAdmin])
    def bulk_status_change(self, request):
        """Bulk change status of leads"""
        lead_ids = request.data.get('lead_ids', [])
        new_status = request.data.get('status')
        
        if not lead_ids or not new_status:
            return Response(
                {'error': 'lead_ids and status are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_status not in dict(Lead.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        leads = self.get_queryset().filter(id__in=lead_ids)
        updated_count = leads.update(status=new_status, updated_at=timezone.now())
        
        return Response({
            'message': f'{updated_count} leads updated successfully',
            'updated_count': updated_count
        })
    
    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        """Get lead timeline/history"""
        lead = self.get_object()
        
        # Get activities related to this lead
        from apps.activities.models import Activity
        from django.contrib.contenttypes.models import ContentType
        
        content_type = ContentType.objects.get_for_model(Lead)
        activities = Activity.objects.filter(
            company=request.user.company,
            content_type=content_type,
            object_id=lead.id
        ).order_by('-created_at')[:50]
        
        from apps.activities.serializers import ActivitySerializer
        timeline = ActivitySerializer(activities, many=True).data
        
        return Response(timeline)
    
    @action(detail=False, methods=['get'])
    def upcoming_followups(self, request):
        """Get leads with upcoming follow-ups"""
        today = timezone.now()
        next_week = today + timedelta(days=7)
        
        leads = self.get_queryset().filter(
            next_follow_up_date__gte=today,
            next_follow_up_date__lte=next_week
        ).order_by('next_follow_up_date')
        
        serializer = self.get_serializer(leads, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue_followups(self, request):
        """Get leads with overdue follow-ups"""
        today = timezone.now()
        
        leads = self.get_queryset().filter(
            next_follow_up_date__lt=today,
            status__in=['new', 'contacted', 'qualified', 'proposal', 'negotiation']
        ).order_by('next_follow_up_date')
        
        serializer = self.get_serializer(leads, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def hot_leads(self, request):
        """Get hot leads (high score + high priority)"""
        leads = self.get_queryset().filter(
            Q(priority__in=['high', 'urgent']) | Q(lead_score__gte=70)
        ).exclude(
            status__in=['closed_won', 'closed_lost']
        ).order_by('-lead_score', '-ai_close_probability')
        
        serializer = self.get_serializer(leads, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def duplicates(self, request):
        """Find potential duplicate leads"""
        queryset = self.get_queryset()
        
        # Group by email
        email_duplicates = queryset.values('email').annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        # Group by phone
        phone_duplicates = queryset.values('phone').annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        duplicate_leads = []
        
        # Get leads with duplicate emails
        for item in email_duplicates:
            leads = queryset.filter(email=item['email'])
            duplicate_leads.append({
                'type': 'email',
                'value': item['email'],
                'count': item['count'],
                'leads': LeadListSerializer(leads, many=True).data
            })
        
        # Get leads with duplicate phones
        for item in phone_duplicates:
            leads = queryset.filter(phone=item['phone'])
            duplicate_leads.append({
                'type': 'phone',
                'value': item['phone'],
                'count': item['count'],
                'leads': LeadListSerializer(leads, many=True).data
            })
        
        return Response(duplicate_leads)
    
    @action(detail=True, methods=['post'])
    def add_note(self, request, pk=None):
        """Add a note to lead"""
        lead = self.get_object()
        note_text = request.data.get('note', '')
        
        if not note_text:
            return Response(
                {'error': 'Note text is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add timestamp and user to note
        timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        user_name = request.user.full_name
        
        new_note = f"[{timestamp}] {user_name}: {note_text}"
        
        if lead.notes:
            lead.notes += f"\n\n{new_note}"
        else:
            lead.notes = new_note
        
        lead.save()
        
        serializer = self.get_serializer(lead)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsManagerOrAdmin])
    def performance_by_source(self, request):
        """Get lead performance metrics by source"""
        queryset = self.get_queryset()
        
        performance = []
        for source_code, source_name in Lead.SOURCE_CHOICES:
            source_leads = queryset.filter(source=source_code)
            total = source_leads.count()
            
            if total > 0:
                converted = source_leads.filter(converted_to_customer=True).count()
                conversion_rate = (converted / total) * 100
                avg_score = source_leads.aggregate(avg=Avg('lead_score'))['avg'] or 0
                
                performance.append({
                    'source': source_code,
                    'source_name': source_name,
                    'total_leads': total,
                    'converted': converted,
                    'conversion_rate': round(conversion_rate, 2),
                    'avg_lead_score': round(avg_score, 2)
                })
        
        return Response(sorted(performance, key=lambda x: x['total_leads'], reverse=True))

