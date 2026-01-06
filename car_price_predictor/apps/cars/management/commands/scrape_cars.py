from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.cars.models import ScrapingJob
from apps.cars.scraper.extractor import CarExtractor
from apps.cars.scraper.transformer import CarTransformer
from apps.cars.scraper.loader import CarLoader


class Command(BaseCommand):
    help = 'Ejecuta web scraping de neoauto.com'

    def add_arguments(self, parser):
        parser.add_argument(
            '--max-pages',
            type=int,
            default=None,
            help='Número máximo de páginas a scrapear'
        )
        parser.add_argument(
            '--job-id',
            type=int,
            default=None,
            help='ID del ScrapingJob existente'
        )

    def handle(self, *args, **options):
        # Crear o recuperar job
        if options['job_id']:
            job = ScrapingJob.objects.get(id=options['job_id'])
        else:
            job = ScrapingJob.objects.create(
                initiated_by='manual_command',
                status='pending'
            )

        # Actualizar estado
        job.status = 'running'
        job.save()

        try:
            # Extraer
            self.stdout.write(self.style.WARNING('Iniciando extracción...'))
            extractor = CarExtractor()
            data = extractor.extract(max_pages=options['max_pages'])
            job.total_records_extracted = len(data)
            job.total_pages_scraped = options['max_pages'] if options['max_pages'] else 0
            job.save()
            self.stdout.write(self.style.SUCCESS(f'[OK] Extraidos {len(data)} registros'))

            # Transformar
            self.stdout.write(self.style.WARNING('Transformando datos...'))
            transformer = CarTransformer()
            df = transformer.transform(data)
            self.stdout.write(self.style.SUCCESS(f'[OK] Transformados {len(df)} registros'))

            # Cargar
            self.stdout.write(self.style.WARNING('Cargando a base de datos...'))
            loader = CarLoader()
            loaded = loader.load(df, scraping_job=job)
            job.total_records_loaded = loaded

            # Completar job
            job.status = 'completed'
            job.completed_at = timezone.now()
            job.log_messages = f'Scraping exitoso: {loaded} registros cargados'
            job.save()

            self.stdout.write(self.style.SUCCESS(f'\n[OK] Scraping completado: {loaded} registros cargados'))
            self.stdout.write(f'  Job ID: {job.id}')
            self.stdout.write(f'  Duracion: {job.duration():.2f} segundos')

        except Exception as e:
            job.status = 'failed'
            job.error_message = str(e)
            job.completed_at = timezone.now()
            job.save()

            self.stdout.write(self.style.ERROR(f'\n[ERROR] Error en scraping: {e}'))
            raise
