# 🦉 OWLY CRM API - Sistema CRM Multi-Tenant para Inmobiliarias

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

API REST completa para gestión de CRM inmobiliario con arquitectura multi-tenant, construida con Django REST Framework, PostgreSQL, Redis y Celery. Lista para producción y optimizada para AWS.

> 🌍 **[English version](README.md)** | 🇪🇸 **Versión en Español**

---

## ⚡ Inicio Súper Rápido (2 minutos)

### 1. Crear archivo .env

```bash
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

### 2. Iniciar servicios

```bash
docker-compose up -d
```

### 3. Configurar base de datos

```bash
# Esperar 10 segundos para que PostgreSQL inicie
sleep 10

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# (Opcional) Poblar con datos de prueba
docker-compose exec web python seed_database.py
```

### ✅ ¡Listo!

Ahora puedes acceder a:

- 🌐 **API**: http://localhost:8000/api/
- 👤 **Admin**: http://localhost:8000/admin/
- 📚 **Documentación**: http://localhost:8000/api/docs/
- ❤️ **Health Check**: http://localhost:8000/api/health/

---

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| **[GUIA_COMPLETA.md](GUIA_COMPLETA.md)** | 📖 **DOCUMENTACIÓN TÉCNICA COMPLETA** - Arquitectura, modelos, endpoints, testing |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | ☁️ **GUÍA DE DEPLOYMENT** - Despliegue en AWS paso a paso |

---

## ✨ Características Principales

### 🏢 Arquitectura Multi-Tenant
- Una base de datos, múltiples empresas con aislamiento total de datos
- Cada empresa opera independientemente
- Escalable y eficiente en costos

### 📊 Gestión Completa de CRM
- **Companies**: Gestión de empresas con planes y límites
- **Users**: Sistema de roles (Admin, Manager, Sales, Marketing, Support)
- **Projects**: Proyectos inmobiliarios con seguimiento completo
- **Units**: Inventario detallado de unidades
- **Leads**: Pipeline de ventas con scoring automático
- **Quotes**: Cotizaciones con cálculos automáticos
- **Activities**: Timeline de interacciones

### 🔐 Seguridad
- **JWT Authentication** con tokens de acceso y refresh
- **Role-Based Access Control (RBAC)**
- **Tenant Isolation** automático
- **Soft Deletes** para recuperación

### 🚀 Features Avanzados
- API RESTful con paginación y filtros
- Analytics Dashboard en tiempo real
- Bulk Operations (operaciones masivas)
- Celery Tasks (procesamiento asíncrono)
- Documentación Swagger/OpenAPI
- Base de datos preparada para IA con pgvector

---

## 🎯 API Endpoints

### Autenticación
```
POST   /api/auth/login/           - Login (obtener JWT tokens)
POST   /api/auth/refresh/         - Refresh access token
GET    /api/auth/users/profile/   - Obtener perfil
```

### Companies (Empresas)
```
GET    /api/companies/            - Listar empresas
POST   /api/companies/            - Crear empresa
GET    /api/companies/{id}/stats/ - Estadísticas
```

### Projects (Proyectos)
```
GET    /api/projects/             - Listar proyectos
POST   /api/projects/             - Crear proyecto
GET    /api/projects/{id}/available_units/ - Unidades disponibles
GET    /api/projects/featured/    - Proyectos destacados
```

### Leads (Prospectos)
```
GET    /api/leads/                - Listar leads
POST   /api/leads/                - Crear lead
GET    /api/leads/{id}/timeline/  - Timeline de interacciones
POST   /api/leads/bulk_assign/    - Asignación masiva
GET    /api/leads/hot_leads/      - Leads calientes (alta prioridad)
GET    /api/leads/performance_by_source/ - Performance por fuente
```

### Quotes (Cotizaciones)
```
GET    /api/quotes/               - Listar cotizaciones
POST   /api/quotes/               - Crear cotización
POST   /api/quotes/{id}/send/     - Enviar cotización
POST   /api/quotes/{id}/accept/   - Aceptar cotización
```

### Analytics (Reportes)
```
GET    /api/analytics/dashboard/  - Dashboard con métricas
GET    /api/analytics/sales-funnel/ - Embudo de ventas
```

> 📘 **Documentación completa:** [GUIA_COMPLETA.md](GUIA_COMPLETA.md)

---

## 🧪 Testing

```bash
# Todos los tests
make test

# Con coverage
make test-coverage

# Solo unit tests
make test-unit

# Solo integration tests
make test-integration
```

### Coverage
- ✅ **49 tests** implementados
- ✅ Unit tests para modelos
- ✅ Integration tests para API
- ✅ E2E tests para flujos completos
- ✅ Multi-tenant isolation verificado

---

## 🚀 Deployment en AWS

### Estimación de Costos

| Servicio | Especificación | Costo Mensual |
|----------|----------------|---------------|
| RDS PostgreSQL | db.t3.micro | ~$15 |
| ElastiCache Redis | cache.t3.micro | ~$12 |
| ECS Fargate | 2 tasks | ~$30 |
| Load Balancer | ALB | ~$16 |
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

# Detener servicios
docker-compose down

# Shell de Django
docker-compose exec web python manage.py shell

# Crear migraciones
docker-compose exec web python manage.py makemigrations

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Tests
make test
make test-coverage

# Backup de base de datos
./scripts/backup.sh
```

---

## 📂 Estructura del Proyecto

```
owly-api-ecosystem/
├── apps/                      # Aplicaciones Django
│   ├── core/                  # Modelos base, middleware
│   ├── companies/             # Gestión de empresas
│   ├── users/                 # Usuarios y autenticación
│   ├── projects/              # Proyectos inmobiliarios
│   ├── leads/                 # Gestión de leads
│   ├── quotes/                # Cotizaciones
│   ├── activities/            # Actividades
│   └── analytics/             # Reportes
│
├── owly_crm/                  # Configuración Django
├── tests/                     # Tests globales
├── scripts/                   # Scripts útiles
│
├── docker-compose.yml         # Servicios Docker
├── Dockerfile                 # Imagen Docker
├── requirements.txt           # Dependencias Python
│
├── README.md                  # 📖 Documentación principal (inglés)
├── README.es.md              # 📖 Documentación principal (español)
├── GUIA_COMPLETA.md          # 📚 Documentación técnica completa
└── DEPLOYMENT.md             # ☁️ Guía de deployment AWS
```

---

## 🏗️ Arquitectura

### Multi-Tenant

```
┌─────────────────────────────────────────────────┐
│              OWLY CRM API                       │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │Company A │  │Company B │  │Company C │     │
│  │5 users   │  │20 users  │  │100 users │     │
│  │3 projects│  │10 projects│  │50 projects│    │
│  └──────────┘  └──────────┘  └──────────┘     │
│                                                 │
│         MISMA BASE DE DATOS                     │
│         DATOS AISLADOS                          │
└─────────────────────────────────────────────────┘
```

### Stack de Servicios

```
┌──────────────────────────────────────┐
│         LOAD BALANCER                │
└────────────┬─────────────────────────┘
             │
┌────────────▼─────────────────────────┐
│      DJANGO API (Gunicorn)           │
└─────┬──────────────┬─────────────┬───┘
      │              │             │
┌─────▼─────┐  ┌────▼────┐  ┌────▼────┐
│PostgreSQL │  │  Redis  │  │ Celery  │
└───────────┘  └─────────┘  └─────────┘
```

---

## 🆘 Problemas Comunes

**Puerto 8000 ocupado:**
```bash
# Editar docker-compose.yml línea 43
"8001:8000"  # en lugar de "8000:8000"
```

**Base de datos no conecta:**
```bash
# Esperar más tiempo después de docker-compose up
sleep 15
docker-compose exec web python manage.py migrate
```

**Olvidé la contraseña:**
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

---

## 📝 Licencia

Este proyecto es **propietario**. Todos los derechos reservados.

© 2024 OWLY CRM. No está permitido el uso, copia, modificación o distribución sin autorización expresa.

---

## 📞 Soporte

- 📧 Email: admin@owlycrm.com
- 📚 Documentación: http://localhost:8000/api/docs/

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
