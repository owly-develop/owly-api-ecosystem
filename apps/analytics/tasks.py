"""
Celery tasks for analytics module
"""
from celery import shared_task
from django.utils import timezone
from django.db.models import Sum, Avg, Count
from datetime import timedelta


@shared_task
def generate_weekly_sales_report():
    """
    Generar reporte de ventas de la semana
    Se ejecuta cada lunes a las 8 AM
    """
    from apps.leads.models import Lead
    from apps.quotes.models import Quote
    from apps.projects.models import Unit
    from django.core.mail import send_mail
    from django.contrib.auth import get_user_model
    
    print("📊 Generando reporte semanal...")
    
    User = get_user_model()
    week_ago = timezone.now() - timedelta(days=7)
    
    # Estadísticas
    stats = {
        'new_leads': Lead.objects.filter(created_at__gte=week_ago).count(),
        'leads_converted': Lead.objects.filter(
            converted_to_customer=True,
            conversion_date__gte=week_ago
        ).count(),
        'quotes_sent': Quote.objects.filter(sent_date__gte=week_ago).count(),
        'quotes_accepted': Quote.objects.filter(accepted_date__gte=week_ago).count(),
    }
    
    # Crear reporte
    report = f"""
REPORTE SEMANAL DE VENTAS
Semana del {week_ago.strftime('%Y-%m-%d')} al {timezone.now().strftime('%Y-%m-%d')}

📈 LEADS:
• Nuevos leads: {stats['new_leads']}
• Convertidos: {stats['leads_converted']}

💰 COTIZACIONES:
• Enviadas: {stats['quotes_sent']}
• Aceptadas: {stats['quotes_accepted']}

¡Excelente trabajo equipo!
    """
    
    # Enviar
    all_users = User.objects.filter(
        status='active',
        role__in=['admin', 'manager', 'sales']
    )
    
    emails = [u.email for u in all_users]
    
    send_mail(
        'Reporte Semanal de Ventas',
        report,
        'reports@owlycrm.com',
        emails,
        fail_silently=True
    )
    
    print("✅ Reporte semanal enviado")
    return "Weekly report sent"

