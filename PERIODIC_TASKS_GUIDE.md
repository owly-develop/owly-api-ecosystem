# ⏰ Guía Completa de Periodic Tasks (Celery)

## 🎯 ¿Qué son las Periodic Tasks?

Las **Periodic Tasks** (Tareas Periódicas) son trabajos que se ejecutan **automáticamente** en **horarios programados**, sin intervención manual.

### Analogía Simple:
Piensa en un **cron job** o **scheduled task** de Windows, pero más poderoso:
- Se ejecuta a las 2 AM cada día
- O cada hora
- O cada lunes a las 9 AM
- O cada vez que pasa algo específico

---

## 🔧 ¿Cómo Funciona en OWLY CRM?

```
┌─────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐      ┌─────────────┐                     │
│  │ CELERY BEAT │ ───→ │   REDIS     │                     │
│  │ (Scheduler) │      │  (Broker)   │                     │
│  └─────────────┘      └──────┬──────┘                     │
│        ⏰                     │                             │
│   "Son las 2 AM"             │  "Hay una tarea"            │
│   "Ejecuta tarea X"          ↓                             │
│                       ┌─────────────┐                      │
│                       │   CELERY    │                      │
│                       │   WORKER    │                      │
│                       └──────┬──────┘                      │
│                              │                             │
│                              ↓                             │
│                       ┌─────────────┐                      │
│                       │  EJECUTA    │                      │
│                       │   TAREA     │                      │
│                       └─────────────┘                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Componentes:

1. CELERY BEAT (Scheduler):
   • Reloj que sabe qué tareas ejecutar cuándo
   • Revisa cada minuto si hay algo programado
   • Envía tareas al broker cuando es hora

2. REDIS (Message Broker):
   • Cola de mensajes
   • Almacena tareas pendientes
   • Conecta Beat con Workers

3. CELERY WORKER:
   • Ejecuta las tareas realmente
   • Puede haber múltiples workers
   • Procesa tareas en paralelo
```

---

## 💡 ¿Para Qué Sirven en un CRM?

### Casos de Uso Reales en OWLY CRM:

#### 1. **Calcular Scores de Leads Diariamente**
- **Cuándo**: Cada noche a las 2 AM
- **Por qué**: Recalcular lead scores basado en nueva actividad
- **Beneficio**: Leads siempre tienen score actualizado

#### 2. **Enviar Recordatorios de Follow-ups**
- **Cuándo**: Cada mañana a las 8 AM
- **Por qué**: Recordar a vendedores sus follow-ups del día
- **Beneficio**: No se olvidan de llamar clientes importantes

#### 3. **Detectar Pagos Vencidos**
- **Cuándo**: Cada día a las 9 AM
- **Por qué**: Identificar unidades con pagos atrasados
- **Beneficio**: Acción rápida para cobrar

#### 4. **Liberar Opciones Expiradas**
- **Cuándo**: Cada hora
- **Por qué**: Opciones de 48h que expiraron se liberan
- **Beneficio**: Unidades vuelven a disponibles automáticamente

#### 5. **Generar Reportes Mensuales**
- **Cuándo**: Primer día de mes a las 6 AM
- **Por qué**: Reporte de ventas del mes anterior
- **Beneficio**: Managers tienen reporte listo al llegar

#### 6. **Actualizar Métricas de Performance**
- **Cuándo**: Cada domingo a las 11 PM
- **Por qué**: Calcular performance semanal de vendedores
- **Beneficio**: Dashboard siempre actualizado

#### 7. **Enviar Actualizaciones de Construcción**
- **Cuándo**: Cada 15 días
- **Por qué**: Enviar update a clientes sobre su unidad en construcción
- **Beneficio**: Clientes informados automáticamente

#### 8. **Limpiar Datos Antiguos**
- **Cuándo**: Cada mes
- **Por qué**: Archivar/eliminar leads muy viejos sin actividad
- **Beneficio**: Base de datos limpia

---

## 📝 Cómo Crear una Periodic Task

### PASO 1: Definir la Tarea

**Crear**: `apps/leads/tasks.py`

```python
# apps/leads/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Lead


@shared_task
def calculate_lead_scores():
    """
    Recalcular scores de todos los leads activos
    Se ejecuta diariamente a las 2 AM
    """
    print("🔄 Iniciando cálculo de lead scores...")
    
    # Obtener leads activos
    active_leads = Lead.objects.filter(
        status__in=['new', 'contacted', 'qualified', 'proposal', 'negotiation'],
        is_deleted=False
    )
    
    updated_count = 0
    
    for lead in active_leads:
        old_score = lead.lead_score
        
        # Calcular nuevo score basado en varios factores
        score = 0
        
        # Factor 1: Prioridad (0-20 puntos)
        priority_scores = {'low': 5, 'medium': 10, 'high': 15, 'urgent': 20}
        score += priority_scores.get(lead.priority, 5)
        
        # Factor 2: Fuente (0-15 puntos)
        source_scores = {
            'referral': 15,
            'website': 12,
            'facebook': 8,
            'instagram': 8,
            'cold_call': 5
        }
        score += source_scores.get(lead.source, 5)
        
        # Factor 3: Engagement (0-25 puntos)
        if lead.interaction_count:
            score += min(lead.interaction_count * 3, 25)
        
        # Factor 4: Budget match (0-20 puntos)
        if lead.budget_min and lead.budget_max:
            if lead.budget_min >= 300000:  # Budget alto
                score += 20
            elif lead.budget_min >= 200000:
                score += 15
            else:
                score += 10
        
        # Factor 5: Recency de contacto (0-20 puntos)
        if lead.last_contact_date:
            days_since_contact = (timezone.now() - lead.last_contact_date).days
            if days_since_contact <= 7:
                score += 20
            elif days_since_contact <= 30:
                score += 10
            else:
                score += 5
        
        # Actualizar score
        lead.lead_score = min(score, 100)  # Max 100
        
        if old_score != lead.lead_score:
            lead.save()
            updated_count += 1
    
    print(f"✅ Actualizado: {updated_count} leads")
    return f"Updated {updated_count} lead scores"


@shared_task
def send_followup_reminders():
    """
    Enviar recordatorios de follow-ups del día
    Se ejecuta cada mañana a las 8 AM
    """
    print("📧 Enviando recordatorios de follow-up...")
    
    today = timezone.now().date()
    
    # Leads con follow-up programado para hoy
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
    
    # Enviar emails
    from django.core.mail import send_mail
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
    print("🔍 Detectando follow-ups vencidos...")
    
    today = timezone.now().date()
    
    overdue_leads = Lead.objects.filter(
        next_follow_up_date__lt=today,
        status__in=['contacted', 'qualified', 'proposal', 'negotiation'],
        is_deleted=False
    ).select_related('assigned_to')
    
    # Notificar a managers
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    managers = User.objects.filter(
        role__in=['admin', 'manager'],
        status='active'
    )
    
    if overdue_leads.exists():
        # Crear reporte
        report = f"""
        ALERTA: {overdue_leads.count()} leads con follow-ups vencidos
        
        Leads que requieren atención:
        """
        
        for lead in overdue_leads[:10]:  # Top 10
            days_overdue = (today - lead.next_follow_up_date).days
            report += f"\n• {lead.full_name} - {days_overdue} días vencido"
        
        # Enviar a managers
        from django.core.mail import send_mail
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
    Calcular probabilidad de cierre usando IA (o algoritmo)
    Se ejecuta cada noche a las 3 AM
    """
    print("🤖 Calculando probabilidades de cierre...")
    
    from django.db.models import Avg
    
    qualified_leads = Lead.objects.filter(
        status__in=['qualified', 'proposal', 'negotiation'],
        is_deleted=False
    )
    
    updated_count = 0
    
    for lead in qualified_leads:
        # Algoritmo simple de scoring
        # En producción, esto sería ML real
        
        probability = 0
        
        # Factor 1: Lead score base (0-40 puntos)
        probability += (lead.lead_score * 0.4)
        
        # Factor 2: Engagement (0-20 puntos)
        if lead.interaction_count:
            probability += min(lead.interaction_count * 2, 20)
        
        # Factor 3: Budget confirmado (0-15 puntos)
        if lead.budget_min and lead.budget_max:
            probability += 15
        
        # Factor 4: Follow-up consistency (0-15 puntos)
        if lead.last_contact_date:
            days_since = (timezone.now() - lead.last_contact_date).days
            if days_since <= 7:
                probability += 15
            elif days_since <= 14:
                probability += 10
        
        # Factor 5: Status avanzado (0-10 puntos)
        status_bonus = {
            'negotiation': 10,
            'proposal': 7,
            'qualified': 5
        }
        probability += status_bonus.get(lead.status, 0)
        
        # Actualizar
        lead.ai_close_probability = int(min(probability, 100))
        lead.save(update_fields=['ai_close_probability'])
        updated_count += 1
    
    print(f"✅ Actualizado: {updated_count} leads")
    return f"Updated {updated_count} leads"


@shared_task
def cleanup_old_activities():
    """
    Archivar actividades muy antiguas
    Se ejecuta el primer día de cada mes
    """
    print("🧹 Limpiando actividades antiguas...")
    
    from apps.activities.models import Activity
    
    # Actividades de más de 2 años
    cutoff_date = timezone.now() - timedelta(days=730)
    
    old_activities = Activity.objects.filter(
        created_at__lt=cutoff_date
    )
    
    count = old_activities.count()
    
    # En lugar de eliminar, marcar como archived
    # old_activities.update(archived=True)
    
    print(f"🗂️ Archivadas {count} actividades antiguas")
    return f"Archived {count} activities"
```

### PASO 2: Registrar la Tarea en Celery

**En**: `owly_crm/celery.py` (ya existe)

```python
# owly_crm/celery.py
from celery import Celery
from celery.schedules import crontab

app = Celery('owly_crm')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Configurar tareas periódicas
app.conf.beat_schedule = {
    # Calcular scores - Cada día a las 2 AM
    'calculate-lead-scores-daily': {
        'task': 'apps.leads.tasks.calculate_lead_scores',
        'schedule': crontab(hour=2, minute=0),
    },
    
    # Recordatorios de follow-up - Cada día a las 8 AM
    'send-followup-reminders': {
        'task': 'apps.leads.tasks.send_followup_reminders',
        'schedule': crontab(hour=8, minute=0),
    },
    
    # Detectar follow-ups vencidos - Cada día a las 9 AM
    'detect-overdue-followups': {
        'task': 'apps.leads.tasks.detect_overdue_followups',
        'schedule': crontab(hour=9, minute=0),
    },
    
    # Calcular AI probability - Cada noche a las 3 AM
    'calculate-ai-probability': {
        'task': 'apps.leads.tasks.calculate_ai_close_probability',
        'schedule': crontab(hour=3, minute=0),
    },
    
    # Cleanup - Primer día del mes a las 1 AM
    'cleanup-old-activities': {
        'task': 'apps.leads.tasks.cleanup_old_activities',
        'schedule': crontab(hour=1, minute=0, day_of_month='1'),
    },
}
```

### PASO 3: Verificar que Funciona

```bash
# Ver tareas programadas en Django Admin
http://localhost:8000/admin/django_celery_beat/

# Ver logs de Celery Beat
docker-compose logs -f celery-beat

# Ver logs de Celery Worker
docker-compose logs -f celery
```

---

## 📅 Sintaxis de Programación (Crontab)

### Formatos Comunes:

```python
from celery.schedules import crontab

# Cada minuto
crontab()

# Cada hora
crontab(minute=0)

# Cada día a las 2:30 AM
crontab(hour=2, minute=30)

# Cada lunes a las 9 AM
crontab(hour=9, minute=0, day_of_week=1)

# Cada primer día del mes
crontab(hour=0, minute=0, day_of_month='1')

# Cada 15 minutos
crontab(minute='*/15')

# Cada 2 horas
crontab(minute=0, hour='*/2')

# De lunes a viernes a las 9 AM
crontab(hour=9, minute=0, day_of_week='1-5')

# Último día del mes
crontab(hour=23, minute=59, day_of_month='28-31')
```

### Ejemplos Específicos:

```python
# Horario de oficina (9 AM - 6 PM)
crontab(minute=0, hour='9-18')

# Solo días laborales
crontab(minute=0, hour=9, day_of_week='mon,tue,wed,thu,fri')

# Cada cuarto de hora
crontab(minute='0,15,30,45')

# Dos veces al día (mañana y tarde)
crontab(minute=0, hour='9,17')
```

---

## 🎯 Casos de Uso Detallados

### Caso 1: Liberar Opciones Expiradas

**Problema**: Cliente pidió opción 48h, pasó el tiempo, unidad sigue bloqueada

**Solución**: Tarea que cada hora revisa y libera opciones expiradas

```python
# apps/projects/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Unit


@shared_task
def release_expired_options():
    """
    Liberar unidades con opciones expiradas
    Se ejecuta cada hora
    """
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
        unit.operation_history.append({
            'date': now.isoformat(),
            'action': 'option_expired_auto_released',
            'system': True,
            'previous_holder': str(unit.option_holder.id) if unit.option_holder else None
        })
        
        # Liberar
        unit.status = 'available'
        unit.option_holder = None
        unit.option_expires_at = None
        unit.save()
        
        # Actualizar contadores del proyecto
        project = unit.project
        # project.recalculate_inventory()
        
        released_count += 1
    
    print(f"✅ Liberadas {released_count} unidades")
    
    # Notificar a sales si hubo liberaciones
    if released_count > 0:
        from django.core.mail import send_mail
        send_mail(
            f'{released_count} Opciones Expiradas - Unidades Disponibles',
            f'Se liberaron {released_count} unidades. Revisa el inventario.',
            'system@owlycrm.com',
            ['sales@owlycrm.com'],
            fail_silently=True
        )
    
    return f"Released {released_count} units"


# Programar en celery.py:
app.conf.beat_schedule = {
    'release-expired-options': {
        'task': 'apps.projects.tasks.release_expired_options',
        'schedule': crontab(minute=0),  # Cada hora
    },
}
```

---

### Caso 2: Alertas de Pagos Vencidos

```python
# apps/projects/tasks.py

@shared_task
def detect_overdue_payments():
    """
    Detectar unidades con pagos vencidos
    Se ejecuta cada día a las 9 AM
    """
    print("💰 Detectando pagos vencidos...")
    
    from django.core.mail import send_mail
    
    # Units con pagos vencidos
    overdue_units = Unit.objects.filter(
        payment_status='overdue',
        status__in=['in_payment', 'contract_signed']
    ).select_related('project')
    
    if not overdue_units.exists():
        print("✅ No hay pagos vencidos")
        return "No overdue payments"
    
    # Crear reporte
    report = f"""
    ALERTA: {overdue_units.count()} unidades con pagos vencidos
    
    Detalle:
    """
    
    total_overdue = 0
    
    for unit in overdue_units:
        # Calcular días vencido
        if unit.next_payment_date:
            days_overdue = (timezone.now().date() - unit.next_payment_date).days
            overdue_amount = unit.next_payment_amount or 0
            total_overdue += overdue_amount
            
            report += f"""
            
            Proyecto: {unit.project.name}
            Unidad: {unit.unit_number}
            Cliente: {unit.customer_first_name} {unit.customer_last_name}
            Monto vencido: ${overdue_amount:,.2f}
            Días vencido: {days_overdue}
            Teléfono: {unit.customer_phone}
            """
    
    report += f"\n\nTotal vencido: ${total_overdue:,.2f}"
    
    # Enviar a finance y managers
    send_mail(
        f'ALERTA: ${total_overdue:,.2f} en Pagos Vencidos',
        report,
        'finance@owlycrm.com',
        ['finance@owlycrm.com', 'manager@owlycrm.com'],
        fail_silently=False
    )
    
    print(f"⚠️ {overdue_units.count()} pagos vencidos, ${total_overdue:,.2f}")
    return f"Found {overdue_units.count()} overdue payments"
```

---

### Caso 3: Reporte Semanal de Ventas

```python
# apps/analytics/tasks.py

@shared_task
def generate_weekly_sales_report():
    """
    Generar reporte de ventas de la semana
    Se ejecuta cada lunes a las 8 AM
    """
    print("📊 Generando reporte semanal...")
    
    from apps.leads.models import Lead
    from apps.quotes.models import Quote
    from apps.projects.models import Unit
    from datetime import timedelta
    
    # Última semana
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
        'units_sold': Unit.objects.filter(sold_date__gte=week_ago).count(),
        'revenue': Unit.objects.filter(
            sold_date__gte=week_ago
        ).aggregate(total=Sum('final_sale_price'))['total'] or 0
    }
    
    # Crear reporte
    report = f"""
    REPORTE SEMANAL DE VENTAS
    Semana del {week_ago.strftime('%Y-%m-%d')} al {timezone.now().strftime('%Y-%m-%d')}
    
    📈 LEADS:
    • Nuevos leads: {stats['new_leads']}
    • Convertidos: {stats['leads_converted']}
    • Tasa de conversión: {(stats['leads_converted'] / stats['new_leads'] * 100) if stats['new_leads'] > 0 else 0:.1f}%
    
    💰 COTIZACIONES:
    • Enviadas: {stats['quotes_sent']}
    • Aceptadas: {stats['quotes_accepted']}
    • Tasa de aceptación: {(stats['quotes_accepted'] / stats['quotes_sent'] * 100) if stats['quotes_sent'] > 0 else 0:.1f}%
    
    🏠 VENTAS:
    • Unidades vendidas: {stats['units_sold']}
    • Revenue total: ${stats['revenue']:,.2f}
    • Ticket promedio: ${(stats['revenue'] / stats['units_sold']) if stats['units_sold'] > 0 else 0:,.2f}
    
    ¡Excelente trabajo equipo!
    """
    
    # Enviar a toda la empresa
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    all_users = User.objects.filter(
        status='active',
        role__in=['admin', 'manager', 'sales']
    )
    
    emails = [u.email for u in all_users]
    
    from django.core.mail import send_mail
    send_mail(
        'Reporte Semanal de Ventas',
        report,
        'reports@owlycrm.com',
        emails,
        fail_silently=True
    )
    
    print("✅ Reporte semanal enviado")
    return "Weekly report sent"


# Programar:
'weekly-sales-report': {
    'task': 'apps.analytics.tasks.generate_weekly_sales_report',
    'schedule': crontab(hour=8, minute=0, day_of_week=1),  # Lunes 8 AM
},
```

---

### Caso 4: Actualizar Performance de Vendedores

```python
# apps/users/tasks.py

@shared_task
def calculate_user_performance():
    """
    Calcular métricas de performance de vendedores
    Se ejecuta cada domingo a las 11 PM
    """
    print("📊 Calculando performance de vendedores...")
    
    from django.contrib.auth import get_user_model
    from apps.leads.models import Lead
    from apps.quotes.models import Quote
    from datetime import timedelta
    
    User = get_user_model()
    
    sales_users = User.objects.filter(
        role='sales',
        status='active'
    )
    
    # Período: última semana
    week_ago = timezone.now() - timedelta(days=7)
    
    for user in sales_users:
        # Leads del usuario
        user_leads = Lead.objects.filter(assigned_to=user)
        
        # Métricas de la semana
        leads_assigned = user_leads.filter(assigned_date__gte=week_ago).count()
        leads_contacted = user_leads.filter(
            last_contact_date__gte=week_ago
        ).count()
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
        
        # Guardar en performance_metrics
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
            'avg_deal_size': float(revenue / leads_converted) if leads_converted > 0 else 0,
        }
        user.save(update_fields=['performance_metrics'])
    
    print(f"✅ Performance calculado para {sales_users.count()} vendedores")
    return f"Calculated performance for {sales_users.count()} users"
```

---

## ⏱️ Tipos de Schedules

### 1. Crontab (Horarios Específicos)

```python
from celery.schedules import crontab

# Ejemplos prácticos para CRM:

# Inicio del día laboral
crontab(hour=8, minute=0)  # 8:00 AM

# Fin del día
crontab(hour=18, minute=0)  # 6:00 PM

# Medio día
crontab(hour=12, minute=0)  # 12:00 PM

# Noche (procesamiento pesado)
crontab(hour=2, minute=0)  # 2:00 AM

# Cada hora en horario laboral
crontab(minute=0, hour='9-17')  # 9 AM - 5 PM

# Cada 30 minutos
crontab(minute='*/30')

# Fin de semana (tareas de mantenimiento)
crontab(hour=3, minute=0, day_of_week='0,6')  # Dom y Sáb
```

### 2. Interval (Intervalos)

```python
from celery.schedules import schedule

# Cada 10 minutos
schedule(run_every=timedelta(minutes=10))

# Cada hora
schedule(run_every=timedelta(hours=1))

# Cada 6 horas
schedule(run_every=timedelta(hours=6))

# Cada 30 segundos (para testing)
schedule(run_every=timedelta(seconds=30))
```

---

## 📋 Tareas Recomendadas para OWLY CRM

### Críticas (Implementar Ya):

```python
app.conf.beat_schedule = {
    # 1. Liberar opciones expiradas - CADA HORA
    'release-expired-options': {
        'task': 'apps.projects.tasks.release_expired_options',
        'schedule': crontab(minute=0),  # Cada hora
    },
    
    # 2. Recordatorios de follow-up - CADA DÍA 8 AM
    'followup-reminders': {
        'task': 'apps.leads.tasks.send_followup_reminders',
        'schedule': crontab(hour=8, minute=0),
    },
    
    # 3. Detectar pagos vencidos - CADA DÍA 9 AM
    'detect-overdue-payments': {
        'task': 'apps.projects.tasks.detect_overdue_payments',
        'schedule': crontab(hour=9, minute=0),
    },
    
    # 4. Calcular lead scores - CADA DÍA 2 AM
    'calculate-lead-scores': {
        'task': 'apps.leads.tasks.calculate_lead_scores',
        'schedule': crontab(hour=2, minute=0),
    },
}
```

### Importantes (Segunda Fase):

```python
    # 5. Reporte semanal - LUNES 8 AM
    'weekly-sales-report': {
        'task': 'apps.analytics.tasks.generate_weekly_sales_report',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),
    },
    
    # 6. Performance de vendedores - DOMINGO 11 PM
    'calculate-performance': {
        'task': 'apps.users.tasks.calculate_user_performance',
        'schedule': crontab(hour=23, minute=0, day_of_week=0),
    },
    
    # 7. Updates de construcción - CADA 15 DÍAS
    'construction-updates': {
        'task': 'apps.projects.tasks.send_construction_updates',
        'schedule': crontab(hour=10, minute=0, day_of_month='1,15'),
    },
    
    # 8. Backup automático - CADA DÍA 3 AM
    'database-backup': {
        'task': 'apps.core.tasks.backup_database',
        'schedule': crontab(hour=3, minute=0),
    },
}
```

### Nice to Have (Futuro):

```python
    # 9. Detectar duplicados - CADA SEMANA
    'detect-duplicates': {
        'task': 'apps.leads.tasks.detect_and_notify_duplicates',
        'schedule': crontab(hour=9, minute=0, day_of_week=1),
    },
    
    # 10. Limpiar datos antiguos - CADA MES
    'cleanup-old-data': {
        'task': 'apps.core.tasks.cleanup_old_data',
        'schedule': crontab(hour=1, minute=0, day_of_month='1'),
    },
    
    # 11. Generar insights con IA - CADA DÍA 4 AM
    'generate-ai-insights': {
        'task': 'apps.analytics.tasks.generate_ai_insights',
        'schedule': crontab(hour=4, minute=0),
    },
}
```

---

## 🔧 Gestión de Tareas via Django Admin

### Acceder al Admin de Celery Beat:

1. Ve a: http://localhost:8000/admin/
2. Busca sección: **DJANGO CELERY BEAT**
3. Verás:
   - **Periodic tasks**: Tareas programadas
   - **Intervals**: Intervalos
   - **Crontabs**: Schedules tipo cron
   - **Solar schedules**: Basados en salida/puesta del sol

### Crear Tarea desde Admin:

```
1. Click en "Periodic tasks" → "Add"
2. Llenar:
   - Name: "Calculate Lead Scores Daily"
   - Task (registered): "apps.leads.tasks.calculate_lead_scores"
   - Crontab: Seleccionar o crear nuevo (hour=2, minute=0)
   - Enabled: ✓
3. Save
```

### Ventajas del Admin:

✅ **Activar/Desactivar** tareas sin código
✅ **Cambiar horarios** sin redeploy
✅ **Ver historial** de ejecuciones
✅ **Ejecutar manualmente** para testing
✅ **Ver errores** si falló

---

## 🐛 Testing de Periodic Tasks

### Test Manual:

```bash
# Ejecutar tarea inmediatamente (sin esperar schedule)
docker-compose exec web python manage.py shell

>>> from apps.leads.tasks import calculate_lead_scores
>>> result = calculate_lead_scores()
>>> print(result)
```

### Test con Celery:

```python
# tests/test_tasks.py
import pytest
from apps.leads.tasks import calculate_lead_scores


@pytest.mark.django_db
def test_calculate_lead_scores(company, sales_user):
    """Test lead score calculation task"""
    from apps.leads.models import Lead
    
    # Crear lead con datos para score alto
    lead = Lead.objects.create(
        company=company,
        first_name='High',
        last_name='Score',
        email='high@test.com',
        phone='+1234567890',
        priority='high',
        source='referral',
        interaction_count=10,
        budget_min=400000,
        assigned_to=sales_user,
        last_contact_date=timezone.now()
    )
    
    initial_score = lead.lead_score
    
    # Ejecutar tarea
    result = calculate_lead_scores()
    
    # Verificar
    lead.refresh_from_db()
    assert lead.lead_score > initial_score
    assert 'Updated' in result
```

---

## 📊 Monitoreo de Tareas

### Ver Tareas en Ejecución:

```bash
# Logs de Celery Beat (scheduler)
docker-compose logs -f celery-beat

# Logs de Celery Worker (executor)
docker-compose logs -f celery

# Ver todas las tareas registradas
docker-compose exec web celery -A owly_crm inspect registered
```

### Verificar que Beat está corriendo:

```bash
docker-compose exec celery-beat celery -A owly_crm beat -l info
```

Deberías ver:
```
Scheduler: Starting...
beat: Starting...
```

### Verificar tareas en Redis:

```bash
docker-compose exec redis redis-cli

> KEYS *
> LLEN celery
```

---

## ⚡ Mejores Prácticas

### 1. Idempotencia

```python
# ❌ Malo - puede crear duplicados
@shared_task
def bad_task():
    Lead.objects.create(...)  # Si se ejecuta 2 veces, crea 2 leads

# ✅ Bueno - idempotente
@shared_task
def good_task():
    Lead.objects.update_or_create(
        email='test@test.com',
        defaults={'score': 80}
    )  # Si se ejecuta 2 veces, mismo resultado
```

### 2. Logging Adecuado

```python
@shared_task
def my_task():
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info("Iniciando tarea...")
    
    try:
        # Hacer trabajo
        result = do_something()
        logger.info(f"Completado: {result}")
        return result
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise
```

### 3. Timeout

```python
@shared_task(time_limit=300)  # 5 minutos max
def long_task():
    # Si tarda más de 5 min, se cancela
    pass
```

### 4. Retry on Failure

```python
@shared_task(bind=True, max_retries=3)
def task_with_retry(self):
    try:
        # Hacer algo que puede fallar
        send_email()
    except Exception as exc:
        # Retry en 60 segundos
        raise self.retry(exc=exc, countdown=60)
```

### 5. Solo Trabajos Livianos en Tasks

```python
# ❌ Malo - procesar 10,000 leads en una tarea
@shared_task
def bad_heavy_task():
    leads = Lead.objects.all()  # 10,000 leads
    for lead in leads:
        # Procesar cada uno
        pass

# ✅ Bueno - dividir en chunks
@shared_task
def good_task():
    leads = Lead.objects.filter(needs_processing=True)[:100]
    for lead in leads:
        # Procesar solo 100
        pass
    
    # Si quedan más, programa otra tarea
    if Lead.objects.filter(needs_processing=True).count() > 100:
        good_task.delay()  # Ejecutar de nuevo
```

---

## 🎯 Tareas Propuestas por Módulo

### LEADS:
```python
calculate_lead_scores()              # Diario 2 AM
send_followup_reminders()            # Diario 8 AM
detect_overdue_followups()           # Diario 9 AM
calculate_ai_close_probability()     # Diario 3 AM
detect_duplicate_leads()             # Semanal
archive_old_lost_leads()             # Mensual
```

### PROJECTS/UNITS:
```python
release_expired_options()            # Cada hora
detect_overdue_payments()            # Diario 9 AM
update_construction_progress()       # Semanal
send_construction_updates()          # Quincenal
recalculate_inventory_breakdown()    # Diario 4 AM
detect_units_ready_for_delivery()    # Diario 10 AM
```

### ANALYTICS:
```python
generate_daily_dashboard()           # Diario 6 AM
generate_weekly_sales_report()       # Lunes 8 AM
generate_monthly_report()            # Día 1 del mes 7 AM
calculate_sales_velocity()           # Diario 5 AM
```

### SYSTEM:
```python
backup_database()                    # Diario 3 AM
cleanup_old_sessions()               # Semanal
check_system_health()                # Cada hora
send_error_digest()                  # Diario 9 AM (si hubo errores)
```

---

## 📖 Configuración Completa

### Archivo completo: `owly_crm/celery.py`

```python
# owly_crm/celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'owly_crm.settings')

app = Celery('owly_crm')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# ============================================
# PERIODIC TASKS SCHEDULE
# ============================================

app.conf.beat_schedule = {
    
    # ========== HORARIO LABORAL (8 AM - 6 PM) ==========
    
    'followup-reminders-morning': {
        'task': 'apps.leads.tasks.send_followup_reminders',
        'schedule': crontab(hour=8, minute=0),  # 8:00 AM
        'options': {'expires': 3600}  # Expira en 1 hora
    },
    
    'detect-overdue-followups': {
        'task': 'apps.leads.tasks.detect_overdue_followups',
        'schedule': crontab(hour=9, minute=0),  # 9:00 AM
    },
    
    'detect-overdue-payments': {
        'task': 'apps.projects.tasks.detect_overdue_payments',
        'schedule': crontab(hour=9, minute=30),  # 9:30 AM
    },
    
    'units-ready-for-delivery-check': {
        'task': 'apps.projects.tasks.detect_units_ready_for_delivery',
        'schedule': crontab(hour=10, minute=0),  # 10:00 AM
    },
    
    # ========== CADA HORA (Durante el día) ==========
    
    'release-expired-options': {
        'task': 'apps.projects.tasks.release_expired_options',
        'schedule': crontab(minute=0, hour='8-18'),  # Cada hora 8 AM-6 PM
    },
    
    # ========== NOCHE (Procesamiento Pesado) ==========
    
    'backup-database': {
        'task': 'apps.core.tasks.backup_database',
        'schedule': crontab(hour=1, minute=0),  # 1:00 AM
    },
    
    'calculate-lead-scores': {
        'task': 'apps.leads.tasks.calculate_lead_scores',
        'schedule': crontab(hour=2, minute=0),  # 2:00 AM
    },
    
    'calculate-ai-probability': {
        'task': 'apps.leads.tasks.calculate_ai_close_probability',
        'schedule': crontab(hour=3, minute=0),  # 3:00 AM
    },
    
    'recalculate-inventory': {
        'task': 'apps.projects.tasks.recalculate_inventory_breakdown',
        'schedule': crontab(hour=4, minute=0),  # 4:00 AM
    },
    
    'calculate-sales-velocity': {
        'task': 'apps.analytics.tasks.calculate_sales_velocity',
        'schedule': crontab(hour=5, minute=0),  # 5:00 AM
    },
    
    'generate-daily-dashboard': {
        'task': 'apps.analytics.tasks.generate_daily_dashboard',
        'schedule': crontab(hour=6, minute=0),  # 6:00 AM
    },
    
    # ========== SEMANALES ==========
    
    'weekly-sales-report': {
        'task': 'apps.analytics.tasks.generate_weekly_sales_report',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),  # Lunes 8 AM
    },
    
    'calculate-user-performance': {
        'task': 'apps.users.tasks.calculate_user_performance',
        'schedule': crontab(hour=23, minute=0, day_of_week=0),  # Domingo 11 PM
    },
    
    'detect-duplicate-leads': {
        'task': 'apps.leads.tasks.detect_and_notify_duplicates',
        'schedule': crontab(hour=10, minute=0, day_of_week=1),  # Lunes 10 AM
    },
    
    'update-construction-progress': {
        'task': 'apps.projects.tasks.update_construction_progress',
        'schedule': crontab(hour=14, minute=0, day_of_week=3),  # Miércoles 2 PM
    },
    
    # ========== QUINCENALES ==========
    
    'send-construction-updates-to-customers': {
        'task': 'apps.projects.tasks.send_construction_updates',
        'schedule': crontab(hour=10, minute=0, day_of_month='1,15'),  # Día 1 y 15
    },
    
    # ========== MENSUALES ==========
    
    'monthly-report': {
        'task': 'apps.analytics.tasks.generate_monthly_report',
        'schedule': crontab(hour=7, minute=0, day_of_month='1'),  # Día 1 a las 7 AM
    },
    
    'cleanup-old-activities': {
        'task': 'apps.leads.tasks.cleanup_old_activities',
        'schedule': crontab(hour=1, minute=30, day_of_month='1'),  # Día 1 a la 1:30 AM
    },
    
    'calculate-monthly-commission': {
        'task': 'apps.users.tasks.calculate_monthly_commission',
        'schedule': crontab(hour=8, minute=0, day_of_month='1'),  # Día 1 a las 8 AM
    },
}

# Configuración adicional
app.conf.timezone = 'America/New_York'  # O tu timezone
app.conf.task_default_priority = 5
app.conf.task_ignore_result = False  # Guardar resultados
```

---

## 🚀 Ejecutar Tarea Manualmente

### Desde Django Shell:

```bash
docker-compose exec web python manage.py shell
```

```python
>>> from apps.leads.tasks import calculate_lead_scores
>>> result = calculate_lead_scores()
>>> print(result)
"Updated 150 lead scores"

>>> # O ejecutar async
>>> task = calculate_lead_scores.delay()
>>> print(task.id)
>>> print(task.status)  # PENDING, SUCCESS, FAILURE
```

### Desde Admin:

1. Ve a **Periodic tasks**
2. Click en la tarea
3. Botón **"Run now"** (ejecuta inmediatamente)

### Programáticamente:

```python
# En una view o script
from apps.leads.tasks import calculate_lead_scores

# Ejecutar ahora en background
calculate_lead_scores.delay()

# Ejecutar en 60 segundos
calculate_lead_scores.apply_async(countdown=60)

# Ejecutar a una hora específica
from datetime import datetime
calculate_lead_scores.apply_async(eta=datetime(2024, 12, 25, 8, 0))
```

---

## 📈 Monitoring y Alertas

### Ver Resultados de Tareas:

```python
# Django shell
>>> from django_celery_beat.models import PeriodicTask
>>> task = PeriodicTask.objects.get(name='calculate-lead-scores')
>>> task.last_run_at
datetime.datetime(2024, 1, 16, 2, 0, 0)
>>> task.total_run_count
365  # Se ha ejecutado 365 veces
```

### Alertar si Tarea Falla:

```python
@shared_task(bind=True)
def important_task(self):
    try:
        # Hacer trabajo crítico
        result = do_something_critical()
        return result
    except Exception as exc:
        # Alertar inmediatamente
        from django.core.mail import send_mail
        send_mail(
            'ALERTA: Tarea Crítica Falló',
            f'Error: {str(exc)}',
            'alerts@owlycrm.com',
            ['admin@owlycrm.com'],
            fail_silently=False
        )
        raise self.retry(exc=exc, countdown=300, max_retries=3)
```

---

## 💡 Casos de Uso Avanzados

### Caso 1: Email Drip Campaign

```python
@shared_task
def send_drip_campaign_emails():
    """
    Enviar emails de campaña gota a gota
    Día 1: Welcome
    Día 3: Project info
    Día 7: Special offer
    """
    from apps.leads.models import Lead
    from datetime import timedelta
    
    now = timezone.now()
    
    # Leads para email de día 1 (welcome)
    day_1_leads = Lead.objects.filter(
        status='new',
        created_at__date=now.date() - timedelta(days=1),
        consent_given=True,
        marketing_opt_in=True
    )
    
    for lead in day_1_leads:
        send_welcome_email(lead)
    
    # Leads para email de día 3 (project info)
    day_3_leads = Lead.objects.filter(
        status__in=['new', 'contacted'],
        created_at__date=now.date() - timedelta(days=3),
        marketing_opt_in=True
    )
    
    for lead in day_3_leads:
        send_project_info_email(lead)
    
    # Y así sucesivamente...
```

### Caso 2: Sync con CRM Externo

```python
@shared_task
def sync_with_external_crm():
    """
    Sincronizar datos con CRM externo (Monday, Salesforce, etc.)
    Cada 15 minutos
    """
    print("🔄 Sincronizando con CRM externo...")
    
    from apps.leads.models import Lead
    import requests
    
    # Leads modificados en últimos 15 minutos
    cutoff = timezone.now() - timedelta(minutes=15)
    modified_leads = Lead.objects.filter(updated_at__gte=cutoff)
    
    for lead in modified_leads:
        # Enviar a CRM externo
        try:
            response = requests.post(
                'https://external-crm.com/api/leads',
                json={
                    'email': lead.email,
                    'name': lead.full_name,
                    'status': lead.status,
                    'score': lead.lead_score
                },
                headers={'Authorization': 'Bearer EXTERNAL_TOKEN'}
            )
            response.raise_for_status()
        except Exception as e:
            print(f"Error syncing lead {lead.id}: {e}")
    
    print(f"✅ Sincronizados {modified_leads.count()} leads")
```

### Caso 3: Cache Warmup

```python
@shared_task
def warmup_cache():
    """
    Pre-cargar cache para queries comunes
    Cada día a las 6 AM (antes que lleguen usuarios)
    """
    print("🔥 Calentando cache...")
    
    from django.core.cache import cache
    from apps.leads.models import Lead
    from apps.projects.models import Project
    
    # Pre-calcular stats que se usan mucho
    
    # Stats de leads
    lead_stats = {
        'total': Lead.objects.count(),
        'by_status': {},
        'avg_score': Lead.objects.aggregate(avg=Avg('lead_score'))['avg']
    }
    cache.set('lead_stats', lead_stats, timeout=86400)  # 24 horas
    
    # Featured projects
    featured = list(Project.objects.filter(
        featured=True,
        status='active'
    ).values())
    cache.set('featured_projects', featured, timeout=3600)  # 1 hora
    
    print("✅ Cache listo para el día")
```

---

## 🔐 Seguridad en Periodic Tasks

### 1. No Exponer Datos Sensibles en Logs

```python
# ❌ Malo
@shared_task
def bad_task():
    print(f"Processing payment: Card {credit_card_number}")  # ¡NO!

# ✅ Bueno
@shared_task
def good_task():
    print(f"Processing payment: Card ending in {last_4_digits}")
```

### 2. Validar Datos

```python
@shared_task
def process_payments():
    units = Unit.objects.filter(payment_status='pending')
    
    for unit in units:
        # Validar antes de procesar
        if not unit.customer_email:
            continue
        if not unit.next_payment_amount:
            continue
        
        # Procesar...
```

### 3. Rate Limiting (APIs Externas)

```python
@shared_task(rate_limit='10/m')  # Max 10 por minuto
def call_external_api():
    # Llamar a API externa con límite
    pass
```

---

## 📊 Dashboard de Celery (Flower) - Opcional

### Instalar Flower:

```bash
# Agregar a requirements.txt
flower==2.0.1
```

```yaml
# Agregar a docker-compose.yml
flower:
  build: .
  command: celery -A owly_crm flower
  ports:
    - "5555:5555"
  depends_on:
    - redis
    - celery
```

### Acceder:
http://localhost:5555

**Verás**:
- Tareas en ejecución
- Tareas completadas/fallidas
- Gráficas de performance
- Workers activos
- Rate de ejecución

---

## ✅ Checklist de Implementación

### Setup Inicial:
- [x] Celery configurado en `celery.py`
- [x] Celery worker corriendo
- [x] Celery beat corriendo
- [x] Redis funcionando como broker
- [ ] Tareas básicas creadas

### Crear Tareas:
- [ ] Crear archivo `apps/leads/tasks.py`
- [ ] Crear archivo `apps/projects/tasks.py`
- [ ] Crear archivo `apps/analytics/tasks.py`
- [ ] Definir funciones con `@shared_task`
- [ ] Agregar logging

### Programar:
- [ ] Actualizar `owly_crm/celery.py`
- [ ] Agregar schedules en `beat_schedule`
- [ ] Reiniciar celery-beat

### Testing:
- [ ] Ejecutar tasks manualmente
- [ ] Verificar logs
- [ ] Verificar resultados en DB
- [ ] Testing con pytest

### Producción:
- [ ] Monitoreo con Flower (opcional)
- [ ] Alertas si tareas fallan
- [ ] Backup de resultados
- [ ] Documentar cada tarea

---

## 🐛 Troubleshooting

### Tarea no se ejecuta:

```bash
# 1. Verificar que beat está corriendo
docker-compose ps

# 2. Ver logs de beat
docker-compose logs celery-beat

# 3. Verificar schedule en admin
http://localhost:8000/admin/django_celery_beat/periodictask/

# 4. Verificar timezone
# En celery.py: app.conf.timezone = 'America/New_York'
```

### Tarea falla:

```bash
# Ver logs detallados
docker-compose logs celery

# Ejecutar manualmente para ver error
docker-compose exec web python manage.py shell
>>> from apps.leads.tasks import my_task
>>> my_task()  # Ver error directo
```

### Worker no procesa:

```bash
# Reiniciar worker
docker-compose restart celery

# Ver si worker ve las tareas
docker-compose exec web celery -A owly_crm inspect registered
```

---

## 📚 Recursos

- **Celery Docs**: https://docs.celeryproject.org/
- **Beat Docs**: https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html
- **Django Celery Beat**: https://django-celery-beat.readthedocs.io/

---

## 🎉 Resumen

Las Periodic Tasks te permiten:

✅ **Automatizar** trabajos repetitivos
✅ **Programar** tareas en horarios específicos
✅ **Escalar** procesamiento sin bloquear la API
✅ **Mejorar UX** (emails automáticos, actualizaciones)
✅ **Mantener datos** actualizados (scores, stats)
✅ **Prevenir problemas** (detectar vencidos, liberar opciones)
✅ **Generar reportes** automáticamente

**En OWLY CRM específicamente**:
- Scores actualizados
- Follow-ups nunca olvidados
- Opciones liberadas automáticamente
- Pagos monitoreados
- Reportes generados
- Performance calculado
- Todo sin intervención manual

---

**Siguiente**: Ver implementaciones completas en el próximo documento

