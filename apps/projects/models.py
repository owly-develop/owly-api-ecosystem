"""
Project models
"""
from django.db import models
from apps.core.models import TenantAwareModel, SoftDeleteModel


class Project(TenantAwareModel, SoftDeleteModel):
    """
    Real estate project model
    """
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('pre_launch', 'Pre-Launch'),
        ('active', 'Active'),
        ('sold_out', 'Sold Out'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]
    
    TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('mixed_use', 'Mixed Use'),
        ('industrial', 'Industrial'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    developer = models.CharField(max_length=255, blank=True)
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='residential')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    description = models.TextField()
    tagline = models.CharField(max_length=255, blank=True)
    
    # Location
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='USA')
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    neighborhood = models.CharField(max_length=100, blank=True)
    zone = models.CharField(max_length=100, blank=True)
    
    # Units
    total_units = models.IntegerField(default=0)
    available_units = models.IntegerField(default=0)
    sold_units = models.IntegerField(default=0)
    reserved_units = models.IntegerField(default=0)
    
    # Pricing
    price_from = models.DecimalField(max_digits=12, decimal_places=2)
    price_to = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    average_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Features and Amenities
    amenities = models.JSONField(default=list, blank=True)
    features = models.JSONField(default=list, blank=True)
    
    # Dates
    launch_date = models.DateField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    construction_start_date = models.DateField(null=True, blank=True)
    construction_progress = models.IntegerField(default=0, help_text="Construction progress percentage (0-100)")
    
    # Media
    main_image = models.URLField(blank=True)
    images = models.JSONField(default=list, blank=True)
    brochure_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)
    
    # Visualization
    visualization_config = models.JSONField(default=dict, blank=True)
    svg_floor_plan = models.TextField(blank=True)
    svg_floor_plan_config = models.JSONField(default=dict, blank=True)
    interactive_units = models.JSONField(default=list, blank=True)
    
    # Documents
    documents = models.JSONField(default=list, blank=True)
    
    # Team
    project_manager = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_projects'
    )
    
    # Marketing
    featured = models.BooleanField(default=False)
    tags = models.JSONField(default=list, blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    
    # Stats
    view_count = models.IntegerField(default=0)
    lead_count = models.IntegerField(default=0)
    quote_count = models.IntegerField(default=0)
    last_activity_date = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['company', 'status']),
            models.Index(fields=['code']),
            models.Index(fields=['city', 'state']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    @property
    def occupancy_rate(self):
        """Calculate occupancy rate (sold + reserved / total)"""
        if self.total_units == 0:
            return 0
        occupied = (self.sold_units or 0) + (self.reserved_units or 0)
        return (occupied / self.total_units) * 100


class Unit(TenantAwareModel, SoftDeleteModel):
    """
    Individual unit within a project
    """
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold'),
        ('blocked', 'Blocked'),
    ]
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='units'
    )
    
    # Basic Information
    unit_number = models.CharField(max_length=50)
    unit_type = models.CharField(max_length=100, help_text="e.g., Studio, 1BR, 2BR, Penthouse")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    # Specifications
    floor = models.IntegerField()
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    area_sqm = models.DecimalField(max_digits=8, decimal_places=2)
    terrace_sqm = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    # Pricing
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Features
    features = models.JSONField(default=list, blank=True)
    orientation = models.CharField(max_length=50, blank=True, help_text="e.g., North, South, East, West")
    view_type = models.CharField(max_length=100, blank=True, help_text="e.g., Ocean view, City view")
    
    # Media
    floor_plan_image = models.URLField(blank=True)
    images = models.JSONField(default=list, blank=True)
    virtual_tour_url = models.URLField(blank=True)
    
    # SVG Visualization
    svg_element_id = models.CharField(max_length=100, blank=True)
    svg_clickable_area = models.TextField(blank=True, help_text="SVG path or coordinates")
    
    # Documents
    documents = models.JSONField(default=list, blank=True)
    
    # Reservation/Sale info
    reserved_by = models.ForeignKey(
        'leads.Lead',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reserved_units'
    )
    reserved_date = models.DateTimeField(null=True, blank=True)
    sold_to = models.CharField(max_length=255, blank=True)
    sold_date = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['project', 'floor', 'unit_number']
        unique_together = ['project', 'unit_number']
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['unit_number']),
        ]
    
    def __str__(self):
        return f"{self.project.name} - Unit {self.unit_number}"
    
    def save(self, *args, **kwargs):
        # Calculate price per sqm
        if self.area_sqm and self.price:
            self.price_per_sqm = self.price / self.area_sqm
        super().save(*args, **kwargs)

