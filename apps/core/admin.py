"""
Core admin configuration
"""
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import ScheduledTask


@admin.register(ScheduledTask)
class ScheduledTaskAdmin(admin.ModelAdmin):
    """
    Admin intuitivo para tareas programadas
    Diseñado para usuarios no técnicos
    """
    list_display = [
        'status_indicator',
        'name',
        'category_badge',
        'schedule_display',
        'last_run_display',
        'success_indicator',
        'total_runs',
        'actions_column'
    ]
    list_filter = [
        'category',
        'frequency',
        'is_active',
        'last_success',
        'company'
    ]
    search_fields = ['name', 'description']
    readonly_fields = [
        'id',
        'schedule_preview',
        'last_run',
        'total_runs',
        'last_result',
        'last_success',
        'periodic_task',
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('📋 Información Básica', {
            'fields': (
                'name',
                'description',
                'category',
                'company'
            ),
            'description': 'Información general de la tarea'
        }),
        ('⏰ Programación (¿Cuándo se ejecuta?)', {
            'fields': (
                'frequency',
                'schedule_preview',  # Read-only preview
                'hour',
                'minute',
                'day_of_week',
                'day_of_month',
            ),
            'description': '''
                <div style="background: #e3f2fd; padding: 15px; border-radius: 5px; margin: 10px 0;">
                    <h3 style="margin-top: 0;">💡 Cómo configurar el horario:</h3>
                    <ul>
                        <li><strong>Cada Hora</strong>: Se ejecuta cada hora a los X minutos</li>
                        <li><strong>Diario</strong>: Se ejecuta todos los días a la hora especificada</li>
                        <li><strong>Semanal</strong>: Especifica el día de la semana y la hora</li>
                        <li><strong>Quincenal</strong>: Días 1 y 15 de cada mes</li>
                        <li><strong>Mensual</strong>: Especifica el día del mes (1-31)</li>
                    </ul>
                    <p><strong>Ejemplos:</strong></p>
                    <ul>
                        <li>Diario a las 8 AM: Frecuencia=Diario, Hora=8, Minuto=0</li>
                        <li>Cada lunes a las 9 AM: Frecuencia=Semanal, Día=Lunes, Hora=9</li>
                        <li>Primer día del mes: Frecuencia=Mensual, Día del mes=1</li>
                    </ul>
                </div>
            '''
        }),
        ('⚙️ Configuración Técnica', {
            'fields': ('task_name', 'created_by'),
            'classes': ('collapse',),
            'description': 'Información técnica (generalmente no necesitas modificar esto)'
        }),
        ('✅ Activación', {
            'fields': ('is_active',),
            'description': '<strong style="color: #f44336;">⚠️ Desactivar para pausar la tarea sin eliminarla</strong>'
        }),
        ('📊 Historial de Ejecuciones', {
            'fields': (
                'last_run',
                'total_runs',
                'last_success',
                'last_result',
            ),
            'classes': ('collapse',),
            'description': 'Información sobre las ejecuciones de la tarea'
        }),
        ('🔗 Sistema', {
            'fields': ('id', 'periodic_task', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = [
        'activate_tasks',
        'deactivate_tasks',
        'run_now',
        'reset_counters'
    ]
    
    def status_indicator(self, obj):
        """Visual indicator of task status"""
        if not obj.is_active:
            return format_html(
                '<span style="display: inline-block; width: 12px; height: 12px; border-radius: 50%; background-color: #9e9e9e;" title="Desactivada"></span>'
            )
        elif not obj.last_success:
            return format_html(
                '<span style="display: inline-block; width: 12px; height: 12px; border-radius: 50%; background-color: #f44336;" title="Última ejecución falló"></span>'
            )
        else:
            return format_html(
                '<span style="display: inline-block; width: 12px; height: 12px; border-radius: 50%; background-color: #4caf50;" title="Activa y funcionando"></span>'
            )
    status_indicator.short_description = '●'
    
    def category_badge(self, obj):
        """Category badge"""
        colors = {
            'leads': '#2196f3',
            'followups': '#ff9800',
            'payments': '#4caf50',
            'reports': '#9c27b0',
            'inventory': '#00bcd4',
            'notifications': '#ff5722',
            'maintenance': '#607d8b'
        }
        color = colors.get(obj.category, '#9e9e9e')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px;">{}</span>',
            color,
            obj.get_category_display()
        )
    category_badge.short_description = 'Categoría'
    
    def schedule_display(self, obj):
        """User-friendly schedule display"""
        return obj.get_schedule_description()
    schedule_display.short_description = 'Programación'
    
    def last_run_display(self, obj):
        """Last run with relative time"""
        if not obj.last_run:
            return format_html('<span style="color: #9e9e9e;">Nunca ejecutada</span>')
        
        # Calculate time ago
        now = timezone.now()
        delta = now - obj.last_run
        
        if delta.days > 0:
            time_ago = f"hace {delta.days} día{'s' if delta.days != 1 else ''}"
        elif delta.seconds >= 3600:
            hours = delta.seconds // 3600
            time_ago = f"hace {hours} hora{'s' if hours != 1 else ''}"
        elif delta.seconds >= 60:
            minutes = delta.seconds // 60
            time_ago = f"hace {minutes} minuto{'s' if minutes != 1 else ''}"
        else:
            time_ago = "hace unos segundos"
        
        return format_html(
            '<span title="{}">{}</span>',
            obj.last_run.strftime('%Y-%m-%d %H:%M:%S'),
            time_ago
        )
    last_run_display.short_description = 'Última Ejecución'
    
    def success_indicator(self, obj):
        """Success/failure indicator"""
        if obj.total_runs == 0:
            return format_html('<span style="color: #9e9e9e;">—</span>')
        
        if obj.last_success:
            return format_html(
                '<span style="color: #4caf50; font-size: 16px;" title="Exitosa">✓</span>'
            )
        else:
            return format_html(
                '<span style="color: #f44336; font-size: 16px;" title="Falló">✗</span>'
            )
    success_indicator.short_description = 'Estado'
    
    def actions_column(self, obj):
        """Quick action buttons"""
        if obj.is_active:
            status_btn = format_html(
                '<a class="button" href="#" onclick="return false;" style="background: #f44336; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px; font-size: 11px;">Pausar</a>'
            )
        else:
            status_btn = format_html(
                '<a class="button" href="#" onclick="return false;" style="background: #4caf50; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px; font-size: 11px;">Activar</a>'
            )
        
        return format_html(
            '{} <a class="button" href="#" onclick="return false;" style="background: #2196f3; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px; font-size: 11px; margin-left: 5px;">Ejecutar Ahora</a>',
            status_btn
        )
    actions_column.short_description = 'Acciones'
    
    def schedule_preview(self, obj):
        """Preview of schedule in user-friendly format"""
        if not obj.id:
            return "Guarda la tarea primero para ver la programación"
        
        schedule_text = obj.get_schedule_description()
        
        # Calculate next run
        next_run = "Calculando..."
        if obj.periodic_task and obj.periodic_task.crontab:
            # This would require celery beat's scheduler logic
            next_run = "Ver en sección de Sistema"
        
        return format_html(
            '''
            <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; border-left: 4px solid #2196f3;">
                <p style="margin: 0; font-size: 14px;"><strong>📅 Programación:</strong> {}</p>
                <p style="margin: 5px 0 0 0; color: #666; font-size: 12px;">Próxima ejecución: {}</p>
            </div>
            ''',
            schedule_text,
            next_run
        )
    schedule_preview.short_description = 'Vista Previa de Programación'
    
    # Bulk Actions
    def activate_tasks(self, request, queryset):
        """Activate selected tasks"""
        updated = queryset.update(is_active=True)
        for task in queryset:
            if task.periodic_task:
                task.periodic_task.enabled = True
                task.periodic_task.save()
        self.message_user(request, f'{updated} tareas activadas.')
    activate_tasks.short_description = '✅ Activar tareas seleccionadas'
    
    def deactivate_tasks(self, request, queryset):
        """Deactivate selected tasks"""
        updated = queryset.update(is_active=False)
        for task in queryset:
            if task.periodic_task:
                task.periodic_task.enabled = False
                task.periodic_task.save()
        self.message_user(request, f'{updated} tareas desactivadas.')
    deactivate_tasks.short_description = '⏸️ Pausar tareas seleccionadas'
    
    def run_now(self, request, queryset):
        """Execute tasks immediately"""
        executed = 0
        for task in queryset:
            try:
                # Import and execute task
                from celery import current_app
                current_app.send_task(task.task_name)
                executed += 1
            except Exception as e:
                self.message_user(
                    request,
                    f'Error ejecutando {task.name}: {str(e)}',
                    level='ERROR'
                )
        
        if executed > 0:
            self.message_user(request, f'{executed} tareas ejecutadas inmediatamente.')
    run_now.short_description = '▶️ Ejecutar ahora (inmediato)'
    
    def reset_counters(self, request, queryset):
        """Reset execution counters"""
        queryset.update(total_runs=0, last_result='', last_success=True)
        self.message_user(request, 'Contadores reiniciados.')
    reset_counters.short_description = '🔄 Reiniciar contadores'

