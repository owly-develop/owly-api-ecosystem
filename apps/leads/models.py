"""
Lead models
"""
from django.db import models
from apps.core.models import TenantAwareModel, SoftDeleteModel


class Lead(TenantAwareModel, SoftDeleteModel):
    """
    Lead/Prospect model
    """
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
        ('nurturing', 'Nurturing'),
    ]
    
    SOURCE_CHOICES = [
        ('website', 'Website'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('whatsapp', 'WhatsApp'),
        ('referral', 'Referral'),
        ('cold_call', 'Cold Call'),
        ('trade_show', 'Trade Show'),
        ('partner', 'Partner'),
        ('other', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Identification
    lead_number = models.CharField(max_length=50, unique=True, editable=False)
    
    # Personal Information
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    alternate_phone = models.CharField(max_length=50, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=100, blank=True)
    
    # Status and Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='website')
    source_detail = models.CharField(max_length=255, blank=True)
    lead_score = models.IntegerField(default=0, help_text="Lead score 0-100")
    
    # AI Scoring and Predictions
    ai_close_probability = models.IntegerField(
        default=0,
        help_text="AI-predicted probability of closing (0-100)"
    )
    ai_insights = models.JSONField(default=dict, blank=True)
    conversion_factors = models.JSONField(default=dict, blank=True)
    
    # Assignment
    assigned_to = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads'
    )
    assigned_date = models.DateTimeField(null=True, blank=True)
    assigned_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads_assigned_by_me'
    )
    
    # Interaction and Engagement
    last_contact_date = models.DateTimeField(null=True, blank=True)
    last_interaction_date = models.DateTimeField(null=True, blank=True)
    interaction_count = models.IntegerField(default=0)
    next_follow_up_date = models.DateTimeField(null=True, blank=True)
    
    # Interests and Preferences
    interested_projects = models.ManyToManyField(
        'projects.Project',
        related_name='interested_leads',
        blank=True
    )
    interested_units = models.ManyToManyField(
        'projects.Unit',
        related_name='interested_leads',
        blank=True
    )
    budget_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    budget_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    budget_currency = models.CharField(max_length=3, default='USD')
    financing = models.BooleanField(default=False)
    down_payment_percentage = models.IntegerField(null=True, blank=True)
    
    # Preferences
    preferences = models.JSONField(default=dict, blank=True, help_text="Property preferences")
    
    # Quotes
    quote_count = models.IntegerField(default=0)
    total_quote_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_quote_date = models.DateTimeField(null=True, blank=True)
    
    # Notes and Communication
    notes = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    # Conversion
    converted_to_customer = models.BooleanField(default=False)
    customer_id = models.CharField(max_length=100, blank=True)
    conversion_date = models.DateTimeField(null=True, blank=True)
    
    # GDPR / Privacy
    consent_given = models.BooleanField(default=False)
    consent_date = models.DateTimeField(null=True, blank=True)
    marketing_opt_in = models.BooleanField(default=False)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['company', 'status']),
            models.Index(fields=['lead_number']),
            models.Index(fields=['email']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['-lead_score']),
            models.Index(fields=['-ai_close_probability']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.lead_number})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.lead_number:
            # Generate lead number (unique globally)
            from django.utils import timezone
            import uuid
            year = timezone.now().year
            # Use UUID for true uniqueness
            unique_suffix = str(uuid.uuid4())[:8].upper()
            company_code = str(self.company.slug)[:3].upper() if self.company else 'XXX'
            self.lead_number = f"LEAD-{company_code}-{year}-{unique_suffix}"
        super().save(*args, **kwargs)

