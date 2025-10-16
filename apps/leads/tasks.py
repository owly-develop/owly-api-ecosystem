"""
Celery tasks for leads module
"""
from celery import shared_task
from django.utils import timezone
from django.db.models import Avg
from datetime import timedelta


@shared_task
def calculate_lead_scores():
    """
    Recalcular scores de todos los leads activos
    Se ejecuta diariamente a las 2 AM
    """
    from .models import Lead
    
    print("🔄 Iniciando cálculo de lead scores...")
    
    # Obtener leads activos
    active_leads = Lead.objects.filter(
        status__in=['new', 'contacted', 'qualified', 'proposal', 'negotiation'],
        is_deleted=False
    )
    
    updated_count = 0
    
    for lead in active_leads:
        old_score = lead.lead_score
        score = 0
        
        # Factor 1: Prioridad (0-20 puntos)
        priority_scores = {'low': 5, 'medium': 10, 'high': 15, 'urgent': 20}
        score += priority_scores.get(lead.priority, 5)
        
        # Factor 2: Fuente (0-15 puntos)
        source_scores = {
            'referral': 15, 'website': 12, 'facebook': 8,
            'instagram': 8, 'cold_call': 5
        }
        score += source_scores.get(lead.source, 5)
        
        # Factor 3: Engagement (0-25 puntos)
        if lead.interaction_count:
            score += min(lead.interaction_count * 3, 25)
        
        # Factor 4: Budget match (0-20 puntos)
        if lead.budget_min and lead.budget_max:
            if lead.budget_min >= 300000:
                score += 20
            elif lead.budget_min >= 200000:
                score += 15
            else:
                score += 10
        
        # Factor 5: Recency (0-20 puntos)
        if lead.last_contact_date:
            days_since = (timezone.now() - lead.last_contact_date).days
            if days_since <= 7:
                score += 20
            elif days_since <= 30:
                score += 10
            else:
                score += 5
        
        lead.lead_score = min(score, 100)
        
        if old_score != lead.lead_score:
            lead.save(update_fields=['lead_score'])
            updated_count += 1
    
    print(f"✅ Actualizado: {updated_count} leads")
    return f"Updated {updated_count} lead scores"


@shared_task
def send_followup_reminders():
    """
    Enviar recordatorios de follow-ups del día
    Se ejecuta cada mañana a las 8 AM
    """
    from .models import Lead
    from django.core.mail import send_mail
    
    print("📧 Enviando recordatorios de follow-up...")
    
    today = timezone.now().date()
    
    leads_today = Lead.objects.filter(
        next_follow_up_date__date=today,
        status__in=['contacted', 'qualified', 'proposal', 'negotiation'],
        is_deleted=False
    ).select_related('assigned_to')
    
    # Agrupar por vendedor
    reminders_by_user = {}
    for lead in leads_today:
        if lead.assigned_to:
            user_email = lead.assigned_to.email
            if user_email not in reminders_by_user:
                reminders_by_user[user_email] = []
            reminders_by_user[user_email].append(lead)
    
    sent_count = 0
    
    for user_email, leads_list in reminders_by_user.items():
        lead_names = [f"{l.full_name} ({l.lead_number})" for l in leads_list]
        
        subject = f"Follow-ups de Hoy - {len(leads_list)} leads"
        message = f"""
Buenos días!

Tienes {len(leads_list)} follow-ups programados para hoy:

{chr(10).join(f"• {name}" for name in lead_names)}

¡Éxito en tus llamadas!

- OWLY CRM
        """
        
        send_mail(
            subject,
            message,
            'noreply@owlycrm.com',
            [user_email],
            fail_silently=True
        )
        sent_count += 1
    
    print(f"✅ Enviados {sent_count} recordatorios")
    return f"Sent {sent_count} reminder emails"


@shared_task
def detect_overdue_followups():
    """
    Identificar leads con follow-ups vencidos
    Se ejecuta cada día a las 9 AM
    """
    from .models import Lead
    from django.core.mail import send_mail
    from django.contrib.auth import get_user_model
    
    print("🔍 Detectando follow-ups vencidos...")
    
    today = timezone.now().date()
    User = get_user_model()
    
    overdue_leads = Lead.objects.filter(
        next_follow_up_date__lt=today,
        status__in=['new', 'contacted', 'qualified', 'proposal', 'negotiation'],
        is_deleted=False
    ).select_related('assigned_to')
    
    managers = User.objects.filter(
        role__in=['admin', 'manager'],
        status='active'
    )
    
    if overdue_leads.exists():
        report = f"ALERTA: {overdue_leads.count()} leads con follow-ups vencidos\n\n"
        
        for lead in overdue_leads[:10]:
            days_overdue = (today - lead.next_follow_up_date).days
            report += f"• {lead.full_name} - {days_overdue} días vencido\n"
        
        manager_emails = [m.email for m in managers]
        
        send_mail(
            'ALERTA: Follow-ups Vencidos',
            report,
            'alerts@owlycrm.com',
            manager_emails,
            fail_silently=True
        )
    
    print(f"⚠️ Encontrados {overdue_leads.count()} follow-ups vencidos")
    return f"Found {overdue_leads.count()} overdue follow-ups"


@shared_task
def calculate_ai_close_probability():
    """
    Calcular probabilidad de cierre usando algoritmo
    Se ejecuta cada noche a las 3 AM
    """
    from .models import Lead
    
    print("🤖 Calculando probabilidades de cierre...")
    
    qualified_leads = Lead.objects.filter(
        status__in=['qualified', 'proposal', 'negotiation'],
        is_deleted=False
    )
    
    updated_count = 0
    
    for lead in qualified_leads:
        probability = 0
        
        # Score base
        probability += (lead.lead_score * 0.4)
        
        # Engagement
        if lead.interaction_count:
            probability += min(lead.interaction_count * 2, 20)
        
        # Budget
        if lead.budget_min and lead.budget_max:
            probability += 15
        
        # Recency
        if lead.last_contact_date:
            days_since = (timezone.now() - lead.last_contact_date).days
            if days_since <= 7:
                probability += 15
            elif days_since <= 14:
                probability += 10
        
        # Status
        status_bonus = {'negotiation': 10, 'proposal': 7, 'qualified': 5}
        probability += status_bonus.get(lead.status, 0)
        
        lead.ai_close_probability = int(min(probability, 100))
        lead.save(update_fields=['ai_close_probability'])
        updated_count += 1
    
    print(f"✅ Actualizado: {updated_count} leads")
    return f"Updated {updated_count} leads"

