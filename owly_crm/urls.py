"""
URL configuration for owly_crm project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # API Endpoints
    path('api/auth/', include('apps.users.urls')),
    path('api/companies/', include('apps.companies.urls')),
    path('api/projects/', include('apps.projects.urls')),
    path('api/leads/', include('apps.leads.urls')),
    path('api/quotes/', include('apps.quotes.urls')),
    path('api/activities/', include('apps.activities.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/', include('apps.core.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

