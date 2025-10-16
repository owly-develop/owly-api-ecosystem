"""
Quote views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from apps.core.permissions import IsTenantUser
from .models import Quote, QuoteTemplate
from .serializers import QuoteSerializer, QuoteTemplateSerializer


class QuoteViewSet(viewsets.ModelViewSet):
    """ViewSet for managing quotes"""
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    permission_classes = [IsAuthenticated, IsTenantUser]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Quote.objects.all()
        if hasattr(user, 'company'):
            return Quote.objects.filter(company=user.company)
        return Quote.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.company,
            created_by=self.request.user
        )
    
    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """Send quote to lead"""
        quote = self.get_object()
        
        if quote.status == 'draft':
            quote.status = 'sent'
            quote.sent_date = timezone.now()
            quote.save()
            
            # TODO: Send email to lead
            
            serializer = self.get_serializer(quote)
            return Response(serializer.data)
        
        return Response(
            {'error': 'Quote can only be sent from draft status'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def mark_viewed(self, request, pk=None):
        """Mark quote as viewed"""
        quote = self.get_object()
        
        if quote.status == 'sent' and not quote.viewed_date:
            quote.status = 'viewed'
            quote.viewed_date = timezone.now()
            quote.save()
        
        serializer = self.get_serializer(quote)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept quote"""
        quote = self.get_object()
        
        quote.status = 'accepted'
        quote.accepted_date = timezone.now()
        quote.save()
        
        serializer = self.get_serializer(quote)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject quote"""
        quote = self.get_object()
        
        quote.status = 'rejected'
        quote.rejected_date = timezone.now()
        quote.save()
        
        serializer = self.get_serializer(quote)
        return Response(serializer.data)


class QuoteTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for managing quote templates"""
    queryset = QuoteTemplate.objects.all()
    serializer_class = QuoteTemplateSerializer
    permission_classes = [IsAuthenticated, IsTenantUser]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return QuoteTemplate.objects.all()
        if hasattr(user, 'company'):
            return QuoteTemplate.objects.filter(company=user.company, is_active=True)
        return QuoteTemplate.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)

