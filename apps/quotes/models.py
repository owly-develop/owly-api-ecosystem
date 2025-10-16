"""
Quote models
"""
from django.db import models
from apps.core.models import TenantAwareModel


class Quote(TenantAwareModel):
    """
    Quote/Proposal model
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('viewed', 'Viewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]
    
    quote_number = models.CharField(max_length=50, unique=True, editable=False)
    
    # Relations
    lead = models.ForeignKey(
        'leads.Lead',
        on_delete=models.CASCADE,
        related_name='quotes'
    )
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='quotes'
    )
    unit = models.ForeignKey(
        'projects.Unit',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quotes'
    )
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Pricing
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Financing
    financing_offered = models.BooleanField(default=False)
    financing_terms = models.JSONField(default=dict, blank=True)
    
    # Dates
    valid_until = models.DateTimeField()
    sent_date = models.DateTimeField(null=True, blank=True)
    viewed_date = models.DateTimeField(null=True, blank=True)
    accepted_date = models.DateTimeField(null=True, blank=True)
    rejected_date = models.DateTimeField(null=True, blank=True)
    
    # Additional Items
    additional_items = models.JSONField(default=list, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    terms_and_conditions = models.TextField(blank=True)
    
    # Created by
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_quotes'
    )
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['company', 'status']),
            models.Index(fields=['quote_number']),
            models.Index(fields=['lead']),
            models.Index(fields=['project']),
        ]
    
    def __str__(self):
        return f"{self.quote_number} - {self.lead.full_name}"
    
    def save(self, *args, **kwargs):
        if not self.quote_number:
            from django.utils import timezone
            import uuid
            year = timezone.now().year
            unique_suffix = str(uuid.uuid4())[:8].upper()
            company_code = str(self.company.slug)[:3].upper() if self.company else 'XXX'
            self.quote_number = f"QT-{company_code}-{year}-{unique_suffix}"
        
        # Calculate totals (ensure Decimal types)
        from decimal import Decimal
        self.subtotal = self.unit_price - self.discount_amount
        self.tax_amount = self.subtotal * (Decimal(str(self.tax_percentage)) / Decimal('100'))
        self.total = self.subtotal + self.tax_amount
        
        super().save(*args, **kwargs)


class QuoteTemplate(TenantAwareModel):
    """
    Template for generating quotes
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Template content
    content = models.TextField(help_text="HTML template content")
    
    # Default settings
    default_terms = models.TextField(blank=True)
    default_validity_days = models.IntegerField(default=30)
    
    # Metadata
    is_active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

