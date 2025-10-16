# 📋 Cómo Copiar y Usar Este Proyecto de Forma Independiente

Este documento explica cómo copiar la carpeta `owly-api-django` a cualquier ubicación y trabajar con ella como un proyecto completamente independiente.

## 🎯 Objetivo

Podrás:
- ✅ Copiar la carpeta a cualquier ubicación
- ✅ Trabajar en el proyecto sin depender del proyecto frontend
- ✅ Hacer commits independientes en Git
- ✅ Desplegar a AWS de forma independiente
- ✅ Escalar y mantener por separado

## 📦 Paso 1: Copiar el Proyecto

### Opción A: Copiar a una ubicación específica

```bash
# Desde la raíz del proyecto actual
cp -r owly-api-django /ruta/donde/quieres/el/proyecto/

# Ejemplo Windows:
xcopy owly-api-django C:\Projects\owly-api /E /I

# Ejemplo Mac/Linux:
cp -r owly-api-django ~/Projects/owly-api/
```

### Opción B: Mover en lugar de copiar

```bash
# Si quieres mover en lugar de copiar
mv owly-api-django /ruta/destino/

# Ejemplo:
mv owly-api-django ~/Projects/owly-api/
```

## 🔧 Paso 2: Configurar el Proyecto Copiado

### 1. Navega al nuevo directorio
```bash
cd /ruta/donde/copiaste/owly-api-django
```

### 2. Inicializa un nuevo repositorio Git (opcional)
```bash
git init
git add .
git commit -m "Initial commit - OWLY CRM API"

# Conecta con tu repositorio remoto
git remote add origin https://github.com/tu-usuario/owly-api.git
git push -u origin main
```

### 3. Crea el archivo .env
```bash
# Opción 1: Copiar desde el ejemplo
cp .env.example .env

# Opción 2: Crear manualmente (ver ENV_SETUP.md)
```

Para desarrollo local, el contenido de `.env` puede ser:
```bash
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

### 4. Inicia los servicios
```bash
# Usando docker-compose
docker-compose up -d

# O usando Make
make up
```

### 5. Ejecuta las migraciones
```bash
# Con docker-compose
docker-compose exec web python manage.py migrate

# O con Make
make migrate
```

### 6. Crea un superusuario
```bash
# Con docker-compose
docker-compose exec web python manage.py createsuperuser

# O con Make
make createsuperuser
```

## ✅ Paso 3: Verificar que Todo Funciona

### 1. Verifica que los servicios estén corriendo
```bash
docker-compose ps
```

Deberías ver 5 servicios activos:
- owly_postgres (PostgreSQL)
- owly_redis (Redis)
- owly_web (Django API)
- owly_celery (Celery worker)
- owly_celery_beat (Celery beat scheduler)

### 2. Prueba el health check
```bash
curl http://localhost:8000/api/health/
```

Deberías ver:
```json
{
  "status": "healthy",
  "database": "connected",
  "cache": "connected"
}
```

### 3. Accede a la documentación de la API
Abre en tu navegador: http://localhost:8000/api/docs/

### 4. Prueba el login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "tu-email@example.com", "password": "tu-password"}'
```

## 🚀 Uso Diario

### Comandos comunes con Make:
```bash
make up              # Iniciar servicios
make down            # Detener servicios
make logs            # Ver logs
make shell           # Abrir Django shell
make bash            # Abrir bash en el contenedor
make migrate         # Ejecutar migraciones
make makemigrations  # Crear nuevas migraciones
make test            # Ejecutar tests
make backup          # Hacer backup de la base de datos
make clean           # Limpiar todo (¡cuidado!)
```

### Sin Make (usando docker-compose directamente):
```bash
docker-compose up -d                          # Iniciar
docker-compose down                           # Detener
docker-compose logs -f                        # Ver logs
docker-compose exec web python manage.py shell  # Django shell
docker-compose exec web /bin/bash             # Bash
```

## 📊 Desarrollo del Proyecto

### Añadir nuevos modelos
1. Edita o crea modelos en `apps/nombre_app/models.py`
2. Crea migraciones: `make makemigrations`
3. Aplica migraciones: `make migrate`

### Añadir nuevos endpoints
1. Define serializers en `apps/nombre_app/serializers.py`
2. Define views en `apps/nombre_app/views.py`
3. Registra URLs en `apps/nombre_app/urls.py`
4. La documentación se actualiza automáticamente en `/api/docs/`

### Añadir nuevas apps
```bash
docker-compose exec web python manage.py startapp nombre_app apps/nombre_app
```

Luego:
1. Añade `'apps.nombre_app'` a `INSTALLED_APPS` en `settings.py`
2. Crea los modelos, views, serializers
3. Registra las URLs

## 🔄 Integración con Frontend

### CORS Configuration
Asegúrate de añadir la URL de tu frontend en `.env`:
```bash
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000,https://tu-frontend.com
```

### API Base URL
Tu frontend debe apuntar a:
- Desarrollo: `http://localhost:8000/api/`
- Producción: `https://api.tudominio.com/api/`

### Autenticación
1. Frontend hace login a `/api/auth/login/`
2. Recibe `access` y `refresh` tokens
3. Incluye `Authorization: Bearer {access_token}` en cada request
4. Refresca el token cuando expire usando `/api/auth/refresh/`

## 🌐 Despliegue a AWS

Sigue la guía completa en [DEPLOYMENT.md](DEPLOYMENT.md)

Resumen:
1. Crea RDS PostgreSQL
2. Crea ElastiCache Redis
3. Crea S3 bucket
4. Construye y sube imagen Docker a ECR
5. Crea ECS cluster y servicio
6. Configura Load Balancer
7. Ejecuta migraciones

Costo estimado: $75-100/mes para producción pequeña

## 📂 Estructura del Proyecto

```
owly-api-django/
├── apps/                    # Aplicaciones Django
│   ├── core/               # Funcionalidad base
│   ├── companies/          # Multi-tenancy
│   ├── users/              # Usuarios y auth
│   ├── projects/           # Proyectos y unidades
│   ├── leads/              # Leads/prospectos
│   ├── quotes/             # Cotizaciones
│   ├── activities/         # Actividades
│   └── analytics/          # Analytics
├── owly_crm/               # Configuración Django
│   ├── settings.py         # Settings
│   ├── urls.py             # URLs principales
│   ├── wsgi.py             # WSGI
│   └── celery.py           # Celery config
├── scripts/                # Scripts útiles
│   ├── setup.sh            # Setup inicial
│   ├── backup.sh           # Backup DB
│   └── restore.sh          # Restore DB
├── docker-compose.yml      # Docker Compose
├── Dockerfile              # Docker image
├── requirements.txt        # Dependencies Python
├── manage.py               # Django CLI
├── Makefile               # Comandos make
├── README.md              # Documentación principal
├── QUICKSTART.md          # Inicio rápido
├── DEPLOYMENT.md          # Guía de despliegue
├── ENV_SETUP.md           # Config de variables
└── PROJECT_SUMMARY.md     # Resumen del proyecto
```

## 🔒 Seguridad

### Para Producción:
1. ✅ Genera un nuevo `SECRET_KEY`
2. ✅ Cambia `DEBUG=False`
3. ✅ Usa contraseñas fuertes para la base de datos
4. ✅ Configura `ALLOWED_HOSTS` correctamente
5. ✅ Habilita HTTPS
6. ✅ Usa AWS Secrets Manager para credenciales
7. ✅ Configura Sentry para monitoreo de errores

### Generar SECRET_KEY seguro:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 🆘 Problemas Comunes

### Puerto 8000 ya está en uso
Edita `docker-compose.yml`:
```yaml
web:
  ports:
    - "8001:8000"  # Cambia el puerto externo
```

### Base de datos no se conecta
```bash
# Espera a que PostgreSQL inicie completamente
docker-compose logs db

# Reinicia los servicios
docker-compose restart
```

### Olvidé mi contraseña de superusuario
```bash
docker-compose exec web python manage.py changepassword tu-email@example.com
```

### Quiero empezar de cero
```bash
make clean    # Elimina todo (contenedores y volúmenes)
make setup    # Configura de nuevo
make createsuperuser  # Crea nuevo admin
```

## 📞 Soporte

- 📖 Documentación completa: [README.md](README.md)
- 🚀 Inicio rápido: [QUICKSTART.md](QUICKSTART.md)
- ☁️ Despliegue AWS: [DEPLOYMENT.md](DEPLOYMENT.md)
- ⚙️ Variables de entorno: [ENV_SETUP.md](ENV_SETUP.md)
- 📊 Resumen del proyecto: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## ✅ Checklist: Proyecto Copiado y Funcionando

- [ ] Carpeta copiada a nueva ubicación
- [ ] Git inicializado (opcional)
- [ ] Archivo `.env` creado
- [ ] Docker Compose levantado
- [ ] Migraciones ejecutadas
- [ ] Superusuario creado
- [ ] Health check funcionando
- [ ] Documentación accesible en /api/docs/
- [ ] Login exitoso
- [ ] CORS configurado para frontend

---

**¡Proyecto listo para desarrollo independiente! 🎉**

Ahora puedes trabajar en este proyecto sin ninguna dependencia del proyecto frontend original.

