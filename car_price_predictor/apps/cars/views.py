"""
Views para la app cars - API only (sin templates HTML)

Las funcionalidades de scraping deben ejecutarse mediante:
- Django management commands (python manage.py scrape_cars)
- Tareas programadas (Celery, cron, etc.)
- No mediante vistas web

Si necesitas endpoints API para scraping, agrégalos aquí usando DRF.
"""

from django.http import JsonResponse
from .models import Car, ScrapingJob


# Ejemplo de endpoint API para obtener estadísticas de scraping
def scraping_stats(request):
    """API endpoint para obtener estadísticas de scraping jobs"""
    total_cars = Car.objects.count()
    recent_jobs = ScrapingJob.objects.all()[:10]

    jobs_data = [
        {
            'id': job.id,
            'status': job.status,
            'started_at': job.started_at.isoformat(),
            'completed_at': job.completed_at.isoformat() if job.completed_at else None,
            'total_pages_scraped': job.total_pages_scraped,
            'total_records_loaded': job.total_records_loaded,
        }
        for job in recent_jobs
    ]

    return JsonResponse({
        'total_cars': total_cars,
        'recent_jobs': jobs_data,
    })
