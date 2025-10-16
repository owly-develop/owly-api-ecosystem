"""
Analytics views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta
from apps.leads.models import Lead
from apps.quotes.models import Quote
from apps.projects.models import Project
from apps.activities.models import Activity


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics for the current user's company
    """
    user = request.user
    
    if not hasattr(user, 'company') or not user.company:
        return Response({'error': 'No company associated with user'}, status=400)
    
    company = user.company
    
    # Date ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Lead stats
    leads = Lead.objects.filter(company=company, is_deleted=False)
    lead_stats = {
        'total': leads.count(),
        'new': leads.filter(status='new').count(),
        'qualified': leads.filter(status='qualified').count(),
        'converted': leads.filter(converted_to_customer=True).count(),
        'this_week': leads.filter(created_at__date__gte=week_ago).count(),
        'avg_score': leads.aggregate(avg=Avg('lead_score'))['avg'] or 0,
    }
    
    # Quote stats
    quotes = Quote.objects.filter(company=company)
    quote_stats = {
        'total': quotes.count(),
        'sent': quotes.filter(status='sent').count(),
        'accepted': quotes.filter(status='accepted').count(),
        'total_value': quotes.aggregate(total=Sum('total'))['total'] or 0,
        'this_month': quotes.filter(created_at__date__gte=month_ago).count(),
    }
    
    # Project stats
    projects = Project.objects.filter(company=company, is_deleted=False)
    project_stats = {
        'total': projects.count(),
        'active': projects.filter(status='active').count(),
        'total_units': projects.aggregate(total=Sum('total_units'))['total'] or 0,
        'available_units': projects.aggregate(total=Sum('available_units'))['total'] or 0,
    }
    
    # Activity stats
    activities = Activity.objects.filter(company=company)
    activity_stats = {
        'total': activities.count(),
        'this_week': activities.filter(created_at__date__gte=week_ago).count(),
        'by_type': dict(
            activities.values('activity_type').annotate(count=Count('id')).values_list('activity_type', 'count')
        ),
    }
    
    return Response({
        'leads': lead_stats,
        'quotes': quote_stats,
        'projects': project_stats,
        'activities': activity_stats,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lead_analytics(request):
    """
    Get detailed lead analytics
    """
    user = request.user
    
    if not hasattr(user, 'company') or not user.company:
        return Response({'error': 'No company associated with user'}, status=400)
    
    company = user.company
    leads = Lead.objects.filter(company=company, is_deleted=False)
    
    # By status
    by_status = dict(
        leads.values('status').annotate(count=Count('id')).values_list('status', 'count')
    )
    
    # By source
    by_source = dict(
        leads.values('source').annotate(count=Count('id')).values_list('source', 'count')
    )
    
    # By priority
    by_priority = dict(
        leads.values('priority').annotate(count=Count('id')).values_list('priority', 'count')
    )
    
    # Conversion rate
    total = leads.count()
    converted = leads.filter(converted_to_customer=True).count()
    conversion_rate = (converted / total * 100) if total > 0 else 0
    
    return Response({
        'by_status': by_status,
        'by_source': by_source,
        'by_priority': by_priority,
        'conversion_rate': round(conversion_rate, 2),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sales_funnel(request):
    """
    Get sales funnel data
    """
    user = request.user
    
    if not hasattr(user, 'company') or not user.company:
        return Response({'error': 'No company associated with user'}, status=400)
    
    company = user.company
    leads = Lead.objects.filter(company=company, is_deleted=False)
    
    funnel = [
        {'stage': 'New', 'count': leads.filter(status='new').count()},
        {'stage': 'Contacted', 'count': leads.filter(status='contacted').count()},
        {'stage': 'Qualified', 'count': leads.filter(status='qualified').count()},
        {'stage': 'Proposal', 'count': leads.filter(status='proposal').count()},
        {'stage': 'Negotiation', 'count': leads.filter(status='negotiation').count()},
        {'stage': 'Closed Won', 'count': leads.filter(status='closed_won').count()},
    ]
    
    return Response(funnel)

