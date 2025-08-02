from django.core.management.base import BaseCommand
from page_analytics.models import PageAccess, PageSection, UserJourney, PagePerformance


class Command(BaseCommand):
    help = 'Limpia todos los datos de page_analytics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sections',
            action='store_true',
            help='También eliminar las secciones de página'
        )

    def handle(self, *args, **options):
        self.stdout.write("Limpiando datos de page_analytics...")
        
        # Contar registros antes de eliminar
        page_access_count = PageAccess.objects.count()
        user_journey_count = UserJourney.objects.count()
        page_performance_count = PagePerformance.objects.count()
        page_section_count = PageSection.objects.count()
        
        # Eliminar datos
        PageAccess.objects.all().delete()
        UserJourney.objects.all().delete()
        PagePerformance.objects.all().delete()
        
        if options['sections']:
            PageSection.objects.all().delete()
            self.stdout.write(f"✅ Eliminadas {page_section_count} secciones de página")
        
        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Se eliminaron {page_access_count} registros de PageAccess, "
                f"{user_journey_count} UserJourney y {page_performance_count} PagePerformance"
            )
        ) 