from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from lead.models import Lead
from lead_type.models import LeadType
from datetime import timedelta
import random

fake = Faker('es_ES')

class Command(BaseCommand):
    help = 'Genera datos de prueba para verificar tendencias'

    def handle(self, *args, **options):
        # Limpiar datos existentes
        Lead.objects.all().delete()
        LeadType.objects.all().delete()
        
        # Crear tipos de leads
        lead_types = []
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
        
        # Productos de interés
        product_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        self.stdout.write("Generando datos de prueba para tendencias...")
        
        # Generar leads distribuidos en los últimos 7 días
        today = timezone.now().date()
        
        # Distribución de leads por día (más realista)
        daily_distribution = {
            0: 15,   # Hoy: 15 leads
            1: 12,   # Ayer: 12 leads
            2: 8,    # Hace 2 días: 8 leads
            3: 10,   # Hace 3 días: 10 leads
            4: 6,    # Hace 4 días: 6 leads
            5: 4,    # Hace 5 días: 4 leads
            6: 3,    # Hace 6 días: 3 leads
        }
        
        total_created = 0
        
        for days_ago, count in daily_distribution.items():
            target_date = today - timedelta(days=days_ago)
            
            for i in range(count):
                # Crear datetime específico para este día
                created_at = timezone.make_aware(
                    timezone.datetime.combine(target_date, timezone.datetime.min.time())
                )
                
                # Distribuir estados según la fecha
                if days_ago == 0:  # Hoy
                    status = random.choices(['pending', 'contacted'], weights=[0.7, 0.3])[0]
                elif days_ago == 1:  # Ayer
                    status = random.choices(['pending', 'contacted', 'process'], weights=[0.4, 0.4, 0.2])[0]
                elif days_ago <= 3:  # Últimos 3 días
                    status = random.choices(['contacted', 'process', 'converted'], weights=[0.3, 0.4, 0.3])[0]
                else:  # Más de 3 días
                    status = random.choices(['converted', 'discarded'], weights=[0.6, 0.4])[0]
                
                # Crear lead sin fecha específica
                lead_data = {
                    'name': fake.name(),
                    'email': fake.email(),
                    'phone_number': fake.phone_number(),
                    'lead_type': random.choice(lead_types),
                    'status': status,
                    'tryet': random.randint(1, 5),
                    'products_interest_ids': random.sample(product_ids, random.randint(1, 3)),
                    'store_id': random.randint(1, 10)
                }
                
                # Crear el lead y luego actualizar la fecha
                lead = Lead.objects.create(**lead_data)
                lead.created_at = created_at
                lead.save(update_fields=['created_at'])
                total_created += 1
        
        self.stdout.write(
            self.style.SUCCESS(f"✅ Se crearon {total_created} leads distribuidos en 7 días")
        )
        
        # Mostrar resumen por día
        self.stdout.write("\n📅 Distribución por día:")
        for days_ago in range(7):
            target_date = today - timedelta(days=days_ago)
            count = Lead.objects.filter(created_at__date=target_date).count()
            converted = Lead.objects.filter(created_at__date=target_date, status='converted').count()
            
            if days_ago == 0:
                day_label = "Hoy"
            elif days_ago == 1:
                day_label = "Ayer"
            else:
                day_label = f"Hace {days_ago} días"
            
            self.stdout.write(f"   {day_label} ({target_date}): {count} leads, {converted} convertidos")
        
        # Mostrar totales
        total_leads = Lead.objects.count()
        total_converted = Lead.objects.filter(status='converted').count()
        conversion_rate = (total_converted / total_leads * 100) if total_leads > 0 else 0
        
        self.stdout.write(f"\n📊 Totales:")
        self.stdout.write(f"   Total leads: {total_leads}")
        self.stdout.write(f"   Convertidos: {total_converted}")
        self.stdout.write(f"   Tasa de conversión: {conversion_rate:.1f}%") 