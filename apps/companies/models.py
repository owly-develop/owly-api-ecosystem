"""
Company models for multi-tenant architecture
"""
from django.db import models
from apps.core.models import TimestampedModel
import uuid


class Company(TimestampedModel):
    """
    Company/Organization model - Main tenant entity
    Each company can have multiple projects
    """
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('starter', 'Starter'),
        ('professional', 'Professional'),
        ('enterprise', 'Enterprise'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('trial', 'Trial'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    
    # Business Information
    legal_name = models.CharField(max_length=255, blank=True)
    tax_id = models.CharField(max_length=50, blank=True, help_text="Tax ID or VAT number")
    industry = models.CharField(max_length=100, blank=True)
    
    # Contact Information
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    
    # Address
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Subscription & Plan
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    subscription_ends_at = models.DateTimeField(null=True, blank=True)
    
    # Limits based on plan
    max_users = models.IntegerField(default=5)
    max_projects = models.IntegerField(default=10)
    max_leads = models.IntegerField(default=1000)
    max_storage_gb = models.IntegerField(default=5)
    
    # Settings
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    primary_color = models.CharField(max_length=7, default='#3B82F6', help_text="Hex color code")
    timezone = models.CharField(max_length=50, default='UTC')
    currency = models.CharField(max_length=3, default='USD')
    
    # Features enabled
    features = models.JSONField(default=dict, blank=True, help_text="Enabled features for this company")
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['plan']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def is_active(self):
        return self.status == 'active'
    
    @property
    def is_trial(self):
        return self.status == 'trial'
    
    def get_user_count(self):
        """Get total users in this company"""
        return self.users.count()
    
    def get_project_count(self):
        """Get total projects in this company"""
        return self.project_set.count()
    
    def can_add_user(self):
        """Check if company can add more users"""
        return self.get_user_count() < self.max_users
    
    def can_add_project(self):
        """Check if company can add more projects"""
        return self.get_project_count() < self.max_projects

