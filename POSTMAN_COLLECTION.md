# 📮 Colección Postman - OWLY CRM API

## 🎯 Cómo Usar Este Archivo

### Opción 1: Copiar y pegar en Postman
1. Copia cada comando curl
2. En Postman: Importar → Raw text → Pega el curl
3. Postman lo convierte automáticamente

### Opción 2: Ejecutar desde terminal
1. Copia el comando
2. Pega en terminal
3. Ejecuta

---

## 🔐 PASO 1: Autenticación (¡Empieza aquí!)

### Login - Obtener Tokens JWT

```bash
curl --location 'http://localhost:8000/api/auth/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "admin@owlycrm.com",
    "password": "admin123"
}'
```

**Response esperado**:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**IMPORTANTE**: Copia el `access` token y úsalo en todos los siguientes requests.

---

### Login con Usuario de Empresa

```bash
# Usuario de "Desarrollos Inmobiliarios Premium"
curl --location 'http://localhost:8000/api/auth/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "william.frías1@company-1.com",
    "password": "demo123"
}'
```

---

### Refresh Token

```bash
curl --location 'http://localhost:8000/api/auth/refresh/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "refresh": "TU_REFRESH_TOKEN_AQUI"
}'
```

---

### Get User Profile

```bash
curl --location 'http://localhost:8000/api/auth/users/profile/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Change Password

```bash
curl --location 'http://localhost:8000/api/auth/users/change_password/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{
    "old_password": "admin123",
    "new_password": "newpass123",
    "new_password_confirm": "newpass123"
}'
```

---

## 👥 LEADS - Gestión de Prospectos

### Listar Todos los Leads

```bash
curl --location 'http://localhost:8000/api/leads/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Listar Leads con Filtros

```bash
# Leads qualificados con score alto
curl --location 'http://localhost:8000/api/leads/?status=qualified&score_min=70' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

```bash
# Leads de Facebook con prioridad alta
curl --location 'http://localhost:8000/api/leads/?source=facebook&priority=high' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

```bash
# Leads creados esta semana
curl --location 'http://localhost:8000/api/leads/?created_after=2025-10-10T00:00:00Z' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

```bash
# Buscar por nombre o email
curl --location 'http://localhost:8000/api/leads/?search=maria' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Crear Nuevo Lead

```bash
curl --location 'http://localhost:8000/api/leads/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{
    "first_name": "Carlos",
    "last_name": "Rodríguez",
    "email": "carlos@example.com",
    "phone": "+1-305-555-1234",
    "source": "website",
    "priority": "high",
    "budget_min": 300000,
    "budget_max": 500000,
    "notes": "Interesado en 2BR, piso alto",
    "consent_given": true,
    "marketing_opt_in": true
}'
```

---

### Ver Detalle de un Lead

```bash
curl --location 'http://localhost:8000/api/leads/LEAD_ID_AQUI/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Actualizar Lead

```bash
curl --location --request PATCH 'http://localhost:8000/api/leads/LEAD_ID_AQUI/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{
    "priority": "urgent",
    "lead_score": 85,
    "notes": "Cliente muy interesado, llamar urgente"
}'
```

---

### Asignar Lead a Usuario

```bash
curl --location 'http://localhost:8000/api/leads/LEAD_ID_AQUI/assign/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user_id": "USER_ID_AQUI"
}'
```

---

### Cambiar Status de Lead

```bash
curl --location 'http://localhost:8000/api/leads/LEAD_ID_AQUI/change_status/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{
    "status": "contacted"
}'
```

---

### Agregar Nota a Lead

```bash
curl --location 'http://localhost:8000/api/leads/LEAD_ID_AQUI/add_note/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{
    "note": "Llamé y dejé mensaje. Cliente dijo que llamará de regreso mañana."
}'
```

---

### Ver Timeline de Lead

```bash
curl --location 'http://localhost:8000/api/leads/LEAD_ID_AQUI/timeline/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Bulk Assign Leads

```bash
curl --location 'http://localhost:8000/api/leads/bulk_assign/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{
    "lead_ids": [
        "LEAD_ID_1",
        "LEAD_ID_2",
        "LEAD_ID_3"
    ],
    "user_id": "USER_ID_AQUI"
}'
```

---

### Hot Leads (Alta Probabilidad)

```bash
curl --location 'http://localhost:8000/api/leads/hot_leads/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Upcoming Follow-ups (Próximos 7 días)

```bash
curl --location 'http://localhost:8000/api/leads/upcoming_followups/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Overdue Follow-ups (Vencidos)

```bash
curl --location 'http://localhost:8000/api/leads/overdue_followups/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Detectar Duplicados

```bash
curl --location 'http://localhost:8000/api/leads/duplicates/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Performance por Fuente

```bash
curl --location 'http://localhost:8000/api/leads/performance_by_source/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Lead Statistics

```bash
curl --location 'http://localhost:8000/api/leads/stats/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

## 🏗️ PROJECTS - Proyectos Inmobiliarios

### Listar Proyectos

```bash
curl --location 'http://localhost:8000/api/projects/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Listar Proyectos con Filtros

```bash
# Proyectos activos en Miami
curl --location 'http://localhost:8000/api/projects/?status=active&city=Miami' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

```bash
# Proyectos con más de 50 unidades disponibles
curl --location 'http://localhost:8000/api/projects/?available_units_min=50' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

```bash
# Proyectos por rango de precio
curl --location 'http://localhost:8000/api/projects/?price_min=200000&price_max=500000' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Crear Proyecto

```bash
curl --location 'http://localhost:8000/api/projects/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Sunset Towers Miami",
    "code": "STM-2025",
    "type": "residential",
    "status": "active",
    "description": "Luxury beachfront apartments with ocean views",
    "address": "100 Ocean Drive",
    "city": "Miami Beach",
    "state": "FL",
    "country": "USA",
    "postal_code": "33139",
    "total_units": 60,
    "available_units": 45,
    "price_from": 350000,
    "price_to": 850000,
    "amenities": ["Pool", "Gym", "Security 24/7", "Beach Access"],
    "featured": true
}'
```

---

### Ver Detalle de Proyecto

```bash
curl --location 'http://localhost:8000/api/projects/PROJECT_ID_AQUI/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Stats de un Proyecto

```bash
curl --location 'http://localhost:8000/api/projects/PROJECT_ID_AQUI/stats/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Unidades de un Proyecto

```bash
curl --location 'http://localhost:8000/api/projects/PROJECT_ID_AQUI/units/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Solo Unidades Disponibles

```bash
curl --location 'http://localhost:8000/api/projects/PROJECT_ID_AQUI/available_units/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Proyectos Destacados (Featured)

```bash
curl --location 'http://localhost:8000/api/projects/featured/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Proyectos por Ubicación

```bash
curl --location 'http://localhost:8000/api/projects/by_location/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

## 🏠 UNITS - Unidades Individuales

### Listar Unidades

```bash
curl --location 'http://localhost:8000/api/projects/units/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Unidades con Filtros

```bash
# Unidades disponibles, 2BR, piso 5+, bajo $400k
curl --location 'http://localhost:8000/api/projects/units/?status=available&bedrooms=2&floor_min=5&price_max=400000' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

```bash
# Unidades por proyecto específico
curl --location 'http://localhost:8000/api/projects/units/?project=PROJECT_ID' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Crear Unidad

```bash
curl --location 'http://localhost:8000/api/projects/units/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{
    "project": "PROJECT_ID_AQUI",
    "unit_number": "1205",
    "unit_type": "2BR/2BA",
    "floor": 12,
    "bedrooms": 2,
    "bathrooms": 2.0,
    "area_sqm": 95.5,
    "price": 450000,
    "status": "available",
    "orientation": "East",
    "view_type": "Ocean View"
}'
```

---

### Reservar Unidad para un Lead

```bash
curl --location 'http://localhost:8000/api/projects/units/UNIT_ID_AQUI/reserve/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{
    "lead_id": "LEAD_ID_AQUI"
}'
```

---

### Marcar Unidad como Vendida

```bash
curl --location 'http://localhost:8000/api/projects/units/UNIT_ID_AQUI/mark_as_sold/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{
    "sold_to": "María González - Contrato #2025-001"
}'
```

---

### Buscar Unidades Similares

```bash
curl --location 'http://localhost:8000/api/projects/units/similar/?bedrooms=2&unit_type=2BR' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

## 💰 QUOTES - Cotizaciones

### Listar Cotizaciones

```bash
curl --location 'http://localhost:8000/api/quotes/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Crear Cotización

```bash
curl --location 'http://localhost:8000/api/quotes/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{
    "lead": "LEAD_ID_AQUI",
    "project": "PROJECT_ID_AQUI",
    "unit": "UNIT_ID_AQUI",
    "unit_price": 450000,
    "discount_percentage": 5,
    "tax_percentage": 7,
    "valid_until": "2025-12-31T23:59:59Z",
    "financing_offered": true,
    "financing_terms": {
        "down_payment_percentage": 20,
        "monthly_payment": 1850,
        "term_months": 240
    },
    "notes": "Incluye parking y storage unit"
}'
```

---

### Enviar Cotización

```bash
curl --location 'http://localhost:8000/api/quotes/QUOTE_ID_AQUI/send/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{}'
```

---

### Aceptar Cotización

```bash
curl --location 'http://localhost:8000/api/quotes/QUOTE_ID_AQUI/accept/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{}'
```

---

### Rechazar Cotización

```bash
curl --location 'http://localhost:8000/api/quotes/QUOTE_ID_AQUI/reject/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{}'
```

---

## 📊 ANALYTICS - Reportes y Estadísticas

### Dashboard Stats

```bash
curl --location 'http://localhost:8000/api/analytics/dashboard/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

**Response incluye**:
- Total de leads, por status, avg score
- Cotizaciones enviadas, aceptadas, valor total
- Proyectos activos, unidades disponibles
- Actividades de la semana

---

### Sales Funnel

```bash
curl --location 'http://localhost:8000/api/analytics/sales-funnel/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Lead Analytics

```bash
curl --location 'http://localhost:8000/api/analytics/leads/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

## 🏢 COMPANIES - Empresas

### Listar Empresas

```bash
curl --location 'http://localhost:8000/api/companies/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Ver Detalle de Empresa

```bash
curl --location 'http://localhost:8000/api/companies/COMPANY_ID_AQUI/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Stats de Empresa

```bash
curl --location 'http://localhost:8000/api/companies/COMPANY_ID_AQUI/stats/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Crear Empresa

```bash
curl --location 'http://localhost:8000/api/companies/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Mi Nueva Inmobiliaria",
    "email": "contact@minueva.com",
    "plan": "professional",
    "phone": "+1-305-555-9999",
    "city": "Miami",
    "state": "FL",
    "country": "USA"
}'
```

---

## 👤 USERS - Usuarios

### Listar Usuarios

```bash
curl --location 'http://localhost:8000/api/auth/users/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Crear Usuario

```bash
curl --location 'http://localhost:8000/api/auth/users/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "nuevo.vendedor@company.com",
    "password": "secure123",
    "password_confirm": "secure123",
    "first_name": "Juan",
    "last_name": "Pérez",
    "role": "sales",
    "phone": "+1-305-555-7777"
}'
```

---

## 📋 ACTIVITIES - Actividades

### Listar Actividades

```bash
curl --location 'http://localhost:8000/api/activities/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Crear Actividad

```bash
curl --location 'http://localhost:8000/api/activities/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{
    "activity_type": "call",
    "title": "Llamada de seguimiento",
    "description": "Llamé al cliente para confirmar interés. Mostró interés en visitar el proyecto este sábado.",
    "content_type": 50,
    "object_id": "LEAD_ID_AQUI",
    "status": "completed",
    "completed_date": "2025-10-16T14:30:00Z",
    "duration_minutes": 15
}'
```

---

## ⏰ SCHEDULED TASKS - Tareas Programadas

### Listar Tareas Programadas

```bash
curl --location 'http://localhost:8000/api/scheduled-tasks/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Crear Tarea Programada

```bash
curl --location 'http://localhost:8000/api/scheduled-tasks/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Recordatorios Matutinos",
    "description": "Envía recordatorios de follow-ups a vendedores",
    "category": "followups",
    "task_name": "apps.leads.tasks.send_followup_reminders",
    "frequency": "daily",
    "hour": 8,
    "minute": 0,
    "is_active": true
}'
```

---

### Ver Plantillas de Tareas

```bash
curl --location 'http://localhost:8000/api/scheduled-tasks/templates/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

### Activar Tarea

```bash
curl --location 'http://localhost:8000/api/scheduled-tasks/TASK_ID_AQUI/activate/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{}'
```

---

### Pausar Tarea

```bash
curl --location 'http://localhost:8000/api/scheduled-tasks/TASK_ID_AQUI/deactivate/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{}'
```

---

### Ejecutar Tarea Ahora

```bash
curl --location 'http://localhost:8000/api/scheduled-tasks/TASK_ID_AQUI/run_now/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI' \
--header 'Content-Type: application/json' \
--data-raw '{}'
```

---

### Tareas por Categoría

```bash
curl --location 'http://localhost:8000/api/scheduled-tasks/by_category/' \
--header 'Authorization: Bearer TU_ACCESS_TOKEN_AQUI'
```

---

## ❤️ HEALTH CHECK

### Verificar Estado del Sistema

```bash
curl --location 'http://localhost:8000/api/health/'
```

**No requiere autenticación**

**Response esperado**:
```json
{
    "status": "healthy",
    "database": "connected",
    "cache": "connected"
}
```

---

## 🎯 FLUJO COMPLETO DE VENTA (Ejemplo)

### 1. Login

```bash
curl --location 'http://localhost:8000/api/auth/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "admin@owlycrm.com",
    "password": "admin123"
}'
```

**→ Guarda el `access` token**

---

### 2. Crear Lead

```bash
curl --location 'http://localhost:8000/api/leads/' \
--header 'Authorization: Bearer TU_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
    "first_name": "Ana",
    "last_name": "Martínez",
    "email": "ana@example.com",
    "phone": "+1-786-555-4321",
    "source": "website",
    "priority": "high"
}'
```

**→ Guarda el `id` del lead**

---

### 3. Ver Proyectos Disponibles

```bash
curl --location 'http://localhost:8000/api/projects/?status=active' \
--header 'Authorization: Bearer TU_TOKEN'
```

**→ Guarda el `id` de un proyecto**

---

### 4. Ver Unidades Disponibles del Proyecto

```bash
curl --location 'http://localhost:8000/api/projects/PROJECT_ID/available_units/' \
--header 'Authorization: Bearer TU_TOKEN'
```

**→ Guarda el `id` de una unidad**

---

### 5. Crear Cotización

```bash
curl --location 'http://localhost:8000/api/quotes/' \
--header 'Authorization: Bearer TU_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
    "lead": "LEAD_ID",
    "project": "PROJECT_ID",
    "unit": "UNIT_ID",
    "unit_price": 450000,
    "discount_percentage": 5,
    "tax_percentage": 7,
    "valid_until": "2025-12-31T23:59:59Z"
}'
```

**→ Guarda el `id` de la cotización**

---

### 6. Enviar Cotización

```bash
curl --location 'http://localhost:8000/api/quotes/QUOTE_ID/send/' \
--header 'Authorization: Bearer TU_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{}'
```

---

### 7. Aceptar Cotización

```bash
curl --location 'http://localhost:8000/api/quotes/QUOTE_ID/accept/' \
--header 'Authorization: Bearer TU_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{}'
```

---

### 8. Reservar Unidad

```bash
curl --location 'http://localhost:8000/api/projects/units/UNIT_ID/reserve/' \
--header 'Authorization: Bearer TU_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
    "lead_id": "LEAD_ID"
}'
```

---

### 9. Ver Dashboard con Stats

```bash
curl --location 'http://localhost:8000/api/analytics/dashboard/' \
--header 'Authorization: Bearer TU_TOKEN'
```

---

## 📝 Tips para Postman

### Configurar Variable de Entorno:

1. En Postman, crea un Environment llamado "OWLY Local"
2. Agrega variables:
   - `base_url`: `http://localhost:8000/api`
   - `access_token`: (Lo pegas después del login)
   - `lead_id`: (Lo pegas después de crear lead)
   - `project_id`: (etc.)

3. Usa en las requests:
   ```
   {{base_url}}/leads/
   Authorization: Bearer {{access_token}}
   ```

### Importar Colección:

1. Postman → Import → Raw text
2. Pega todos estos curls juntos
3. Postman los convierte automáticamente
4. Organiza en carpetas por módulo

### Pre-request Script para Token:

En Postman, agrega este script en la colección:

```javascript
// Pre-request Script
pm.sendRequest({
    url: 'http://localhost:8000/api/auth/login/',
    method: 'POST',
    header: 'Content-Type: application/json',
    body: {
        mode: 'raw',
        raw: JSON.stringify({
            email: 'admin@owlycrm.com',
            password: 'admin123'
        })
    }
}, function (err, res) {
    if (!err) {
        pm.environment.set('access_token', res.json().access);
    }
});
```

**Esto hace login automático antes de cada request!**

---

## 🎯 Requests Más Útiles Para Empezar

### 1. Login y Dashboard (Primero)

```bash
# 1. Login
curl --location 'http://localhost:8000/api/auth/login/' \
--header 'Content-Type: application/json' \
--data-raw '{"email": "admin@owlycrm.com", "password": "admin123"}'

# 2. Dashboard (usar token del login)
curl --location 'http://localhost:8000/api/analytics/dashboard/' \
--header 'Authorization: Bearer TU_TOKEN'
```

---

### 2. Ver Datos Existentes

```bash
# Leads
curl --location 'http://localhost:8000/api/leads/' \
--header 'Authorization: Bearer TU_TOKEN'

# Projects
curl --location 'http://localhost:8000/api/projects/' \
--header 'Authorization: Bearer TU_TOKEN'

# Quotes
curl --location 'http://localhost:8000/api/quotes/' \
--header 'Authorization: Bearer TU_TOKEN'
```

---

### 3. Probar Filtros

```bash
# Hot Leads
curl --location 'http://localhost:8000/api/leads/hot_leads/' \
--header 'Authorization: Bearer TU_TOKEN'

# Featured Projects
curl --location 'http://localhost:8000/api/projects/featured/' \
--header 'Authorization: Bearer TU_TOKEN'

# Available Units bajo $400k
curl --location 'http://localhost:8000/api/projects/units/?status=available&price_max=400000' \
--header 'Authorization: Bearer TU_TOKEN'
```

---

## 🔍 Buscar IDs para Testing

### Obtener un Lead ID:

```bash
curl --location 'http://localhost:8000/api/leads/?page_size=1' \
--header 'Authorization: Bearer TU_TOKEN'
```

Copia el `id` del primer resultado.

### Obtener un Project ID:

```bash
curl --location 'http://localhost:8000/api/projects/?page_size=1' \
--header 'Authorization: Bearer TU_TOKEN'
```

### Obtener un Unit ID:

```bash
curl --location 'http://localhost:8000/api/projects/units/?status=available&page_size=1' \
--header 'Authorization: Bearer TU_TOKEN'
```

---

## 📦 Archivo JSON para Importar en Postman

También puedes usar la **especificación OpenAPI** que genera Django:

```bash
# Descargar schema OpenAPI
curl --location 'http://localhost:8000/api/schema/' --output owly-crm-schema.json

# Luego en Postman:
# Import → Upload Files → Selecciona owly-crm-schema.json
```

**Esto importa TODOS los 83+ endpoints automáticamente!**

---

## 🎓 Recomendaciones

### Para Empezar:
1. ✅ Ejecuta Health Check (sin auth)
2. ✅ Login y guarda el token
3. ✅ Dashboard para ver stats
4. ✅ GET /api/leads/ para ver datos

### Para Testing:
1. ✅ Crea Environment en Postman
2. ✅ Guarda token como variable
3. ✅ Usa {{access_token}} en headers
4. ✅ Guarda IDs como variables

### Para Desarrollo:
1. ✅ Importa schema OpenAPI
2. ✅ Usa pre-request script para auto-login
3. ✅ Organiza en carpetas
4. ✅ Guarda colección para el equipo

---

## 🌐 URLs Útiles

| Recurso | URL |
|---------|-----|
| Admin | http://localhost:8000/admin/ |
| API Docs (Swagger) | http://localhost:8000/api/docs/ |
| OpenAPI Schema | http://localhost:8000/api/schema/ |
| Health Check | http://localhost:8000/api/health/ |

---

## 💡 Ejemplos Rápidos de Copia/Pega

### Setup Rápido en Postman:

```bash
# 1. Login (copia este curl en Postman)
curl --location 'http://localhost:8000/api/auth/login/' \
--header 'Content-Type: application/json' \
--data-raw '{"email": "admin@owlycrm.com", "password": "admin123"}'

# 2. Copia el access token del response

# 3. Dashboard (pega tu token)
curl --location 'http://localhost:8000/api/analytics/dashboard/' \
--header 'Authorization: Bearer PEGA_TU_TOKEN_AQUI'

# 4. Leads
curl --location 'http://localhost:8000/api/leads/' \
--header 'Authorization: Bearer PEGA_TU_TOKEN_AQUI'
```

---

**¡Listo para probar en Postman!** 🚀

Cada curl está listo para copiar y pegar. Solo recuerda:
1. Hacer login primero
2. Usar el token en todos los requests
3. Reemplazar IDs donde dice `_ID_AQUI`

