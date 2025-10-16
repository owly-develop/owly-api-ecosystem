"""
Core models for multi-tenant architecture
"""
from django.db import models
from django.utils import timezone
import uuid


class TenantAwareModel(models.Model):
    """
    Abstract base model for all tenant-aware models
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='%(class)s_set'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['company', '-created_at']),
        ]


class SoftDeleteModel(models.Model):
    """
    Abstract base model for soft delete functionality
    """
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def soft_delete(self):
        """Soft delete the object"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    def restore(self):
        """Restore a soft deleted object"""
        self.is_deleted = False
        self.deleted_at = None
        self.save()


class TimestampedModel(models.Model):
    """
    Abstract base model with timestamp fields
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class ScheduledTask(TenantAwareModel):
    """
    User-friendly wrapper for periodic tasks
    Allows non-technical users to configure scheduled tasks from admin
    """
    CATEGORY_CHOICES = [
        ('leads', '📊 Gestión de Leads'),
        ('followups', '📅 Seguimiento y Recordatorios'),
        ('payments', '💰 Pagos y Cobranzas'),
        ('reports', '📈 Reportes y Análisis'),
        ('inventory', '🏗️ Inventario'),
        ('notifications', '📧 Notificaciones'),
        ('maintenance', '🔧 Mantenimiento del Sistema'),
    ]
    
    FREQUENCY_CHOICES = [
        ('hourly', 'Cada Hora'),
        ('daily', 'Diario'),
        ('weekly', 'Semanal'),
        ('biweekly', 'Quincenal'),
        ('monthly', 'Mensual'),
    ]
    
    DAY_OF_WEEK_CHOICES = [
        ('1', 'Lunes'),
        ('2', 'Martes'),
        ('3', 'Miércoles'),
        ('4', 'Jueves'),
        ('5', 'Viernes'),
        ('6', 'Sábado'),
        ('0', 'Domingo'),
    ]
    
    # Basic info
    name = models.CharField(
        max_length=255,
        help_text="Nombre de la tarea. Ej: 'Recordatorios de Follow-ups'"
    )
    description = models.TextField(
        help_text="Qué hace esta tarea. Ej: 'Envía emails a vendedores con sus follow-ups del día'"
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        help_text="Categoría de la tarea"
    )
    
    # Task reference
    task_name = models.CharField(
        max_length=255,
        help_text="Nombre técnico (automático)"
    )
    
    # Schedule (simple)
    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default='daily',
        help_text="¿Con qué frecuencia se ejecuta?"
    )
    
    hour = models.IntegerField(
        default=8,
        help_text="Hora (0-23). Ej: 8 = 8 AM, 14 = 2 PM, 20 = 8 PM"
    )
    minute = models.IntegerField(
        default=0,
        help_text="Minuto (0-59)"
    )
    
    # For weekly
    day_of_week = models.CharField(
        max_length=10,
        choices=DAY_OF_WEEK_CHOICES,
        blank=True,
        help_text="Para tareas semanales: qué día ejecutar"
    )
    
    # For monthly
    day_of_month = models.IntegerField(
        null=True,
        blank=True,
        help_text="Para tareas mensuales: día del mes (1-31)"
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        help_text="Activar/Desactivar tarea"
    )
    
    # Tracking
    last_run = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        help_text="Última vez que se ejecutó"
    )
    total_runs = models.IntegerField(
        default=0,
        editable=False,
        help_text="Total de ejecuciones"
    )
    last_result = models.TextField(
        blank=True,
        editable=False,
        help_text="Resultado de última ejecución"
    )
    last_success = models.BooleanField(
        default=True,
        editable=False,
        help_text="¿Última ejecución fue exitosa?"
    )
    
    # Metadata
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_scheduled_tasks'
    )
    
    # Link to celery task
    periodic_task = models.OneToOneField(
        'django_celery_beat.PeriodicTask',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=False
    )
    
    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Tarea Programada'
        verbose_name_plural = 'Tareas Programadas'
    
    def __str__(self):
        return f"{self.name}"
    
    def get_schedule_description(self):
        """Human-readable schedule"""
        if self.frequency == 'hourly':
            return f"Cada hora a los {self.minute} minutos"
        elif self.frequency == 'daily':
            hour_12 = self.hour if self.hour <= 12 else self.hour - 12
            am_pm = 'AM' if self.hour < 12 else 'PM'
            return f"Todos los días a las {hour_12}:{self.minute:02d} {am_pm}"
        elif self.frequency == 'weekly':
            day_name = dict(self.DAY_OF_WEEK_CHOICES).get(self.day_of_week, 'Lunes')
            hour_12 = self.hour if self.hour <= 12 else self.hour - 12
            am_pm = 'AM' if self.hour < 12 else 'PM'
            return f"Cada {day_name} a las {hour_12}:{self.minute:02d} {am_pm}"
        elif self.frequency == 'biweekly':
            return f"Días 1 y 15 de cada mes a las {self.hour}:{self.minute:02d}"
        elif self.frequency == 'monthly':
            hour_12 = self.hour if self.hour <= 12 else self.hour - 12
            am_pm = 'AM' if self.hour < 12 else 'PM'
            return f"Día {self.day_of_month} de cada mes a las {hour_12}:{self.minute:02d} {am_pm}"
        return "Personalizado"
    
    def save(self, *args, **kwargs):
        """Create or update corresponding PeriodicTask"""
        from django_celery_beat.models import PeriodicTask, CrontabSchedule
        
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Create crontab based on frequency
        crontab_kwargs = self._get_crontab_kwargs()
        schedule, _ = CrontabSchedule.objects.get_or_create(**crontab_kwargs)
        
        # Create or update PeriodicTask
        if is_new or not self.periodic_task:
            task = PeriodicTask.objects.create(
                name=f"{self.company.slug}-{self.name}-{self.pk}",
                task=self.task_name,
                crontab=schedule,
                enabled=self.is_active
            )
            self.periodic_task = task
            super().save(update_fields=['periodic_task'])
        else:
            self.periodic_task.crontab = schedule
            self.periodic_task.enabled = self.is_active
            self.periodic_task.save()
    
    def _get_crontab_kwargs(self):
        """Get crontab kwargs based on frequency"""
        if self.frequency == 'hourly':
            return {
                'minute': str(self.minute),
                'hour': '*',
                'day_of_week': '*',
                'day_of_month': '*',
                'month_of_year': '*'
            }
        elif self.frequency == 'daily':
            return {
                'minute': str(self.minute),
                'hour': str(self.hour),
                'day_of_week': '*',
                'day_of_month': '*',
                'month_of_year': '*'
            }
        elif self.frequency == 'weekly':
            return {
                'minute': str(self.minute),
                'hour': str(self.hour),
                'day_of_week': self.day_of_week or '1',
                'day_of_month': '*',
                'month_of_year': '*'
            }
        elif self.frequency == 'biweekly':
            return {
                'minute': str(self.minute),
                'hour': str(self.hour),
                'day_of_week': '*',
                'day_of_month': '1,15',
                'month_of_year': '*'
            }
        elif self.frequency == 'monthly':
            return {
                'minute': str(self.minute),
                'hour': str(self.hour),
                'day_of_week': '*',
                'day_of_month': str(self.day_of_month or 1),
                'month_of_year': '*'
            }
        
        # Default
        return {
            'minute': '0',
            'hour': '2',
            'day_of_week': '*',
            'day_of_month': '*',
            'month_of_year': '*'
        }

