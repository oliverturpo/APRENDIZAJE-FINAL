from django.db import models
from django.utils import timezone


class Prediction(models.Model):
    """Modelo para guardar historial de predicciones"""

    # Inputs del usuario
    marca = models.CharField(max_length=100)
    anio = models.IntegerField()
    combustible = models.CharField(max_length=50)
    transmision = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=100)
    subcategoria = models.CharField(max_length=100, null=True, blank=True)

    # Output
    precio_predicho = models.DecimalField(max_digits=12, decimal_places=2)

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Predicción'
        verbose_name_plural = 'Predicciones'

    def __str__(self):
        return f"{self.marca} {self.anio} - ${self.precio_predicho}"
