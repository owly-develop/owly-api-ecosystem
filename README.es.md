# OWLY CRM API - Django REST Framework

API multi-tenant para CRM construida con Django REST Framework, PostgreSQL, Redis y Celery. Dockerizada y lista para despliegue en AWS.

## 🚀 Características Principales

- **Arquitectura Multi-Tenant**: Una base de datos, múltiples empresas con aislamiento de datos
- **CRM Completo**: Empresas, Usuarios, Proyectos, Unidades, Leads, Cotizaciones, Actividades
- **Autenticación JWT**: Autenticación segura basada en tokens
- **API RESTful**: Operaciones CRUD completas con filtrado, búsqueda y paginación
- **Analytics en Tiempo Real**: Estadísticas del dashboard y embudo de ventas
- **Tareas Asíncronas**: Celery para trabajos en segundo plano
- **Documentación de API**: Auto-generada con drf-spectacular (Swagger/OpenAPI)
- **Listo para Producción**: Docker, AWS S3, Redis cache, seguimiento de errores

## 🎯 Inicio Rápido (3 pasos)

### 1. Crea el archivo .env
```bash
# En la raíz del proyecto, crea un archivo .env con este contenido:
SECRET_KEY=django-insecure-local-dev-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DATABASE_URL=postgresql://owly_user:owly_secure_password_2024@db:5432/owly_crm
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
USE_S3=False
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
DEFAULT_FROM_EMAIL=noreply@owlycrm.com
ADMIN_EMAIL=admin@owlycrm.com
```

### 2. Inicia los servicios
```bash
docker-compose up -d
```

Esto iniciará:
- Base de datos PostgreSQL
- Cache Redis
- Servidor web Django
- Worker Celery
- Celery beat scheduler

### 3. Ejecuta las migraciones y crea un admin
```bash
# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser
```

### 4. Accede a la aplicación

- **API**: http://localhost:8000/api/
- **Panel Admin**: http://localhost:8000/admin/
- **Documentación API**: http://localhost:8000/api/docs/
- **Health Check**: http://localhost:8000/api/health/

## 📚 Documentación Completa

| Documento | Descripción |
|-----------|-------------|
| [README.md](README.md) | Documentación completa en inglés |
| [QUICKSTART.md](QUICKSTART.md) | Inicio rápido en 5 minutos |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Guía de despliegue en AWS |
| [ENV_SETUP.md](ENV_SETUP.md) | Configuración de variables de entorno |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Resumen del proyecto |
| [COPY_AND_USE.md](COPY_AND_USE.md) | Cómo copiar y usar independientemente |

## 🛠️ Comandos Útiles

### Usando Make (recomendado):
```bash
make up              # Iniciar todos los servicios
make down            # Detener todos los servicios
make logs            # Ver logs de todos los servicios
make logs-web        # Ver logs solo del servidor web
make shell           # Abrir Django shell
make bash            # Abrir bash en el contenedor
make migrate         # Ejecutar migraciones
make makemigrations  # Crear nuevas migraciones
make createsuperuser # Crear un superusuario
make test            # Ejecutar tests
make backup          # Hacer backup de la base de datos
make clean           # Limpiar todo (¡cuidado!)
```

### Sin Make (usando docker-compose):
```bash
docker-compose up -d                          # Iniciar servicios
docker-compose down                           # Detener servicios
docker-compose logs -f                        # Ver logs
docker-compose logs -f web                    # Ver logs del web
docker-compose exec web python manage.py shell  # Django shell
docker-compose exec web python manage.py migrate  # Migrar DB
```

## 🔐 Autenticación

La API usa JWT (JSON Web Tokens) para autenticación.

### Hacer Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@owlycrm.com", "password": "tu-password"}'
```

Respuesta:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Usar el Token
```bash
curl -X GET http://localhost:8000/api/leads/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

## 📊 Modelos de Datos

### 7 Entidades Principales:

1. **Company** (Empresa/Tenant)
   - Organización multi-tenant
   - Planes de suscripción
   - Límites por plan

2. **User** (Usuario)
   - Modelo de usuario personalizado
   - Roles: Admin, Manager, Sales, Marketing, Support
   - Métricas de rendimiento

3. **Project** (Proyecto)
   - Proyectos inmobiliarios
   - Ubicación, precios, amenidades
   - Visualizaciones interactivas

4. **Unit** (Unidad)
   - Unidades individuales
   - Especificaciones y pricing
   - Estado de disponibilidad

5. **Lead** (Prospecto)
   - Gestión de leads
   - Pipeline de ventas
   - Scoring con IA

6. **Quote** (Cotización)
   - Generación de cotizaciones
   - Cálculos de precio
   - Seguimiento de estado

7. **Activity** (Actividad)
   - Seguimiento de interacciones
   - Múltiples tipos
   - Programación de tareas

## 🌐 Endpoints Principales

### Autenticación
```
POST   /api/auth/login/          - Login (obtener tokens JWT)
POST   /api/auth/refresh/        - Refrescar access token
GET    /api/auth/users/profile/  - Obtener perfil actual
POST   /api/auth/users/change_password/ - Cambiar contraseña
```

### Empresas
```
GET    /api/companies/           - Listar empresas
POST   /api/companies/           - Crear empresa
GET    /api/companies/{id}/      - Obtener detalles
GET    /api/companies/{id}/stats/ - Estadísticas
```

### Proyectos
```
GET    /api/projects/            - Listar proyectos
POST   /api/projects/            - Crear proyecto
GET    /api/projects/{id}/       - Obtener detalles
GET    /api/projects/{id}/units/ - Obtener unidades
```

### Leads
```
GET    /api/leads/               - Listar leads
POST   /api/leads/               - Crear lead
POST   /api/leads/{id}/assign/   - Asignar lead
GET    /api/leads/stats/         - Estadísticas
```

### Analytics
```
GET    /api/analytics/dashboard/ - Estadísticas del dashboard
GET    /api/analytics/leads/     - Analytics de leads
GET    /api/analytics/sales-funnel/ - Embudo de ventas
```

Ver documentación completa en: http://localhost:8000/api/docs/

## 🚀 Desplegar en AWS

### Resumen Rápido:
1. Crear RDS PostgreSQL
2. Crear ElastiCache Redis
3. Crear bucket S3
4. Construir y subir imagen Docker a ECR
5. Crear ECS cluster y servicio
6. Configurar Load Balancer
7. Ejecutar migraciones

**Costo estimado**: $75-100/mes para producción pequeña

Ver guía completa en [DEPLOYMENT.md](DEPLOYMENT.md)

## 📦 Copiar a Otro Lugar

Para usar este proyecto de forma independiente:

```bash
# Copiar la carpeta
cp -r owly-api-django /tu/nueva/ubicacion/

# Ir al nuevo directorio
cd /tu/nueva/ubicacion/owly-api-django

# Crear .env
cp .env.example .env

# Iniciar servicios
docker-compose up -d

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear admin
docker-compose exec web python manage.py createsuperuser
```

Ver guía completa en [COPY_AND_USE.md](COPY_AND_USE.md)

## 🔧 Desarrollo

### Añadir Nuevos Modelos
1. Editar modelos en `apps/nombre_app/models.py`
2. Crear migraciones: `make makemigrations`
3. Aplicar migraciones: `make migrate`

### Añadir Nuevos Endpoints
1. Crear serializers en `apps/nombre_app/serializers.py`
2. Crear views en `apps/nombre_app/views.py`
3. Registrar URLs en `apps/nombre_app/urls.py`
4. Documentación se actualiza automáticamente

### Testing
```bash
make test
# o
docker-compose exec web python manage.py test
```

## 🆘 Problemas Comunes

### Puerto 8000 ocupado
Edita `docker-compose.yml` y cambia `"8000:8000"` por `"8001:8000"`

### Base de datos no conecta
```bash
# Ver logs de PostgreSQL
docker-compose logs db

# Esperar unos segundos y reintentar
docker-compose restart
```

### Empezar de cero
```bash
make clean    # Elimina todo
make setup    # Configura de nuevo
```

## 📞 Soporte

- 📖 Documentación: http://localhost:8000/api/docs/
- 💬 Email: admin@owlycrm.com

## 📝 Licencia

Proyecto propietario para OWLY CRM. Todos los derechos reservados.

---

**¡Construido con ❤️ para OWLY CRM!**

