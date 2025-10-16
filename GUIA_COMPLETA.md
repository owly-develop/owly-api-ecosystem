# 📚 GUÍA COMPLETA - OWLY CRM API

## 📋 Índice

1. [Arquitectura del Sistema](#1-arquitectura-del-sistema)
2. [Modelos de Base de Datos](#2-modelos-de-base-de-datos)
3. [API Endpoints - Documentación Completa](#3-api-endpoints---documentación-completa)
4. [Testing](#4-testing)
5. [Features Avanzados](#5-features-avanzados)
6. [Desarrollo](#6-desarrollo)

---

# 1. ARQUITECTURA DEL SISTEMA

## 🏛️ Visión General

OWLY CRM API es un sistema **multi-tenant** donde múltiples empresas inmobiliarias comparten la misma infraestructura pero sus datos están completamente aislados.

## 🏗️ Arquitectura Multi-Tenant

### ¿Qué es Multi-Tenant?

**Multi-tenant** = Múltiples empresas (tenants) usando la misma aplicación con **datos completamente separados**.

```
┌─────────────────────────────────────────────────────────────┐
│                     OWLY CRM API                            │
│                                                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │ Company A  │  │ Company B  │  │ Company C  │           │
│  ├────────────┤  ├────────────┤  ├────────────┤           │
│  │ 5 users    │  │ 20 users   │  │ 100 users  │           │
│  │ 3 projects │  │ 10 projects│  │ 50 projects│           │
│  │ 50 leads   │  │ 500 leads  │  │ 5000 leads │           │
│  └────────────┘  └────────────┘  └────────────┘           │
│                                                             │
│           MISMA BASE DE DATOS                               │
│           DATOS AISLADOS                                    │
└─────────────────────────────────────────────────────────────┘
```

### Beneficios

1. **Costo eficiente**: Una sola infraestructura para N empresas
2. **Mantenimiento simple**: Actualizar una vez, beneficia a todos
3. **Escalabilidad**: Agregar nueva empresa = solo crear registro
4. **Datos aislados**: Empresa A nunca ve datos de Empresa B

### Cómo Funciona el Aislamiento

**Cada modelo tiene campo `company`:**
```python
class Lead(models.Model):
    company = models.ForeignKey('companies.Company', ...)
    # ...
```

**Middleware filtra automáticamente:**
```python
# Usuario de Company A hace request
GET /api/leads/

# Middleware añade filtro automático:
leads = Lead.objects.filter(company=user.company)

# Usuario SOLO ve leads de su empresa
```

**Imposible acceder datos de otra empresa:**
- Queries filtran por `company` automáticamente
- Permissions verifican ownership
- Middleware valida cada request

## 🔐 Sistema de Autenticación y Permisos

### JWT (JSON Web Tokens)

**¿Por qué JWT?**
- **Stateless**: No necesita sesiones en servidor
- **Escalable**: Perfecto para microservicios
- **Seguro**: Firmado criptográficamente
- **Mobile-friendly**: Fácil de usar en apps móviles

### Flujo de Autenticación

```
1. Usuario hace login
   POST /api/auth/login/
   → Recibe access token (1h) + refresh token (7d)

2. Usuario hace requests
   GET /api/leads/
   Header: Authorization: Bearer {access_token}
   → API valida token y extrae user_id

3. Access token expira (1h)
   POST /api/auth/refresh/
   {refresh: "..."}
   → Recibe nuevo access token

4. Refresh token expira (7d)
   → Usuario debe hacer login de nuevo
```

### Sistema de Roles

```
┌─────────────────────────────────────────────────────────────┐
│                         ROLES                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ADMIN                                                      │
│  ├─ Gestiona empresa completa                              │
│  ├─ Crea/elimina usuarios                                  │
│  ├─ Ve todos los datos                                     │
│  └─ Configura settings                                     │
│                                                             │
│  MANAGER                                                    │
│  ├─ Supervisa equipo                                       │
│  ├─ Ve todos los leads de su equipo                        │
│  ├─ Reasigna leads                                         │
│  └─ Genera reportes                                        │
│                                                             │
│  SALES                                                      │
│  ├─ Ve solo sus leads asignados                            │
│  ├─ Crea cotizaciones                                      │
│  ├─ Gestiona su pipeline                                   │
│  └─ Registra actividades                                   │
│                                                             │
│  MARKETING                                                  │
│  ├─ Ve analytics de fuentes                                │
│  ├─ Crea campañas                                          │
│  ├─ Asigna fuentes a leads                                 │
│  └─ Reportes de ROI                                        │
│                                                             │
│  SUPPORT                                                    │
│  ├─ Atención post-venta                                    │
│  ├─ Ve clientes convertidos                                │
│  └─ Registra tickets                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Diagrama de Relaciones

```
                    ┌─────────────┐
                    │   COMPANY   │ (Tenant)
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
    │  USERS  │      │ PROJECT │      │  LEADS  │
    └────┬────┘      └────┬────┘      └────┬────┘
         │                │                 │
         │           ┌────▼────┐            │
         │           │  UNITS  │            │
         │           └────┬────┘            │
         │                │                 │
         │                └────────┬────────┘
         │                         │
         │                    ┌────▼────┐
         └────────────────────┤ QUOTES  │
                              └─────────┘
                                   │
                              ┌────▼────────┐
                              │ ACTIVITIES  │
                              └─────────────┘
```

## 🔄 Flujo de Trabajo: Lead → Cliente

```
┌──────────────────────────────────────────────────────────────┐
│  CAPTURA                                                     │
├──────────────────────────────────────────────────────────────┤
│  1. Lead llena formulario web                                │
│     POST /api/leads/                                         │
│     Status: NEW                                              │
└──────────────┬───────────────────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────────────────┐
│  ASIGNACIÓN                                                  │
├──────────────────────────────────────────────────────────────┤
│  2. Sistema auto-asigna a vendedor                          │
│     Status: NEW → CONTACTED                                  │
└──────────────┬───────────────────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────────────────┐
│  CALIFICACIÓN                                                │
├──────────────────────────────────────────────────────────────┤
│  3. Vendedor califica lead                                  │
│     POST /api/leads/{id}/add_note/                          │
│     Status: CONTACTED → QUALIFIED                            │
└──────────────┬───────────────────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────────────────┐
│  COTIZACIÓN                                                  │
├──────────────────────────────────────────────────────────────┤
│  5. Vendedor crea cotización                                │
│     POST /api/quotes/                                        │
│     POST /api/quotes/{id}/send/                             │
│     Status: QUALIFIED → PROPOSAL                             │
└──────────────┬───────────────────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────────────────┐
│  NEGOCIACIÓN                                                 │
├──────────────────────────────────────────────────────────────┤
│  6. Cliente negocia                                         │
│     Status: PROPOSAL → NEGOTIATION                           │
└──────────────┬───────────────────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────────────────┐
│  CIERRE                                                      │
├──────────────────────────────────────────────────────────────┤
│  7. Cliente acepta                                          │
│     POST /api/quotes/{id}/accept/                           │
│     POST /api/projects/units/{id}/reserve/                  │
│     Status: NEGOTIATION → CLOSED_WON                         │
└──────────────┬───────────────────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────────────────┐
│  VENTA FINAL                                                 │
├──────────────────────────────────────────────────────────────┤
│  8. Contrato firmado                                        │
│     POST /api/projects/units/{id}/mark_as_sold/             │
│     UNIT.status = 'sold'                                     │
└──────────────────────────────────────────────────────────────┘
```

## ⚙️ Stack de Servicios

```
┌──────────────────────────────────────────────────────────────┐
│                    DOCKER COMPOSE                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │    WEB     │  │  CELERY    │  │CELERY BEAT │            │
│  │  (Django)  │  │  (Worker)  │  │(Scheduler) │            │
│  │   :8000    │  │            │  │            │            │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘            │
│        │               │               │                    │
│  ┌─────▼───────────────▼───────────────▼──────┐            │
│  │           POSTGRESQL :5432                  │            │
│  │         (Base de Datos Principal)           │            │
│  └─────────────────────────────────────────────┘            │
│                                                              │
│  ┌─────────────────────────────────────────────┐            │
│  │           REDIS :6379                       │            │
│  │    (Cache + Celery Broker)                  │            │
│  └─────────────────────────────────────────────┘            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Responsabilidades:**

- **WEB (Django + Gunicorn)**: API REST, autenticación, business logic
- **PostgreSQL**: Almacenamiento de datos, transacciones ACID
- **Redis**: Cache, sesiones, Celery broker
- **Celery Worker**: Tareas asíncronas (emails, reportes)
- **Celery Beat**: Tareas programadas (cálculo de scores, limpieza)

---

# 2. MODELOS DE BASE DE DATOS

## 🏢 Company (Empresa/Tenant)

### ¿Qué es?
El **tenant** en la arquitectura multi-tenant. Representa una empresa inmobiliaria que usa el CRM.

### Campos Importantes
- `plan`: free/starter/professional/enterprise
- `max_users`, `max_projects`, `max_leads`: Límites según plan
- `status`: active/trial/suspended
- `features`: JSON con características habilitadas

### Ejemplo
```json
{
  "name": "Desarrollos Inmobiliarios XYZ",
  "slug": "desarrollos-xyz",
  "plan": "professional",
  "max_users": 50,
  "max_projects": 100,
  "status": "active",
  "features": {
    "ai_scoring": true,
    "bulk_sms": true,
    "advanced_reporting": true
  }
}
```

## 👤 User (Usuario)

### ¿Qué es?
Empleado de la empresa que usa el CRM (vendedor, gerente, marketing, etc.)

### Roles
- **Admin**: Control total
- **Manager**: Supervisa equipos
- **Sales**: Gestiona sus leads
- **Marketing**: Campañas y fuentes
- **Support**: Atención post-venta

### Campos Importantes
- `role`: Define permisos
- `company`: A qué empresa pertenece
- `assigned_projects`: Proyectos que maneja
- `territories`: Zonas geográficas asignadas

### Ejemplo
```json
{
  "email": "juan@xyz.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "role": "sales",
  "company": "desarrollos-xyz",
  "territories": ["Zona Norte", "Centro"],
  "sales_target": 500000
}
```

## 🏗️ Project (Proyecto Inmobiliario)

### ¿Qué es?
Desarrollo inmobiliario que la empresa está vendiendo (edificio, conjunto de villas, etc.)

### Tipos
- **Residential**: Apartamentos, casas
- **Commercial**: Oficinas, locales
- **Mixed Use**: Combinación
- **Industrial**: Bodegas

### Estados
- **Planning**: En planificación
- **Pre-launch**: Pre-venta
- **Active**: En venta activa
- **Sold Out**: Todo vendido
- **Completed**: Entregado

### Campos Importantes
- `total_units`, `available_units`, `sold_units`: Control inventario
- `price_from`, `price_to`: Rango de precios
- `construction_progress`: 0-100%
- `amenities`: Servicios (piscina, gym, etc.)
- `featured`: Destacado en web

### Ejemplo
```json
{
  "name": "Torres del Mar",
  "code": "TDM-2024",
  "type": "residential",
  "status": "active",
  "city": "Miami Beach",
  "total_units": 120,
  "available_units": 48,
  "sold_units": 65,
  "reserved_units": 7,
  "price_from": 250000,
  "price_to": 750000,
  "construction_progress": 75,
  "delivery_date": "2025-12-31",
  "amenities": ["Piscina", "Gym", "Beach Club"]
}
```

## 🏠 Unit (Unidad)

### ¿Qué es?
Unidad individual dentro de un proyecto (apartamento específico, villa, local)

### Estados
- **Available**: Disponible para vender
- **Reserved**: Reservada por un lead
- **Sold**: Vendida
- **Blocked**: Bloqueada temporalmente

### Campos Importantes
- `unit_number`: Número único (ej: "1205")
- `unit_type`: Tipo (1BR, 2BR, Penthouse)
- `floor`: Piso
- `bedrooms`, `bathrooms`: Especificaciones
- `area_sqm`: Área en m²
- `price`: Precio de venta
- `orientation`: Norte, Sur, Este, Oeste
- `view_type`: Vista (mar, ciudad)

### Ejemplo
```json
{
  "unit_number": "1205",
  "project": "Torres del Mar",
  "unit_type": "2BR/2BA",
  "status": "available",
  "floor": 12,
  "bedrooms": 2,
  "bathrooms": 2,
  "area_sqm": 85,
  "price": 350000,
  "orientation": "East",
  "view_type": "Ocean View"
}
```

## 👥 Lead (Prospecto)

### ¿Qué es?
Persona interesada en comprar. Es el corazón del CRM.

### Estados del Pipeline
1. **New**: Recién llegado
2. **Contacted**: Ya contactado
3. **Qualified**: Calificado (tiene presupuesto)
4. **Proposal**: Cotización enviada
5. **Negotiation**: Negociando
6. **Closed Won**: ¡Ganado!
7. **Closed Lost**: Perdido
8. **Nurturing**: Follow-up largo plazo

### Fuentes
- Website, Facebook, Instagram, WhatsApp
- Referral, Cold Call, Trade Show

### Prioridades
- Low, Medium, High, Urgent

### Campos Importantes
- `lead_number`: Auto-generado (LEAD-2024-0234)
- `status`: Dónde está en el pipeline
- `priority`: Qué tan urgente
- `source`: De dónde vino
- `lead_score`: 0-100 (calculado automáticamente)
- `ai_close_probability`: % de cerrar (IA)
- `assigned_to`: Vendedor responsable
- `budget_min`, `budget_max`: Presupuesto
- `next_follow_up_date`: Cuándo hacer seguimiento

### Ejemplo
```json
{
  "lead_number": "LEAD-2024-0234",
  "first_name": "María",
  "last_name": "González",
  "email": "maria@email.com",
  "phone": "+1-305-555-0123",
  "status": "qualified",
  "priority": "high",
  "source": "facebook",
  "lead_score": 78,
  "ai_close_probability": 65,
  "budget_min": 300000,
  "budget_max": 450000,
  "assigned_to": "Juan Pérez",
  "interested_projects": ["Torres del Mar"],
  "next_follow_up_date": "2024-01-17T10:00:00Z"
}
```

## 💰 Quote (Cotización)

### ¿Qué es?
Propuesta formal de venta enviada a un lead.

### Estados
- **Draft**: Borrador
- **Sent**: Enviada al cliente
- **Viewed**: Cliente la vio
- **Accepted**: ¡Cliente aceptó!
- **Rejected**: Cliente rechazó
- **Expired**: Venció

### Campos Importantes
- `quote_number`: Auto-generado (QT-2024-0456)
- `unit_price`: Precio base
- `discount_percentage`, `discount_amount`: Descuentos
- `total`: Precio final (calculado automáticamente)
- `valid_until`: Fecha de vencimiento
- `financing_offered`: Si incluye financiamiento

### Ejemplo
```json
{
  "quote_number": "QT-2024-0234",
  "lead": "LEAD-2024-0234",
  "project": "Torres del Mar",
  "unit": "1205",
  "unit_price": 350000,
  "discount_percentage": 5,
  "discount_amount": 17500,
  "subtotal": 332500,
  "tax_amount": 23275,
  "total": 355775,
  "status": "sent",
  "valid_until": "2024-02-15",
  "financing_offered": true,
  "financing_terms": {
    "down_payment_percentage": 20,
    "monthly_payment": 1850,
    "term_months": 240
  }
}
```

## 📋 Activity (Actividad)

### ¿Qué es?
Registro de cada interacción con un lead. El "log" de todo.

### Tipos
- Call, Email, Meeting, Note, Task
- Quote Sent, Quote Viewed, Status Change

### Campos Importantes
- `activity_type`: Tipo de actividad
- `title`: Título corto
- `description`: Descripción detallada
- `user`: Quién la realizó
- `related_object`: A qué está relacionada (Lead, Project)
- `scheduled_date`, `completed_date`: Fechas

### Ejemplo
```json
{
  "activity_type": "call",
  "title": "Llamada de seguimiento",
  "description": "Cliente confirma visita. Preguntó sobre acabados.",
  "user": "Juan Pérez",
  "related_to": "LEAD-2024-0234",
  "scheduled_date": "2024-01-18T14:00:00Z",
  "completed_date": "2024-01-18T14:15:00Z",
  "duration_minutes": 15,
  "status": "completed"
}
```

---

# 3. API ENDPOINTS - DOCUMENTACIÓN COMPLETA

## 🔐 AUTENTICACIÓN

### POST `/api/auth/login/`

**🎯 Propósito:** Iniciar sesión y obtener JWT tokens

**📥 Request:**
```json
{
  "email": "juan@xyz.com",
  "password": "secure_password_123"
}
```

**📤 Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJh...",
  "refresh": "eyJ0eXAiOiJKV1QiLC..."
}
```

**💡 Uso:** Guardar access token para requests, refresh token para renovar.

---

### POST `/api/auth/refresh/`

**🎯 Propósito:** Renovar access token sin hacer login

**📥 Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLC..."
}
```

**📤 Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJo...",
  "refresh": "eyJ0eXAiOiJKV1QiLC..."
}
```

---

### GET `/api/auth/users/profile/`

**🎯 Propósito:** Obtener perfil del usuario actual

**Headers:** `Authorization: Bearer {access_token}`

**📤 Response:**
```json
{
  "id": "uuid-123",
  "email": "juan@xyz.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "role": "sales",
  "company": {
    "id": "uuid-company",
    "name": "Desarrollos XYZ"
  },
  "territories": ["Zona Norte"],
  "sales_target": 500000
}
```

---

## 👥 LEADS

### GET `/api/leads/`

**🎯 Propósito:** Listar leads con filtros avanzados

**Filtros Disponibles:**
```
?status=qualified              # Por status
?priority=high                 # Por prioridad
?source=facebook               # Por fuente
?assigned_to=current_user      # Solo mis leads
?score_min=70                  # Score mínimo
?budget_min=300000             # Presupuesto mínimo
?created_after=2024-01-01      # Fecha de creación
?search=maria                  # Búsqueda multi-campo
?ordering=-lead_score          # Ordenar por score (desc)
```

**Ejemplo de Uso:**
```bash
GET /api/leads/?status=qualified&score_min=70&priority_in=high,urgent
```

**📤 Response:**
```json
{
  "count": 150,
  "next": "http://.../api/leads/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid-123",
      "lead_number": "LEAD-2024-0234",
      "full_name": "María González",
      "email": "maria@email.com",
      "phone": "+1-305-555-0123",
      "status": "qualified",
      "priority": "high",
      "lead_score": 78,
      "ai_close_probability": 65,
      "assigned_to_name": "Juan Pérez",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

### POST `/api/leads/`

**🎯 Propósito:** Crear un nuevo lead

**📥 Request:**
```json
{
  "first_name": "Carlos",
  "last_name": "Rodríguez",
  "email": "carlos@email.com",
  "phone": "+1-305-555-9999",
  "source": "website",
  "source_detail": "Formulario - Torres del Mar",
  "interested_projects": ["project-uuid-123"],
  "budget_min": 250000,
  "budget_max": 400000,
  "notes": "Quiere 2 habitaciones, piso alto",
  "priority": "medium"
}
```

**📤 Response:**
```json
{
  "id": "uuid-456",
  "lead_number": "LEAD-2024-0235",
  "status": "new",
  "assigned_to": "current-user-id",
  "created_at": "2024-01-16T14:20:00Z",
  // ... resto de campos
}
```

---

### GET `/api/leads/{id}/timeline/`

**🎯 Propósito:** Ver historial completo de interacciones

**📤 Response:**
```json
[
  {
    "activity_type": "call",
    "title": "Llamada de seguimiento",
    "description": "Cliente preguntó sobre fechas de entrega",
    "user_name": "Juan Pérez",
    "created_at": "2024-01-16T10:00:00Z"
  },
  {
    "activity_type": "email",
    "title": "Envío de brochure",
    "user_name": "Juan Pérez",
    "created_at": "2024-01-15T15:30:00Z"
  }
]
```

---

### POST `/api/leads/{id}/add_note/`

**🎯 Propósito:** Agregar nota rápida con timestamp automático

**📥 Request:**
```json
{
  "note": "Cliente prefiere pisos altos (10+). Le interesa el apto 1505."
}
```

**📤 Response:**
```json
{
  "id": "uuid-123",
  "notes": "[2024-01-16 10:30:00] Juan Pérez: Cliente prefiere pisos altos...\n\n[2024-01-15 14:00:00] Juan Pérez: Primera llamada - no contestó"
}
```

---

### POST `/api/leads/bulk_assign/`

**🎯 Propósito:** Asignar múltiples leads de una vez

**💼 Caso de Uso:** Manager distribuye 50 leads del weekend entre su equipo

**📥 Request:**
```json
{
  "lead_ids": [
    "uuid-lead-1",
    "uuid-lead-2",
    "uuid-lead-3"
  ],
  "user_id": "uuid-maria"
}
```

**📤 Response:**
```json
{
  "message": "3 leads assigned successfully",
  "updated_count": 3
}
```

---

### GET `/api/leads/hot_leads/`

**🎯 Propósito:** Leads calientes que merecen atención inmediata

**Criterios:**
- Priority = "high" o "urgent" OR
- Lead Score >= 70
- Y NO están en closed_won ni closed_lost

**📤 Response:**
```json
[
  {
    "id": "uuid-123",
    "full_name": "María González",
    "lead_score": 85,
    "ai_close_probability": 72,
    "priority": "urgent",
    "status": "proposal",
    "next_follow_up_date": "2024-01-17T10:00:00Z"
  }
]
```

---

### GET `/api/leads/duplicates/`

**🎯 Propósito:** Detectar leads duplicados

**Detecta por:** Email o teléfono idéntico

**📤 Response:**
```json
[
  {
    "type": "email",
    "value": "maria@email.com",
    "count": 2,
    "leads": [
      {
        "id": "uuid-1",
        "lead_number": "LEAD-2024-0100",
        "status": "qualified",
        "created_at": "2024-01-10"
      },
      {
        "id": "uuid-2",
        "lead_number": "LEAD-2024-0234",
        "status": "new",
        "created_at": "2024-01-15"
      }
    ]
  }
]
```

---

### GET `/api/leads/upcoming_followups/`

**🎯 Propósito:** Follow-ups programados en próximos 7 días

**📤 Response:**
```json
[
  {
    "id": "uuid-123",
    "full_name": "Carlos Rodríguez",
    "next_follow_up_date": "2024-01-17T14:00:00Z",
    "status": "qualified",
    "notes": "Llamar para confirmar visita"
  }
]
```

---

### GET `/api/leads/performance_by_source/`

**🎯 Propósito:** Analizar ROI de fuentes de leads

**💼 Caso de Uso:** Marketing Manager decide dónde invertir presupuesto

**📤 Response:**
```json
[
  {
    "source": "website",
    "total_leads": 120,
    "converted": 28,
    "conversion_rate": 23.33,
    "avg_lead_score": 68.5
  },
  {
    "source": "facebook",
    "total_leads": 250,
    "converted": 35,
    "conversion_rate": 14.00,
    "avg_lead_score": 58.2
  },
  {
    "source": "referral",
    "total_leads": 45,
    "converted": 18,
    "conversion_rate": 40.00,
    "avg_lead_score": 75.8
  }
]
```

**💡 Insight:** Referencias tienen mejor conversion (40%) aunque menor volumen.

---

## 🏗️ PROJECTS

### GET `/api/projects/`

**🎯 Propósito:** Listar proyectos con filtros

**Filtros:**
```
?status=active                 # Solo activos
?city=Miami                    # Por ciudad
?price_max=500000              # Precio máximo
?available_units_min=5         # Con inventario disponible
?featured=true                 # Solo destacados
?type=residential              # Por tipo
```

**📤 Response:**
```json
{
  "results": [
    {
      "id": "uuid-proj-1",
      "name": "Torres del Mar",
      "code": "TDM-2024",
      "type": "residential",
      "status": "active",
      "city": "Miami Beach",
      "total_units": 120,
      "available_units": 48,
      "occupancy_rate": 60.0,
      "price_from": 250000,
      "price_to": 750000,
      "featured": true
    }
  ]
}
```

---

### GET `/api/projects/{id}/available_units/`

**🎯 Propósito:** Ver SOLO unidades disponibles

**💼 Caso de Uso:** Vendedor muestra opciones al cliente

**📤 Response:**
```json
[
  {
    "unit_number": "1205",
    "unit_type": "2BR/2BA",
    "floor": 12,
    "status": "available",
    "bedrooms": 2,
    "bathrooms": 2,
    "area_sqm": 85,
    "price": 350000,
    "orientation": "East",
    "view_type": "Ocean View"
  }
]
```

---

### GET `/api/projects/{id}/stats/`

**🎯 Propósito:** Dashboard completo del proyecto

**📤 Response:**
```json
{
  "total_units": 120,
  "available_units": 48,
  "sold_units": 65,
  "reserved_units": 7,
  "occupancy_rate": 60.0,
  "lead_count": 234,
  "quote_count": 89,
  "avg_unit_price": 425000,
  "units_by_type": {
    "1BR": 15,
    "2BR": 80,
    "3BR": 20,
    "Penthouse": 5
  }
}
```

---

## 🏠 UNITS

### POST `/api/projects/units/{id}/reserve/`

**🎯 Propósito:** Reservar unidad para un lead

**💼 Caso de Uso:** Lead necesita 48h para decidir, vendedor reserva

**📥 Request:**
```json
{
  "lead_id": "uuid-lead-123"
}
```

**📤 Response:**
```json
{
  "id": "uuid-unit-456",
  "unit_number": "1205",
  "status": "reserved",
  "reserved_by": {
    "id": "uuid-lead-123",
    "full_name": "María González"
  },
  "reserved_date": "2024-01-16T14:30:00Z"
}
```

**Qué pasa automáticamente:**
1. Unit.status → 'reserved'
2. Project.available_units → decrece 1
3. Project.reserved_units → aumenta 1

---

### POST `/api/projects/units/{id}/mark_as_sold/`

**🎯 Propósito:** Marcar unidad como vendida (venta final)

**💼 Caso de Uso:** Cliente firmó contrato y pagó enganche

**📥 Request:**
```json
{
  "sold_to": "María González - Contrato #2024-0234"
}
```

**📤 Response:**
```json
{
  "id": "uuid-unit-456",
  "unit_number": "1205",
  "status": "sold",
  "sold_to": "María González - Contrato #2024-0234",
  "sold_date": "2024-01-18T16:00:00Z"
}
```

---

## 💰 QUOTES

### POST `/api/quotes/`

**🎯 Propósito:** Crear cotización formal

**📥 Request:**
```json
{
  "lead": "uuid-lead-123",
  "project": "uuid-project-456",
  "unit": "uuid-unit-789",
  "unit_price": 350000,
  "discount_percentage": 5,
  "tax_percentage": 7,
  "valid_until": "2024-02-16T23:59:59Z",
  "financing_offered": true,
  "financing_terms": {
    "down_payment_percentage": 20,
    "monthly_payment": 1850,
    "term_months": 240
  }
}
```

**📤 Response:**
```json
{
  "quote_number": "QT-2024-0234",
  "status": "draft",
  "unit_price": 350000,
  "discount_amount": 17500,
  "subtotal": 332500,
  "tax_amount": 23275,
  "total": 355775
}
```

**💡 Sistema calcula automáticamente:** discount_amount, subtotal, tax_amount, total

---

### POST `/api/quotes/{id}/send/`

**🎯 Propósito:** Enviar cotización al cliente

**📤 Response:**
```json
{
  "status": "sent",
  "sent_date": "2024-01-16T15:30:00Z"
}
```

---

### POST `/api/quotes/{id}/accept/`

**🎯 Propósito:** Marcar cotización como aceptada

**📤 Response:**
```json
{
  "status": "accepted",
  "accepted_date": "2024-01-18T10:00:00Z"
}
```

---

## 📊 ANALYTICS

### GET `/api/analytics/dashboard/`

**🎯 Propósito:** Dashboard ejecutivo con métricas clave

**📤 Response:**
```json
{
  "leads": {
    "total": 1247,
    "new": 156,
    "qualified": 234,
    "converted": 89,
    "this_week": 47,
    "avg_score": 65.8
  },
  "quotes": {
    "total": 456,
    "sent": 123,
    "accepted": 45,
    "total_value": 15780000,
    "this_month": 89
  },
  "projects": {
    "total": 8,
    "active": 5,
    "total_units": 850,
    "available_units": 342
  },
  "activities": {
    "total": 5678,
    "this_week": 234,
    "by_type": {
      "call": 1200,
      "email": 890,
      "meeting": 450
    }
  }
}
```

---

### GET `/api/analytics/sales-funnel/`

**🎯 Propósito:** Ver embudo de ventas

**📤 Response:**
```json
[
  {"stage": "New", "count": 156},
  {"stage": "Contacted", "count": 234},
  {"stage": "Qualified", "count": 189},
  {"stage": "Proposal", "count": 123},
  {"stage": "Negotiation", "count": 67},
  {"stage": "Closed Won", "count": 45}
]
```

---

# 4. TESTING

## 🧪 Visión General

Suite completa de tests con **pytest**:
- ✅ 49 tests implementados
- ✅ Unit tests (modelos)
- ✅ Integration tests (API)
- ✅ E2E tests (flujos completos)
- ✅ Multi-tenant isolation

## 🚀 Ejecutar Tests

```bash
# Todos los tests
make test

# Con coverage
make test-coverage

# Solo unit tests
make test-unit

# Solo integration tests
make test-integration

# Test específico
docker-compose exec web pytest apps/leads/tests/test_api.py::test_create_lead
```

## 📊 Estructura de Tests

```
tests/
├── factories.py              # Factory Boy factories
├── test_e2e.py              # End-to-end tests
├── test_multi_tenant.py     # Multi-tenant tests
└── test_filters.py          # Filter tests

apps/
├── companies/tests/
│   ├── test_models.py       # Unit tests
│   └── test_api.py          # Integration tests
├── leads/tests/
│   ├── test_models.py
│   └── test_api.py
└── projects/tests/
    ├── test_models.py
    └── test_api.py
```

## 🎯 Ejemplo de Test

### Unit Test
```python
@pytest.mark.unit
def test_lead_full_name_property(company):
    lead = Lead.objects.create(
        company=company,
        first_name='John',
        last_name='Doe',
        email='john@test.com',
        phone='+1234567890'
    )
    assert lead.full_name == 'John Doe'
```

### Integration Test
```python
@pytest.mark.integration
def test_create_lead(authenticated_client):
    url = reverse('lead-list')
    data = {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane@test.com',
        'phone': '+1234567891'
    }
    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
```

### E2E Test
```python
@pytest.mark.e2e
def test_complete_sales_flow(api_client, company):
    # 1. Login
    # 2. Create project
    # 3. Create unit
    # 4. Create lead
    # 5. Create quote
    # 6. Send quote
    # 7. Accept quote
    # 8. Reserve unit
    # 9. Mark as sold
    # ✅ Verify all states
```

## 📈 Coverage

```bash
# Generar reporte
make test-coverage

# Ver HTML report
open htmlcov/index.html
```

---

# 5. FEATURES AVANZADOS

## 🤖 Base de Datos Preparada para IA

### pgvector - Búsqueda Semántica

**¿Qué es?**
Extensión de PostgreSQL para almacenar embeddings vectoriales y hacer búsqueda semántica.

**Ejemplo:**
```python
# Búsqueda tradicional
"apartamento 2 habitaciones cerca al parque"
→ Solo encuentra palabras exactas

# Búsqueda semántica con pgvector
"departamento para pareja con mascota cerca a zonas verdes"
→ Encuentra apartamentos de 2 habitaciones cerca a parques
   AUNQUE no usen esas palabras exactas
```

**Casos de Uso:**
1. **Búsqueda inteligente de unidades**
2. **Recomendaciones personalizadas**
3. **Clasificación automática de consultas**
4. **Detección de duplicados semánticos**

### JSONB para Datos Flexibles

Campos JSON en modelos permiten almacenar datos sin schema fijo:

```python
# Company features
{
  "ai_scoring": true,
  "bulk_sms": true,
  "whatsapp_integration": true,
  "custom_branding": {
    "logo_url": "...",
    "primary_color": "#0066cc"
  }
}

# Lead metadata
{
  "utm_source": "facebook",
  "utm_campaign": "summer-2024",
  "landing_page": "/projects/torres-del-mar",
  "device": "mobile",
  "location": {
    "lat": 25.7617,
    "lon": -80.1918
  }
}
```

### UUID Primary Keys

Todos los modelos usan UUID en lugar de integers:

**Beneficios:**
- No predecibles (seguridad)
- Únicos globalmente
- Fácil merge de datos
- Compatible con sistemas distribuidos

## 📊 Bulk Operations

### Bulk Assign Leads
```python
POST /api/leads/bulk_assign/
{
  "lead_ids": ["uuid-1", "uuid-2", "uuid-3"],
  "user_id": "uuid-maria"
}
```

### Bulk Status Change
```python
POST /api/leads/bulk_status_change/
{
  "lead_ids": ["uuid-1", "uuid-2"],
  "status": "contacted"
}
```

## 🔔 Celery Tasks (Asíncronos)

### Tareas Programadas
- Cálculo diario de lead scores
- Limpieza de datos antiguos
- Generación de reportes automáticos
- Notificaciones de follow-ups

### Tareas On-Demand
- Envío de emails masivos
- Exportación de datos CSV
- Generación de reportes pesados
- Sincronización con APIs externas

---

# 6. DESARROLLO

## 🛠️ Setup Entorno Local

```bash
# 1. Clonar repo
git clone <repo-url>
cd owly-api-ecosystem

# 2. Crear .env
cp .env.example .env

# 3. Iniciar servicios
docker-compose up -d

# 4. Migraciones
docker-compose exec web python manage.py migrate

# 5. Crear superuser
docker-compose exec web python manage.py createsuperuser

# 6. Poblar datos de prueba
docker-compose exec web python seed_database.py
```

## 📝 Comandos Útiles

```bash
# Logs
docker-compose logs -f web
docker-compose logs -f celery

# Shell
docker-compose exec web python manage.py shell

# Migraciones
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Tests
make test
make test-coverage

# Linting
flake8 apps/
black apps/ --check
```

## 🏗️ Agregar Nuevo Endpoint

1. **Crear método en ViewSet:**
```python
# apps/leads/views.py
@action(detail=False, methods=['get'])
def my_custom_endpoint(self, request):
    # Tu lógica aquí
    return Response(data)
```

2. **Automáticamente disponible en:**
```
GET /api/leads/my_custom_endpoint/
```

## 🎨 Mejores Prácticas

### API Design
- ✅ RESTful endpoints
- ✅ Verbos HTTP correctos
- ✅ Status codes apropiados
- ✅ Paginación en listas
- ✅ Filtros y búsqueda

### Database
- ✅ Índices en campos frecuentes
- ✅ Foreign keys apropiados
- ✅ Soft deletes
- ✅ Timestamps automáticos

### Security
- ✅ JWT tokens
- ✅ Password hashing
- ✅ CORS configurado
- ✅ SQL injection prevention
- ✅ Tenant isolation

### Performance
- ✅ Select related / prefetch related
- ✅ Database connection pooling
- ✅ Redis caching
- ✅ Celery para tareas pesadas

---

## 📚 Recursos Adicionales

- **Django Docs**: https://docs.djangoproject.com/
- **DRF Docs**: https://www.django-rest-framework.org/
- **Celery Docs**: https://docs.celeryproject.org/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **pgvector**: https://github.com/pgvector/pgvector

---

## 🎉 ¡Documentación Completa!

Has llegado al final de la guía completa. Ahora tienes:

✅ Comprensión profunda de la arquitectura
✅ Conocimiento de todos los modelos
✅ Documentación completa de endpoints
✅ Guía de testing
✅ Features avanzados explicados
✅ Mejores prácticas implementadas

**¿Siguiente paso?** 

- 🚀 [Deploy a AWS](DEPLOYMENT.md)
- 📖 [Ver README principal](README.md)
- 💻 Empezar a desarrollar

---

**Built with ❤️ for OWLY CRM**

