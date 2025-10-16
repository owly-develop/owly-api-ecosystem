"""
Quote URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.QuoteViewSet, basename='quote')
router.register(r'templates', views.QuoteTemplateViewSet, basename='quote-template')

urlpatterns = [
    path('', include(router.urls)),
]

