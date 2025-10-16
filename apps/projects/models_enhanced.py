# 🏗️ MODELOS MEJORADOS - Projects y Units
# Este archivo documenta los campos adicionales propuestos
# Para implementar: copiar estos campos a models.py y crear nueva migración

from django.db import models
from apps.core.models import TenantAwareModel, SoftDeleteModel
from decimal import Decimal


class ProjectEnhanced(TenantAwareModel, SoftDeleteModel):
    """
    Project model mejorado con campos para inventario robusto
    CAMPOS ADICIONALES PROPUESTOS - Agregar a models.py
    """
    
    # ========== CAMPOS EXISTENTES ==========
    # (Mantener todos los campos actuales)
    # name, code, type, status, description, etc.
    
    # ========== NUEVOS CAMPOS FINANCIEROS ==========
    
    # Costos y Márgenes
    cost_per_unit = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="Costo promedio por unidad"
    )
    total_development_cost = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True,
        help_text="Costo total del desarrollo"
    )
    projected_revenue = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True,
        help_text="Revenue proyectado"
    )
    actual_revenue = models.DecimalField(
        max_digits=15, decimal_places=2, default=0,
        help_text="Revenue real recibido"
    )
    profit_margin_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="Margen de ganancia esperado"
    )
    
    # Esquemas de Pago Disponibles
    payment_plans = models.JSONField(
        default=list, blank=True,
        help_text="""Planes de pago disponibles. Ejemplo:
        [
            {
                "name": "Plan A - 30/70",
                "down_payment_percentage": 30,
                "financing_months": 120,
                "interest_rate": 8.5,
                "description": "30% enganche, 70% financiado a 10 años"
            },
            {
                "name": "Plan B - Cash",
                "down_payment_percentage": 100,
                "discount_percentage": 5,
                "description": "Pago de contado con 5% descuento"
            }
        ]"""
    )
    
    # Promociones Activas
    active_promotions = models.JSONField(
        default=list, blank=True,
        help_text="""Promociones activas. Ejemplo:
        [
            {
                "name": "Early Bird Discount",
                "discount_percentage": 10,
                "valid_until": "2024-12-31",
                "conditions": "Primeras 20 unidades",
                "units_remaining": 8
            }
        ]"""
    )
    
    # ========== FASES DE CONSTRUCCIÓN ==========
    
    construction_phases = models.JSONField(
        default=list, blank=True,
        help_text="""Fases del proyecto. Ejemplo:
        [
            {
                "phase": "Foundation",
                "progress": 100,
                "start_date": "2023-01-01",
                "end_date": "2023-06-30",
                "status": "completed"
            },
            {
                "phase": "Structure",
                "progress": 75,
                "start_date": "2023-07-01",
                "estimated_end": "2024-03-31",
                "status": "in_progress"
            },
            {
                "phase": "Finishing",
                "progress": 0,
                "start_date": null,
                "estimated_start": "2024-04-01",
                "status": "not_started"
            }
        ]"""
    )
    
    current_phase = models.CharField(
        max_length=100, blank=True,
        help_text="Fase actual de construcción"
    )
    
    next_milestone = models.JSONField(
        default=dict, blank=True,
        help_text="""Próximo hito. Ejemplo:
        {
            "name": "Completion of Structure",
            "date": "2024-03-31",
            "description": "All floors completed"
        }"""
    )
    
    # ========== DOCUMENTACIÓN LEGAL ==========
    
    building_permit_number = models.CharField(max_length=100, blank=True)
    building_permit_date = models.DateField(null=True, blank=True)
    building_permit_expires = models.DateField(null=True, blank=True)
    environmental_license = models.CharField(max_length=100, blank=True)
    use_permit = models.CharField(max_length=100, blank=True)
    
    legal_documents = models.JSONField(
        default=list, blank=True,
        help_text="""Documentos legales. Ejemplo:
        [
            {
                "type": "escritura_terreno",
                "number": "ESC-2024-001",
                "date": "2024-01-15",
                "url": "https://s3.../document.pdf",
                "expiry": null
            },
            {
                "type": "permiso_construccion",
                "number": "PC-2024-045",
                "date": "2024-02-01",
                "url": "https://s3.../permit.pdf",
                "expiry": "2026-02-01"
            }
        ]"""
    )
    
    # ========== MARKETING AVANZADO ==========
    
    marketing_campaigns = models.JSONField(
        default=list, blank=True,
        help_text="""Campañas de marketing. Ejemplo:
        [
            {
                "name": "Launch Campaign",
                "budget": 50000,
                "start_date": "2024-01-01",
                "end_date": "2024-03-31",
                "channels": ["Facebook", "Instagram", "Google Ads"],
                "leads_generated": 234,
                "conversions": 45,
                "roi": 1.8
            }
        ]"""
    )
    
    seo_keywords = models.JSONField(default=list, blank=True)
    virtual_tour_enabled = models.BooleanField(default=False)
    show_on_website = models.BooleanField(default=True)
    show_on_marketplace = models.BooleanField(
        default=False,
        help_text="Mostrar en portales inmobiliarios externos"
    )
    
    # ========== INVENTARIO DETALLADO ==========
    
    inventory_breakdown = models.JSONField(
        default=dict, blank=True,
        help_text="""Breakdown del inventario. Ejemplo:
        {
            "by_type": {
                "1BR": {"total": 30, "available": 12, "sold": 15, "reserved": 3},
                "2BR": {"total": 60, "available": 25, "sold": 30, "reserved": 5}
            },
            "by_floor_range": {
                "1-5": {"available": 15, "sold": 25},
                "6-10": {"available": 20, "sold": 20}
            },
            "by_price_range": {
                "200k-300k": {"available": 25},
                "300k-400k": {"available": 35}
            },
            "by_orientation": {
                "north": {"available": 15},
                "south": {"available": 20},
                "east": {"available": 10},
                "west": {"available": 3}
            }
        }"""
    )
    
    # ========== GARANTÍAS Y POST-VENTA ==========
    
    warranty_period_years = models.IntegerField(
        default=1,
        help_text="Años de garantía del proyecto"
    )
    warranty_details = models.TextField(
        blank=True,
        help_text="Detalles de qué cubre la garantía"
    )
    after_sales_contact = models.EmailField(blank=True)
    after_sales_phone = models.CharField(max_length=50, blank=True)
    maintenance_company = models.CharField(max_length=255, blank=True)
    
    # ========== MÉTODOS CALCULADOS ==========
    
    def calculate_profit_margin(self):
        """Calcular margen de ganancia"""
        if self.total_development_cost and self.projected_revenue:
            profit = self.projected_revenue - self.total_development_cost
            return (profit / self.projected_revenue) * 100
        return 0
    
    def get_sales_velocity(self):
        """Calcular velocidad de ventas (unidades/mes)"""
        # Implementar cálculo basado en ventas históricas
        pass
    
    def update_inventory_breakdown(self):
        """Actualizar breakdown del inventario"""
        # Recalcular desde las units
        pass


class UnitEnhanced(TenantAwareModel, SoftDeleteModel):
    """
    Unit model mejorado con workflow completo
    CAMPOS ADICIONALES PROPUESTOS - Agregar a models.py
    """
    
    # ========== CAMPOS EXISTENTES ==========
    # (Mantener todos los campos actuales)
    # project, unit_number, unit_type, floor, etc.
    
    # ========== ESTADOS MEJORADOS ==========
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('option', 'Option'),  # 24-48h pensando
        ('separated', 'Separated'),  # Apartado con señas
        ('reserved', 'Reserved'),  # Reservado formalmente
        ('contract_pending', 'Contract Pending'),
        ('contract_signed', 'Contract Signed'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid'),
        ('in_construction', 'In Construction'),
        ('ready_for_delivery', 'Ready for Delivery'),
        ('delivered', 'Delivered'),
        ('blocked', 'Blocked'),
        ('cancelled', 'Cancelled'),
    ]
    
    sub_status = models.CharField(
        max_length=100, blank=True,
        help_text="Estado más específico: pending_bank_approval, waiting_signature, etc."
    )
    status_changed_at = models.DateTimeField(null=True, blank=True)
    status_changed_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='unit_status_changes'
    )
    previous_status = models.CharField(max_length=20, blank=True)
    status_expires_at = models.DateTimeField(
        null=True, blank=True,
        help_text="Para opciones temporales"
    )
    
    # ========== OPCIÓN (24-48h) ==========
    
    option_holder = models.ForeignKey(
        'leads.Lead',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='options_held'
    )
    option_start_date = models.DateTimeField(null=True, blank=True)
    option_expires_at = models.DateTimeField(null=True, blank=True)
    option_extended_count = models.IntegerField(default=0)
    
    # ========== APARTADO CON SEÑAS ==========
    
    separated_by = models.ForeignKey(
        'leads.Lead',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='separated_units'
    )
    separated_date = models.DateTimeField(null=True, blank=True)
    separation_deposit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        help_text="Monto de señas pagadas"
    )
    separation_receipt = models.CharField(max_length=100, blank=True)
    separation_expires_at = models.DateTimeField(null=True, blank=True)
    
    # ========== CLIENTE Y CONTRATO ==========
    
    customer_first_name = models.CharField(max_length=150, blank=True)
    customer_last_name = models.CharField(max_length=150, blank=True)
    customer_email = models.EmailField(blank=True)
    customer_phone = models.CharField(max_length=50, blank=True)
    customer_id_number = models.CharField(
        max_length=50, blank=True,
        help_text="ID, passport o tax ID"
    )
    
    contract_number = models.CharField(max_length=100, blank=True, unique=True)
    contract_date = models.DateField(null=True, blank=True)
    contract_type = models.CharField(
        max_length=50, blank=True,
        choices=[
            ('cash', 'Cash Payment'),
            ('bank_financing', 'Bank Financing'),
            ('developer_financing', 'Developer Financing'),
            ('mixed', 'Mixed')
        ]
    )
    notary = models.CharField(max_length=255, blank=True)
    notary_date = models.DateField(null=True, blank=True)
    deed_number = models.CharField(max_length=100, blank=True)
    
    # ========== FINANCIAMIENTO DETALLADO ==========
    
    payment_scheme = models.JSONField(
        default=dict, blank=True,
        help_text="""Esquema de pago. Ejemplo:
        {
            "type": "developer_financing",
            "down_payment": 71155,
            "down_payment_percentage": 20,
            "down_payment_date": "2024-01-20",
            "monthly_payment": 1850,
            "num_payments": 240,
            "interest_rate": 8.5,
            "balloon_payment": null,
            "first_payment_date": "2024-02-01",
            "final_payment_date": "2044-01-01"
        }"""
    )
    
    payments_received = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    payments_pending = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    payment_history = models.JSONField(
        default=list, blank=True,
        help_text="""Historial de pagos. Ejemplo:
        [
            {
                "date": "2024-01-20",
                "amount": 71155,
                "type": "down_payment",
                "method": "wire_transfer",
                "reference": "TRX-2024-001",
                "received_by": "user_id"
            }
        ]"""
    )
    
    next_payment_date = models.DateField(null=True, blank=True)
    next_payment_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('current', 'Current'),
            ('overdue', 'Overdue'),
            ('paid_off', 'Paid Off')
        ],
        default='current',
        blank=True
    )
    
    # ========== HISTORIAL DE PRECIOS ==========
    
    price_history = models.JSONField(
        default=list, blank=True,
        help_text="""Historial de cambios de precio. Ejemplo:
        [
            {
                "date": "2024-01-01",
                "price": 350000,
                "reason": "Launch price",
                "changed_by": "admin_user_id"
            },
            {
                "date": "2024-03-01",
                "price": 375000,
                "reason": "Market adjustment",
                "changed_by": "manager_user_id"
            }
        ]"""
    )
    
    original_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="Precio original de lista"
    )
    current_discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    final_sale_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="Precio final negociado con cliente"
    )
    
    # ========== PERSONALIZACIONES ==========
    
    customizations = models.JSONField(
        default=list, blank=True,
        help_text="""Personalizaciones del cliente. Ejemplo:
        [
            {
                "category": "kitchen",
                "item": "Countertop upgrade",
                "original": "Granite",
                "selected": "Quartz",
                "cost": 2500,
                "status": "approved",
                "approved_by": "user_id",
                "approved_date": "2024-02-15"
            }
        ]"""
    )
    
    total_customizations_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    customizations_approved = models.BooleanField(default=False)
    customizations_deadline = models.DateField(
        null=True, blank=True,
        help_text="Fecha límite para solicitar personalizaciones"
    )
    
    # ========== CONSTRUCCIÓN Y ENTREGA ==========
    
    construction_status = models.CharField(
        max_length=50,
        choices=[
            ('not_started', 'Not Started'),
            ('foundation', 'Foundation'),
            ('structure', 'Structure'),
            ('walls', 'Walls'),
            ('plumbing', 'Plumbing'),
            ('electrical', 'Electrical'),
            ('finishing', 'Finishing'),
            ('completed', 'Completed')
        ],
        default='not_started',
        blank=True
    )
    construction_progress_percentage = models.IntegerField(
        default=0,
        help_text="Progreso específico de esta unidad (0-100)"
    )
    estimated_completion_date = models.DateField(null=True, blank=True)
    actual_completion_date = models.DateField(null=True, blank=True)
    
    # Inspecciones
    inspections = models.JSONField(
        default=list, blank=True,
        help_text="""Inspecciones realizadas. Ejemplo:
        [
            {
                "type": "pre_delivery",
                "date": "2024-06-15",
                "inspector": "John Smith",
                "result": "approved",
                "issues_found": [],
                "notes": "Unit ready for delivery"
            }
        ]"""
    )
    
    # Entrega
    scheduled_delivery_date = models.DateField(null=True, blank=True)
    actual_delivery_date = models.DateField(null=True, blank=True)
    delivery_status = models.CharField(
        max_length=20,
        choices=[
            ('not_scheduled', 'Not Scheduled'),
            ('scheduled', 'Scheduled'),
            ('delivered', 'Delivered'),
            ('delivery_pending', 'Delivery Pending Issues')
        ],
        default='not_scheduled',
        blank=True
    )
    delivery_notes = models.TextField(blank=True)
    keys_delivered = models.BooleanField(default=False)
    keys_delivered_date = models.DateTimeField(null=True, blank=True)
    keys_received_by = models.CharField(max_length=255, blank=True)
    
    # ========== DOCUMENTOS DE LA UNIDAD ==========
    
    unit_documents = models.JSONField(
        default=list, blank=True,
        help_text="""Documentos de la unidad. Ejemplo:
        [
            {
                "type": "floor_plan",
                "name": "Plano Unidad 1205",
                "url": "https://s3.../1205-plan.pdf",
                "version": "v3",
                "date": "2024-01-15"
            },
            {
                "type": "contract",
                "name": "Contrato de Compraventa",
                "url": "https://s3.../contract.pdf",
                "signed": true,
                "signed_date": "2024-02-01"
            },
            {
                "type": "deed",
                "name": "Escritura",
                "url": "https://s3.../deed.pdf",
                "registered": true,
                "registration_number": "REG-2024-567",
                "date": "2024-06-01"
            }
        ]"""
    )
    
    # ========== ESPECIFICACIONES TÉCNICAS ==========
    
    specifications = models.JSONField(
        default=dict, blank=True,
        help_text="""Especificaciones técnicas completas. Ver ejemplo en docstring"""
    )
    
    finishes = models.JSONField(
        default=dict, blank=True,
        help_text="""Acabados seleccionados. Ejemplo:
        {
            "standard": {
                "walls": "Paint",
                "floors": "Porcelain tile",
                "doors": "Wood veneer",
                "windows": "Aluminum"
            },
            "premium_option": {
                "walls": "Textured paint",
                "floors": "Italian marble",
                "doors": "Solid wood",
                "windows": "Impact glass"
            },
            "selected": "premium_option"
        }"""
    )
    
    # ========== PARKING Y STORAGE ==========
    
    parking_spaces = models.JSONField(
        default=list, blank=True,
        help_text="""Espacios de parking. Ejemplo:
        [
            {
                "number": "P-125",
                "type": "covered",
                "level": "B2",
                "included": true,
                "price": 0
            },
            {
                "number": "P-125B",
                "type": "visitor",
                "level": "B1",
                "included": false,
                "price": 15000
            }
        ]"""
    )
    
    storage_units = models.JSONField(
        default=list, blank=True,
        help_text="""Bodegas/storage. Ejemplo:
        [
            {
                "number": "ST-125",
                "size_sqm": 6,
                "level": "B1",
                "included": true,
                "price": 0
            }
        ]"""
    )
    
    # ========== HOA Y GASTOS ==========
    
    hoa_fee_monthly = models.DecimalField(
        max_digits=8, decimal_places=2, default=0,
        help_text="Cuota mensual de condominio"
    )
    hoa_details = models.JSONField(default=dict, blank=True)
    
    estimated_monthly_costs = models.JSONField(
        default=dict, blank=True,
        help_text="""Gastos mensuales estimados. Ejemplo:
        {
            "hoa": 150,
            "electricity": 80,
            "water": 30,
            "internet": 50,
            "property_tax": 120,
            "insurance": 45,
            "total": 475
        }"""
    )
    
    # ========== CONDICIONES ESPECIALES ==========
    
    special_conditions = models.JSONField(
        default=dict, blank=True,
        help_text="""Condiciones especiales de venta. Ejemplo:
        {
            "early_bird_discount": {
                "amount": 10000,
                "reason": "First 20 buyers",
                "approved_by": "manager_id"
            },
            "referral_bonus": {
                "amount": 3000,
                "referrer": "John Doe",
                "referrer_commission": 1000
            }
        }"""
    )
    
    total_discounts = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    discount_breakdown = models.JSONField(default=list, blank=True)
    
    # ========== VECINDARIO Y UBICACIÓN ==========
    
    neighbors = models.JSONField(
        default=dict, blank=True,
        help_text="""Unidades vecinas. Ejemplo:
        {
            "left": "1204",
            "right": "1206",
            "above": "1305",
            "below": "1105",
            "diagonal": ["1304", "1306"]
        }"""
    )
    
    tower_or_block = models.CharField(max_length=100, blank=True)
    block_number = models.CharField(max_length=50, blank=True)
    section = models.CharField(max_length=100, blank=True)
    
    # ========== SOSTENIBILIDAD ==========
    
    energy_rating = models.CharField(
        max_length=10, blank=True,
        help_text="A+, A, B, C, D, E"
    )
    green_certifications = models.JSONField(default=list, blank=True)
    estimated_consumption = models.JSONField(
        default=dict, blank=True,
        help_text="""Consumos estimados. Ejemplo:
        {
            "electricity_kwh_month": 300,
            "water_m3_month": 12,
            "gas_m3_month": 8,
            "carbon_footprint_kg_year": 1200
        }"""
    )
    
    # ========== GARANTÍAS ==========
    
    warranty_start_date = models.DateField(null=True, blank=True)
    warranty_end_date = models.DateField(null=True, blank=True)
    warranty_claims = models.JSONField(
        default=list, blank=True,
        help_text="""Reclamos de garantía. Ejemplo:
        [
            {
                "date": "2024-09-15",
                "issue": "Water leak in master bathroom",
                "status": "resolved",
                "resolved_date": "2024-09-20",
                "cost": 450,
                "notes": "Pipe connection fixed"
            }
        ]"""
    )
    
    # ========== HISTORIAL DE OPERACIONES ==========
    
    operation_history = models.JSONField(
        default=list, blank=True,
        help_text="""Audit trail completo. Ver ejemplo en docstring"""
    )
    
    # ========== MÉTODOS MEJORADOS ==========
    
    def can_be_reserved(self):
        """Verificar si puede ser reservada"""
        return self.status in ['available', 'option', 'separated']
    
    def can_be_sold(self):
        """Verificar si puede ser vendida"""
        return self.status not in ['sold', 'delivered', 'cancelled']
    
    def calculate_total_price(self):
        """Calcular precio total con upgrades y descuentos"""
        base = self.price
        upgrades = self.total_customizations_cost
        discounts = self.total_discounts
        return base + upgrades - discounts
    
    def is_payment_current(self):
        """Verificar si pagos están al día"""
        if self.payment_status == 'overdue':
            return False
        return True
    
    def days_until_delivery(self):
        """Días hasta entrega estimada"""
        if self.scheduled_delivery_date:
            from django.utils import timezone
            delta = self.scheduled_delivery_date - timezone.now().date()
            return delta.days
        return None

