# 🦉 OWLY CRM API - Sistema CRM Multi-Tenant para Inmobiliarias

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)]()

API REST completa para gestión de CRM inmobiliario con arquitectura multi-tenant, construida con Django REST Framework, PostgreSQL, Redis y Celery. Lista para producción y optimizada para AWS.

---

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Inicio Rápido](#-inicio-rápido-5-minutos)
- [Arquitectura](#-arquitectura)
- [Documentación](#-documentación)
- [API Endpoints](#-api-endpoints)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Licencia](#-licencia)

---

## ✨ Características Principales

### 🏢 Multi-Tenant Architecture
- **Una base de datos, múltiples empresas** con aislamiento total de datos
- Cada empresa (tenant) opera independientemente
- Escalable y eficiente en costos

### 📊 Gestión Completa de CRM
- **Companies**: Gestión de empresas con planes y límites
- **Users**: Sistema de roles (Admin, Manager, Sales, Marketing, Support)
- **Projects**: Proyectos inmobiliarios con tracking completo
- **Units**: Inventario detallado de unidades disponibles/vendidas
- **Leads**: Pipeline completo de ventas con scoring automático
- **Quotes**: Cotizaciones con cálculos automáticos
- **Activities**: Timeline de interacciones con clientes

### 🔐 Seguridad
- **JWT Authentication** con tokens de acceso y refresh
- **Role-Based Access Control (RBAC)**
- **Tenant Isolation** automático en todas las queries
- **Soft Deletes** para recuperación de datos

### 🚀 Features Avanzados
- **API RESTful** con paginación, filtros y búsqueda
- **Analytics Dashboard** con métricas en tiempo real
- **Bulk Operations** para operaciones masivas
- **Celery Tasks** para procesamiento asíncrono
- **Documentación Swagger/OpenAPI** auto-generada
- **Base de datos preparada para IA** con pgvector

### 🛠️ Stack Tecnológico
- **Backend**: Django 5.0, Django REST Framework 3.14
- **Base de Datos**: PostgreSQL 16 con pgvector
- **Cache**: Redis 7
- **Task Queue**: Celery + Redis
- **Containerización**: Docker & Docker Compose
- **Cloud Ready**: AWS (RDS, ElastiCache, S3, ECS)

---

## ⚡ Inicio Rápido (5 minutos)

### Prerrequisitos
- Docker Desktop instalado
- Docker Compose instalado
- 4GB RAM disponible

### 1. Clonar el Repositorio
```bash
git clone <repository-url>
cd owly-api-ecosystem
```

### 2. Crear Archivo de Entorno
```bash
# Copia el archivo de ejemplo
cp .env.example .env

# O crea uno nuevo con estas variables mínimas:
cat > .env << EOF
SECRET_KEY=django-insecure-local-dev-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://owly_user:owly_password@db:5432/owly_crm
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
USE_S3=False
EOF
```

### 3. Iniciar Servicios
```bash
docker-compose up -d
```

Esto inicia:
- PostgreSQL (base de datos)
- Redis (cache + celery broker)
- Django Web Server
- Celery Worker
- Celery Beat (scheduler)

### 4. Ejecutar Migraciones
```bash
# Espera 10 segundos para que PostgreSQL inicie completamente
sleep 10

# Ejecuta migraciones
docker-compose exec web python manage.py migrate
```

### 5. Crear Superusuario
```bash
docker-compose exec web python manage.py createsuperuser
```

### 6. (Opcional) Poblar Base de Datos con Datos de Prueba
```bash
docker-compose exec web python seed_database.py
```

### 7. Acceder a la Aplicación

| Servicio | URL | Descripción |
|----------|-----|-------------|
| 🌐 **API** | http://localhost:8000/api/ | API REST endpoints |
| 👤 **Admin Panel** | http://localhost:8000/admin/ | Django admin interface |
| 📚 **API Docs** | http://localhost:8000/api/docs/ | Swagger/OpenAPI documentation |
| ❤️ **Health Check** | http://localhost:8000/api/health/ | Health status endpoint |

---

## 🏗️ Arquitectura

### Arquitectura Multi-Tenant

```
┌─────────────────────────────────────────────────┐
│              OWLY CRM API                       │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │Company A │  │Company B │  │Company C │     │
│  ├──────────┤  ├──────────┤  ├──────────┤     │
│  │5 users   │  │20 users  │  │100 users │     │
│  │3 projects│  │10 projects│  │50 projects│    │
│  │50 leads  │  │500 leads │  │5000 leads│     │
│  └──────────┘  └──────────┘  └──────────┘     │
│                                                 │
│         MISMA BASE DE DATOS                     │
│         DATOS COMPLETAMENTE AISLADOS            │
└─────────────────────────────────────────────────┘
```

### Stack de Servicios

```
┌──────────────────────────────────────┐
│         LOAD BALANCER (AWS ALB)      │
└────────────┬─────────────────────────┘
             │
┌────────────▼─────────────────────────┐
│      DJANGO API (Gunicorn)           │
│      - JWT Authentication            │
│      - REST API Endpoints            │
│      - Business Logic                │
└─────┬──────────────┬─────────────┬───┘
      │              │             │
┌─────▼─────┐  ┌────▼────┐  ┌────▼────┐
│PostgreSQL │  │  Redis  │  │ Celery  │
│  (RDS)    │  │(Cache)  │  │ Worker  │
└───────────┘  └─────────┘  └─────────┘
```

### Diagrama de Modelos

```
              ┌─────────────┐
              │   COMPANY   │ (Tenant)
              └──────┬──────┘
                     │
       ┌─────────────┼─────────────┐
       │             │             │
  ┌────▼────┐   ┌───▼────┐   ┌───▼────┐
  │  USERS  │   │PROJECT │   │ LEADS  │
  └────┬────┘   └───┬────┘   └───┬────┘
       │            │             │
       │       ┌────▼────┐        │
       │       │  UNITS  │        │
       │       └────┬────┘        │
       │            │             │
       │            └─────┬───────┘
       │                  │
       │             ┌────▼────┐
       └─────────────┤ QUOTES  │
                     └────┬────┘
                          │
                     ┌────▼────────┐
                     │ ACTIVITIES  │
                     └─────────────┘
```

---

## 📚 Documentación

### Documentos Principales

| Documento | Descripción |
|-----------|-------------|
| **[GUIA_COMPLETA.md](GUIA_COMPLETA.md)** | 📖 **DOCUMENTACIÓN TÉCNICA COMPLETA** - Arquitectura, modelos, endpoints, casos de uso |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | ☁️ **GUÍA DE DEPLOYMENT** - Despliegue en AWS paso a paso |

### Contenido de la Guía Completa

La guía completa incluye:

1. **Arquitectura del Sistema**
   - Multi-tenancy explicado
   - Sistema de autenticación y permisos
   - Flujos de trabajo

2. **Modelos de Base de Datos**
   - Documentación detallada de cada modelo
   - Relaciones entre modelos
   - Casos de uso reales

3. **API Endpoints**
   - Documentación completa de todos los endpoints
   - Ejemplos de requests y responses
   - Casos de uso prácticos

4. **Testing**
   - Cómo ejecutar tests
   - Escribir nuevos tests
   - Estrategias de testing

5. **Features Avanzados**
   - Búsqueda semántica con pgvector
   - Análisis con IA
   - Bulk operations

---

## 🎯 API Endpoints

### Autenticación
```
POST   /api/auth/login/           - Login (obtener JWT tokens)
POST   /api/auth/refresh/         - Refresh access token
POST   /api/auth/verify/          - Verificar token
GET    /api/auth/users/profile/   - Obtener perfil
POST   /api/auth/users/change_password/ - Cambiar contraseña
```

### Companies (Empresas)
```
GET    /api/companies/            - Listar empresas
POST   /api/companies/            - Crear empresa
GET    /api/companies/{id}/       - Detalle de empresa
PUT    /api/companies/{id}/       - Actualizar empresa
GET    /api/companies/{id}/stats/ - Estadísticas de empresa
POST   /api/companies/{id}/upgrade_plan/ - Cambiar plan
```

### Projects (Proyectos)
```
GET    /api/projects/             - Listar proyectos
POST   /api/projects/             - Crear proyecto
GET    /api/projects/{id}/        - Detalle de proyecto
PUT    /api/projects/{id}/        - Actualizar proyecto
GET    /api/projects/{id}/units/  - Unidades del proyecto
GET    /api/projects/{id}/stats/  - Estadísticas del proyecto
GET    /api/projects/{id}/available_units/ - Unidades disponibles
GET    /api/projects/featured/    - Proyectos destacados
GET    /api/projects/by_location/ - Proyectos por ubicación
```

### Units (Unidades)
```
GET    /api/projects/units/       - Listar unidades
POST   /api/projects/units/       - Crear unidad
GET    /api/projects/units/{id}/  - Detalle de unidad
PUT    /api/projects/units/{id}/  - Actualizar unidad
POST   /api/projects/units/{id}/reserve/ - Reservar unidad
POST   /api/projects/units/{id}/mark_as_sold/ - Marcar como vendida
GET    /api/projects/units/similar/ - Buscar unidades similares
```

### Leads (Prospectos)
```
GET    /api/leads/                - Listar leads
POST   /api/leads/                - Crear lead
GET    /api/leads/{id}/           - Detalle de lead
PUT    /api/leads/{id}/           - Actualizar lead
POST   /api/leads/{id}/assign/    - Asignar lead
POST   /api/leads/{id}/change_status/ - Cambiar status
POST   /api/leads/{id}/add_note/  - Agregar nota
GET    /api/leads/{id}/timeline/  - Timeline de interacciones
GET    /api/leads/hot_leads/      - Leads calientes (alta prioridad)
GET    /api/leads/duplicates/     - Detectar duplicados
GET    /api/leads/upcoming_followups/ - Follow-ups próximos
GET    /api/leads/overdue_followups/ - Follow-ups vencidos
POST   /api/leads/bulk_assign/    - Asignación masiva
POST   /api/leads/bulk_status_change/ - Cambio de status masivo
GET    /api/leads/stats/          - Estadísticas de leads
GET    /api/leads/performance_by_source/ - Performance por fuente
```

### Quotes (Cotizaciones)
```
GET    /api/quotes/               - Listar cotizaciones
POST   /api/quotes/               - Crear cotización
GET    /api/quotes/{id}/          - Detalle de cotización
PUT    /api/quotes/{id}/          - Actualizar cotización
POST   /api/quotes/{id}/send/     - Enviar cotización
POST   /api/quotes/{id}/accept/   - Aceptar cotización
POST   /api/quotes/{id}/reject/   - Rechazar cotización
POST   /api/quotes/{id}/mark_viewed/ - Marcar como vista
```

### Activities (Actividades)
```
GET    /api/activities/           - Listar actividades
POST   /api/activities/           - Crear actividad
GET    /api/activities/{id}/      - Detalle de actividad
PUT    /api/activities/{id}/      - Actualizar actividad
DELETE /api/activities/{id}/      - Eliminar actividad
```

### Analytics (Reportes)
```
GET    /api/analytics/dashboard/  - Dashboard con métricas clave
GET    /api/analytics/leads/      - Análisis de leads
GET    /api/analytics/sales-funnel/ - Embudo de ventas
```

> 📘 **Documentación completa de endpoints con ejemplos:** [GUIA_COMPLETA.md](GUIA_COMPLETA.md)

---

## 🧪 Testing

### Ejecutar Tests

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
docker-compose exec web pytest apps/leads/tests/test_api.py
```

### Coverage Actual

- ✅ **49 tests** implementados
- ✅ Unit tests para modelos
- ✅ Integration tests para API
- ✅ E2E tests para flujos completos
- ✅ Multi-tenant isolation verificado

> 📘 **Guía completa de testing:** Ver sección Testing en [GUIA_COMPLETA.md](GUIA_COMPLETA.md)

---

## 🚀 Deployment

### AWS Deployment (Recomendado)

```bash
# Ver guía completa de deployment en AWS
cat DEPLOYMENT.md
```

La guía incluye:
- Setup de RDS (PostgreSQL)
- Setup de ElastiCache (Redis)
- Setup de S3 para media files
- Setup de ECS/Fargate
- Configuración de Load Balancer
- Auto-scaling
- Monitoreo con CloudWatch

### Estimación de Costos AWS

| Servicio | Especificación | Costo Mensual |
|----------|----------------|---------------|
| RDS PostgreSQL | db.t3.micro | ~$15 |
| ElastiCache Redis | cache.t3.micro | ~$12 |
| ECS Fargate | 2 tasks (0.5 vCPU, 1GB) | ~$30 |
| Load Balancer | Application LB | ~$16 |
| S3 | Storage + Transfer | ~$5 |
| **Total** | | **~$78/mes** |

> 📘 **Guía completa de deployment:** [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 🛠️ Comandos Útiles

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f web
docker-compose logs -f celery

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Shell de Django
docker-compose exec web python manage.py shell

# Crear migraciones
docker-compose exec web python manage.py makemigrations

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Poblar base de datos
docker-compose exec web python seed_database.py

# Ejecutar tests
make test

# Ver cobertura de tests
make test-coverage

# Backup de base de datos
./scripts/backup.sh

# Restore de base de datos
./scripts/restore.sh backup-file.sql
```

---

## 📂 Estructura del Proyecto

```
owly-api-ecosystem/
├── apps/                      # Aplicaciones Django
│   ├── core/                  # Modelos base, middleware, permisos
│   ├── companies/             # Gestión de empresas (tenants)
│   ├── users/                 # Usuarios y autenticación
│   ├── projects/              # Proyectos inmobiliarios
│   ├── leads/                 # Gestión de leads
│   ├── quotes/                # Cotizaciones
│   ├── activities/            # Actividades e interacciones
│   └── analytics/             # Reportes y analytics
│
├── owly_crm/                  # Configuración Django
│   ├── settings.py            # Settings principales
│   ├── urls.py                # URLs principales
│   ├── celery.py              # Configuración Celery
│   └── wsgi.py                # WSGI application
│
├── tests/                     # Tests globales
│   ├── factories.py           # Factory Boy factories
│   ├── test_e2e.py            # End-to-end tests
│   └── test_multi_tenant.py  # Tests de multi-tenancy
│
├── scripts/                   # Scripts útiles
│   ├── backup.sh              # Backup de BD
│   ├── restore.sh             # Restore de BD
│   └── setup.sh               # Setup inicial
│
├── docker-compose.yml         # Definición de servicios Docker
├── Dockerfile                 # Imagen Docker
├── requirements.txt           # Dependencias Python
├── manage.py                  # Django management
├── Makefile                   # Comandos útiles
├── pytest.ini                 # Configuración pytest
├── .env                       # Variables de entorno
│
├── README.md                  # 📖 Este archivo
├── GUIA_COMPLETA.md          # 📚 Documentación técnica completa
└── DEPLOYMENT.md             # ☁️ Guía de deployment AWS
```

---

## 🔧 Configuración

### Variables de Entorno Importantes

```bash
# Django
SECRET_KEY=                    # Secret key de Django (cambiar en producción)
DEBUG=                         # True en desarrollo, False en producción
ALLOWED_HOSTS=                 # Hosts permitidos

# Base de Datos
DATABASE_URL=                  # URL de conexión PostgreSQL

# Redis
REDIS_URL=                     # URL de conexión Redis
CELERY_BROKER_URL=             # URL del broker Celery
CELERY_RESULT_BACKEND=         # URL del backend de resultados

# CORS
CORS_ALLOWED_ORIGINS=          # Orígenes permitidos para CORS

# AWS S3 (Opcional)
USE_S3=                        # True para usar S3, False para local
AWS_ACCESS_KEY_ID=             # AWS access key
AWS_SECRET_ACCESS_KEY=         # AWS secret key
AWS_STORAGE_BUCKET_NAME=       # Nombre del bucket S3

# Email
EMAIL_BACKEND=                 # Backend de email
DEFAULT_FROM_EMAIL=            # Email remitente por defecto

# JWT
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=  # Duración del access token (default: 60)
JWT_REFRESH_TOKEN_LIFETIME_DAYS=    # Duración del refresh token (default: 7)
```

---

## 🤝 Contribución

### Cómo Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guías de Contribución

- Escribe tests para nuevas funcionalidades
- Mantén coverage > 80%
- Sigue PEP 8 para código Python
- Documenta nuevos endpoints en la guía completa
- Actualiza el README si es necesario

---

## 📝 Licencia

Este proyecto es **propietario**. Todos los derechos reservados.

© 2024 OWLY CRM. No está permitido el uso, copia, modificación o distribución sin autorización expresa.

---

## 🆘 Soporte

### Problemas Comunes

**Puerto 8000 ocupado:**
```bash
# Cambiar puerto en docker-compose.yml línea 43
"8001:8000"  # en lugar de "8000:8000"
```

**Base de datos no conecta:**
```bash
# Esperar 10-15 segundos después de docker-compose up
sleep 15
docker-compose exec web python manage.py migrate
```

**Olvidé la contraseña del superusuario:**
```bash
docker-compose exec web python manage.py changepassword tu-email@example.com
```

**Empezar de cero:**
```bash
docker-compose down -v  # Elimina todo incluyendo volumes
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### Contacto

- 📧 Email: admin@owlycrm.com
- 📚 Documentación: http://localhost:8000/api/docs/
- 🐛 Issues: Reportar en el repositorio

---

## 🎉 Agradecimientos

Construido con:
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Celery](https://docs.celeryproject.org/)
- [Docker](https://www.docker.com/)

---

## 🚀 Quick Links

- 🌐 **API Local**: http://localhost:8000/api/
- 📚 **API Docs**: http://localhost:8000/api/docs/
- 👤 **Admin**: http://localhost:8000/admin/
- ❤️ **Health**: http://localhost:8000/api/health/

---

**¿Listo para empezar?** 

```bash
docker-compose up -d && docker-compose exec web python manage.py migrate
```

**¡Feliz coding! 🎉**

---

**Built with ❤️ for Real Estate CRM**
