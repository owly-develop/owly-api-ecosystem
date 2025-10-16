"""
Celery tasks for projects module
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta


@shared_task
def release_expired_options():
    """
    Liberar unidades con opciones expiradas
    Se ejecuta cada hora
    """
    from .models import Unit
    
    print("🔓 Liberando opciones expiradas...")
    
    now = timezone.now()
    
    # Buscar units con option expirado
    expired_options = Unit.objects.filter(
        status='option',
        option_expires_at__lte=now
    )
    
    released_count = 0
    
    for unit in expired_options:
        # Guardar en historial
        if not hasattr(unit, 'operation_history') or unit.operation_history is None:
            unit.operation_history = []
        
        unit.operation_history.append({
            'date': now.isoformat(),
            'action': 'option_expired_auto_released',
            'system': True,
        })
        
        # Liberar
        unit.status = 'available'
        unit.option_holder = None
        unit.option_expires_at = None
        unit.save()
        
        released_count += 1
    
    print(f"✅ Liberadas {released_count} unidades")
    
    if released_count > 0:
        from django.core.mail import send_mail
        send_mail(
            f'{released_count} Opciones Expiradas',
            f'Se liberaron {released_count} unidades.',
            'system@owlycrm.com',
            ['sales@owlycrm.com'],
            fail_silently=True
        )
    
    return f"Released {released_count} units"


@shared_task
def detect_overdue_payments():
    """
    Detectar unidades con pagos vencidos
    Se ejecuta cada día a las 9 AM
    """
    from .models import Unit
    from django.core.mail import send_mail
    
    print("💰 Detectando pagos vencidos...")
    
    # Units con pagos vencidos
    overdue_units = Unit.objects.filter(
        payment_status='overdue',
        status__in=['in_payment', 'contract_signed']
    ).select_related('project')
    
    if not overdue_units.exists():
        print("✅ No hay pagos vencidos")
        return "No overdue payments"
    
    report = f"ALERTA: {overdue_units.count()} unidades con pagos vencidos\n\n"
    
    for unit in overdue_units[:20]:
        report += f"Proyecto: {unit.project.name}\n"
        report += f"Unidad: {unit.unit_number}\n"
        if hasattr(unit, 'customer_first_name'):
            report += f"Cliente: {unit.customer_first_name} {unit.customer_last_name}\n"
        report += f"---\n"
    
    send_mail(
        'ALERTA: Pagos Vencidos',
        report,
        'finance@owlycrm.com',
        ['finance@owlycrm.com', 'manager@owlycrm.com'],
        fail_silently=True
    )
    
    print(f"⚠️ {overdue_units.count()} pagos vencidos")
    return f"Found {overdue_units.count()} overdue payments"

