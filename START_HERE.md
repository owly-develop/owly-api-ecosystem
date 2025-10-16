# 🎉 ¡Bienvenido a OWLY CRM API!

## ⚡ Inicio Súper Rápido (2 minutos)

### Paso 1: Crear archivo .env

Crea un archivo llamado `.env` en esta carpeta con este contenido:

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

### Paso 2: Iniciar servicios

```bash
docker-compose up -d
```

### Paso 3: Configurar base de datos

```bash
# Esperar 10 segundos para que PostgreSQL inicie
# Luego ejecutar:

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## ✅ ¡Listo!

Ahora puedes acceder a:

- 🌐 **API**: http://localhost:8000/api/
- 👤 **Admin**: http://localhost:8000/admin/
- 📚 **Documentación**: http://localhost:8000/api/docs/
- ❤️ **Health Check**: http://localhost:8000/api/health/

## 📖 Documentación

| Archivo | Para qué sirve |
|---------|----------------|
| **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** | 📚 **ÍNDICE MAESTRO** - Empieza aquí |
| **[MODELS_DOCUMENTATION.md](MODELS_DOCUMENTATION.md)** | 📖 **NUEVO** - Qué es cada modelo |
| **[ENDPOINTS_GUIDE.md](ENDPOINTS_GUIDE.md)** | 🎯 **NUEVO** - Intención de cada endpoint |
| **[ARCHITECTURE_GUIDE.md](ARCHITECTURE_GUIDE.md)** | 🏛️ **NUEVO** - Arquitectura y flujos |
| **[API_ENHANCEMENTS.md](API_ENHANCEMENTS.md)** | ⚡ 25+ endpoints nuevos |
| **[README.es.md](README.es.md)** | 📖 Documentación completa (español) |
| **[QUICKSTART.md](QUICKSTART.md)** | 🚀 Guía de inicio rápido |
| **[COPY_AND_USE.md](COPY_AND_USE.md)** | 📦 Cómo copiar y usar independientemente |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | ☁️ Desplegar en AWS |
| **[ENV_SETUP.md](ENV_SETUP.md)** | ⚙️ Configuración de variables |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | 📊 Resumen completo del proyecto |
| [README.md](README.md) | 📖 Full documentation (English) |

## 🎯 ¿Qué Incluye Este Proyecto?

✅ **API Multi-Tenant** - Una empresa puede tener múltiples proyectos
✅ **7 Modelos Principales** - Company, User, Project, Unit, Lead, Quote, Activity
✅ **50+ Endpoints RESTful** - CRUD completo con filtros y búsqueda
✅ **Autenticación JWT** - Login seguro con tokens
✅ **PostgreSQL + Redis** - Base de datos robusta y cache
✅ **Celery** - Tareas asíncronas
✅ **Docker** - Todo containerizado
✅ **Documentación Automática** - Swagger UI
✅ **Listo para AWS** - Deployment guide incluida

## 🛠️ Comandos Útiles

```bash
make up              # Iniciar todo
make down            # Detener todo
make logs            # Ver logs
make shell           # Django shell
make migrate         # Ejecutar migraciones
make backup          # Backup de la BD
```

## 🚀 Próximos Pasos

1. ✅ Lee [README.es.md](README.es.md) para documentación completa
2. ✅ Explora la API en http://localhost:8000/api/docs/
3. ✅ Crea algunos datos de prueba en el admin
4. ✅ Conecta tu frontend modificando CORS_ALLOWED_ORIGINS en .env
5. ✅ Cuando estés listo, lee [DEPLOYMENT.md](DEPLOYMENT.md) para subir a AWS

## 💡 Tips

- Los emails se muestran en la consola (no se envían realmente)
- El admin tiene acceso a todo
- Cada empresa (Company) es un tenant independiente
- Los usuarios solo ven datos de su empresa
- La documentación de la API es interactiva (puedes probar endpoints)

## 🆘 ¿Problemas?

### Puerto 8000 ocupado
Edita `docker-compose.yml` línea 43: cambia `"8000:8000"` por `"8001:8000"`

### Base de datos no conecta
Espera 10-15 segundos después de `docker-compose up -d` antes de ejecutar migraciones

### Olvidé la contraseña
```bash
docker-compose exec web python manage.py changepassword tu-email@example.com
```

### Empezar de cero
```bash
docker-compose down -v    # Elimina todo
docker-compose up -d      # Inicia de nuevo
# Luego ejecuta migraciones y crea superuser
```

## 📞 Soporte

- 📖 Documentación interactiva: http://localhost:8000/api/docs/
- 💬 Email: admin@owlycrm.com

---

**¡Feliz coding! 🎉**

*Proyecto creado con Django 5.0, Django REST Framework, PostgreSQL, Redis, Celery y mucho ❤️*

