# ⏰ Guía de Tareas Programadas para Usuarios No Técnicos

## 🎯 ¿Qué son las Tareas Programadas?

Son **trabajos automáticos** que el sistema ejecuta **sin que nadie tenga que hacer nada**.

### Analogía Simple:
Es como poner una **alarma** que cuando suena, el sistema hace algo automáticamente:
- Como un despertador que suena a las 7 AM cada día
- Pero en lugar de despertarte, el sistema envía emails, calcula números, genera reportes, etc.

---

## 💡 Ejemplos del Mundo Real

### Ejemplo 1: Recordatorios de Follow-ups
**Qué hace**: Cada mañana a las 8 AM, el sistema revisa qué vendedores tienen follow-ups programados para ese día y les envía un email recordándoles.

**Beneficio**: Vendedores nunca olvidan llamar a sus clientes.

### Ejemplo 2: Liberar Opciones Expiradas  
**Qué hace**: Cada hora, el sistema busca unidades que están "en opción" pero el tiempo (48h) ya pasó, y las marca como disponibles de nuevo.

**Beneficio**: Inventario siempre actualizado sin trabajo manual.

### Ejemplo 3: Reporte Semanal
**Qué hace**: Cada lunes a las 8 AM, genera un reporte con las ventas de la semana anterior y lo envía por email al equipo.

**Beneficio**: Equipo empieza la semana viendo su performance, sin tener que generar reportes manualmente.

---

## 🖥️ Cómo Gestionar Tareas desde el Admin

### Acceder:

1. Ve a: http://localhost:8000/admin/
2. Login con tus credenciales
3. Busca sección: **"Tareas Programadas"**

### Vista Principal:

Verás una tabla con:
- **● (punto de color)**:
  - 🟢 Verde = Activa y funcionando
  - 🔴 Rojo = Última ejecución falló
  - ⚫ Gris = Pausada
- **Nombre**: Qué hace la tarea
- **Categoría**: Tipo de tarea (badge de color)
- **Programación**: Cuándo se ejecuta (en lenguaje simple)
- **Última Ejecución**: Cuándo corrió por última vez
- **Estado**: ✓ o ✗
- **Total**: Cuántas veces se ha ejecutado

---

## ➕ Crear una Nueva Tarea

### Paso 1: Click en "Agregar Tarea Programada"

### Paso 2: Llenar Información Básica

**Nombre**:
- Escribe un nombre descriptivo
- Ejemplo: "Recordatorios Matutinos de Follow-ups"

**Descripción**:
- Explica qué hace en lenguaje simple
- Ejemplo: "Envía un email a cada vendedor con sus follow-ups del día"

**Categoría**:
- Selecciona de la lista:
  - 📊 Gestión de Leads
  - 📅 Seguimiento y Recordatorios
  - 💰 Pagos y Cobranzas
  - 📈 Reportes y Análisis
  - 🏗️ Inventario
  - 📧 Notificaciones
  - 🔧 Mantenimiento del Sistema

### Paso 3: Configurar Programación

**Frecuencia** (¿con qué frecuencia?):
- **Cada Hora**: Se ejecuta cada hora
- **Diario**: Una vez al día
- **Semanal**: Una vez a la semana
- **Quincenal**: Días 1 y 15 del mes
- **Mensual**: Una vez al mes

**Hora** (0-23):
- 0 = 12 AM (medianoche)
- 8 = 8 AM (mañana)
- 12 = 12 PM (medio día)
- 14 = 2 PM (tarde)
- 18 = 6 PM (tarde)
- 20 = 8 PM (noche)

**Minuto** (0-59):
- Generalmente 0
- O el minuto específico que quieras

**Día de la Semana** (solo para tareas semanales):
- Lunes, Martes, Miércoles, etc.

**Día del Mes** (solo para tareas mensuales):
- 1 = Primer día del mes
- 15 = Día 15
- 31 = Último día (o último del mes si tiene menos de 31)

### Paso 4: Configuración Técnica

**Nombre de la Tarea** (técnico):
- Este campo lo llena un desarrollador
- Ejemplo: `apps.leads.tasks.send_followup_reminders`
- Si no sabes qué poner, usa una plantilla (ver abajo)

### Paso 5: Activar

**Está activa**:
- ✅ Marcado = La tarea se ejecutará automáticamente
- ⬜ Sin marcar = La tarea está pausada

### Paso 6: Guardar

Click en "Guardar" y la tarea comenzará a ejecutarse automáticamente según la programación.

---

## 📋 Usar Plantillas Pre-configuradas (Fácil)

En lugar de crear desde cero, usa una **plantilla**:

### Desde el Admin:

1. Ve a "Tareas Programadas"
2. En la parte superior, busca botón "Usar Plantilla"
3. Selecciona una:
   - ✅ Recordatorios de Follow-ups
   - ✅ Calcular Scores de Leads
   - ✅ Detectar Pagos Vencidos
   - ✅ Liberar Opciones Expiradas
   - ✅ Reporte Semanal de Ventas
   - ✅ Backup de Base de Datos
4. Todo ya viene pre-configurado
5. Solo ajusta el horario si quieres
6. Guardar

---

## 🎛️ Gestionar Tareas Existentes

### Ver Detalles:
- Click en el nombre de la tarea
- Verás toda la información

### Editar Programación:
1. Click en la tarea
2. Cambia la hora o frecuencia
3. Click "Guardar"
4. Los cambios aplican automáticamente

### Pausar una Tarea:
1. Click en la tarea
2. Desmarca "Está activa"
3. Guardar
4. La tarea no se ejecutará hasta que la reactives

### Activar una Tarea Pausada:
1. Click en la tarea
2. Marca "Está activa"
3. Guardar

### Eliminar una Tarea:
1. Click en la tarea
2. Botón "Eliminar" (abajo a la izquierda)
3. Confirmar

---

## ▶️ Ejecutar Tarea Inmediatamente

A veces quieres ejecutar una tarea **ahora**, sin esperar a que llegue la hora programada.

### Opción 1: Desde la Lista
1. Selecciona la(s) tarea(s) con el checkbox
2. En "Acción" (dropdown arriba), selecciona "▶️ Ejecutar ahora"
3. Click "Ir"
4. La tarea se ejecuta inmediatamente

### Opción 2: Desde el Detalle
1. Entra a la tarea
2. Botón "Ejecutar Ahora" (si está disponible)

---

## 📊 Entender el Historial

Cuando ves una tarea, hay una sección de **"Historial de Ejecuciones"**:

### Última Ejecución:
- **Nunca ejecutada**: La tarea es nueva o está pausada
- **hace 2 horas**: Se ejecutó hace 2 horas
- **hace 1 día**: Se ejecutó ayer

### Total de Ejecuciones:
- Cuántas veces se ha ejecutado desde que se creó
- Ejemplo: 365 = se ha ejecutado 365 veces (un año diario)

### Estado de Última Ejecución:
- **✓ (verde)**: Exitosa
- **✗ (rojo)**: Falló (ver resultado para detalles)

### Último Resultado:
- Mensaje de qué pasó
- Ejemplo: "Updated 150 lead scores"
- Si falló, verás el error aquí

---

## 🎨 Acciones en Masa

Puedes hacer cosas con **múltiples tareas** a la vez:

### Activar Varias:
1. Selecciona checkboxes de las tareas
2. Acción: "✅ Activar tareas seleccionadas"
3. Ir

### Pausar Varias:
1. Selecciona checkboxes
2. Acción: "⏸️ Pausar tareas seleccionadas"
3. Ir

### Ejecutar Varias Ahora:
1. Selecciona checkboxes
2. Acción: "▶️ Ejecutar ahora"
3. Ir

---

## 📱 Gestionar desde la API (Para Apps)

Si tienes una app móvil o web personalizada, puedes gestionar tareas vía API.

### Listar Todas las Tareas:
```
GET /api/scheduled-tasks/
```

**Response**:
```json
{
  "results": [
    {
      "id": "uuid-123",
      "name": "Recordatorios de Follow-ups",
      "description": "Envía emails...",
      "category": "followups",
      "category_display": "📅 Seguimiento y Recordatorios",
      "frequency": "daily",
      "frequency_display": "Diario",
      "hour": 8,
      "minute": 0,
      "is_active": true,
      "schedule_description": "Todos los días a las 8:00 AM",
      "status_text": "Activa y funcionando",
      "last_run": "2024-01-16T08:00:00Z",
      "total_runs": 45
    }
  ]
}
```

### Crear Tarea:
```
POST /api/scheduled-tasks/
```

**Request**:
```json
{
  "name": "Mi Tarea Personalizada",
  "description": "Hace algo útil cada día",
  "category": "notifications",
  "task_name": "apps.myapp.tasks.my_task",
  "frequency": "daily",
  "hour": 10,
  "minute": 30,
  "is_active": true
}
```

### Activar/Pausar:
```
POST /api/scheduled-tasks/{id}/activate/
POST /api/scheduled-tasks/{id}/deactivate/
```

### Ejecutar Ahora:
```
POST /api/scheduled-tasks/{id}/run_now/
```

### Ver Plantillas:
```
GET /api/scheduled-tasks/templates/
```

### Ver por Categoría:
```
GET /api/scheduled-tasks/by_category/
```

---

## 🔍 Filtrar y Buscar

### En el Admin:

**Filtros Laterales**:
- Por categoría
- Por frecuencia
- Activas / Pausadas
- Exitosas / Con errores
- Por empresa

**Buscador**:
- Busca por nombre o descripción
- Ejemplo: busca "follow" y encuentra todas las tareas relacionadas

---

## ⚠️ Cosas Importantes a Saber

### 1. Zona Horaria
- Todas las horas son en la zona horaria del servidor
- Por defecto: UTC
- Configurar en settings si necesitas otra

### 2. Primera Ejecución
- La tarea NO se ejecuta inmediatamente al crearla
- Se ejecuta en el próximo horario programado
- Si quieres probarla ya, usa "Ejecutar Ahora"

### 3. Pausar vs Eliminar
- **Pausar** (desactivar): La tarea se guarda pero no se ejecuta
- **Eliminar**: La tarea se borra completamente
- Recomendación: Siempre pausar en lugar de eliminar

### 4. Cambios Aplican Inmediatamente
- Si cambias el horario, aplica en la próxima ejecución
- No necesitas reiniciar nada

### 5. No Crear Duplicados
- Si ya existe una tarea que hace lo mismo
- Mejor edita la existente que crear nueva

---

## 🎓 Ejemplos Paso a Paso

### Ejemplo 1: "Quiero recibir reporte de ventas cada lunes"

1. Admin → Tareas Programadas → Agregar
2. Nombre: `Reporte Semanal de Ventas`
3. Descripción: `Genera reporte de ventas de la semana anterior`
4. Categoría: `📈 Reportes y Análisis`
5. Frecuencia: `Semanal`
6. Hora: `8` (8 AM)
7. Minuto: `0`
8. Día de la semana: `Lunes`
9. Nombre técnico: `apps.analytics.tasks.generate_weekly_sales_report`
10. Está activa: ✅
11. Guardar

✅ **Resultado**: Cada lunes a las 8 AM recibirás el reporte automáticamente

---

### Ejemplo 2: "Quiero que el sistema detecte pagos vencidos cada día"

1. Admin → Tareas Programadas → Agregar
2. Nombre: `Detectar Pagos Vencidos`
3. Descripción: `Revisa unidades con pagos atrasados y notifica`
4. Categoría: `💰 Pagos y Cobranzas`
5. Frecuencia: `Diario`
6. Hora: `9` (9 AM)
7. Minuto: `0`
8. Nombre técnico: `apps.projects.tasks.detect_overdue_payments`
9. Está activa: ✅
10. Guardar

✅ **Resultado**: Cada día a las 9 AM recibes alerta si hay pagos vencidos

---

### Ejemplo 3: "Quiero que opciones de 48h se liberen automáticamente"

**Usa Plantilla**:
1. Admin → Tareas Programadas → Usar Plantilla
2. Selecciona: "Liberar Opciones Expiradas"
3. Ya viene configurada para cada hora
4. Solo edita si quieres cambiar el horario
5. Guardar

✅ **Resultado**: Cada hora el sistema libera opciones expiradas

---

## 🎨 Interfaz del Admin - Guía Visual

### Lista de Tareas:

```
┌─────────────────────────────────────────────────────────────────┐
│ TAREAS PROGRAMADAS                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ● │ Nombre              │ Categoría │ Programación      │ ✓/✗  │
│───┼────────────────────┼───────────┼──────────────────┼──────│
│ 🟢│ Recordatorios      │ 📅Follow  │ Diario 8:00 AM   │  ✓   │
│ 🟢│ Calcular Scores    │ 📊 Leads  │ Diario 2:00 AM   │  ✓   │
│ ⚫│ Reporte Mensual    │ 📈Report  │ Mensual día 1    │  —   │
│ 🔴│ Enviar Newsletter  │ 📧Notif   │ Semanal Viernes  │  ✗   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Leyenda:
🟢 = Activa y funcionando
⚫ = Pausada
🔴 = Última ejecución falló
✓ = Exitosa
✗ = Error
— = Nunca ejecutada
```

### Formulario de Edición:

```
┌─────────────────────────────────────────────────────────────────┐
│ 📋 INFORMACIÓN BÁSICA                                           │
├─────────────────────────────────────────────────────────────────┤
│ Nombre: [Recordatorios de Follow-ups                        ]  │
│                                                                 │
│ Descripción:                                                    │
│ [Envía emails a vendedores con sus follow-ups del día       ]  │
│                                                                 │
│ Categoría: [📅 Seguimiento y Recordatorios ▼]                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ ⏰ PROGRAMACIÓN                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 💡 Cómo configurar:                                             │
│ • Diario: Se ejecuta todos los días a la hora especificada     │
│ • Semanal: Especifica día de semana y hora                     │
│ • Ejemplos:                                                     │
│   - Diario 8 AM: Frecuencia=Diario, Hora=8                    │
│   - Lunes 9 AM: Frecuencia=Semanal, Día=Lunes, Hora=9        │
│                                                                 │
│ Frecuencia: [Diario ▼]                                         │
│                                                                 │
│ 📅 Vista Previa:                                                │
│ ┌───────────────────────────────────────────┐                  │
│ │ 📅 Programación: Todos los días a las 8:00 AM               │
│ │ Próxima ejecución: Mañana a las 8:00 AM                    │
│ └───────────────────────────────────────────┘                  │
│                                                                 │
│ Hora (0-23): [8]   ← 8 = 8 AM, 14 = 2 PM                      │
│ Minuto (0-59): [0]                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ ✅ ACTIVACIÓN                                                   │
├─────────────────────────────────────────────────────────────────┤
│ ⚠️ Desactivar para pausar la tarea sin eliminarla              │
│                                                                 │
│ Está activa: [✓]                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

[Guardar]  [Guardar y continuar]  [Guardar y agregar otra]
```

---

## 💡 Consejos para Elegir Horarios

### Tareas de Recordatorios:
- **8:00 AM** - Inicio del día laboral
- Los vendedores ven el email al llegar

### Tareas de Cálculos:
- **2:00 AM - 4:00 AM** - Madrugada
- No afecta performance durante el día
- Datos listos por la mañana

### Tareas de Reportes:
- **Diarios**: 6:00 AM - Listo al llegar
- **Semanales**: Lunes 8:00 AM - Arranque de semana
- **Mensuales**: Día 1 a las 7:00 AM

### Tareas Críticas (Inventario):
- **Cada hora** - Liberar opciones expiradas
- Necesita frecuencia alta para mantener inventario actualizado

### Tareas de Mantenimiento:
- **1:00 AM - 3:00 AM** - Madrugada
- Backup, limpieza, optimización

---

## 🎯 Tareas Recomendadas por Tipo de Negocio

### Para Ventas Activas:
✅ Recordatorios de follow-ups (Diario 8 AM)
✅ Detectar follow-ups vencidos (Diario 9 AM)
✅ Liberar opciones expiradas (Cada hora)
✅ Calcular scores de leads (Diario 2 AM)

### Para Finanzas:
✅ Detectar pagos vencidos (Diario 9 AM)
✅ Reporte de cobranzas (Semanal Lunes 8 AM)
✅ Proyección de cash flow (Mensual día 1)

### Para Management:
✅ Reporte semanal de ventas (Lunes 8 AM)
✅ Performance de vendedores (Domingo 11 PM)
✅ Dashboard mensual (Día 1 del mes 7 AM)

### Para Todos:
✅ Backup de base de datos (Diario 3 AM)

---

## ❓ Preguntas Frecuentes

### ¿Puedo cambiar el horario de una tarea existente?
✅ Sí, solo edita y guarda. Los cambios aplican inmediatamente.

### ¿Qué pasa si pausé una tarea y quiero reactivarla?
✅ Solo marca "Está activa" y guarda.

### ¿Cómo sé si una tarea está funcionando?
✅ Mira el indicador de color:
- 🟢 = Funciona
- 🔴 = Tuvo error
- ⚫ = Está pausada

### ¿Puedo ejecutar una tarea manualmente para probarla?
✅ Sí, usa "Ejecutar Ahora" en las acciones.

### ¿Qué hago si una tarea falla?
1. Ve el "Último resultado" para ver el error
2. Si no entiendes el error, contacta a soporte técnico
3. Puedes pausar la tarea mientras se arregla

### ¿Puedo crear mis propias tareas?
⚠️ Necesitas conocimiento técnico para el "Nombre técnico"
✅ Mejor usa plantillas o pide ayuda a desarrollo

### ¿Las tareas se ejecutan si el servidor está apagado?
❌ No, necesitas que el servidor esté encendido
✅ En producción (AWS), el servidor siempre está encendido

### ¿Cuántas tareas puedo tener?
✅ No hay límite práctico
⚠️ Pero no abuses - demasiadas tareas pueden afectar performance

---

## 🎓 Tutorial Completo para Principiantes

### Objetivo: Configurar recordatorios diarios de follow-up

**Paso 1**: Ve al admin
- Abre navegador
- http://localhost:8000/admin/
- Login

**Paso 2**: Encuentra Tareas Programadas
- En el menú lateral izquierdo
- Busca "Tareas Programadas"
- Click

**Paso 3**: Agregar Nueva
- Botón "Agregar Tarea Programada" (arriba derecha)
- Click

**Paso 4**: Nombre
- Campo "Nombre"
- Escribe: `Recordatorios Matutinos`
- Este es el nombre que verás en la lista

**Paso 5**: Descripción
- Campo "Descripción"
- Escribe: `Envía un email a cada vendedor con sus follow-ups programados para hoy`
- Esto explica qué hace

**Paso 6**: Categoría
- Dropdown "Categoría"
- Selecciona: `📅 Seguimiento y Recordatorios`

**Paso 7**: Frecuencia
- Dropdown "Frecuencia"
- Selecciona: `Diario`
- Significa que se ejecutará todos los días

**Paso 8**: Hora
- Campo "Hora"
- Escribe: `8`
- Esto significa 8 AM (mañana)
- Si quisieras 2 PM, pondrías `14`

**Paso 9**: Minuto
- Campo "Minuto"  
- Deja: `0`
- Esto significa en punto (8:00 AM)

**Paso 10**: Nombre Técnico
- Campo "Nombre de la tarea"
- Escribe: `apps.leads.tasks.send_followup_reminders`
- (O pide a desarrollo este nombre)

**Paso 11**: Activar
- Checkbox "Está activa"
- Marca ✅
- Esto hace que la tarea se ejecute

**Paso 12**: Guardar
- Botón "Guardar" (abajo)
- Click

**Paso 13**: Verificar
- Verás la tarea en la lista
- 🟢 = Todo bien
- Mañana a las 8 AM se ejecutará automáticamente

✅ **¡Listo!** Has creado tu primera tarea programada.

---

## 📞 Soporte

Si tienes dudas:
- 📧 Email: soporte@owlycrm.com
- 💬 Chat interno
- 📖 Esta guía

---

**¡Las tareas programadas hacen tu trabajo más fácil!** ⏰

