from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from lead.models import Lead
from lead_type.models import LeadType
from datetime import timedelta
import random

fake = Faker('es_ES')

class Command(BaseCommand):
    help = 'Genera leads falsos para testing de métricas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Número de leads a generar (default: 100)'
        )
        parser.add_argument(
            '--days-back',
            type=int,
            default=30,
            help='Días hacia atrás para distribuir los leads (default: 30)'
        )

    def handle(self, *args, **options):
        count = options['count']
        days_back = options['days_back']
        
        # Obtener tipos de leads existentes o crear algunos por defecto
        lead_types = list(LeadType.objects.all())
        if not lead_types:
            self.stdout.write("Creando tipos de leads por defecto...")
            default_types = [
                {'name': 'Consulta General', 'description': 'Consultas generales sobre productos'},
                {'name': 'Compra Inmediata', 'description': 'Clientes listos para comprar'},
                {'name': 'Cotización', 'description': 'Solicitudes de cotización'},
                {'name': 'Soporte Técnico', 'description': 'Problemas técnicos'},
                {'name': 'Información Producto', 'description': 'Información específica de productos'}
            ]
            for type_data in default_types:
                lead_type = LeadType.objects.create(**type_data)
                lead_types.append(lead_type)
        
        # Estados posibles
        statuses = ['pending', 'contacted', 'process', 'converted', 'discarded']
        
        # Productos de interés (IDs ficticios)
        product_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        self.stdout.write(f"Generando {count} leads falsos...")
        
        leads_created = 0
        for i in range(count):
            # Generar fecha aleatoria en los últimos días
            days_ago = random.randint(0, days_back)
            created_at = timezone.now() - timedelta(days=days_ago)
            
            # Distribuir estados de manera realista
            if days_ago == 0:  # Hoy
                status_weights = {'pending': 0.7, 'contacted': 0.2, 'process': 0.1}
            elif days_ago <= 3:  # Últimos 3 días
                status_weights = {'pending': 0.4, 'contacted': 0.4, 'process': 0.2}
            elif days_ago <= 7:  # Última semana
                status_weights = {'contacted': 0.3, 'process': 0.4, 'converted': 0.2, 'discarded': 0.1}
            else:  # Más de una semana
                status_weights = {'converted': 0.4, 'discarded': 0.3, 'process': 0.2, 'contacted': 0.1}
            
            # Seleccionar estado basado en pesos
            status = random.choices(
                list(status_weights.keys()),
                weights=list(status_weights.values())
            )[0]
            
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
                
                if (i + 1) % 10 == 0:
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
        total_leads = Lead.objects.count()
        new_today = Lead.objects.filter(created_at__date=timezone.now().date()).count()
        new_week = Lead.objects.filter(created_at__date__gte=timezone.now().date() - timedelta(days=7)).count()
        converted = Lead.objects.filter(status='converted').count()
        conversion_rate = (converted / total_leads * 100) if total_leads > 0 else 0
        
        self.stdout.write("\n📊 Resumen de métricas:")
        self.stdout.write(f"   Total de leads: {total_leads}")
        self.stdout.write(f"   Nuevos hoy: {new_today}")
        self.stdout.write(f"   Nuevos esta semana: {new_week}")
        self.stdout.write(f"   Convertidos: {converted}")
        self.stdout.write(f"   Tasa de conversión: {conversion_rate:.1f}%")
        
        # Distribución por estado
        self.stdout.write("\n📈 Distribución por estado:")
        for status in statuses:
            count = Lead.objects.filter(status=status).count()
            percentage = (count / total_leads * 100) if total_leads > 0 else 0
            self.stdout.write(f"   {status}: {count} ({percentage:.1f}%)")
        
        # Distribución por tipo
        self.stdout.write("\n🏷️ Distribución por tipo:")
        for lead_type in lead_types:
            count = Lead.objects.filter(lead_type=lead_type).count()
            percentage = (count / total_leads * 100) if total_leads > 0 else 0
            self.stdout.write(f"   {lead_type.name}: {count} ({percentage:.1f}%)") 