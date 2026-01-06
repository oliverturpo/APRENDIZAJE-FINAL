from apps.cars.models import Car, ScrapingJob
from django.utils import timezone


class CarLoader:
    """Carga datos a base de datos Django"""

    def load(self, df, scraping_job=None):
        """
        Carga DataFrame a base de datos

        Args:
            df (pd.DataFrame): DataFrame con datos transformados
            scraping_job (ScrapingJob): Job asociado

        Returns:
            int: Número de registros cargados
        """
        records_loaded = 0

        for _, row in df.iterrows():
            try:
                car, created = Car.objects.update_or_create(
                    codigo=row['id'],
                    defaults={
                        'titulo': row['title'],
                        'link': row['link'],
                        'etiqueta': row.get('tag'),
                        'imagen': row.get('image'),
                        'combustible': row.get('fuel', ''),
                        'ubicacion': row.get('location', ''),
                        'precio': row.get('price'),
                        'marca': row.get('brand', ''),
                        'anio': row.get('year', 0),
                        'anunciante': row.get('advertiser'),
                        'categoria': row.get('category'),
                        'subcategoria': row.get('subcategory'),
                        'transmision': row.get('transmission', ''),
                        'slug': row.get('slug'),
                        'fecha': timezone.now(),
                        'scraping_job': scraping_job
                    }
                )
                records_loaded += 1
                if created:
                    print(f'  + Creado: {car.codigo} - {car.titulo}')
                else:
                    print(f'  ↻ Actualizado: {car.codigo} - {car.titulo}')
            except Exception as e:
                print(f"Error cargando registro {row.get('id')}: {e}")
                continue

        return records_loaded
