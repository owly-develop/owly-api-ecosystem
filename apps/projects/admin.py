"""
Project admin configuration
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Project, Unit, Stage, Block, Typology, Amenity, OrbitView


class UnitInline(admin.TabularInline):
    """Inline for managing units within a project"""
    model = Unit
    extra = 0
    fields = ['unit_number', 'unit_type', 'floor', 'bedrooms', 'bathrooms', 'area_sqm', 'price', 'status']
    readonly_fields = []
    can_delete = False
    show_change_link = True
    max_num = 20  # Show max 20 units in inline


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'code_link', 'name', 'copy_id_button', 'type_badge', 'status_badge',
        'city', 'units_display', 'occupancy_display',
        'price_range_display', 'featured', 'created_at'
    ]
    list_filter = [
        'status',
        'type',
        'featured',
        'company',
        'city',
        'state',
        'created_at'
    ]
    search_fields = ['name', 'code', 'city', 'state', 'description', 'address']
    readonly_fields = [
        'id', 'created_at', 'updated_at',
        'view_count', 'lead_count', 'quote_count',
        'occupancy_rate'
    ]
    date_hierarchy = 'created_at'
    list_per_page = 25
    inlines = [UnitInline]
    actions = ['mark_as_active', 'mark_as_featured', 'export_projects']
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'id',
                ('name', 'code'),
                ('company', 'developer'),
                ('type', 'status'),
                'description',
                'tagline'
            )
        }),
        ('Location', {
            'fields': (
                'address',
                ('city', 'state'),
                ('country', 'postal_code'),
                ('latitude', 'longitude'),
                ('neighborhood', 'zone')
            )
        }),
        ('Units & Availability', {
            'fields': (
                ('total_units', 'available_units'),
                ('sold_units', 'reserved_units')
            )
        }),
        ('Pricing', {
            'fields': (
                ('price_from', 'price_to', 'currency'),
                ('average_price', 'price_per_sqm')
            )
        }),
        ('Timeline', {
            'fields': (
                ('launch_date', 'delivery_date'),
                ('construction_start_date', 'construction_progress')
            )
        }),
        ('Features', {
            'fields': ('amenities', 'features'),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': (
                'main_image',
                'media_items',
                'brochure_url',
                'video_url'
            ),
            'classes': ('collapse',)
        }),
        ('Visualization', {
            'fields': (
                'visualization_config',
                'svg_floor_plan',
                'svg_floor_plan_config',
                'interactive_units'
            ),
            'classes': ('collapse',)
        }),
        ('Marketing', {
            'fields': (
                'featured',
                'tags',
                ('meta_title', 'meta_description')
            )
        }),
        ('Stats & Metadata', {
            'fields': (
                ('view_count', 'lead_count', 'quote_count'),
                ('project_manager', 'last_activity_date'),
                ('created_at', 'updated_at')
            ),
            'classes': ('collapse',)
        })
    )
    
    def code_link(self, obj):
        url = reverse('admin:projects_project_change', args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, obj.code)
    code_link.short_description = 'Code'
    code_link.admin_order_field = 'code'
    
    def copy_id_button(self, obj):
        return format_html(
            '<div style="font-family: monospace; font-size: 11px;">'
            '<span title="{}" style="cursor: pointer;" onclick="navigator.clipboard.writeText(\'{}\'); alert(\'ID copiado!\')">📋 {}</span>'
            '</div>',
            obj.id,
            obj.id,
            str(obj.id)[:8] + '...'
        )
    copy_id_button.short_description = 'ID (click to copy)'
    
    def type_badge(self, obj):
        colors = {
            'residential': '#007bff',
            'commercial': '#28a745',
            'mixed_use': '#fd7e14',
            'industrial': '#6c757d'
        }
        color = colors.get(obj.type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_type_display()
        )
    type_badge.short_description = 'Type'
    type_badge.admin_order_field = 'type'
    
    def status_badge(self, obj):
        colors = {
            'planning': '#6c757d',
            'pre_launch': '#17a2b8',
            'active': '#28a745',
            'sold_out': '#dc3545',
            'completed': '#007bff',
            'on_hold': '#ffc107',
            'cancelled': '#dc3545'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def units_display(self, obj):
        return f"{obj.available_units}/{obj.total_units}"
    units_display.short_description = 'Units (Avail/Total)'
    
    def occupancy_display(self, obj):
        rate = float(obj.occupancy_rate)
        if rate >= 80:
            color = '#28a745'
        elif rate >= 50:
            color = '#ffc107'
        else:
            color = '#dc3545'
        
        rate_text = f"{rate:.1f}%"
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            rate_text
        )
    occupancy_display.short_description = 'Occupancy'
    
    def price_range_display(self, obj):
        price_from = f"${float(obj.price_from):,.0f}"
        price_to = f"${float(obj.price_to):,.0f}"
        return f"{price_from} - {price_to}"
    price_range_display.short_description = 'Price Range'
    
    def mark_as_active(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} projects marked as active.')
    mark_as_active.short_description = 'Mark selected as Active'
    
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f'{updated} projects marked as featured.')
    mark_as_featured.short_description = 'Mark selected as Featured'
    
    def export_projects(self, request, queryset):
        self.message_user(request, f'Export functionality coming soon for {queryset.count()} projects.')
    export_projects.short_description = 'Export selected projects'


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = [
        'unit_number', 'project_link', 'unit_type', 'status_badge',
        'floor', 'bedrooms', 'bathrooms', 'area_sqm',
        'price_display', 'created_at'
    ]
    list_filter = [
        'status',
        'unit_type',
        'project__name',
        'floor',
        'bedrooms',
        'orientation'
    ]
    search_fields = ['unit_number', 'project__name', 'project__code', 'unit_type']
    readonly_fields = ['id', 'company', 'price_per_sqm', 'created_at', 'updated_at']
    list_per_page = 50
    actions = ['mark_as_available', 'mark_as_sold', 'export_units']
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('project', 'company'),
                ('unit_number', 'unit_type'),
                'status'
            )
        }),
        ('Specifications', {
            'fields': (
                'floor',
                ('bedrooms', 'bathrooms'),
                ('area_sqm', 'terrace_sqm'),
                ('orientation', 'view_type')
            )
        }),
        ('Pricing', {
            'fields': (
                ('price', 'currency'),
                'price_per_sqm'
            )
        }),
        ('Features & Media', {
            'fields': (
                'features',
                'floor_plan_image',
                'images',
                'virtual_tour_url'
            ),
            'classes': ('collapse',)
        }),
        ('SVG Visualization', {
            'fields': ('svg_element_id', 'svg_clickable_area'),
            'classes': ('collapse',)
        }),
        ('Reservation/Sale Info', {
            'fields': (
                ('reserved_by', 'reserved_date'),
                ('sold_to', 'sold_date')
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def project_link(self, obj):
        url = reverse('admin:projects_project_change', args=[obj.project.id])
        return format_html('<a href="{}">{}</a>', url, obj.project.name)
    project_link.short_description = 'Project'
    
    def status_badge(self, obj):
        colors = {
            'available': '#28a745',
            'reserved': '#ffc107',
            'sold': '#dc3545',
            'blocked': '#6c757d'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def price_display(self, obj):
        return f"${float(obj.price):,.0f}"
    price_display.short_description = 'Price'
    price_display.admin_order_field = 'price'
    
    def mark_as_available(self, request, queryset):
        updated = queryset.update(status='available')
        self.message_user(request, f'{updated} units marked as available.')
    mark_as_available.short_description = 'Mark selected as Available'
    
    def mark_as_sold(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='sold', sold_date=timezone.now())
        self.message_user(request, f'{updated} units marked as sold.')
    mark_as_sold.short_description = 'Mark selected as Sold'
    
    def export_units(self, request, queryset):
        self.message_user(request, f'Export functionality coming soon for {queryset.count()} units.')
    export_units.short_description = 'Export selected units'


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'stage_number', 'housing_typology', 'closing_date', 'created_at']
    list_filter = ['project', 'housing_typology', 'created_at']
    search_fields = ['name', 'code', 'slug', 'project__name']
    readonly_fields = ['id', 'slug', 'created_at', 'updated_at']
    list_per_page = 50
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'project',
                ('name', 'code'),
                'slug',
                ('stage_number', 'glb_code'),
                'description',
                'housing_typology'
            )
        }),
        ('Financial', {
            'fields': (
                ('separation', 'down_payment'),
                ('discount', 'projected_increase')
            )
        }),
        ('Dates', {
            'fields': ('closing_date',)
        }),
        ('Media & Metadata', {
            'fields': ('media_items', 'metadata'),
            'classes': ('collapse',)
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ['name', 'stage', 'code', 'target_frame', 'created_at']
    list_filter = ['stage__project', 'stage', 'created_at']
    search_fields = ['name', 'code', 'slug', 'stage__name']
    readonly_fields = ['id', 'slug', 'created_at', 'updated_at']
    list_per_page = 50
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'stage',
                ('name', 'code'),
                'slug',
                ('glb_code', 'target_frame'),
                'description'
            )
        }),
        ('Pricing', {
            'fields': (
                ('price_list', 'smlv_price'),
            )
        }),
        ('Media & Metadata', {
            'fields': ('media_items', 'metadata'),
            'classes': ('collapse',)
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Typology)
class TypologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'stage', 'code', 'bedrooms', 'bathrooms', 'target_frame', 'created_at']
    list_filter = ['stage__project', 'stage', 'bedrooms', 'bathrooms', 'created_at']
    search_fields = ['name', 'code', 'slug', 'stage__name']
    readonly_fields = ['id', 'slug', 'created_at', 'updated_at']
    list_per_page = 50
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'stage',
                ('name', 'code'),
                'slug',
                ('glb_code', 'target_frame'),
                'description'
            )
        }),
        ('Specifications', {
            'fields': (
                ('bedrooms', 'bathrooms'),
            )
        }),
        ('Media & Metadata', {
            'fields': ('media_items', 'metadata'),
            'classes': ('collapse',)
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_type', 'parent_id', 'icon', 'floor', 'created_at']
    list_filter = ['parent_type', 'floor', 'created_at']
    search_fields = ['name', 'slug', 'glb_code', 'parent_id']
    readonly_fields = ['id', 'slug', 'created_at', 'updated_at']
    list_per_page = 50
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('parent_type', 'parent_id'),
                'name',
                'slug',
                ('glb_code', 'icon'),
                'description'
            )
        }),
        ('Location', {
            'fields': (
                ('area', 'floor'),
            )
        }),
        ('Media & Metadata', {
            'fields': ('media_items', 'metadata'),
            'classes': ('collapse',)
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(OrbitView)
class OrbitViewAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'orbit_type', 'num_images', 'images_extension', 'created_at']
    list_filter = ['project', 'orbit_type', 'created_at']
    search_fields = ['name', 'slug', 'code', 'project__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_per_page = 50
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'project',
                ('name', 'code'),
                'slug',
                'orbit_type',
                'description'
            )
        }),
        ('Configuration', {
            'fields': (
                'images_folder',
                ('images_extension', 'num_images'),
                'glb_file'
            )
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

