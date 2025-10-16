# 🏛️ Guía de Arquitectura - OWLY CRM API

## 🎯 Visión General

Este documento explica **cómo está construida** la API, **por qué** está diseñada así, y **cómo** todo trabaja junto.

---

## 🏗️ Arquitectura Multi-Tenant

### ¿Qué es Multi-Tenant?

**Multi-tenant** = Múltiples empresas (tenants) usando la misma aplicación con **datos completamente separados**.

### ¿Por qué Multi-Tenant?

**Beneficios:**
1. **Costo eficiente**: Una sola infraestructura para N empresas
2. **Mantenimiento simple**: Actualizar una vez, beneficia a todos
3. **Escalabilidad**: Agregar nueva empresa = solo crear registro
4. **Datos aislados**: Empresa A nunca ve datos de Empresa B

### Cómo Funciona:

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

### Aislamiento de Datos:

**Cada modelo tiene campo `company`**:
```python
class Lead(models.Model):
    company = models.ForeignKey('companies.Company', ...)
    # ...
```

**Middleware filtra automáticamente**:
```python
# Usuario de Company A hace request
GET /api/leads/

# Middleware añade filtro automático:
leads = Lead.objects.filter(company=user.company)

# Usuario SOLO ve leads de su empresa
```

**Imposible acceder datos de otra empresa**:
- Queries filtran por `company` automáticamente
- Permissions verifican ownership
- Middleware valida cada request

---

## 🔐 Sistema de Autenticación y Permisos

### JWT (JSON Web Tokens)

**¿Por qué JWT?**
- **Stateless**: No necesita sesiones en servidor
- **Escalable**: Perfecto para microservicios
- **Seguro**: Firmado criptográficamente
- **Mobile-friendly**: Fácil de usar en apps móviles

### Flujo de Autenticación:

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

### Sistema de Roles y Permisos:

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

### Permissions en la API:

```python
# Permission Classes:

1. IsAuthenticated
   → Usuario debe estar logueado

2. IsTenantUser
   → Usuario solo ve datos de su empresa

3. IsAdminUser
   → Solo admins pueden ejecutar

4. IsManagerOrAdmin
   → Managers y admins pueden ejecutar

# Ejemplos:
GET /api/leads/                    → IsAuthenticated + IsTenantUser
POST /api/leads/bulk_assign/       → IsManagerOrAdmin
POST /api/companies/{id}/upgrade/  → IsAdminUser
```

---

## 📊 Modelos y Relaciones

### Diagrama de Relaciones:

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

### Relaciones Explicadas:

**Company (1) → Users (N)**
- Una empresa tiene muchos usuarios
- Usuario pertenece a una sola empresa

**Company (1) → Projects (N)**
- Una empresa tiene muchos proyectos
- Proyecto pertenece a una empresa

**Project (1) → Units (N)**
- Un proyecto tiene muchas unidades
- Unidad pertenece a un proyecto

**Company (1) → Leads (N)**
- Una empresa tiene muchos leads
- Lead pertenece a una empresa

**Lead (N) ← → Projects (N)** [Many-to-Many]
- Un lead puede estar interesado en varios proyectos
- Un proyecto puede tener múltiples leads interesados

**Lead (1) → Quotes (N)**
- Un lead puede tener múltiples cotizaciones
- Cotización pertenece a un lead

**Quote (1) → Unit (1)**
- Una cotización es para una unidad específica

**User (1) → Leads (N)** [assigned_to]
- Un usuario tiene leads asignados
- Lead tiene un usuario responsable

---

## 🔄 Flujos de Trabajo

### Flujo 1: Lead → Cliente (Happy Path)

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
│  2. Sistema auto-asigna a vendedor de esa zona              │
│     Vendedor recibe notificación                             │
│     Status: NEW → CONTACTED                                  │
└──────────────┬───────────────────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────────────────┐
│  CALIFICACIÓN                                                │
├──────────────────────────────────────────────────────────────┤
│  3. Vendedor llama, califica lead                           │
│     POST /api/leads/{id}/add_note/                          │
│     Verifica presupuesto, timing, interés                    │
│     Status: CONTACTED → QUALIFIED                            │
└──────────────┬───────────────────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────────────────┐
│  BÚSQUEDA DE OPCIONES                                        │
├──────────────────────────────────────────────────────────────┤
│  4. Vendedor busca proyectos que match                      │
│     GET /api/projects/?city=Miami&price_max=500000          │
│     GET /api/projects/{id}/available_units/                 │
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
│  6. Cliente revisa, negocia                                 │
│     POST /api/quotes/{id}/mark_viewed/                      │
│     Llamadas, ajustes de precio                              │
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
│  8. Contrato firmado, pago recibido                         │
│     POST /api/projects/units/{id}/mark_as_sold/             │
│     Lead.converted_to_customer = true                        │
│     Unit.status = 'sold'                                     │
└──────────────────────────────────────────────────────────────┘
```

### Flujo 2: Manager Distribuye Leads

```
1. Llegaron 50 leads del weekend
   GET /api/leads/?status=new&created_after=2024-01-13

2. Manager revisa y categoriza
   - 20 leads calientes → Juan (top closer)
   - 15 leads medios → María (vendedora senior)
   - 15 leads fríos → Pedro (vendedor junior)

3. Asigna en bulk
   POST /api/leads/bulk_assign/
   {
     "lead_ids": [20 ids de leads calientes],
     "user_id": "juan_id"
   }

4. Equipo recibe notificaciones
   Cada vendedor ve sus nuevos leads asignados

5. Manager monitorea
   GET /api/analytics/dashboard/
   Ve quién está convirtiendo mejor
```

### Flujo 3: Cliente Busca Propiedad

```
Frontend App / Website:

1. Cliente busca:
   "2 habitaciones, Miami Beach, hasta $400k"
   
2. App llama API:
   GET /api/projects/?city=Miami Beach&status=active
   
3. Cliente selecciona proyecto:
   GET /api/projects/{id}/available_units/?bedrooms=2&price_max=400000
   
4. Cliente ve unidades disponibles:
   - Apto 1205: $350k, Piso 12, Vista al mar
   - Apto 1305: $360k, Piso 13, Vista al mar
   
5. Cliente se interesa:
   POST /api/leads/ (captura info del cliente)
   
6. Vendedor contacta:
   POST /api/leads/{id}/add_note/
   "Cliente vio aptos 1205 y 1305, prefiere 1305"
   
7. Vendedor envía cotización:
   POST /api/quotes/ (para apto 1305)
   POST /api/quotes/{id}/send/
   
8. Cliente acepta:
   POST /api/quotes/{id}/accept/
   
9. Reserva:
   POST /api/projects/units/{unit_id}/reserve/
```

---

## 🗄️ Estructura de Base de Datos

### Tablas Principales:

```sql
companies_company          -- Empresas (tenants)
users_user                 -- Usuarios
projects_project           -- Proyectos inmobiliarios
projects_unit              -- Unidades individuales
leads_lead                 -- Leads/Prospectos
quotes_quote               -- Cotizaciones
quotes_quotetemplate       -- Plantillas de cotización
activities_activity        -- Actividades/Interacciones

-- Django internals
auth_group
auth_permission
django_session
django_celery_beat_*       -- Tareas programadas
```

### Índices Importantes:

**Performance Optimization:**
```sql
-- Búsquedas frecuentes:
leads_lead (company, status)         -- Ver leads por status
leads_lead (assigned_to)             -- Leads de un vendedor
leads_lead (lead_score DESC)         -- Ordenar por score
projects_project (company, status)   -- Proyectos activos
projects_unit (project, status)      -- Unidades disponibles

-- UUID primary keys:
Todos los modelos usan UUID (no integers incrementales)
Beneficio: Seguridad, no predecibles, merge fácil
```

---

## 🚀 Capa de API (Django REST Framework)

### Arquitectura de Capas:

```
┌─────────────────────────────────────────────────────────┐
│  1. URLS (Routing)                                      │
│     apps/leads/urls.py                                  │
│     Define qué URL llama qué view                       │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│  2. VIEWS (Business Logic)                              │
│     apps/leads/views.py                                 │
│     LeadViewSet - maneja requests, aplica permisos      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│  3. SERIALIZERS (Validación + Transformación)           │
│     apps/leads/serializers.py                           │
│     Valida input, transforma a JSON                     │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│  4. MODELS (Database Layer)                             │
│     apps/leads/models.py                                │
│     Define estructura de datos, guarda en DB            │
└────────────────────┬────────────────────────────────────┘
                     │
                ┌────▼────┐
                │  POSTGRES│
                └─────────┘
```

### Ejemplo de Request Completo:

```
REQUEST:
GET /api/leads/?status=qualified&score_min=70

↓

1. URL Routing (urls.py):
   /api/leads/ → LeadViewSet.list()

↓

2. Authentication:
   JWT middleware valida token
   Extrae user_id del token

↓

3. Permissions:
   IsTenantUser verifica que user pertenece a una company

↓

4. View (views.py):
   get_queryset() filtra por company
   Aplica filtros: status=qualified, score>=70

↓

5. Query Database:
   SELECT * FROM leads_lead
   WHERE company_id = 'user-company-id'
   AND status = 'qualified'
   AND lead_score >= 70
   AND is_deleted = false

↓

6. Serializer:
   Transforma objetos Python → JSON
   Añade campos calculados (full_name, etc.)

↓

RESPONSE:
{
  "count": 25,
  "results": [
    {
      "id": "uuid-123",
      "full_name": "María González",
      "status": "qualified",
      "lead_score": 85
    }
  ]
}
```

---

## ⚙️ Servicios en Docker

### Arquitectura de Contenedores:

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

### Responsabilidades de Cada Servicio:

**WEB (Django + Gunicorn)**
- Sirve la API REST
- Procesa requests HTTP
- Valida autenticación
- Ejecuta business logic
- 3 workers para concurrencia

**PostgreSQL**
- Almacena todos los datos
- Transacciones ACID
- Índices para performance
- Backup automático

**Redis**
- Cache de queries
- Session storage
- Celery message broker
- Celery result backend

**Celery Worker**
- Tareas asíncronas
- Envío de emails
- Generación de reportes
- Cálculos pesados

**Celery Beat**
- Tareas programadas
- Cálculo diario de scores
- Limpieza de datos
- Reportes automáticos

---

## 🔒 Seguridad

### Capas de Seguridad:

```
┌─────────────────────────────────────────────────────────────┐
│  1. HTTPS/SSL                                               │
│     Todo el tráfico encriptado en producción                │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│  2. CORS                                                    │
│     Solo orígenes permitidos pueden hacer requests          │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│  3. JWT Authentication                                      │
│     Token firmado, expira, rotación automática              │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│  4. Permissions                                             │
│     Verificación de roles y ownership                       │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│  5. Tenant Isolation                                        │
│     Filtrado automático por company                         │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│  6. Django ORM                                              │
│     SQL injection prevention                                │
└────────────────────┬────────────────────────────────────────┘
                     │
                ┌────▼────┐
                │ DATABASE│
                └─────────┘
```

### Validaciones:

1. **Input Validation** (Serializers)
   - Email format
   - Phone format
   - Required fields
   - Data types

2. **Business Rules** (Views)
   - Solo puedes ver leads de tu empresa
   - Solo manager puede reasignar leads
   - Unidad debe estar disponible para reservar

3. **Database Constraints**
   - Unique constraints (email, lead_number)
   - Foreign keys
   - NOT NULL constraints

---

## 📈 Escalabilidad

### Horizontal Scaling (AWS):

```
┌─────────────────────────────────────────────────────────────┐
│                   LOAD BALANCER                             │
└────────┬────────────────────────┬───────────────────────────┘
         │                        │
    ┌────▼────┐              ┌────▼────┐
    │  WEB 1  │              │  WEB 2  │  ... hasta N
    └────┬────┘              └────┬────┘
         │                        │
         └────────┬───────────────┘
                  │
         ┌────────▼────────┐
         │   RDS (Primary) │
         │   + Read Replica│
         └─────────────────┘
```

**Componentes Escalables:**
- Web: 2-20 instancias según carga
- Celery Workers: 1-10 según tareas
- RDS: Read replicas para queries
- Redis: Redis Cluster para high availability

---

## 🎯 Casos de Uso de Arquitectura

### Caso 1: Nueva Empresa se Une

```
1. Creas Company en /admin/
   Name: "Nueva Inmobiliaria XYZ"
   Plan: Professional
   
2. Sistema crea slug automáticamente:
   slug: "nueva-inmobiliaria-xyz"
   
3. Creas primer usuario admin:
   Email: admin@xyz.com
   Company: Nueva Inmobiliaria XYZ
   Role: Admin
   
4. Admin XYZ puede:
   ✅ Crear sus proyectos
   ✅ Invitar su equipo
   ✅ Importar leads
   ✅ Configurar branding

5. Datos completamente aislados:
   ✅ XYZ nunca ve datos de otras empresas
   ✅ Otras empresas nunca ven datos de XYZ
```

### Caso 2: Escalar para Black Friday

```
Situación:
- Campaña masiva de Black Friday
- Esperan 10,000 leads en un día
- Tráfico 20x normal

Solución con esta arquitectura:

1. AWS Auto Scaling:
   2 instancias → 10 instancias automáticamente

2. Database Connection Pooling:
   Reusa conexiones, no crea nuevas

3. Redis Caching:
   Queries frecuentes en cache

4. Celery:
   Procesamiento de leads en background

5. Bulk Operations:
   /api/leads/bulk_assign/ para distribuir rápido

Resultado:
✅ Sistema maneja la carga
✅ Performance se mantiene
✅ Costos controlados (auto-scaling down después)
```

---

## 🔧 Extensibilidad

### Agregar Nuevo Modelo:

```python
# 1. Crear modelo
class Customer(TenantAwareModel):
    lead = models.ForeignKey(Lead, ...)
    contract_number = models.CharField(...)
    # ...

# 2. Crear serializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

# 3. Crear viewset
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsTenantUser]

# 4. Registrar URLs
router.register(r'customers', CustomerViewSet)

# ¡Listo! Tienes CRUD completo automáticamente:
# GET    /api/customers/
# POST   /api/customers/
# GET    /api/customers/{id}/
# PUT    /api/customers/{id}/
# DELETE /api/customers/{id}/
```

### Agregar Endpoint Personalizado:

```python
# En tu ViewSet:
@action(detail=False, methods=['get'])
def my_custom_endpoint(self, request):
    # Tu lógica aquí
    return Response(data)

# Automáticamente disponible en:
# GET /api/leads/my_custom_endpoint/
```

---

## 📊 Monitoreo y Observabilidad

### Health Checks:

```
GET /api/health/

Responde:
{
  "status": "healthy",
  "database": "connected",
  "cache": "connected"
}

Si algo falla:
{
  "status": "unhealthy",
  "database": "error: connection timeout",
  "cache": "connected"
}
```

**AWS usa esto para:**
- Load balancer health checks
- Auto-scaling decisions
- Alertas automáticas

### Logging:

**Niveles:**
1. ERROR: Errores que requieren acción
2. WARNING: Situaciones anormales
3. INFO: Eventos importantes
4. DEBUG: Información detallada (solo desarrollo)

**Destinos:**
- Console: Para Docker logs
- File: `/app/logs/django.log`
- Sentry: Error tracking en producción

---

## 🎯 Mejores Prácticas Implementadas

### API Design:
✅ RESTful endpoints
✅ Verbos HTTP correctos (GET/POST/PUT/DELETE)
✅ Status codes apropiados (200, 201, 400, 404, 500)
✅ Paginación en listas
✅ Filtros y búsqueda
✅ Versionado preparado

### Database:
✅ Índices en campos frecuentes
✅ Foreign keys con ON DELETE apropiado
✅ Soft deletes (is_deleted flag)
✅ Timestamps automáticos
✅ JSON fields para flexibilidad

### Security:
✅ JWT tokens
✅ Password hashing (PBKDF2)
✅ CORS configuration
✅ SQL injection prevention (ORM)
✅ XSS protection
✅ CSRF protection

### Performance:
✅ Select related / prefetch related
✅ Database connection pooling
✅ Redis caching
✅ Celery para tareas pesadas
✅ Índices optimizados

---

## 📚 Referencias

- **Django Documentation**: https://docs.djangoproject.com/
- **DRF Documentation**: https://www.django-rest-framework.org/
- **Celery Documentation**: https://docs.celeryproject.org/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/

---

**Para entender los modelos**: [MODELS_DOCUMENTATION.md](MODELS_DOCUMENTATION.md)
**Para usar los endpoints**: [ENDPOINTS_GUIDE.md](ENDPOINTS_GUIDE.md)
**Para mejoras recientes**: [API_ENHANCEMENTS.md](API_ENHANCEMENTS.md)

