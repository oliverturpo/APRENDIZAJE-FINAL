from django.db import models
from django.utils import timezone


class ScrapingJob(models.Model):
    """Modelo para tracking de trabajos de scraping"""

    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('running', 'En ejecución'),
        ('completed', 'Completado'),
        ('failed', 'Fallido'),
    ]

    initiated_by = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Estadísticas
    total_pages_scraped = models.IntegerField(default=0)
    total_records_extracted = models.IntegerField(default=0)
    total_records_loaded = models.IntegerField(default=0)

    # Logs
    log_messages = models.TextField(blank=True)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ['-started_at']
        verbose_name = 'Trabajo de Scraping'
        verbose_name_plural = 'Trabajos de Scraping'

    def __str__(self):
        return f"Scraping Job #{self.id} - {self.status} ({self.started_at.strftime('%Y-%m-%d %H:%M')})"

    def duration(self):
        if self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None


class Car(models.Model):
    """Modelo principal para almacenar datos de autos scrapeados"""

    # Campos que coinciden con la tabla real en PostgreSQL
    title = models.CharField(max_length=255, db_column='title')
    link = models.URLField(max_length=500, db_column='link')
    tag = models.CharField(max_length=100, null=True, blank=True, db_column='tag')
    image = models.URLField(max_length=500, null=True, blank=True, db_column='image')

    # Campos para predicción
    fuel = models.CharField(max_length=50, db_column='fuel')
    location = models.CharField(max_length=100, db_column='location')
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_column='price')
    brand = models.CharField(max_length=100, db_column='brand')
    year = models.IntegerField(db_column='year')
    subcategory = models.CharField(max_length=100, null=True, blank=True, db_column='subcategory')
    transmission = models.CharField(max_length=50, db_column='transmission')

    # Metadata adicional
    advertiser = models.CharField(max_length=100, null=True, blank=True, db_column='advertiser')
    category = models.CharField(max_length=100, null=True, blank=True, db_column='category')
    slug = models.SlugField(max_length=255, null=True, blank=True, db_column='slug')

    # Control de datos
    fecha = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = 'tbl_auto_raw_taller'
        ordering = ['-fecha']
        verbose_name = 'Auto'
        verbose_name_plural = 'Autos'
        managed = False  # No dejar que Django maneje la tabla

    def __str__(self):
        return f"{self.brand} - {self.title} ({self.year})"

    # Propiedades de conveniencia
    @property
    def image_url(self):
        return self.image

    @property
    def detail_url(self):
        return self.link
