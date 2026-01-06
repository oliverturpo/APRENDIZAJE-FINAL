"""
URLs para la app predictor - Solo API REST endpoints
"""
from django.urls import path
from . import api_views

app_name = 'predictor'

urlpatterns = [
    # API endpoints
    path('api/options/', api_views.get_form_options, name='api_options'),
    path('api/predict/', api_views.predict_price, name='api_predict'),
    path('api/stats/', api_views.get_dashboard_stats, name='api_stats'),
]
