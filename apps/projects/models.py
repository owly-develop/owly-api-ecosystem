"""
Project models
"""
from django.db import models
from django.utils.text import slugify
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
    
    CRM_CHOICES = [
        ('monday', 'Monday.com'),
        ('salesforce', 'Salesforce'),
        ('hubspot', 'HubSpot'),
        ('none', 'None'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    developer = models.CharField(max_length=255, blank=True)
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='residential')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    description = models.TextField()
    tagline = models.CharField(max_length=255, blank=True)
    
    # Location
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='CO')
    postal_code = models.CharField(max_length=20, blank=True)
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
    price_from = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_to = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='COP')
    average_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    measure_unit = models.CharField(max_length=10, default='m²')
    
    # Financial settings
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Interest rate percentage")
    show_prices = models.BooleanField(default=True)
    allow_quote = models.BooleanField(default=True)
    
    # Features and Amenities
    amenities = models.JSONField(default=list, blank=True)
    features = models.JSONField(default=list, blank=True)
    economic_profiles = models.JSONField(default=list, blank=True)
    
    # Dates
    launch_date = models.DateField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    construction_start_date = models.DateField(null=True, blank=True)
    construction_progress = models.IntegerField(default=0, help_text="Construction progress percentage (0-100)")
    
    # Media
    main_image = models.URLField(blank=True)
    media_items = models.JSONField(default=list, blank=True, help_text="Array of media items with type, reference, and url")
    brochure_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)
    
    # Visualization
    visualization_config = models.JSONField(default=dict, blank=True)
    svg_floor_plan = models.TextField(blank=True)
    svg_floor_plan_config = models.JSONField(default=dict, blank=True)
    interactive_units = models.JSONField(default=list, blank=True)
    orbit_view_project = models.CharField(max_length=255, blank=True)
    orbit_view_amenities = models.CharField(max_length=255, blank=True)
    orbit_views_string = models.CharField(max_length=255, blank=True, help_text="Legacy orbit views reference")
    
    # Design/Branding
    background_color = models.CharField(max_length=7, blank=True, help_text="Hex color code")
    accent_color = models.CharField(max_length=7, blank=True, help_text="Hex color code")
    status_colors = models.JSONField(default=dict, blank=True, help_text="Colors for different unit statuses")
    
    # Documents
    documents = models.JSONField(default=list, blank=True)
    
    # CRM Integration
    crm = models.CharField(max_length=20, choices=CRM_CHOICES, default='none')
    crm_config = models.JSONField(default=dict, blank=True, help_text="CRM configuration (API keys, board IDs, etc)")
    crm_list = models.JSONField(default=list, blank=True)
    
    # Scoring/Lead qualification
    score_weights = models.JSONField(default=dict, blank=True, help_text="Weights for scoring leads")
    
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
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
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
        ('optioned', 'Optioned'),
        ('unavailable', 'Unavailable'),
    ]
    
    PRICE_TYPE_CHOICES = [
        ('fixedPrice', 'Fixed Price'),
        ('smlvPrice', 'SMLV Price'),
    ]
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='units'
    )
    
    block = models.ForeignKey(
        'Block',
        on_delete=models.CASCADE,
        related_name='units',
        null=True,
        blank=True
    )
    
    typology = models.ForeignKey(
        'Typology',
        on_delete=models.SET_NULL,
        related_name='units',
        null=True,
        blank=True
    )
    
    # Basic Information
    name = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=50, default='')
    unit_number = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    glb_code = models.CharField(max_length=255, blank=True)
    unit_type = models.CharField(max_length=100, blank=True, help_text="e.g., Studio, 1BR, 2BR, Penthouse")
    typology_slug = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    # Specifications
    floor = models.CharField(max_length=10, blank=True)
    bedrooms = models.CharField(max_length=10, blank=True)
    bathrooms = models.CharField(max_length=10, blank=True)
    
    # Areas
    private_area = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    build_area = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    area_sqm = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    terrace_area = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    terrace_sqm = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    terrace_private_area = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    balcony_area = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mezzanine_area = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    # Counts
    terrace_number = models.IntegerField(default=0)
    balcony_number = models.IntegerField(default=0)
    
    # Pricing
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    fixed_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_type = models.CharField(max_length=20, choices=PRICE_TYPE_CHOICES, default='fixedPrice')
    currency = models.CharField(max_length=3, default='COP')
    price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Complementary units
    complementary_unit = models.JSONField(default=dict, blank=True)
    complementary_units = models.JSONField(default=list, blank=True)
    
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
        # Auto-generate slug from block and unit number if not provided
        if not self.slug and self.block:
            self.slug = slugify(f"{self.block.slug}-{self.unit_number}")
        elif not self.slug:
            self.slug = slugify(f"{self.project.slug}-{self.unit_number}")
        
        # Auto-fill name if not provided
        if not self.name:
            self.name = self.unit_number
        
        # Calculate price per sqm
        active_price = self.price or self.fixed_price
        active_area = self.area_sqm or self.private_area or self.build_area
        if active_area and active_price:
            self.price_per_sqm = active_price / active_area
        super().save(*args, **kwargs)


class Stage(TenantAwareModel, SoftDeleteModel):
    """
    Project stage/phase (e.g., Stage 1, Stage 2)
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='stages'
    )
    
    # Basic Information
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    code = models.CharField(max_length=50, blank=True)
    glb_code = models.CharField(max_length=255, blank=True)
    stage_number = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)
    
    # Housing typology
    housing_typology = models.CharField(max_length=100, blank=True, help_text="e.g., NOVIS, VIS")
    
    # Financial
    separation = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Separation percentage")
    down_payment = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Down payment percentage")
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Discount percentage")
    projected_increase = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Projected price increase percentage")
    
    # Dates
    closing_date = models.DateField(null=True, blank=True)
    
    # Media
    media_items = models.JSONField(default=list, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['project', 'stage_number', 'name']
        unique_together = ['project', 'slug']
        indexes = [
            models.Index(fields=['project', 'stage_number']),
        ]
    
    def __str__(self):
        return f"{self.project.name} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.project.slug}-{self.name}")
        super().save(*args, **kwargs)


class Block(TenantAwareModel, SoftDeleteModel):
    """
    Block/Tower within a stage
    """
    stage = models.ForeignKey(
        Stage,
        on_delete=models.CASCADE,
        related_name='blocks'
    )
    
    # Basic Information
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    code = models.CharField(max_length=50, blank=True)
    glb_code = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    
    # Visualization
    target_frame = models.CharField(max_length=10, blank=True)
    
    # Price list reference
    price_list = models.CharField(max_length=255, blank=True)
    smlv_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="SMLV price")
    
    # Media
    media_items = models.JSONField(default=list, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['stage', 'code', 'name']
        unique_together = ['stage', 'slug']
        indexes = [
            models.Index(fields=['stage', 'code']),
        ]
    
    def __str__(self):
        return f"{self.stage.name} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.stage.slug}-{self.name}")
        super().save(*args, **kwargs)


class Typology(TenantAwareModel, SoftDeleteModel):
    """
    Unit typology/type (e.g., Type A, Type B, 1BR, 2BR)
    """
    stage = models.ForeignKey(
        Stage,
        on_delete=models.CASCADE,
        related_name='typologies'
    )
    
    # Basic Information
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    code = models.CharField(max_length=50, blank=True)
    glb_code = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    
    # Specifications
    bedrooms = models.CharField(max_length=10, blank=True)
    bathrooms = models.CharField(max_length=10, blank=True)
    
    # Visualization
    target_frame = models.CharField(max_length=10, blank=True)
    
    # Media
    media_items = models.JSONField(default=list, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['stage', 'code', 'name']
        unique_together = ['stage', 'slug']
        indexes = [
            models.Index(fields=['stage', 'code']),
        ]
    
    def __str__(self):
        return f"{self.stage.name} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.stage.slug}-{self.name}")
        super().save(*args, **kwargs)


class Amenity(TenantAwareModel, SoftDeleteModel):
    """
    Project or Block amenity
    """
    AMENITY_TYPE_CHOICES = [
        ('project', 'Project'),
        ('block', 'Block'),
    ]
    
    # Parent can be either project or block
    parent_type = models.CharField(max_length=10, choices=AMENITY_TYPE_CHOICES)
    parent_id = models.CharField(max_length=255)  # UUID of parent (project or block)
    
    # Basic Information
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    glb_code = models.CharField(max_length=255, blank=True)
    icon = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    
    # Location
    area = models.CharField(max_length=50, blank=True)
    floor = models.IntegerField(null=True, blank=True)
    
    # Media
    media_items = models.JSONField(default=list, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['parent_type', 'parent_id', 'name']
        indexes = [
            models.Index(fields=['parent_type', 'parent_id']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.parent_type})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.parent_id}-{self.name}")
        super().save(*args, **kwargs)


class OrbitView(TenantAwareModel, SoftDeleteModel):
    """
    360° Orbit view configuration
    """
    ORBIT_TYPE_CHOICES = [
        ('project', 'Project'),
        ('amenities', 'Amenities'),
        ('unit-types', 'Unit Types'),
        ('block', 'Block'),
    ]
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='orbit_views'
    )
    
    # Basic Information
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    code = models.CharField(max_length=50, blank=True)
    orbit_type = models.CharField(max_length=20, choices=ORBIT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    
    # Configuration
    images_folder = models.CharField(max_length=255, blank=True)
    images_extension = models.CharField(max_length=10, default='webp')
    num_images = models.IntegerField(default=0)
    glb_file = models.CharField(max_length=500, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['project', 'orbit_type', 'name']
        indexes = [
            models.Index(fields=['project', 'orbit_type']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return f"{self.project.name} - {self.name}"

