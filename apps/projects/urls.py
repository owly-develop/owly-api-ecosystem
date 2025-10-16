"""
Project URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'stages', views.StageViewSet, basename='stage')
router.register(r'blocks', views.BlockViewSet, basename='block')
router.register(r'typologies', views.TypologyViewSet, basename='typology')
router.register(r'amenities', views.AmenityViewSet, basename='amenity')
router.register(r'orbit-views', views.OrbitViewViewSet, basename='orbit-view')
router.register(r'units', views.UnitViewSet, basename='unit')
router.register(r'', views.ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
]

