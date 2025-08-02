from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from lead.models import Lead
from lead_type.models import LeadType
from datetime import timedelta
import random

fake = Faker('es_ES')

class Command(BaseCommand):
    help = 'Genera leads con distribución temporal realista para testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=500,
            help='Número total de leads a generar (default: 500)'
        )
        parser.add_argument(
            '--days-back',
            type=int,
            default=90,
            help='Días hacia atrás para distribuir los leads (default: 90)'
        )

    def handle(self, *args, **options):
        count = options['count']
        days_back = options['days_back']
        
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
        
        # Estados posibles
        statuses = ['pending', 'contacted', 'process', 'converted', 'discarded']
        
        # Productos de interés (IDs ficticios)
        product_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        self.stdout.write(f"Generando {count} leads distribuidos en {days_back} días...")
        
        # Crear distribución temporal más realista
        date_distribution = self._create_date_distribution(count, days_back)
        
        leads_created = 0
        
        for i, days_ago in enumerate(date_distribution):
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
                
                if (i + 1) % 50 == 0:
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
    
    def _create_date_distribution(self, count, days_back):
        """Crea una distribución temporal más realista"""
        distribution = []
        
        # Distribución por períodos:
        # - Últimos 7 días: 40% de los leads
        # - Últimos 30 días: 30% de los leads  
        # - Últimos 60 días: 20% de los leads
        # - Resto: 10% de los leads
        
        # Últimos 7 días (40%)
        recent_count = int(count * 0.4)
        for _ in range(recent_count):
            days_ago = random.randint(0, 7)
            distribution.append(days_ago)
        
        # Últimos 30 días (30%)
        month_count = int(count * 0.3)
        for _ in range(month_count):
            days_ago = random.randint(8, 30)
            distribution.append(days_ago)
        
        # Últimos 60 días (20%)
        two_months_count = int(count * 0.2)
        for _ in range(two_months_count):
            days_ago = random.randint(31, 60)
            distribution.append(days_ago)
        
        # Resto hasta days_back (10%)
        remaining_count = count - len(distribution)
        for _ in range(remaining_count):
            days_ago = random.randint(61, days_back)
            distribution.append(days_ago)
        
        # Mezclar la distribución
        random.shuffle(distribution)
        return distribution
    
    def _get_realistic_status(self, days_ago):
        """Determina el estado basado en cuánto tiempo ha pasado"""
        if days_ago == 0:  # Hoy
            return random.choices(
                ['pending', 'contacted', 'process'],
                weights=[0.7, 0.2, 0.1]
            )[0]
        elif days_ago <= 1:  # Ayer
            return random.choices(
                ['pending', 'contacted', 'process'],
                weights=[0.5, 0.3, 0.2]
            )[0]
        elif days_ago <= 3:  # Últimos 3 días
            return random.choices(
                ['contacted', 'process', 'converted'],
                weights=[0.4, 0.4, 0.2]
            )[0]
        elif days_ago <= 7:  # Última semana
            return random.choices(
                ['process', 'converted', 'discarded'],
                weights=[0.4, 0.4, 0.2]
            )[0]
        elif days_ago <= 30:  # Último mes
            return random.choices(
                ['converted', 'discarded', 'process'],
                weights=[0.5, 0.3, 0.2]
            )[0]
        else:  # Más de un mes
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
        
        # Distribución temporal
        self.stdout.write("\n📅 Distribución temporal:")
        for days in [0, 1, 3, 7, 30]:
            if days == 0:
                count = Lead.objects.filter(created_at__date=timezone.now().date()).count()
                self.stdout.write(f"   Hoy: {count} leads")
            else:
                start_date = timezone.now().date() - timedelta(days=days)
                count = Lead.objects.filter(created_at__date__gte=start_date).count()
                self.stdout.write(f"   Últimos {days} días: {count} leads") 