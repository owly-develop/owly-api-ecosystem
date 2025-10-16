# 🎯 Endpoints Adicionales para Inventario Robusto

## 📋 Nuevos Endpoints Propuestos

Estos endpoints complementan el sistema de inventario para hacerlo profesional.

---

## 🏗️ PROJECTS - Endpoints Adicionales (12 nuevos)

### Inventario y Disponibilidad

```
GET /api/projects/{id}/inventory_breakdown/
```
**Propósito**: Ver inventario detallado por tipo, piso, precio, orientación

**Response**:
```json
{
  "by_type": {
    "1BR": {"total": 30, "available": 12, "sold": 15, "reserved": 3},
    "2BR": {"total": 60, "available": 25, "sold": 30, "reserved": 5},
    "3BR": {"total": 20, "available": 8, "sold": 10, "reserved": 2}
  },
  "by_floor_range": {
    "1-5": {"available": 15, "avg_price": 280000},
    "6-10": {"available": 20, "avg_price": 310000},
    "11-15": {"available": 13, "avg_price": 350000}
  },
  "by_price_range": {
    "200k-300k": {"count": 25, "available": 10},
    "300k-400k": {"count": 35, "available": 15},
    "400k-500k": {"count": 20, "available": 8}
  },
  "by_orientation": {
    "north": {"available": 15, "premium": 5},
    "south": {"available": 20, "premium": 8},
    "east": {"available": 10, "premium": 3},
    "west": {"available": 3, "premium": 1}
  }
}
```

---

```
GET /api/projects/{id}/sales_velocity/
```
**Propósito**: Calcular velocidad de ventas (unidades/mes)

**Response**:
```json
{
  "current_month": 8,  // Vendidas este mes
  "last_month": 12,
  "last_3_months_avg": 9.3,
  "last_6_months_avg": 10.5,
  "projected_sellout_date": "2025-08-15",
  "days_to_sellout": 487,
  "velocity_status": "healthy"  // slow, average, healthy, hot
}
```

---

```
POST /api/projects/{id}/update_construction_phase/
```
**Propósito**: Actualizar fase de construcción

**Request**:
```json
{
  "phase": "Structure",
  "progress": 85,
  "notes": "All floors completed, starting roofing"
}
```

---

```
GET /api/projects/{id}/payment_collections/
```
**Propósito**: Estado de cobranzas del proyecto

**Response**:
```json
{
  "total_expected": 42500000,  // Total esperado
  "total_received": 28350000,  // Total cobrado
  "total_pending": 14150000,   // Pendiente de cobrar
  "collection_rate": 66.7,     // % cobrado
  "units_paid_off": 35,
  "units_in_payment": 25,
  "units_current": 20,
  "units_overdue": 5,
  "overdue_amount": 185000
}
```

---

```
GET /api/projects/{id}/available_by_criteria/
```
**Propósito**: Disponibles con filtros multi-criterio inteligente

**Query Params**:
```
?bedrooms=2
&price_max=400000
&floor_min=5
&orientation=east,south
&parking=true
&view_type=ocean
```

**Response**:
```json
{
  "matches": 12,
  "perfect_matches": 5,  // 100% match
  "good_matches": 7,     // 80%+ match
  "units": [
    {
      "id": "uuid-1",
      "unit_number": "1205",
      "match_score": 100,
      "price": 375000,
      "floor": 12,
      "bedrooms": 2,
      "orientation": "east",
      "view_type": "ocean view"
    }
  ]
}
```

---

```
POST /api/projects/{id}/apply_promotion/
```
**Propósito**: Aplicar promoción a unidades disponibles

**Request**:
```json
{
  "promotion_name": "Black Friday 2024",
  "discount_percentage": 5,
  "applicable_to": "all_available",  // o array de unit_ids
  "valid_until": "2024-12-31"
}
```

---

### Reportes

```
GET /api/projects/{id}/financial_report/
```
**Propósito**: Reporte financiero completo

**Response**:
```json
{
  "development_cost": 12000000,
  "projected_revenue": 18500000,
  "actual_revenue": 14200000,
  "profit_margin": 35.1,
  "roi": 53.8,
  "cash_collected": 10500000,
  "pending_collections": 3700000,
  "units_metrics": {
    "sold": 72,
    "avg_sale_price": 425000,
    "avg_days_to_sell": 45,
    "fastest_sale": 3,
    "slowest_sale": 180
  }
}
```

---

```
GET /api/projects/{id}/construction_schedule/
```
**Propósito**: Cronograma de construcción

**Response**:
```json
{
  "current_phase": "Structure",
  "overall_progress": 65,
  "on_schedule": true,
  "delay_days": 0,
  "phases": [
    {
      "name": "Foundation",
      "status": "completed",
      "progress": 100,
      "start": "2023-01-01",
      "end": "2023-06-30",
      "duration_days": 180
    },
    {
      "name": "Structure",
      "status": "in_progress",
      "progress": 75,
      "start": "2023-07-01",
      "estimated_end": "2024-03-31"
    }
  ],
  "next_milestone": {
    "name": "Structure Completion",
    "date": "2024-03-31",
    "days_remaining": 45
  }
}
```

---

## 🏠 UNITS - Endpoints Adicionales (18 nuevos)

### Workflow de Venta

```
POST /api/units/{id}/put_on_option/
```
**Propósito**: Cliente quiere pensar (opción 24-48h)

**Request**:
```json
{
  "lead_id": "uuid-lead",
  "duration_hours": 48,
  "notes": "Cliente quiere consultar con esposa"
}
```

**Response**:
```json
{
  "status": "option",
  "option_expires_at": "2024-01-18T14:00:00Z",
  "option_holder": {
    "id": "uuid-lead",
    "name": "Maria Gonzalez"
  }
}
```

---

```
POST /api/units/{id}/separate/
```
**Propósito**: Apartar unidad con señas (formal)

**Request**:
```json
{
  "lead_id": "uuid-lead",
  "deposit_amount": 3500,
  "receipt_number": "RC-2024-001",
  "payment_method": "cash",
  "duration_days": 15,
  "notes": "Cliente pagó señas, tiene 15 días para decidir"
}
```

**Response**:
```json
{
  "status": "separated",
  "separated_by": {...},
  "separation_deposit": 3500,
  "separation_expires_at": "2024-02-01T23:59:59Z",
  "next_step": "Cliente debe confirmar en 15 días o pierde señas"
}
```

---

```
POST /api/units/{id}/sign_contract/
```
**Propósito**: Firmar contrato de compraventa

**Request**:
```json
{
  "customer": {
    "first_name": "Maria",
    "last_name": "Gonzalez",
    "email": "maria@email.com",
    "phone": "+1-305-555-1234",
    "id_number": "12345678"
  },
  "contract_number": "CT-2024-001",
  "contract_type": "developer_financing",
  "payment_scheme": {
    "down_payment": 71155,
    "down_payment_percentage": 20,
    "monthly_payment": 1850,
    "num_payments": 240,
    "interest_rate": 8.5,
    "first_payment_date": "2024-02-01"
  },
  "notary": "Notaria Publica #5",
  "contract_date": "2024-01-16"
}
```

---

```
POST /api/units/{id}/record_payment/
```
**Propósito**: Registrar pago recibido

**Request**:
```json
{
  "amount": 1850,
  "payment_type": "monthly",  // down_payment, monthly, balloon, final
  "payment_number": 1,
  "method": "wire_transfer",
  "reference": "TRX-2024-0045",
  "date": "2024-02-01",
  "notes": "Pago a tiempo"
}
```

**Response**:
```json
{
  "payment_recorded": true,
  "payments_received": 73005,  // Total acumulado
  "payments_pending": 282770,  // Pendiente
  "percentage_paid": 20.6,
  "next_payment_date": "2024-03-01",
  "next_payment_amount": 1850,
  "payment_status": "current"
}
```

---

```
POST /api/units/{id}/add_customization/
```
**Propósito**: Agregar personalización solicitada por cliente

**Request**:
```json
{
  "category": "kitchen",
  "item": "Upgrade to Quartz Countertop",
  "original": "Granite",
  "selected": "Quartz Premium",
  "cost": 2500,
  "requires_approval": true,
  "notes": "Cliente prefiere color blanco carrara"
}
```

---

```
POST /api/units/{id}/approve_customizations/
```
**Propósito**: Aprobar todas las personalizaciones (manager/admin)

**Request**:
```json
{
  "approved": true,
  "notes": "All customizations within budget, approved",
  "total_additional_cost": 7200
}
```

---

```
POST /api/units/{id}/schedule_delivery/
```
**Propósito**: Programar entrega de unidad

**Request**:
```json
{
  "delivery_date": "2024-08-15",
  "delivery_time": "10:00",
  "customer_contact": "+1-305-555-1234",
  "notes": "Cliente confirmó disponibilidad",
  "items_to_deliver": ["keys", "manuals", "warranties", "parking_remote"]
}
```

---

```
POST /api/units/{id}/deliver/
```
**Propósito**: Marcar unidad como entregada

**Request**:
```json
{
  "delivered_date": "2024-08-15",
  "keys_delivered": true,
  "keys_received_by": "Maria Gonzalez",
  "inspection_approved": true,
  "customer_signature": "base64_signature",
  "notes": "Cliente satisfecha, todo en orden"
}
```

---

```
GET /api/units/{id}/payment_schedule/
```
**Propósito**: Ver calendario de pagos completo

**Response**:
```json
{
  "scheme": {
    "type": "developer_financing",
    "down_payment": 71155,
    "monthly": 1850,
    "num_payments": 240
  },
  "schedule": [
    {
      "payment_number": 0,
      "type": "down_payment",
      "amount": 71155,
      "due_date": "2024-01-20",
      "paid": true,
      "paid_date": "2024-01-20",
      "status": "paid"
    },
    {
      "payment_number": 1,
      "type": "monthly",
      "amount": 1850,
      "due_date": "2024-02-01",
      "paid": true,
      "paid_date": "2024-02-01",
      "status": "paid"
    },
    {
      "payment_number": 2,
      "type": "monthly",
      "amount": 1850,
      "due_date": "2024-03-01",
      "paid": false,
      "status": "upcoming"
    }
    // ... 238 payments more
  ],
  "summary": {
    "total_amount": 355775,
    "paid_to_date": 73005,
    "remaining": 282770,
    "percentage_paid": 20.5,
    "payments_made": 2,
    "payments_remaining": 238,
    "status": "current",
    "overdue_amount": 0
  }
}
```

---

```
GET /api/units/{id}/operation_history/
```
**Propósito**: Audit trail completo de la unidad

**Response**:
```json
[
  {
    "date": "2024-01-10",
    "action": "unit_created",
    "user": "admin@company.com",
    "details": "Unit added to inventory"
  },
  {
    "date": "2024-01-15",
    "action": "price_set",
    "user": "manager@company.com",
    "old_value": null,
    "new_value": 350000
  },
  {
    "date": "2024-01-16",
    "action": "put_on_option",
    "user": "sales@company.com",
    "lead": "Maria Gonzalez",
    "duration": "48h"
  },
  {
    "date": "2024-01-18",
    "action": "separated",
    "user": "sales@company.com",
    "deposit": 3500,
    "receipt": "RC-2024-001"
  },
  {
    "date": "2024-01-20",
    "action": "contract_signed",
    "user": "sales@company.com",
    "contract": "CT-2024-001",
    "customer": "Maria Gonzalez"
  },
  {
    "date": "2024-01-20",
    "action": "payment_received",
    "type": "down_payment",
    "amount": 71155,
    "method": "wire_transfer"
  }
]
```

---

```
POST /api/units/{id}/apply_discount/
```
**Propósito**: Aplicar descuento especial (requiere aprobación manager)

**Request**:
```json
{
  "discount_type": "early_bird",
  "amount": 10000,
  "percentage": null,
  "reason": "First 20 buyers promotion",
  "approved_by": "manager_user_id",
  "approval_notes": "Within authorized promotion limits"
}
```

---

```
POST /api/units/{id}/change_price/
```
**Propósito**: Cambiar precio (trackea historial)

**Request**:
```json
{
  "new_price": 365000,
  "reason": "Market adjustment",
  "effective_date": "2024-02-01"
}
```

**Response**:
```json
{
  "price": 365000,
  "previous_price": 350000,
  "change_amount": 15000,
  "change_percentage": 4.3,
  "reason": "Market adjustment",
  "changed_by": "manager@company.com",
  "effective_date": "2024-02-01"
}
```

---

### Consultas Especiales

```
GET /api/units/expiring_options/
```
**Propósito**: Unidades con opciones que expiran pronto (follow-up)

**Response**:
```json
[
  {
    "id": "uuid-1",
    "unit_number": "1205",
    "option_expires_at": "2024-01-18T14:00:00Z",
    "hours_remaining": 8,
    "option_holder": {
      "name": "Carlos Rodriguez",
      "phone": "+1-305-555-5555"
    },
    "assigned_to": "sales@company.com"
  }
]
```

---

```
GET /api/units/payment_overdue/
```
**Propósito**: Unidades con pagos vencidos

**Response**:
```json
[
  {
    "id": "uuid-2",
    "unit_number": "1505",
    "customer": "Pedro Lopez",
    "payment_status": "overdue",
    "overdue_amount": 5550,  // 3 mensualidades
    "days_overdue": 15,
    "next_action": "Send payment reminder",
    "assigned_to": "collections@company.com"
  }
]
```

---

```
GET /api/units/ready_for_delivery/
```
**Propósito**: Unidades listas para entregar

**Response**:
```json
[
  {
    "id": "uuid-3",
    "unit_number": "0801",
    "customer": "Ana Martinez",
    "construction_complete": true,
    "inspection_passed": true,
    "payment_complete": true,
    "documents_ready": true,
    "delivery_scheduled": false,
    "action_needed": "Schedule delivery appointment"
  }
]
```

---

```
GET /api/units/in_construction/
```
**Propósito**: Unidades vendidas en construcción (para updates a clientes)

**Response**:
```json
[
  {
    "id": "uuid-4",
    "unit_number": "1801",
    "customer": "Roberto Silva",
    "construction_status": "finishing",
    "construction_progress": 85,
    "estimated_completion": "2024-06-30",
    "days_until_completion": 45,
    "last_update_sent": "2024-01-01",
    "should_send_update": true
  }
]
```

---

```
GET /api/units/customizations_pending/
```
**Propósito**: Unidades con personalizaciones pendientes de aprobación

**Response**:
```json
[
  {
    "id": "uuid-5",
    "unit_number": "1405",
    "customer": "Laura Fernandez",
    "customizations_count": 3,
    "total_cost": 8700,
    "pending_approval": true,
    "deadline": "2024-02-15",
    "days_remaining": 10
  }
]
```

---

## 📊 Analytics Avanzados

```
GET /api/analytics/inventory_health/
```
**Propósito**: Salud general del inventario

**Response**:
```json
{
  "total_units": 850,
  "available": 342,
  "in_process": 125,  // option + separated + reserved
  "sold_pending_delivery": 298,
  "delivered": 85,
  "availability_rate": 40.2,
  "sales_velocity": {
    "current_month": 45,
    "projected_annual": 540
  },
  "aging_analysis": {
    "new_0_30_days": 120,
    "aging_31_90_days": 150,
    "aging_91_180_days": 50,
    "aging_180_plus_days": 22  // ⚠️ Requiere atención
  },
  "payment_health": {
    "current": 250,
    "overdue_1_30_days": 35,
    "overdue_31_90_days": 10,
    "overdue_90_plus_days": 3  // ⚠️ Acción urgente
  },
  "delivery_pipeline": {
    "ready_to_deliver": 25,
    "scheduled_this_month": 15,
    "in_construction": 298
  }
}
```

---

```
GET /api/analytics/pricing_intelligence/
```
**Propósito**: Análisis de precios y pricing strategy

**Response**:
```json
{
  "avg_price_per_sqm": 3825,
  "price_by_floor": {
    "1-5": 3200,
    "6-10": 3650,
    "11-15": 4100,
    "16-20": 4500
  },
  "price_by_orientation": {
    "north": 3600,
    "south": 3800,
    "east": 4000,  // Premium por vista al mar
    "west": 3400
  },
  "discount_analysis": {
    "avg_discount_given": 3.5,
    "most_common_discount": 5,
    "units_with_discount": 45,
    "total_discount_cost": 675000
  },
  "market_comparison": {
    "our_avg_price": 425000,
    "market_avg_price": 445000,
    "competitive_advantage": "Price below market"
  }
}
```

---

```
GET /api/analytics/customer_insights/
```
**Propósito**: Insights sobre los clientes compradores

**Response**:
```json
{
  "demographics": {
    "age_ranges": {
      "25-35": 25,
      "36-45": 45,
      "46-55": 20,
      "56+": 10
    },
    "buyer_types": {
      "first_time_buyer": 35,
      "investor": 40,
      "upgrading": 25
    }
  },
  "preferences": {
    "most_popular_type": "2BR",
    "avg_bedrooms_selected": 2.3,
    "floor_preference": {
      "low_1_5": 20,
      "mid_6_12": 50,
      "high_13_plus": 30
    }
  },
  "payment_patterns": {
    "cash_buyers": 15,
    "bank_financing": 45,
    "developer_financing": 40,
    "avg_down_payment_percentage": 25
  },
  "customizations": {
    "units_with_customizations": 60,
    "avg_customization_cost": 5200,
    "most_requested": [
      "Kitchen upgrade",
      "Hardwood floors",
      "Smart home package"
    ]
  }
}
```

---

## 🔄 Implementación Paso a Paso

### Fase 1: Extender Modelos (2-3 horas)
1. Copiar campos de `models_enhanced.py` a `models.py`
2. Crear migración: `docker-compose exec web python manage.py makemigrations`
3. Aplicar: `docker-compose exec web python manage.py migrate`

### Fase 2: Crear Serializers (1-2 horas)
1. Actualizar serializers con nuevos campos
2. Crear serializers específicos para workflows
3. Agregar validaciones

### Fase 3: Implementar Views (3-4 horas)
1. Agregar actions a ProjectViewSet
2. Agregar actions a UnitViewSet
3. Crear endpoints de analytics

### Fase 4: Testing (2-3 horas)
1. Tests para nuevos endpoints
2. Tests de workflows
3. Tests de cálculos

### Fase 5: Admin (1-2 horas)
1. Actualizar admin con nuevos campos
2. Agregar bulk actions para workflows
3. Mejorar inline displays

**Total estimado**: 9-14 horas de desarrollo

---

## 📋 Priorización Sugerida

### Crítico (Implementar Ya):
1. ✅ Estados mejorados (option, separated, etc.)
2. ✅ Workflow de venta completo
3. ✅ Tracking de pagos
4. ✅ Operation history

### Importante (Siguiente Sprint):
1. ✅ Personalizaciones
2. ✅ Reportes financieros
3. ✅ Inventory breakdown
4. ✅ Sales velocity

### Nice to Have (Futuro):
1. ✅ Garantías y reclamos
2. ✅ Sostenibilidad y certificaciones
3. ✅ Customer insights avanzados

---

Siguiente documento: Implementación completa en código

