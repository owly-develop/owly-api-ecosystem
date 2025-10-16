"""
Analytics URLs
"""
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_stats, name='dashboard-stats'),
    path('leads/', views.lead_analytics, name='lead-analytics'),
    path('sales-funnel/', views.sales_funnel, name='sales-funnel'),
]

