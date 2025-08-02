from django.core.management.base import BaseCommand
from lead.models import Lead
from lead_type.models import LeadType

class Command(BaseCommand):
    help = 'Limpia todos los leads falsos generados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--keep-types',
            action='store_true',
            help='Mantener los tipos de leads creados'
        )

    def handle(self, *args, **options):
        keep_types = options['keep_types']
        
        # Contar leads antes de eliminar
        total_leads = Lead.objects.count()
        
        self.stdout.write(f"Eliminando {total_leads} leads...")
        
        # Eliminar todos los leads
        deleted_count = Lead.objects.all().delete()[0]
        
        self.stdout.write(
            self.style.SUCCESS(f"✅ Se eliminaron {deleted_count} leads exitosamente")
        )
        
        # Eliminar tipos de leads si no se especifica mantenerlos
        if not keep_types:
            lead_types = LeadType.objects.all()
            if lead_types.exists():
                types_deleted = lead_types.delete()[0]
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Se eliminaron {types_deleted} tipos de leads")
                )
        
        # Mostrar estado final
        remaining_leads = Lead.objects.count()
        remaining_types = LeadType.objects.count()
        
        self.stdout.write(f"\n📊 Estado final:")
        self.stdout.write(f"   Leads restantes: {remaining_leads}")
        self.stdout.write(f"   Tipos de leads restantes: {remaining_types}") 