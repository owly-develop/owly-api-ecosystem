# 📊 Documentación de Modelos - OWLY CRM

## 🎯 Propósito General

Este documento explica **qué es cada modelo**, **para qué sirve** y **cómo se relaciona** con el flujo de trabajo de un CRM inmobiliario.

---

## 🏢 1. Company (Empresa/Organización)

### ¿Qué es?
El **tenant** (inquilino) en la arquitectura multi-tenant. Representa una empresa inmobiliaria que usa el CRM.

### ¿Para qué sirve?
- **Aislamiento de datos**: Cada empresa solo ve sus propios datos
- **Gestión de suscripciones**: Control de planes (Free, Starter, Professional, Enterprise)
- **Límites y cuotas**: Define cuántos usuarios, proyectos y leads puede tener
- **Branding**: Logo, colores corporativos, configuraciones específicas

### Casos de uso:
1. **Empresa pequeña**: Plan Starter, 10 usuarios, 25 proyectos
2. **Desarrolladora grande**: Plan Enterprise, 100 usuarios, proyectos ilimitados
3. **Franquicia**: Múltiples empresas (Companies) independientes en el mismo sistema

### Campos importantes:
- `plan`: Define el nivel de servicio (free/starter/professional/enterprise)
- `max_users`, `max_projects`, `max_leads`: Límites según el plan
- `status`: active/trial/suspended - Estado de la suscripción
- `features`: JSON con características habilitadas (ej: {"ai_scoring": true, "whatsapp": false})

### Ejemplo real:
```
Company: "Desarrollos Inmobiliarios XYZ"
Plan: Professional
Max Users: 50
Max Projects: 100
Status: Active
Features: {"ai_scoring": true, "bulk_sms": true, "advanced_reporting": true}
```

---

## 👤 2. User (Usuario)

### ¿Qué es?
Un empleado de la empresa que usa el CRM. Puede ser vendedor, gerente, marketing, soporte, etc.

### ¿Para qué sirve?
- **Autenticación**: Login seguro con JWT
- **Autorización**: Control de qué puede hacer cada usuario según su rol
- **Asignación**: A quién se le asignan leads, proyectos, tareas
- **Performance tracking**: Métricas de rendimiento individuales

### Roles disponibles:
1. **Admin**: Control total, gestiona la empresa
2. **Manager**: Supervisa equipos, ve todos los datos
3. **Sales**: Vendedor, gestiona sus leads asignados
4. **Marketing**: Crea campañas, gestiona fuentes de leads
5. **Support**: Atención post-venta

### Casos de uso:
1. **Juan (Sales)**: Ve solo sus leads asignados, puede crear cotizaciones
2. **María (Manager)**: Ve todos los leads del equipo, reasigna, genera reportes
3. **Pedro (Admin)**: Configura la empresa, gestiona usuarios, planes

### Campos importantes:
- `role`: Define qué permisos tiene
- `assigned_projects`: Proyectos en los que trabaja
- `territories`: Zonas geográficas asignadas (ej: ["Miami", "Fort Lauderdale"])
- `performance_metrics`: JSON con estadísticas (leads convertidos, revenue, etc.)
- `sales_target`: Meta mensual/trimestral

### Ejemplo real:
```
User: "Juan Pérez"
Role: Sales
Email: juan@xyz.com
Assigned Projects: ["Torres del Mar", "Villas del Sol"]
Territories: ["Zona Norte", "Centro"]
Sales Target: $500,000/month
Performance: {
  "leads_converted": 15,
  "conversion_rate": 35%,
  "revenue": $450,000
}
```

---

## 🏗️ 3. Project (Proyecto Inmobiliario)

### ¿Qué es?
Un desarrollo inmobiliario que la empresa está vendiendo. Puede ser un edificio de apartamentos, conjunto de villas, centro comercial, etc.

### ¿Para qué sirve?
- **Inventario**: Qué estás vendiendo
- **Organización**: Agrupar unidades por proyecto
- **Marketing**: Información para mostrar a clientes
- **Tracking**: Seguimiento de ventas, disponibilidad, progreso de construcción

### Tipos de proyecto:
1. **Residential**: Apartamentos, casas, villas
2. **Commercial**: Oficinas, locales comerciales
3. **Mixed Use**: Combinación de residencial y comercial
4. **Industrial**: Bodegas, naves industriales

### Estados del proyecto:
1. **Planning**: En planificación, aún no se vende
2. **Pre-launch**: Pre-venta antes del lanzamiento oficial
3. **Active**: En venta activa
4. **Sold Out**: Todo vendido
5. **Completed**: Construcción terminada y entregado
6. **On Hold**: Pausado temporalmente

### Casos de uso:
1. **Torres del Mar**: 120 apartamentos, 60% vendido, entrega 2025
2. **Villas del Sol**: 30 casas, pre-lanzamiento, entrega 2026
3. **Centro Plaza**: 50 locales comerciales, activo

### Campos importantes:
- `status`: En qué fase está el proyecto
- `total_units`, `available_units`, `sold_units`: Control de inventario
- `price_from`, `price_to`: Rango de precios
- `construction_progress`: 0-100% del avance de construcción
- `amenities`: Servicios (piscina, gym, seguridad, etc.)
- `featured`: Si aparece destacado en el sitio web

### Ejemplo real:
```
Project: "Torres del Mar"
Type: Residential
Status: Active
Location: Miami Beach, FL
Total Units: 120
Available: 48
Sold: 65
Reserved: 7
Price Range: $250,000 - $750,000
Construction Progress: 75%
Delivery Date: Dec 2025
Amenities: ["Piscina", "Gym", "Seguridad 24/7", "Beach Club"]
Featured: true
```

---

## 🏠 4. Unit (Unidad)

### ¿Qué es?
Una unidad individual dentro de un proyecto. Un apartamento específico, una villa específica, un local específico.

### ¿Para qué sirve?
- **Inventario detallado**: Qué hay disponible para vender
- **Especificaciones**: Características exactas de cada unidad
- **Reservas y ventas**: Control de qué está disponible, reservado o vendido
- **Matching**: Encontrar la unidad perfecta para cada lead

### Estados de unidad:
1. **Available**: Disponible para vender
2. **Reserved**: Reservada por un lead (opción)
3. **Sold**: Vendida
4. **Blocked**: Bloqueada temporalmente (no disponible)

### Casos de uso:
1. **Apto 1205**: 2BR/2BA, piso 12, disponible, $350,000
2. **Apto 1801**: Penthouse, reservado por Lead #2024-045
3. **Villa 15**: 3BR/3BA, vendida a Juan Pérez

### Campos importantes:
- `unit_number`: Número único (ej: "1205", "PH-01")
- `unit_type`: Tipo (Studio, 1BR, 2BR, Penthouse)
- `status`: available/reserved/sold/blocked
- `floor`: Piso
- `bedrooms`, `bathrooms`: Especificaciones
- `area_sqm`: Área en metros cuadrados
- `price`: Precio de venta
- `orientation`: Norte, Sur, Este, Oeste
- `view_type`: Vista (mar, ciudad, montaña)
- `reserved_by`: Lead que la tiene reservada
- `sold_to`: Cliente que la compró

### Ejemplo real:
```
Unit: "1205"
Project: "Torres del Mar"
Type: 2BR/2BA
Status: Available
Floor: 12
Area: 85 m²
Price: $350,000
Orientation: East
View: Ocean View
Features: ["Balcony", "Walk-in Closet", "Master Bath"]
```

---

## 👥 5. Lead (Prospecto/Cliente Potencial)

### ¿Qué es?
Una persona interesada en comprar una propiedad. Es el corazón del CRM.

### ¿Para qué sirve?
- **Pipeline de ventas**: Mover prospectos desde primer contacto hasta cierre
- **Seguimiento**: Historial de todas las interacciones
- **Calificación**: Scoring y priorización
- **Asignación**: Distribuir leads entre vendedores
- **Conversión**: Tracking de quién se convierte en cliente

### Estados del lead (Pipeline):
1. **New**: Recién llegado, sin contactar
2. **Contacted**: Ya se contactó
3. **Qualified**: Calificado (tiene presupuesto, interés real)
4. **Proposal**: Se envió cotización
5. **Negotiation**: En negociación
6. **Closed Won**: ¡Ganado! Cliente compró
7. **Closed Lost**: Perdido, no compró
8. **Nurturing**: En nutrición (follow-up de largo plazo)

### Fuentes de leads:
- **Website**: Formulario del sitio web
- **Facebook/Instagram**: Campañas en redes sociales
- **WhatsApp**: Consultas por WhatsApp
- **Referral**: Referencias de clientes actuales
- **Cold Call**: Llamadas en frío
- **Trade Show**: Ferias y eventos

### Prioridades:
- **Low**: No urgente
- **Medium**: Prioridad normal
- **High**: Alta prioridad
- **Urgent**: Atención inmediata

### Casos de uso:
1. **Lead nuevo**: Llegó del website, sin asignar, score bajo
2. **Lead caliente**: Presupuesto confirmado, urgencia alta, score 85/100
3. **Lead en negociación**: Ya vio propiedades, recibió cotización, en proceso de cierre

### Campos importantes:
- `status`: Dónde está en el pipeline
- `priority`: Qué tan urgente es atenderlo
- `source`: De dónde vino
- `lead_score`: 0-100, calculado automáticamente
- `ai_close_probability`: 0-100, probabilidad de cerrar (IA)
- `assigned_to`: Vendedor responsable
- `budget_min`, `budget_max`: Presupuesto del cliente
- `interested_projects`: Proyectos que le interesan
- `next_follow_up_date`: Cuándo hacer seguimiento
- `converted_to_customer`: Si ya compró

### Ejemplo real:
```
Lead: "María González"
Lead #: LEAD-2024-0234
Status: Qualified
Priority: High
Source: Facebook
Lead Score: 78/100
AI Close Probability: 65%
Email: maria.g@email.com
Phone: +1-305-555-0123
Budget: $300,000 - $450,000
Interested In: ["Torres del Mar - 2BR units"]
Assigned To: Juan Pérez (Sales)
Next Follow-up: Tomorrow at 10:00 AM
Notes: "Quiere piso alto, vista al mar, 2 habitaciones. Tiene pre-aprobación del banco."
```

---

## 💰 6. Quote (Cotización)

### ¿Qué es?
Una propuesta formal de venta enviada a un lead. Documento con precio, condiciones, términos.

### ¿Para qué sirve?
- **Formalizar oferta**: Poner por escrito la propuesta
- **Tracking**: Saber qué cotizaciones están abiertas, vistas, aceptadas
- **Conversión**: Medir efectividad de cotizaciones
- **Historial**: Registro de todas las ofertas hechas a un lead

### Estados de cotización:
1. **Draft**: Borrador, aún no enviada
2. **Sent**: Enviada al cliente
3. **Viewed**: Cliente la abrió/vio
4. **Accepted**: ¡Cliente aceptó!
5. **Rejected**: Cliente rechazó
6. **Expired**: Venció (pasó la fecha de validez)

### Casos de uso:
1. **Cotización inicial**: Primera oferta al lead
2. **Cotización revisada**: Ajuste de precio o condiciones
3. **Cotización múltiple**: Varias opciones para que el cliente elija

### Campos importantes:
- `quote_number`: Número único (QT-2024-0456)
- `status`: Estado actual
- `lead`: Para quién es
- `project`, `unit`: Qué se está cotizando
- `unit_price`: Precio base
- `discount_percentage`, `discount_amount`: Descuentos
- `total`: Precio final
- `valid_until`: Hasta cuándo es válida
- `financing_offered`: Si incluye financiamiento
- `sent_date`, `viewed_date`, `accepted_date`: Tracking de fechas

### Ejemplo real:
```
Quote: "QT-2024-0234"
For: María González (LEAD-2024-0234)
Project: Torres del Mar
Unit: Apartment 1205
Unit Price: $350,000
Discount: 5% ($17,500)
Subtotal: $332,500
Tax: $23,275
Total: $355,775
Status: Viewed
Sent: Jan 15, 2024
Viewed: Jan 16, 2024 10:30 AM
Valid Until: Feb 15, 2024
Financing: Yes
  - Down Payment: 20% ($71,155)
  - Monthly Payment: $1,850 x 240 months
Terms: "Includes parking space and storage unit"
```

---

## 📋 7. Activity (Actividad)

### ¿Qué es?
Un registro de cada interacción con un lead u otro objeto del CRM. El "log" de todo lo que pasa.

### ¿Para qué sirve?
- **Timeline**: Historial completo de interacciones
- **Accountability**: Quién hizo qué y cuándo
- **Seguimiento**: Programar tareas futuras
- **Reporting**: Análisis de actividad del equipo

### Tipos de actividad:
1. **Call**: Llamada telefónica
2. **Email**: Email enviado/recibido
3. **Meeting**: Reunión presencial o virtual
4. **Note**: Nota o comentario
5. **Task**: Tarea pendiente
6. **Quote Sent**: Cotización enviada
7. **Quote Viewed**: Cotización vista
8. **Status Change**: Cambio de estado

### Casos de uso:
1. **Llamada registrada**: "Llamé a María, no contestó, dejé voicemail"
2. **Reunión programada**: "Cita para mostrar apto 1205 - Sábado 10 AM"
3. **Email enviado**: "Envié brochure del proyecto"
4. **Nota**: "Cliente menciona que prefiere pisos altos"

### Campos importantes:
- `activity_type`: Tipo de actividad
- `title`: Título corto
- `description`: Descripción detallada
- `user`: Quién la realizó
- `related_object`: A qué está relacionada (Lead, Project, etc.)
- `scheduled_date`: Cuándo está programada
- `completed_date`: Cuándo se completó
- `status`: planned/completed/cancelled

### Ejemplo real:
```
Activity: "Llamada de seguimiento"
Type: Call
User: Juan Pérez
Related To: María González (LEAD-2024-0234)
Description: "Llamé para confirmar visita al apartamento. Cliente confirma para el sábado 10 AM. Preguntó sobre posibilidad de personalizar acabados."
Scheduled: Jan 18, 2024 2:00 PM
Completed: Jan 18, 2024 2:15 PM
Duration: 15 minutes
Status: Completed
```

---

## 🎨 8. QuoteTemplate (Plantilla de Cotización)

### ¿Qué es?
Una plantilla HTML reutilizable para generar cotizaciones con el branding de la empresa.

### ¿Para qué sirve?
- **Consistencia**: Todas las cotizaciones se ven igual
- **Branding**: Logo, colores, estilo de la empresa
- **Eficiencia**: No crear cada cotización desde cero
- **Personalización**: Diferentes plantillas para diferentes tipos de propiedades

### Casos de uso:
1. **Plantilla Residencial**: Para apartamentos y casas
2. **Plantilla Comercial**: Para locales y oficinas
3. **Plantilla Premium**: Para penthouses y propiedades de lujo

### Ejemplo real:
```
Template: "Residential Standard"
Description: "Plantilla estándar para unidades residenciales"
Content: [HTML con logo, campos dinámicos, términos]
Default Validity: 30 días
Default Terms: "Precio sujeto a disponibilidad..."
Active: Yes
```

---

## 🔗 Relaciones Entre Modelos

### Flujo Típico de Venta:

```
1. LEAD llega (desde Facebook)
   ↓
2. Se asigna a USER (vendedor)
   ↓
3. USER ve los PROJECTS disponibles
   ↓
4. USER registra ACTIVITIES (llamadas, emails)
   ↓
5. LEAD se interesa en un PROJECT específico
   ↓
6. USER busca UNITS disponibles en ese proyecto
   ↓
7. USER crea una QUOTE para una UNIT específica
   ↓
8. QUOTE se envía al LEAD
   ↓
9. LEAD acepta → UNIT se marca como "reserved"
   ↓
10. Cierre de venta → LEAD se marca como "converted"
    UNIT se marca como "sold"
```

### Relaciones Principales:

```
COMPANY (1) ──┬── (N) USERS
              ├── (N) PROJECTS
              ├── (N) LEADS
              └── (N) QUOTES

PROJECT (1) ──── (N) UNITS

LEAD (1) ──┬── (N) QUOTES
           ├── (N) ACTIVITIES
           └── (N) INTERESTED_UNITS (many-to-many)

USER (1) ──┬── (N) ASSIGNED_LEADS
           ├── (N) CREATED_QUOTES
           └── (N) ACTIVITIES
```

---

## 💡 Casos de Uso del Mundo Real

### Caso 1: Lead Nuevo desde Facebook
```
1. María llena formulario en Facebook → crea LEAD
2. Sistema asigna a Juan (vendedor de esa zona) → LEAD.assigned_to = Juan
3. Juan llama → crea ACTIVITY (tipo: call)
4. María califica (tiene presupuesto) → LEAD.status = 'qualified'
5. Juan envía info de proyectos → ACTIVITY (tipo: email)
6. María se interesa en "Torres del Mar" → LEAD.interested_projects
7. Juan crea cotización → QUOTE para Unit 1205
8. María acepta → QUOTE.status = 'accepted', UNIT.status = 'reserved'
9. Cierre de venta → LEAD.converted_to_customer = true, UNIT.status = 'sold'
```

### Caso 2: Manager Analizando Performance
```
1. Manager ve dashboard
2. Filtra LEADS by assigned_to = "Juan Pérez"
3. Ve ACTIVITIES de la semana
4. Analiza QUOTES enviadas vs aceptadas
5. Identifica UNITS con más interés
6. Reasigna LEADS sin contactar hace 7 días
```

### Caso 3: Marketing Evaluando Fuentes
```
1. Marketing ve LEADS por source
2. Calcula conversion rate por fuente:
   - Facebook: 100 leads → 15 conversiones (15%)
   - Website: 50 leads → 12 conversiones (24%)
3. Analiza lead_score promedio por fuente
4. Identifica qué fuente trae leads de mejor calidad
5. Ajusta presupuesto de marketing
```

---

## 📈 Métricas Clave por Modelo

### LEAD Metrics:
- Conversion Rate: % que compran
- Avg Lead Score: Score promedio
- Avg Time to Convert: Días desde nuevo hasta cierre
- Source Performance: Mejor fuente de leads

### PROJECT Metrics:
- Occupancy Rate: % vendido
- Avg Days to Sell Unit: Velocidad de ventas
- Price Per SqM: Precio por metro cuadrado
- Lead Interest: Cuántos leads lo miran

### USER Metrics:
- Leads Assigned: Cuántos tiene
- Conversion Rate: % de cierre
- Response Time: Rapidez de respuesta
- Revenue Generated: Ventas totales

### QUOTE Metrics:
- Acceptance Rate: % aceptadas
- Avg Time to View: Rapidez en ver
- Avg Discount: Descuento promedio
- Conversion Rate: Cotizadas → Vendidas

---

Esta documentación explica el **"por qué"** de cada modelo y cómo trabajan juntos para crear un CRM completo. 

**Siguiente paso**: Ver la documentación de endpoints para entender cómo interactuar con estos modelos via API.

