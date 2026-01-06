"""
URLs para la app cars - Solo API REST endpoints
"""
from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    # API endpoints
    path('api/stats/', views.scraping_stats, name='api_scraping_stats'),
]
