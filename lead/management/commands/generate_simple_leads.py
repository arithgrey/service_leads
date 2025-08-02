from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from lead.models import Lead
from lead_type.models import LeadType
from datetime import timedelta
import random

fake = Faker('es_ES')

class Command(BaseCommand):
    help = 'Genera leads simples con fechas distribuidas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Número total de leads a generar (default: 100)'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Obtener tipos de leads existentes o crear algunos por defecto
        lead_types = list(LeadType.objects.all())
        if not lead_types:
            self.stdout.write("Creando tipos de leads por defecto...")
            default_types = [
                {'name': 'Consulta General'},
                {'name': 'Compra Inmediata'},
                {'name': 'Cotización'},
                {'name': 'Soporte Técnico'},
                {'name': 'Información Producto'}
            ]
            for type_data in default_types:
                lead_type = LeadType.objects.create(**type_data)
                lead_types.append(lead_type)
        
        # Productos de interés (IDs ficticios)
        product_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        self.stdout.write(f"Generando {count} leads con fechas distribuidas...")
        
        leads_created = 0
        
        # Generar leads con fechas distribuidas
        for i in range(count):
            # Distribuir días de manera simple
            if i < count * 0.3:  # 30% hoy
                days_ago = 0
            elif i < count * 0.5:  # 20% ayer
                days_ago = 1
            elif i < count * 0.7:  # 20% hace 3 días
                days_ago = 3
            elif i < count * 0.85:  # 15% hace 7 días
                days_ago = 7
            elif i < count * 0.95:  # 10% hace 15 días
                days_ago = 15
            else:  # 5% hace 30 días
                days_ago = 30
            
            # Crear fecha específica
            created_at = timezone.now() - timedelta(days=days_ago)
            
            # Distribuir estados de manera realista según la fecha
            status = self._get_realistic_status(days_ago)
            
            # Generar datos del lead
            lead_data = {
                'name': fake.name(),
                'email': fake.email(),
                'phone_number': fake.phone_number(),
                'lead_type': random.choice(lead_types),
                'created_at': created_at,
                'status': status,
                'tryet': random.randint(1, 5),
                'products_interest_ids': random.sample(product_ids, random.randint(1, 3)),
                'store_id': random.randint(1, 10)
            }
            
            try:
                Lead.objects.create(**lead_data)
                leads_created += 1
                
                if (i + 1) % 20 == 0:
                    self.stdout.write(f"Progreso: {i + 1}/{count} leads creados")
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error creando lead {i + 1}: {str(e)}")
                )
        
        # Mostrar estadísticas finales
        self.stdout.write(
            self.style.SUCCESS(f"✅ Se crearon {leads_created} leads exitosamente")
        )
        
        # Mostrar resumen de métricas
        self._show_metrics_summary()
    
    def _get_realistic_status(self, days_ago):
        """Determina el estado basado en cuánto tiempo ha pasado"""
        if days_ago == 0:  # Hoy
            return random.choices(
                ['pending', 'contacted', 'process'],
                weights=[0.7, 0.2, 0.1]
            )[0]
        elif days_ago == 1:  # Ayer
            return random.choices(
                ['pending', 'contacted', 'process'],
                weights=[0.5, 0.3, 0.2]
            )[0]
        elif days_ago == 3:  # Hace 3 días
            return random.choices(
                ['contacted', 'process', 'converted'],
                weights=[0.4, 0.4, 0.2]
            )[0]
        elif days_ago == 7:  # Hace 7 días
            return random.choices(
                ['process', 'converted', 'discarded'],
                weights=[0.4, 0.4, 0.2]
            )[0]
        elif days_ago == 15:  # Hace 15 días
            return random.choices(
                ['converted', 'discarded', 'process'],
                weights=[0.5, 0.3, 0.2]
            )[0]
        else:  # Hace 30 días
            return random.choices(
                ['converted', 'discarded'],
                weights=[0.6, 0.4]
            )[0]
    
    def _show_metrics_summary(self):
        """Muestra un resumen de las métricas generadas"""
        from django.utils import timezone
        from datetime import timedelta
        
        total_leads = Lead.objects.count()
        new_today = Lead.objects.filter(created_at__date=timezone.now().date()).count()
        new_week = Lead.objects.filter(created_at__date__gte=timezone.now().date() - timedelta(days=7)).count()
        new_month = Lead.objects.filter(created_at__date__gte=timezone.now().date() - timedelta(days=30)).count()
        converted = Lead.objects.filter(status='converted').count()
        conversion_rate = (converted / total_leads * 100) if total_leads > 0 else 0
        
        self.stdout.write("\n📊 Resumen de métricas:")
        self.stdout.write(f"   Total de leads: {total_leads}")
        self.stdout.write(f"   Nuevos hoy: {new_today}")
        self.stdout.write(f"   Nuevos esta semana: {new_week}")
        self.stdout.write(f"   Nuevos este mes: {new_month}")
        self.stdout.write(f"   Convertidos: {converted}")
        self.stdout.write(f"   Tasa de conversión: {conversion_rate:.1f}%")
        
        # Distribución por estado
        statuses = ['pending', 'contacted', 'process', 'converted', 'discarded']
        self.stdout.write("\n📈 Distribución por estado:")
        for status in statuses:
            count = Lead.objects.filter(status=status).count()
            percentage = (count / total_leads * 100) if total_leads > 0 else 0
            self.stdout.write(f"   {status}: {count} ({percentage:.1f}%)")
        
        # Distribución por tipo
        lead_types = LeadType.objects.all()
        self.stdout.write("\n🏷️ Distribución por tipo:")
        for lead_type in lead_types:
            count = Lead.objects.filter(lead_type=lead_type).count()
            percentage = (count / total_leads * 100) if total_leads > 0 else 0
            self.stdout.write(f"   {lead_type.name}: {count} ({percentage:.1f}%)")
        
        # Distribución temporal específica
        self.stdout.write("\n📅 Distribución temporal:")
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        three_days_ago = today - timedelta(days=3)
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        self.stdout.write(f"   Hoy ({today}): {Lead.objects.filter(created_at__date=today).count()}")
        self.stdout.write(f"   Ayer ({yesterday}): {Lead.objects.filter(created_at__date=yesterday).count()}")
        self.stdout.write(f"   Hace 3 días ({three_days_ago}): {Lead.objects.filter(created_at__date=three_days_ago).count()}")
        self.stdout.write(f"   Hace 7 días ({week_ago}): {Lead.objects.filter(created_at__date=week_ago).count()}")
        self.stdout.write(f"   Hace 30 días ({month_ago}): {Lead.objects.filter(created_at__date=month_ago).count()}") 