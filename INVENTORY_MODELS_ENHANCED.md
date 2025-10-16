# 🏗️ Modelos Mejorados para Inventario Robusto

## 🎯 Mejoras Propuestas para Projects y Units

Esta guía documenta las mejoras necesarias para convertir el sistema básico actual en un **sistema de inventario inmobiliario profesional**.

---

## 📦 Campos Adicionales Propuestos

### 🏗️ PROJECT - Mejoras

#### Tracking Financiero Avanzado
```python
# Costos y Márgenes
cost_per_unit = models.DecimalField()  # Costo promedio por unidad
total_development_cost = models.DecimalField()  # Costo total del desarrollo
projected_revenue = models.DecimalField()  # Revenue proyectado
actual_revenue = models.DecimalField()  # Revenue real
profit_margin_percentage = models.DecimalField()  # Margen de ganancia

# Esquemas de Pago
payment_plans = models.JSONField()  # Diferentes esquemas disponibles
# Ejemplo: [
#   {
#     "name": "Plan A - 30/70",
#     "down_payment": 30,
#     "financing_months": 120,
#     "interest_rate": 8.5
#   }
# ]

# Descuentos y Promociones
active_promotions = models.JSONField()
# Ejemplo: [
#   {
#     "name": "Early Bird",
#     "discount_percentage": 10,
#     "valid_until": "2024-12-31",
#     "conditions": "First 20 units"
#   }
# ]
```

#### Fases del Proyecto
```python
# Fases de Construcción
construction_phases = models.JSONField()
# Ejemplo: [
#   {
#     "phase": "Foundation",
#     "progress": 100,
#     "start_date": "2023-01-01",
#     "end_date": "2023-06-30",
#     "status": "completed"
#   },
#   {
#     "phase": "Structure",
#     "progress": 75,
#     "start_date": "2023-07-01",
#     "estimated_end": "2024-03-31",
#     "status": "in_progress"
#   }
# ]

current_phase = models.CharField()  # Fase actual
next_milestone = models.JSONField()  # Próximo hito importante
```

#### Documentación Legal
```python
# Permisos y Licencias
building_permit_number = models.CharField()
building_permit_date = models.DateField()
building_permit_expires = models.DateField()
environmental_license = models.CharField()
use_permit = models.CharField()

# Documentos Legales
legal_documents = models.JSONField()
# Ejemplo: [
#   {
#     "type": "escritura",
#     "number": "ESC-2024-001",
#     "date": "2024-01-15",
#     "url": "https://s3.../escritura.pdf",
#     "expiry": null
#   }
# ]
```

#### Marketing y Visibilidad
```python
# Campañas de Marketing
marketing_campaigns = models.JSONField()
# Ejemplo: [
#   {
#     "name": "Launch Campaign",
#     "budget": 50000,
#     "start_date": "2024-01-01",
#     "end_date": "2024-03-31",
#     "leads_generated": 234,
#     "conversions": 45
#   }
# ]

# SEO y Web
seo_keywords = models.JSONField()  # Keywords para SEO
virtual_tour_enabled = models.BooleanField()
show_on_website = models.BooleanField()
show_on_marketplace = models.BooleanField()  # Portales inmobiliarios
```

#### Inventario por Tipo
```python
# Breakdown de Inventario
inventory_breakdown = models.JSONField()
# Ejemplo: {
#   "by_type": {
#     "1BR": {"total": 30, "available": 12, "sold": 15, "reserved": 3},
#     "2BR": {"total": 60, "available": 25, "sold": 30, "reserved": 5},
#     "3BR": {"total": 20, "available": 8, "sold": 10, "reserved": 2},
#     "Penthouse": {"total": 10, "available": 3, "sold": 5, "reserved": 2}
#   },
#   "by_floor": {
#     "1-5": {"available": 15},
#     "6-10": {"available": 20},
#     "11-15": {"available": 13}
#   },
#   "by_price_range": {
#     "200k-300k": 25,
#     "300k-400k": 35,
#     "400k-500k": 20
#   }
# }
```

#### Garantías y Post-Venta
```python
# Garantías
warranty_period_years = models.IntegerField()  # Años de garantía
warranty_details = models.TextField()

# Servicio Post-Venta
after_sales_contact = models.EmailField()
after_sales_phone = models.CharField()
maintenance_company = models.CharField()
```

---

### 🏠 UNIT - Mejoras

#### Estado Detallado del Proceso
```python
# Estados más granulares
STATUS_CHOICES = [
    ('available', 'Available'),  # Disponible
    ('option', 'Option'),  # En opción (cliente pensando)
    ('separated', 'Separated'),  # Apartada (señas pagadas)
    ('reserved', 'Reserved'),  # Reservada formalmente
    ('contract_pending', 'Contract Pending'),  # Contrato en proceso
    ('contract_signed', 'Contract Signed'),  # Contrato firmado
    ('in_payment', 'In Payment'),  # En proceso de pago
    ('paid', 'Paid'),  # Pagada completamente
    ('in_construction', 'In Construction'),  # En construcción
    ('ready_for_delivery', 'Ready for Delivery'),  # Lista para entregar
    ('delivered', 'Delivered'),  # Entregada
    ('blocked', 'Blocked'),  # Bloqueada temporalmente
    ('cancelled', 'Cancelled'),  # Cancelada
]

# Sub-estado
sub_status = models.CharField()  # Estado más específico
# Ejemplos: "pending_bank_approval", "waiting_signature", "in_notary"
```

#### Cliente y Contrato
```python
# Información del Cliente (cuando se vende)
customer_first_name = models.CharField()
customer_last_name = models.CharField()
customer_email = models.EmailField()
customer_phone = models.CharField()
customer_id_number = models.CharField()  # ID/Passport

# Información del Contrato
contract_number = models.CharField()
contract_date = models.DateField()
contract_type = models.CharField()  # "cash", "financing", "developer_financing"
notary = models.CharField()  # Notaría
notary_date = models.DateField()
deed_number = models.CharField()  # Número de escritura
```

#### Financiamiento Detallado
```python
# Esquema de Pago
payment_scheme = models.JSONField()
# Ejemplo: {
#   "type": "developer_financing",
#   "down_payment": 71155,  # 20%
#   "down_payment_date": "2024-01-20",
#   "monthly_payments": 1850,
#   "num_payments": 240,
#   "interest_rate": 8.5,
#   "balloon_payment": null,
#   "first_payment_date": "2024-02-01"
# }

# Tracking de Pagos
payments_received = models.DecimalField()  # Total recibido
payments_pending = models.DecimalField()  # Pendiente por recibir
payment_history = models.JSONField()  # Historial de pagos
# Ejemplo: [
#   {
#     "date": "2024-01-20",
#     "amount": 71155,
#     "type": "down_payment",
#     "method": "wire_transfer",
#     "reference": "TRX-2024-001"
#   },
#   {
#     "date": "2024-02-01",
#     "amount": 1850,
#     "type": "monthly",
#     "payment_number": 1,
#     "method": "auto_debit"
#   }
# ]

next_payment_date = models.DateField()
next_payment_amount = models.DecimalField()
payment_status = models.CharField()  # "current", "overdue", "paid_off"
```

#### Historial de Precios
```python
# Tracking de Cambios de Precio
price_history = models.JSONField()
# Ejemplo: [
#   {
#     "date": "2024-01-01",
#     "price": 350000,
#     "reason": "Launch price",
#     "changed_by": "admin@company.com"
#   },
#   {
#     "date": "2024-03-01",
#     "price": 375000,
#     "reason": "Market adjustment",
#     "changed_by": "manager@company.com"
#   }
# ]

original_price = models.DecimalField()  # Precio original/lista
current_discount = models.DecimalField()  # Descuento actual
final_sale_price = models.DecimalField()  # Precio final negociado
```

#### Personalizaciones
```python
# Customizaciones del Cliente
customizations = models.JSONField()
# Ejemplo: [
#   {
#     "item": "Kitchen countertop",
#     "original": "Granite",
#     "selected": "Quartz",
#     "cost": 2500,
#     "status": "approved"
#   },
#   {
#     "item": "Flooring",
#     "original": "Ceramic",
#     "selected": "Hardwood",
#     "cost": 4500,
#     "status": "pending_approval"
#   }
# ]

total_customizations_cost = models.DecimalField()
customizations_approved = models.BooleanField()
```

#### Construcción y Entrega
```python
# Construcción
construction_status = models.CharField()  # "not_started", "foundation", "structure", "finishing"
construction_progress_percentage = models.IntegerField()  # 0-100
estimated_completion_date = models.DateField()
actual_completion_date = models.DateField()

# Inspecciones
inspections = models.JSONField()
# Ejemplo: [
#   {
#     "type": "pre_delivery",
#     "date": "2024-06-15",
#     "inspector": "John Smith",
#     "result": "approved",
#     "notes": "All items checked",
#     "issues": []
#   }
# ]

# Entrega
scheduled_delivery_date = models.DateField()
actual_delivery_date = models.DateField()
delivery_status = models.CharField()  # "not_scheduled", "scheduled", "delivered"
delivery_notes = models.TextField()
keys_delivered = models.BooleanField()
```

#### Documentos de la Unidad
```python
# Documentos Específicos de la Unidad
unit_documents = models.JSONField()
# Ejemplo: [
#   {
#     "type": "floor_plan",
#     "name": "Plano Unidad 1205",
#     "url": "https://s3.../1205-plan.pdf",
#     "version": "v3",
#     "date": "2024-01-15"
#   },
#   {
#     "type": "contract",
#     "name": "Contrato de Compraventa",
#     "url": "https://s3.../contract-1205.pdf",
#     "signed": true,
#     "date": "2024-02-01"
#   },
#   {
#     "type": "deed",
#     "name": "Escritura",
#     "url": "https://s3.../deed-1205.pdf",
#     "date": "2024-06-01"
#   }
# ]
```

#### Especificaciones Técnicas Detalladas
```python
# Especificaciones Completas
specifications = models.JSONField()
# Ejemplo: {
#   "structure": {
#     "walls": "Concrete block",
#     "ceiling_height": "2.80m",
#     "floor": "Porcelain tile"
#   },
#   "kitchen": {
#     "cabinets": "Modular white",
#     "countertop": "Granite",
#     "appliances": ["Stove", "Oven", "Hood"]
#   },
#   "bathrooms": {
#     "master": {
#       "fixtures": "Kohler",
#       "shower": "Glass enclosed",
#       "vanity": "Double sink"
#     }
#   },
#   "ac": {
#     "type": "Split",
#     "brand": "LG",
#     "btu": 18000
#   },
#   "water_heater": {
#     "type": "Electric",
#     "capacity": "80L"
#   }
# }

# Acabados
finishes = models.JSONField()
# Ejemplo: {
#   "standard": {
#     "walls": "Paint",
#     "floors": "Porcelain",
#     "doors": "Wood veneer"
#   },
#   "premium": {  // Si eligió upgrade
#     "walls": "Texture paint",
#     "floors": "Italian marble",
#     "doors": "Solid wood"
#   },
#   "selected": "premium"
# }
```

#### Historial de Operaciones
```python
# Audit Trail
operation_history = models.JSONField()
# Ejemplo: [
#   {
#     "date": "2024-01-15",
#     "action": "unit_created",
#     "user": "admin@company.com",
#     "details": "Unit added to inventory"
#   },
#   {
#     "date": "2024-01-20",
#     "action": "price_changed",
#     "user": "manager@company.com",
#     "old_price": 350000,
#     "new_price": 360000,
#     "reason": "Market adjustment"
#   },
#   {
#     "date": "2024-02-01",
#     "action": "reserved",
#     "user": "sales@company.com",
#     "lead": "LEAD-2024-001",
#     "customer": "Maria Gonzalez"
#   },
#   {
#     "date": "2024-02-05",
#     "action": "contract_signed",
#     "user": "sales@company.com",
#     "contract": "CT-2024-001"
#   }
# ]
```

#### Parking y Storage
```python
# Parkings Asignados
parking_spaces = models.JSONField()
# Ejemplo: [
#   {
#     "number": "P-125",
#     "type": "covered",
#     "level": "B2",
#     "included": true,  // o false si es adicional
#     "price": 0  // o precio si es adicional
#   }
# ]

# Bodegas/Storage
storage_units = models.JSONField()
# Ejemplo: [
#   {
#     "number": "ST-125",
#     "size_sqm": 6,
#     "level": "B1",
#     "included": true,
#     "price": 0
#   }
# ]
```

#### HOA y Gastos Mensuales
```python
# Gastos de Condominio
hoa_fee_monthly = models.DecimalField()  # Cuota mensual HOA
hoa_details = models.JSONField()
# Ejemplo: {
#   "fee": 150,
#   "includes": [
#     "Security 24/7",
#     "Common area maintenance",
#     "Pool maintenance",
#     "Elevator maintenance",
#     "Insurance"
#   ],
#   "utilities_included": ["Water", "Trash"],
#   "utilities_separate": ["Electricity", "Gas", "Internet"]
# }

# Gastos estimados del propietario
estimated_monthly_costs = models.JSONField()
# Ejemplo: {
#   "hoa": 150,
#   "electricity": 80,
#   "internet": 50,
#   "property_tax_monthly": 120,
#   "insurance_monthly": 45,
#   "total_estimated": 445
# }
```

---

### 🏠 UNIT - Estados y Workflow

#### Estados Mejorados con Workflow

```python
# Estado actual con sub-estados
class UnitStatusWorkflow:
    WORKFLOW = {
        'available': {
            'next_states': ['option', 'separated', 'reserved', 'blocked'],
            'can_sell': True,
            'requires_approval': False
        },
        'option': {  # Cliente pensando (24-48h)
            'next_states': ['available', 'separated', 'reserved'],
            'can_sell': False,
            'duration_hours': 48,
            'expires_at': 'auto_calculated'
        },
        'separated': {  # Apartada con señas (7-15 días)
            'next_states': ['available', 'reserved', 'cancelled'],
            'can_sell': False,
            'requires': ['deposit_paid'],
            'deposit_percentage': 1  # 1% del precio
        },
        'reserved': {  # Reservada formalmente (30-90 días)
            'next_states': ['contract_pending', 'cancelled'],
            'can_sell': False,
            'requires': ['reservation_agreement', 'down_payment_scheduled'],
            'deposit_percentage': 5
        },
        'contract_pending': {
            'next_states': ['contract_signed', 'cancelled'],
            'requires': ['legal_review', 'bank_approval']
        },
        'contract_signed': {
            'next_states': ['in_payment'],
            'requires': ['contract_document', 'down_payment_received']
        },
        'in_payment': {
            'next_states': ['paid', 'payment_default'],
            'payment_tracking': True
        },
        'paid': {
            'next_states': ['ready_for_delivery'],
            'requires': ['payment_complete']
        },
        'ready_for_delivery': {
            'next_states': ['delivered'],
            'requires': ['construction_complete', 'inspection_passed']
        },
        'delivered': {
            'next_states': [],
            'final_state': True,
            'requires': ['keys_delivered', 'documents_delivered']
        }
    }

# Campos para workflow
status = models.CharField(choices=STATUS_CHOICES)
sub_status = models.CharField()  # Estado más detallado
status_changed_at = models.DateTimeField()
status_changed_by = models.ForeignKey(User)
previous_status = models.CharField()
status_expires_at = models.DateTimeField()  # Para opciones temporales
```

#### Tracking de Opción/Apartado
```python
# Sistema de Opciones (24-48h sin compromiso)
option_holder = models.ForeignKey('leads.Lead', null=True)
option_start_date = models.DateTimeField()
option_expires_at = models.DateTimeField()
option_extended_count = models.IntegerField()  # Veces extendida

# Sistema de Apartado (señas pagadas)
separated_by = models.ForeignKey('leads.Lead', null=True)
separated_date = models.DateTimeField()
separation_deposit = models.DecimalField()  # Monto de señas
separation_receipt = models.CharField()  # Número de recibo
separation_expires_at = models.DateTimeField()
```

#### Modificaciones y Upgrades
```python
# Modificaciones Estructurales
structural_modifications = models.JSONField()
# Ejemplo: [
#   {
#     "type": "wall_removal",
#     "description": "Remove wall between kitchen and living",
#     "cost": 3500,
#     "approved": true,
#     "approved_by": "architect@company.com",
#     "completion_date": "2024-08-15"
#   }
# ]

# Upgrades y Extras
selected_upgrades = models.JSONField()
# Ejemplo: [
#   {
#     "category": "kitchen",
#     "item": "Premium Appliances Package",
#     "cost": 8500,
#     "includes": ["Bosch dishwasher", "LG fridge", "Gas stove"]
#   },
#   {
#     "category": "flooring",
#     "item": "Hardwood in bedrooms",
#     "cost": 4200,
#     "area_sqm": 35
#   }
# ]

total_upgrades_cost = models.DecimalField()
```

#### Condiciones Especiales
```python
# Condiciones de la Venta
special_conditions = models.JSONField()
# Ejemplo: {
#   "early_bird_discount": {
#     "amount": 10000,
#     "reason": "First 20 buyers"
#   },
#   "family_discount": {
#     "amount": 5000,
#     "reason": "Employee family member"
#   },
#   "bulk_purchase": {
#     "amount": 15000,
#     "reason": "Buying 2 units"
#   },
#   "referral_bonus": {
#     "amount": 3000,
#     "referrer": "John Doe"
#   }
# }

total_discounts = models.DecimalField()
final_negotiated_price = models.DecimalField()  # Precio final después de todo
```

#### Vecinos y Comunidad
```python
# Vecinos (para proyectos horizontales)
neighbors = models.JSONField()
# Ejemplo: {
#   "left": "Unit 1204",
#   "right": "Unit 1206",
#   "above": "Unit 1305",
#   "below": "Unit 1105"
# }

# Información de la Torre/Bloque
tower_or_block = models.CharField()  # "Torre A", "Bloque 3"
block_number = models.CharField()
section = models.CharField()
```

#### Energía y Sostenibilidad
```python
# Certificaciones
energy_rating = models.CharField()  # A+, A, B, C...
green_certifications = models.JSONField()
# Ejemplo: ["LEED Silver", "Energy Star"]

# Consumos Estimados
estimated_consumption = models.JSONField()
# Ejemplo: {
#   "electricity_kwh_month": 300,
#   "water_m3_month": 12,
#   "gas_m3_month": 8
# }
```

#### Garantías Específicas
```python
# Garantías de la Unidad
warranty_start_date = models.DateField()
warranty_end_date = models.DateField()
warranty_claims = models.JSONField()
# Ejemplo: [
#   {
#     "date": "2024-09-15",
#     "issue": "Water leak in bathroom",
#     "status": "resolved",
#     "resolved_date": "2024-09-20",
#     "cost_to_company": 450
#   }
# ]
```

---

## 🎯 Nuevos Endpoints Necesarios

### Projects:
```
GET    /api/projects/{id}/inventory_breakdown/     - Inventario detallado por tipo
GET    /api/projects/{id}/sales_velocity/          - Velocidad de ventas
GET    /api/projects/{id}/price_history/           - Historial de precios
POST   /api/projects/{id}/update_phase/            - Actualizar fase construcción
GET    /api/projects/{id}/payment_status/          - Estado de pagos del proyecto
GET    /api/projects/{id}/available_by_type/       - Disponibles por tipo
```

### Units:
```
POST   /api/units/{id}/put_on_option/              - Poner en opción (24-48h)
POST   /api/units/{id}/separate/                   - Apartar con señas
POST   /api/units/{id}/sign_contract/              - Firmar contrato
POST   /api/units/{id}/record_payment/             - Registrar pago
POST   /api/units/{id}/add_customization/          - Agregar personalización
POST   /api/units/{id}/schedule_delivery/          - Programar entrega
POST   /api/units/{id}/deliver/                    - Marcar como entregada
GET    /api/units/{id}/payment_schedule/           - Ver calendario de pagos
GET    /api/units/{id}/operation_history/          - Historial completo
POST   /api/units/{id}/apply_discount/             - Aplicar descuento especial
```

---

## 🔍 Consultas Avanzadas

### Inventario Inteligente:
```python
# Unidades que necesitan atención
GET /api/units/?status=in_payment&payment_status=overdue

# Unidades casi listas para entregar
GET /api/units/?construction_progress_min=95&status=paid

# Unidades con opciones que expiran hoy
GET /api/units/?status=option&option_expires_before=today

# Unidades con mejor ROI
GET /api/units/?sort_by=profit_margin&available=true

# Unidades personalizables aún
GET /api/units/?status=contract_signed&construction_progress_max=50
```

---

## 📊 Reportes Propuestos

### Para Project Managers:
```
GET /api/projects/{id}/reports/sales_performance/
GET /api/projects/{id}/reports/construction_schedule/
GET /api/projects/{id}/reports/payment_collection/
GET /api/projects/{id}/reports/inventory_aging/
```

### Para Finance:
```
GET /api/projects/{id}/reports/cash_flow/
GET /api/projects/{id}/reports/payment_forecast/
GET /api/projects/{id}/reports/collections_status/
```

### Para Legal:
```
GET /api/projects/{id}/reports/contracts_pending/
GET /api/projects/{id}/reports/documents_missing/
```

---

## 🔄 Workflow States Diagram

```
AVAILABLE
    ↓ (Cliente interesado)
OPTION (24-48h)
    ↓ (Cliente decide, paga señas)
SEPARATED (Apartado con señas)
    ↓ (Se formaliza, paga % inicial)
RESERVED (Reservado formalmente)
    ↓ (Proceso legal)
CONTRACT_PENDING
    ↓ (Firma de contrato)
CONTRACT_SIGNED
    ↓ (Recibe enganche)
IN_PAYMENT (Pagando en cuotas)
    ↓ (Completa pagos)
PAID (Pagado totalmente)
    ↓ (Construcción termina)
READY_FOR_DELIVERY
    ↓ (Inspección OK, coordina entrega)
DELIVERED (Entregado al cliente)
```

---

Esta documentación será implementada en el próximo documento con el código completo.

