# 🚀 Guía Completa de Endpoints - OWLY CRM API

## 📖 Cómo Leer Esta Guía

Cada endpoint incluye:
- **🎯 Intención**: Por qué existe este endpoint
- **💼 Caso de Uso Real**: Cuándo lo usarías
- **📥 Request**: Qué enviar
- **📤 Response**: Qué recibes
- **💡 Tips**: Mejores prácticas

---

## 🔐 AUTENTICACIÓN

### POST `/api/auth/login/`

**🎯 Intención**: Permitir que un usuario inicie sesión y obtenga tokens JWT para acceder a la API.

**💼 Caso de Uso Real**:
- Usuario abre la app web/móvil
- Ingresa email y contraseña
- App llama a este endpoint
- Recibe tokens que usa en todas las siguientes llamadas

**📥 Request**:
```json
{
  "email": "juan@xyz.com",
  "password": "secure_password_123"
}
```

**📤 Response**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJh...",  // Token de acceso (válido 1 hora)
  "refresh": "eyJ0eXAiOiJKV1QiLC..."    // Token para renovar (válido 7 días)
}
```

**💡 Tips**:
- Guarda el `access` token en memoria (no localStorage por seguridad)
- Guarda el `refresh` token en httpOnly cookie
- Incluye el access token en cada request: `Authorization: Bearer {access_token}`

---

### POST `/api/auth/refresh/`

**🎯 Intención**: Renovar el access token cuando expire, sin hacer login de nuevo.

**💼 Caso de Uso Real**:
- Usuario ha estado usando la app por 1 hora
- Access token expira
- App automáticamente llama a refresh
- Usuario continúa sin interrupciones

**📥 Request**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLC..."
}
```

**📤 Response**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJo...",  // Nuevo access token
  "refresh": "eyJ0eXAiOiJKV1QiLC..."   // Nuevo refresh token (rotación)
}
```

---

## 👥 LEADS - Gestión de Prospectos

### GET `/api/leads/`

**🎯 Intención**: Listar todos los leads con filtros avanzados para encontrar exactamente lo que necesitas.

**💼 Casos de Uso Reales**:

**Caso 1: Ver mis leads asignados**
```bash
GET /api/leads/?assigned_to=current_user
```
→ Vendedor ve solo sus leads

**Caso 2: Buscar leads calientes con presupuesto alto**
```bash
GET /api/leads/?score_min=70&budget_min=300000&status=qualified
```
→ Manager busca mejores oportunidades

**Caso 3: Leads que requieren atención**
```bash
GET /api/leads/?requires_attention=true&priority_in=high,urgent
```
→ Ver leads que no se han contactado en días

**📤 Response**:
```json
{
  "count": 150,
  "next": "http://.../api/leads/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid-123",
      "lead_number": "LEAD-2024-0234",
      "first_name": "María",
      "last_name": "González",
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

**💡 Tips**:
- Usa `?search=maria` para búsqueda rápida
- Combina filtros: `?status=new&source=facebook&created_after=2024-01-01`
- Ordena: `?ordering=-lead_score` (mayor score primero)

---

### POST `/api/leads/`

**🎯 Intención**: Crear un nuevo lead en el sistema.

**💼 Casos de Uso Reales**:

**Caso 1: Lead desde formulario web**
```json
{
  "first_name": "Carlos",
  "last_name": "Rodríguez",
  "email": "carlos@email.com",
  "phone": "+1-305-555-9999",
  "source": "website",
  "source_detail": "Formulario de contacto - Torres del Mar",
  "interested_projects": ["project-uuid-123"],
  "budget_min": 250000,
  "budget_max": 400000,
  "notes": "Quiere 2 habitaciones, piso alto",
  "consent_given": true,
  "marketing_opt_in": true
}
```

**Caso 2: Lead desde Facebook Ads**
```json
{
  "first_name": "Ana",
  "last_name": "Martínez",
  "email": "ana@email.com",
  "phone": "+1-786-555-1111",
  "source": "facebook",
  "source_detail": "Campaign: Summer 2024 - Ad Set: 2BR Apartments",
  "priority": "high"
}
```

**📤 Response**:
```json
{
  "id": "uuid-456",
  "lead_number": "LEAD-2024-0235",  // Auto-generado
  "status": "new",                  // Estado inicial
  "assigned_to": "current-user-id", // Auto-asignado
  "created_at": "2024-01-16T14:20:00Z",
  // ... resto de campos
}
```

**💡 Tips**:
- El lead se auto-asigna al usuario que lo crea
- `lead_number` se genera automáticamente
- Si incluyes `assigned_to`, puedes asignarlo a otro vendedor

---

### GET `/api/leads/{id}/timeline/`

**🎯 Intención**: Ver el historial completo de interacciones con un lead.

**💼 Caso de Uso Real**:
- Vendedor abre ficha de lead
- Ve timeline con todas las llamadas, emails, reuniones
- Entiende contexto completo antes de contactar

**📤 Response**:
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
  },
  {
    "activity_type": "status_change",
    "title": "Estado cambiado: new → contacted",
    "user_name": "Sistema",
    "created_at": "2024-01-15T09:00:00Z"
  }
]
```

**💡 Por qué es útil**:
- Continuidad cuando el lead cambia de vendedor
- Manager puede supervisar actividad del equipo
- Documentación de todas las interacciones

---

### POST `/api/leads/{id}/add_note/`

**🎯 Intención**: Agregar una nota rápida a un lead con timestamp automático.

**💼 Caso de Uso Real**:
- Acabas de llamar al cliente
- Quieres registrar rápido lo que discutieron
- No necesitas crear una Activity completa

**📥 Request**:
```json
{
  "note": "Cliente menciona que prefiere pisos altos (10+). Le interesa más el apto 1505. Volveré a llamar el viernes."
}
```

**📤 Response**:
```json
{
  "id": "uuid-123",
  "notes": "[2024-01-16 10:30:00] Juan Pérez: Cliente menciona que prefiere pisos altos (10+). Le interesa más el apto 1505. Volveré a llamar el viernes.\n\n[2024-01-15 14:00:00] Juan Pérez: Primera llamada - no contestó"
}
```

**💡 Por qué es útil**:
- Notas quedan con timestamp y nombre del usuario
- Historial de notas en un solo campo
- Más rápido que crear Activities

---

### POST `/api/leads/bulk_assign/`

**🎯 Intención**: Asignar múltiples leads a un vendedor de una sola vez.

**💼 Casos de Uso Reales**:

**Caso 1: Manager distribuye leads nuevos**
- Llegaron 50 leads del weekend
- Manager los revisa y distribuye entre su equipo

**Caso 2: Reasignación por vacaciones**
- Juan se va de vacaciones
- Manager reasigna todos sus leads activos a María

**📥 Request**:
```json
{
  "lead_ids": [
    "uuid-lead-1",
    "uuid-lead-2",
    "uuid-lead-3",
    "uuid-lead-4",
    "uuid-lead-5"
  ],
  "user_id": "uuid-maria"
}
```

**📤 Response**:
```json
{
  "message": "5 leads assigned successfully",
  "updated_count": 5
}
```

**💡 Por qué es útil**:
- Ahorra tiempo vs asignar uno por uno
- Mantiene registro de quién asignó (assigned_by)
- Actualiza assigned_date automáticamente

---

### POST `/api/leads/bulk_status_change/`

**🎯 Intención**: Cambiar el estado de múltiples leads simultáneamente.

**💼 Caso de Uso Real**:
- Hiciste evento de puertas abiertas
- 20 leads asistieron
- Los marcas todos como "contacted" al mismo tiempo

**📥 Request**:
```json
{
  "lead_ids": ["uuid-1", "uuid-2", "uuid-3"],
  "status": "contacted"
}
```

**📤 Response**:
```json
{
  "message": "20 leads updated successfully",
  "updated_count": 20
}
```

---

### GET `/api/leads/hot_leads/`

**🎯 Intención**: Encontrar leads con alta probabilidad de cerrar que merecen atención inmediata.

**💼 Caso de Uso Real**:
- Inicio del día
- Vendedor revisa qué leads atender primero
- Ve leads calientes para maximizar conversiones

**Criterios de "hot lead"**:
- Priority = "high" o "urgent" OR
- Lead Score >= 70
- Y NO están en closed_won ni closed_lost

**📤 Response**:
```json
[
  {
    "id": "uuid-123",
    "full_name": "María González",
    "lead_score": 85,
    "ai_close_probability": 72,
    "priority": "urgent",
    "status": "proposal",
    "next_follow_up_date": "2024-01-17T10:00:00Z",
    "notes": "Lista para cerrar, esperando aprobación del banco"
  }
]
```

**💡 Por qué es útil**:
- Priorización automática
- Focus en leads con mayor ROI
- Evita perder oportunidades calientes

---

### GET `/api/leads/duplicates/`

**🎯 Intención**: Detectar leads duplicados antes de que causen problemas.

**💼 Casos de Uso Reales**:

**Caso 1: Antes de importar lista**
- Tienes lista de 500 leads de evento
- Verificas duplicados antes de importar
- Evitas crear duplicados

**Caso 2: Limpieza de base de datos**
- Quincenalmente revisas duplicados
- Merge o eliminas según sea necesario

**Detecta duplicados por**:
- Email idéntico
- Teléfono idéntico

**📤 Response**:
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

**💡 Por qué es útil**:
- Previene confusión en el equipo
- Evita contactar mismo lead múltiples veces
- Mejora calidad de datos

---

### GET `/api/leads/upcoming_followups/`

**🎯 Intención**: Ver qué leads necesitan seguimiento en los próximos 7 días.

**💼 Caso de Uso Real**:
- Lunes por la mañana
- Vendedor planea su semana
- Ve todas las follow-ups programadas

**📤 Response**:
```json
[
  {
    "id": "uuid-123",
    "full_name": "Carlos Rodríguez",
    "next_follow_up_date": "2024-01-17T14:00:00Z",
    "status": "qualified",
    "notes": "Llamar para confirmar visita al apto 1205"
  },
  {
    "id": "uuid-456",
    "full_name": "Ana Martínez",
    "next_follow_up_date": "2024-01-19T10:00:00Z",
    "status": "proposal",
    "notes": "Seguimiento post-envío de cotización"
  }
]
```

**💡 Por qué es útil**:
- Nunca olvidas hacer seguimiento
- Planificación semanal
- Mejora experiencia del cliente

---

### GET `/api/leads/overdue_followups/`

**🎯 Intención**: Identificar leads donde se pasó la fecha de seguimiento (¡urgente!).

**💼 Caso de Uso Real**:
- Manager revisa qué vendedores tienen follow-ups atrasados
- Vendedor ve qué llamadas debió hacer ayer

**📤 Response**:
```json
[
  {
    "id": "uuid-789",
    "full_name": "Pedro López",
    "next_follow_up_date": "2024-01-14T10:00:00Z",  // Era hace 2 días!
    "status": "contacted",
    "assigned_to_name": "Juan Pérez",
    "days_overdue": 2
  }
]
```

**💡 Por qué es útil**:
- Recuperar leads que se están enfriando
- Accountability del equipo
- Prevenir pérdida de ventas por falta de seguimiento

---

### GET `/api/leads/performance_by_source/`

**🎯 Intención**: Analizar qué fuente de leads genera mejores resultados (Marketing Analytics).

**💼 Caso de Uso Real**:
- Marketing Manager revisa ROI de campañas
- Decide dónde invertir más presupuesto

**📤 Response**:
```json
[
  {
    "source": "website",
    "source_name": "Website",
    "total_leads": 120,
    "converted": 28,
    "conversion_rate": 23.33,
    "avg_lead_score": 68.5
  },
  {
    "source": "facebook",
    "source_name": "Facebook",
    "total_leads": 250,
    "converted": 35,
    "conversion_rate": 14.00,
    "avg_lead_score": 58.2
  },
  {
    "source": "referral",
    "source_name": "Referral",
    "total_leads": 45,
    "converted": 18,
    "conversion_rate": 40.00,  // ¡Mejor conversión!
    "avg_lead_score": 75.8
  }
]
```

**💡 Insights del ejemplo**:
- Referencias tienen mejor conversion rate (40%)
- Website trae leads de mejor calidad (score 68.5)
- Facebook trae volumen pero menor conversión
- **Acción**: Invertir más en programa de referencias

---

## 🏗️ PROJECTS - Gestión de Proyectos

### GET `/api/projects/`

**🎯 Intención**: Listar proyectos inmobiliarios con filtros para encontrar el indicado.

**💼 Casos de Uso Reales**:

**Caso 1: Vendedor busca opciones para un lead**
```bash
GET /api/projects/?status=active&price_max=500000&city=Miami&available_units_min=5
```
→ Proyectos activos en Miami con inventario disponible

**Caso 2: Manager revisa proyectos próximos a sold out**
```bash
GET /api/projects/?status=active&available_units_min=1&available_units_max=10
```
→ Proyectos con poco inventario (actuar rápido!)

**📤 Response**:
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
      "main_image": "https://...",
      "featured": true
    }
  ]
}
```

---

### GET `/api/projects/{id}/available_units/`

**🎯 Intención**: Ver SOLO las unidades disponibles de un proyecto (no mostrar vendidas/reservadas).

**💼 Caso de Uso Real**:
- Lead quiere ver qué hay disponible en Torres del Mar
- Vendedor filtra solo disponibles, ordenadas por piso

**📤 Response**:
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
  },
  {
    "unit_number": "1505",
    "unit_type": "2BR/2BA",
    "floor": 15,
    "status": "available",
    "bedrooms": 2,
    "bathrooms": 2,
    "area_sqm": 87,
    "price": 375000,
    "orientation": "East",
    "view_type": "Ocean View"
  }
]
```

**💡 Por qué es útil**:
- Cliente no ve unidades ya vendidas
- Lista limpia para presentación
- Ordenada por piso o precio

---

### GET `/api/projects/featured/`

**🎯 Intención**: Proyectos destacados para mostrar en homepage o campañas.

**💼 Caso de Uso Real**:
- Website muestra proyectos destacados en portada
- App móvil muestra carrusel de proyectos premium

**📤 Response**:
```json
[
  {
    "id": "uuid-1",
    "name": "Torres del Mar - Beachfront Living",
    "tagline": "Your Dream Home Awaits",
    "main_image": "https://...",
    "price_from": 250000,
    "featured": true,
    "construction_progress": 75
  }
]
```

---

### GET `/api/projects/by_location/`

**🎯 Intención**: Agrupar proyectos por ciudad/estado para análisis geográfico.

**💼 Caso de Uso Real**:
- Executive dashboard muestra proyectos por región
- Cliente busca por ubicación

**📤 Response**:
```json
{
  "Miami Beach, FL": {
    "count": 3,
    "total_units": 350,
    "available_units": 145,
    "projects": [
      {"name": "Torres del Mar", "available_units": 48},
      {"name": "Ocean View Residences", "available_units": 67}
    ]
  },
  "Fort Lauderdale, FL": {
    "count": 2,
    "total_units": 180,
    "available_units": 95,
    "projects": [...]
  }
}
```

**💡 Por qué es útil**:
- Visualización geográfica del inventario
- Identificar zonas con más/menos disponibilidad
- Planificación de marketing por región

---

### GET `/api/projects/{id}/stats/`

**🎯 Intención**: Dashboard completo de un proyecto con todas sus métricas.

**💼 Caso de Uso Real**:
- Project Manager revisa performance del proyecto
- Executive revisa velocidad de ventas

**📤 Response**:
```json
{
  "total_units": 120,
  "available_units": 48,
  "sold_units": 65,
  "reserved_units": 7,
  "occupancy_rate": 60.0,
  "lead_count": 234,
  "quote_count": 89,
  "view_count": 1580,
  "avg_unit_price": 425000,
  "avg_unit_area": 92.5,
  "units_by_type": {
    "1BR": 15,
    "2BR": 80,
    "3BR": 20,
    "Penthouse": 5
  },
  "units_by_floor": {
    "10": 10,
    "11": 10,
    "12": 10
  }
}
```

**💡 Insights del ejemplo**:
- 60% de ocupación → buen ritmo
- 234 leads para 48 unidades disponibles → buen interés
- Tipo más popular: 2BR (80 unidades)

---

## 🏠 UNITS - Gestión de Unidades

### POST `/api/projects/units/{id}/reserve/`

**🎯 Intención**: Reservar una unidad para un lead (opción de compra temporal).

**💼 Caso de Uso Real**:
- Lead está decidido pero necesita 48 horas para confirmar con familia
- Vendedor reserva la unidad para que nadie más la venda
- Lead tiene tiempo para decidir sin perder la oportunidad

**📥 Request**:
```json
{
  "lead_id": "uuid-lead-123"
}
```

**📤 Response**:
```json
{
  "id": "uuid-unit-456",
  "unit_number": "1205",
  "status": "reserved",  // Cambió de 'available'
  "reserved_by": {
    "id": "uuid-lead-123",
    "full_name": "María González"
  },
  "reserved_date": "2024-01-16T14:30:00Z",
  "project": {
    "available_units": 47  // Se actualizó automáticamente
  }
}
```

**💡 Qué pasa automáticamente**:
1. Unit.status → 'reserved'
2. Unit.reserved_by → Lead
3. Unit.reserved_date → ahora
4. Project.available_units → decrece en 1
5. Project.reserved_units → aumenta en 1

**⚠️ Importante**:
- Reserva NO es venta final
- Típicamente dura 48-72 horas
- Después debes confirmar venta o liberar

---

### POST `/api/projects/units/{id}/mark_as_sold/`

**🎯 Intención**: Marcar unidad como vendida (venta final).

**💼 Caso de Uso Real**:
- Cliente firmó contrato
- Dio enganche/down payment
- Venta está cerrada

**📥 Request**:
```json
{
  "sold_to": "María González - Contrato #2024-0234"
}
```

**📤 Response**:
```json
{
  "id": "uuid-unit-456",
  "unit_number": "1205",
  "status": "sold",
  "sold_to": "María González - Contrato #2024-0234",
  "sold_date": "2024-01-18T16:00:00Z",
  "project": {
    "available_units": 47,  // Si era available
    "reserved_units": 6,    // Si era reserved
    "sold_units": 66        // Aumentó en 1
  }
}
```

**💡 Qué pasa automáticamente**:
1. Unit.status → 'sold'
2. Unit.sold_date → ahora
3. Project counts se ajustan automáticamente
4. Ya NO aparece en búsquedas de disponibles

---

### GET `/api/projects/units/similar/`

**🎯 Intención**: Encontrar unidades similares cuando la que quería el lead no está disponible.

**💼 Caso de Uso Real**:
- Lead quiere apto 1205 pero ya está vendido
- Vendedor busca similares: mismo tipo, piso similar, precio similar
- Ofrece alternativas al cliente

**📥 Request**:
```bash
GET /api/projects/units/similar/?unit_type=2BR&bedrooms=2&floor_min=10&floor_max=15&price_max=400000
```

**📤 Response**:
```json
[
  {
    "unit_number": "1305",
    "unit_type": "2BR/2BA",
    "floor": 13,
    "bedrooms": 2,
    "price": 360000,
    "status": "available",
    "similarity_score": 95  // Qué tan similar
  },
  {
    "unit_number": "1405",
    "unit_type": "2BR/2BA",
    "floor": 14,
    "bedrooms": 2,
    "price": 370000,
    "status": "available",
    "similarity_score": 92
  }
]
```

**💡 Por qué es útil**:
- Recuperas venta que pensabas perdida
- Cliente ve que tienes opciones
- Experiencia de compra mejorada

---

## 💰 QUOTES - Gestión de Cotizaciones

### POST `/api/quotes/`

**🎯 Intención**: Crear cotización formal para un lead.

**💼 Caso de Uso Real**:
- Lead está interesado en apto 1205
- Vendedor crea cotización con precio, descuento, términos
- Sistema calcula automáticamente totales

**📥 Request**:
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
  },
  "notes": "Incluye parking y storage unit",
  "terms_and_conditions": "Precio sujeto a disponibilidad..."
}
```

**📤 Response**:
```json
{
  "quote_number": "QT-2024-0234",  // Auto-generado
  "status": "draft",
  "unit_price": 350000,
  "discount_amount": 17500,        // Calculado: 5% de 350000
  "subtotal": 332500,              // Calculado
  "tax_amount": 23275,             // Calculado: 7% de 332500
  "total": 355775,                 // Calculado
  "created_at": "2024-01-16T15:00:00Z"
}
```

**💡 Sistema calcula automáticamente**:
- discount_amount
- subtotal
- tax_amount
- total

---

### POST `/api/quotes/{id}/send/`

**🎯 Intención**: Enviar cotización al cliente (de draft → sent).

**💼 Caso de Uso Real**:
- Cotización creada y revisada
- Vendedor la envía al cliente por email
- Sistema registra fecha de envío

**📤 Response**:
```json
{
  "id": "uuid-quote-123",
  "status": "sent",              // Cambió de 'draft'
  "sent_date": "2024-01-16T15:30:00Z",
  "valid_until": "2024-02-16T23:59:59Z"
}
```

**💡 En el futuro**:
- Sistema puede enviar email automático
- Template de cotización con branding
- Link para que cliente vea online

---

### POST `/api/quotes/{id}/accept/`

**🎯 Intención**: Marcar cotización como aceptada por el cliente.

**💼 Caso de Uso Real**:
- Cliente llama y dice "acepto la oferta"
- Vendedor marca cotización como aceptada
- Proceso de cierre comienza

**📤 Response**:
```json
{
  "status": "accepted",
  "accepted_date": "2024-01-18T10:00:00Z"
}
```

**💡 Siguiente paso típico**:
1. Marcar unidad como reservada
2. Preparar contrato
3. Programar firma
4. Coordinar pago de enganche

---

## 📊 ANALYTICS - Reportes y Análisis

### GET `/api/analytics/dashboard/`

**🎯 Intención**: Dashboard ejecutivo con métricas clave del negocio.

**💼 Caso de Uso Real**:
- CEO abre app cada mañana
- Ve snapshot completo del negocio
- Identifica áreas que requieren atención

**📤 Response**:
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

**💡 Insights del ejemplo**:
- 47 leads esta semana → buen flujo
- 45 cotizaciones aceptadas → $15.7M en pipeline
- 342 unidades disponibles → buen inventario
- 234 actividades esta semana → equipo activo

---

### GET `/api/analytics/sales-funnel/`

**🎯 Intención**: Ver el embudo de ventas (cuántos leads en cada etapa).

**💼 Caso de Uso Real**:
- Manager identifica dónde se pierden leads
- Optimiza proceso de ventas

**📤 Response**:
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

**📊 Visualización**:
```
New         ████████████████ 156
Contacted   ███████████████████████ 234
Qualified   ███████████████████ 189
Proposal    ███████████████ 123
Negotiation ████████ 67
Closed Won  █████ 45
```

**💡 Análisis**:
- Mayor drop-off: Negotiation → Closed Won
- **Acción**: Entrenar equipo en técnicas de cierre

---

## 🎯 Resumen de Intenciones por Módulo

### LEADS = Pipeline de Ventas
- **Listar/Filtrar**: Encontrar leads específicos
- **Crear**: Capturar nuevos prospectos
- **Timeline**: Ver historial completo
- **Bulk Assign**: Distribuir trabajo eficientemente
- **Hot Leads**: Priorizar mejor
- **Duplicates**: Mantener datos limpios
- **Follow-ups**: Nunca olvidar seguimiento

### PROJECTS = Inventario
- **Listar**: Qué vendemos
- **Stats**: Cómo va cada proyecto
- **Available Units**: Qué hay para ofrecer
- **Featured**: Destacar los mejores
- **By Location**: Análisis geográfico

### UNITS = Producto Específico
- **Reserve**: Apartar para cliente
- **Mark as Sold**: Cerrar venta
- **Similar**: Ofrecer alternativas

### QUOTES = Propuestas Formales
- **Crear**: Formalizar oferta
- **Send**: Enviar al cliente
- **Accept/Reject**: Tracking de decisiones

### ANALYTICS = Inteligencia de Negocio
- **Dashboard**: Vista ejecutiva
- **Sales Funnel**: Optimizar proceso
- **Performance by Source**: ROI de marketing

---

## 💡 Mejores Prácticas

1. **Siempre usa filtros**: No cargues todo, filtra lo que necesitas
2. **Pagina resultados**: Usa `?page=1&page_size=50`
3. **Ordena inteligentemente**: `?ordering=-created_at` (más recientes primero)
4. **Combina filtros**: `?status=qualified&score_min=70&source=website`
5. **Usa search**: `?search=maria` busca en múltiples campos
6. **Revisa stats regularmente**: Toma decisiones basadas en datos

---

**Para documentación de modelos detallada, ver [MODELS_DOCUMENTATION.md](MODELS_DOCUMENTATION.md)**

