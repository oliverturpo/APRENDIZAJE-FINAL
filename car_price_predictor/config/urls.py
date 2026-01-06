"""
URL configuration for config project - API only backend

Django sirve únicamente endpoints de API REST.
El frontend React (en /frontend) maneja toda la interfaz de usuario.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def api_root(request):
    """Endpoint raíz que muestra las APIs disponibles"""
    return JsonResponse({
        'message': 'AutoPredict API - Backend only',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
            'predictor_api': '/predictor/api/',
            'cars_api': '/cars/api/',
        },
        'api_docs': {
            'predict': 'POST /predictor/api/predict/',
            'stats': 'GET /predictor/api/stats/',
            'options': 'GET /predictor/api/options/',
        },
        'frontend': 'React app en /frontend (puerto 5173 en desarrollo)'
    })


urlpatterns = [
    path('', api_root, name='api_root'),
    path('cars/', include('apps.cars.urls')),
    path('predictor/', include('apps.predictor.urls')),
    path('admin/', admin.site.urls),
]
