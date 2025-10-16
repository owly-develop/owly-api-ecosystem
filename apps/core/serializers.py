"""
Core serializers
"""
from rest_framework import serializers
from .models import ScheduledTask


class ScheduledTaskSerializer(serializers.ModelSerializer):
    """
    Serializer for ScheduledTask - User-friendly
    """
    schedule_description = serializers.SerializerMethodField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    frequency_display = serializers.CharField(source='get_frequency_display', read_only=True)
    status_text = serializers.SerializerMethodField()
    
    class Meta:
        model = ScheduledTask
        fields = [
            'id', 'name', 'description', 'category', 'category_display',
            'task_name', 'frequency', 'frequency_display',
            'hour', 'minute', 'day_of_week', 'day_of_month',
            'is_active', 'schedule_description', 'status_text',
            'last_run', 'total_runs', 'last_result', 'last_success',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'last_run', 'total_runs', 'last_result', 'last_success',
            'created_at', 'updated_at'
        ]
    
    def get_schedule_description(self, obj):
        """Get user-friendly schedule description"""
        return obj.get_schedule_description()
    
    def get_status_text(self, obj):
        """Get status in plain text"""
        if not obj.is_active:
            return 'Pausada'
        elif obj.total_runs == 0:
            return 'Nunca ejecutada'
        elif not obj.last_success:
            return 'Última ejecución falló'
        else:
            return 'Activa y funcionando'


class ScheduledTaskCreateSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for creating tasks
    """
    class Meta:
        model = ScheduledTask
        fields = [
            'name', 'description', 'category', 'task_name',
            'frequency', 'hour', 'minute', 'day_of_week', 'day_of_month',
            'is_active'
        ]
    
    def validate_hour(self, value):
        """Validate hour is between 0-23"""
        if not 0 <= value <= 23:
            raise serializers.ValidationError("Hora debe estar entre 0 y 23")
        return value
    
    def validate_minute(self, value):
        """Validate minute is between 0-59"""
        if not 0 <= value <= 59:
            raise serializers.ValidationError("Minuto debe estar entre 0 y 59")
        return value
    
    def validate_day_of_month(self, value):
        """Validate day of month"""
        if value is not None and not 1 <= value <= 31:
            raise serializers.ValidationError("Día del mes debe estar entre 1 y 31")
        return value
    
    def validate(self, data):
        """Cross-field validation"""
        frequency = data.get('frequency')
        
        # If weekly, day_of_week is required
        if frequency == 'weekly' and not data.get('day_of_week'):
            raise serializers.ValidationError({
                'day_of_week': 'Requerido para tareas semanales'
            })
        
        # If monthly, day_of_month is required
        if frequency == 'monthly' and not data.get('day_of_month'):
            raise serializers.ValidationError({
                'day_of_month': 'Requerido para tareas mensuales'
            })
        
        return data


class TaskTemplateSerializer(serializers.Serializer):
    """
    Serializer for task templates (pre-configured tasks)
    """
    id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    category = serializers.CharField()
    task_name = serializers.CharField()
    recommended_frequency = serializers.CharField()
    recommended_hour = serializers.IntegerField()
    why_useful = serializers.CharField()

