"""
Activity models
"""
from django.db import models
from apps.core.models import TenantAwareModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Activity(TenantAwareModel):
    """
    Activity/Interaction model for tracking all actions
    """
    TYPE_CHOICES = [
        ('call', 'Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('note', 'Note'),
        ('task', 'Task'),
        ('quote_sent', 'Quote Sent'),
        ('quote_viewed', 'Quote Viewed'),
        ('quote_accepted', 'Quote Accepted'),
        ('status_change', 'Status Change'),
        ('assignment', 'Assignment'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Type and Status
    activity_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    
    # Title and Description
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Related Object (Generic relation)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    related_object = GenericForeignKey('content_type', 'object_id')
    
    # User who performed the activity
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='activities'
    )
    
    # Timing
    scheduled_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    
    # Additional data
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name_plural = 'Activities'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['company', 'activity_type']),
            models.Index(fields=['user']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.activity_type} - {self.title}"

