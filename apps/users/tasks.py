"""
Celery tasks for users module
"""
from celery import shared_task
from django.utils import timezone
from django.db.models import Sum, Avg, Count
from datetime import timedelta


@shared_task
def calculate_user_performance():
    """
    Calcular métricas de performance de vendedores
    Se ejecuta cada domingo a las 11 PM
    """
    from django.contrib.auth import get_user_model
    from apps.leads.models import Lead
    from apps.quotes.models import Quote
    
    print("📊 Calculando performance de vendedores...")
    
    User = get_user_model()
    week_ago = timezone.now() - timedelta(days=7)
    
    sales_users = User.objects.filter(
        role='sales',
        status='active'
    )
    
    for user in sales_users:
        user_leads = Lead.objects.filter(assigned_to=user)
        
        # Métricas de la semana
        leads_assigned = user_leads.filter(assigned_date__gte=week_ago).count()
        leads_contacted = user_leads.filter(last_contact_date__gte=week_ago).count()
        leads_converted = user_leads.filter(
            converted_to_customer=True,
            conversion_date__gte=week_ago
        ).count()
        
        # Cotizaciones
        quotes = Quote.objects.filter(created_by=user)
        quotes_sent = quotes.filter(sent_date__gte=week_ago).count()
        quotes_accepted = quotes.filter(accepted_date__gte=week_ago).count()
        
        # Revenue
        revenue = quotes.filter(
            status='accepted',
            accepted_date__gte=week_ago
        ).aggregate(total=Sum('total'))['total'] or 0
        
        # Calcular tasas
        conversion_rate = (leads_converted / leads_assigned * 100) if leads_assigned > 0 else 0
        quote_acceptance_rate = (quotes_accepted / quotes_sent * 100) if quotes_sent > 0 else 0
        
        # Guardar
        user.performance_metrics = {
            'period': 'week',
            'week_ending': timezone.now().date().isoformat(),
            'leads_assigned': leads_assigned,
            'leads_contacted': leads_contacted,
            'leads_converted': leads_converted,
            'conversion_rate': round(conversion_rate, 2),
            'quotes_generated': quotes_sent,
            'quotes_accepted': quotes_accepted,
            'quote_acceptance_rate': round(quote_acceptance_rate, 2),
            'revenue': float(revenue),
        }
        user.save(update_fields=['performance_metrics'])
    
    print(f"✅ Performance calculado para {sales_users.count()} vendedores")
    return f"Calculated performance for {sales_users.count()} users"

