from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random
from faker import Faker
from page_analytics.models import PageAccess, PageSection, UserJourney, PagePerformance

fake = Faker('es_ES')


class Command(BaseCommand):
    help = 'Genera datos de prueba para page_analytics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Número de registros de PageAccess a generar'
        )
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Número de días hacia atrás para generar datos'
        )

    def handle(self, *args, **options):
        count = options['count']
        days = options['days']
        
        self.stdout.write(f"Generando {count} registros de PageAccess para los últimos {days} días...")
        
        # URLs de ejemplo
        urls = [
            '/',
            '/productos',
            '/productos/categoria/ejercicio',
            '/productos/categoria/nutricion',
            '/productos/detalle/123',
            '/carrito',
            '/checkout',
            '/perfil',
            '/leads',
            '/leads/buscar',
            '/leads/dashboard',
            '/ayuda',
            '/contacto',
            '/sobre-nosotros',
            '/blog',
            '/blog/articulo-1',
            '/blog/articulo-2',
        ]
        
        # Secciones de ejemplo
        sections = [
            'header',
            'hero',
            'productos-destacados',
            'categorias',
            'testimonios',
            'footer',
            'sidebar',
            'navegacion',
            'buscador',
            'filtros',
            'paginacion',
            'formulario-contacto',
            'mapa',
            'redes-sociales',
        ]
        
        # Dispositivos y navegadores
        devices = ['mobile', 'desktop', 'tablet']
        browsers = ['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera']
        os_list = ['Windows', 'macOS', 'Linux', 'iOS', 'Android']
        
        # Generar secciones de página
        self.stdout.write("Creando secciones de página...")
        for i, section in enumerate(sections):
            PageSection.objects.get_or_create(
                name=section,
                defaults={
                    'description': f'Sección {section}',
                    'page_url_pattern': f'*{section}*',
                    'section_selector': f'.{section}',
                    'priority': i,
                    'is_active': True
                }
            )
        
        # Generar datos de PageAccess
        total_created = 0
        start_date = timezone.now() - timedelta(days=days)
        
        for i in range(count):
            # Generar fecha aleatoria en el rango
            days_back = random.randint(0, days)
            hours_back = random.randint(0, 23)
            minutes_back = random.randint(0, 59)
            created_at = start_date + timedelta(
                days=days_back,
                hours=hours_back,
                minutes=minutes_back
            )
            
            # Crear datos básicos
            page_data = {
                'page_url': fake.uri_path(),
                'page_title': fake.sentence(),
                'section': fake.random_element(elements=sections),
                'user_id': fake.uuid4() if fake.boolean() else '',
                'session_id': f"session_{fake.unix_time()}_{fake.pystr()}",
                'user_agent': fake.user_agent(),
                'device_type': fake.random_element(elements=['desktop', 'mobile', 'tablet']),
                'browser': fake.random_element(elements=['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera']),
                'os': fake.random_element(elements=['Windows', 'macOS', 'Linux', 'iOS', 'Android']),
                'ip_address': fake.ipv4() if fake.boolean() else None,
                'country': fake.country(),
                'city': fake.city(),
                'time_on_page': fake.random_int(min=0, max=600),
                'scroll_depth': fake.random_int(min=0, max=100),
                'interactions': fake.random_int(min=0, max=20),
                'referrer': fake.url() if fake.boolean() else '',
                'utm_source': fake.random_element(elements=['google', 'facebook', 'twitter', 'email', '']),
                'utm_medium': fake.random_element(elements=['cpc', 'social', 'email', 'organic', '']),
                'utm_campaign': fake.random_element(elements=['summer_sale', 'new_products', 'brand_awareness', '']),
                'metadata': {
                    'language': fake.language_code(),
                    'timezone': fake.timezone(),
                    'screen_resolution': f"{fake.random_int(min=800, max=2560)}x{fake.random_int(min=600, max=1440)}"
                }
            }
            
            # Agregar eventos de ecommerce aleatorios
            if fake.boolean(chance_of_getting_true=30):  # 30% de probabilidad
                ecommerce_events = ['product_view', 'add_to_cart', 'begin_checkout', 'purchase']
                event_type = fake.random_element(elements=ecommerce_events)
                
                page_data['metadata']['event_type'] = event_type
                page_data['metadata']['ecommerce_data'] = {
                    'product_id': fake.uuid4() if event_type in ['product_view', 'add_to_cart'] else None,
                    'product_name': fake.word() if event_type in ['product_view', 'add_to_cart'] else None,
                    'quantity': fake.random_int(min=1, max=5) if event_type == 'add_to_cart' else None,
                    'price': fake.random_int(min=100, max=5000) if event_type in ['product_view', 'add_to_cart'] else None,
                    'order_id': fake.uuid4() if event_type == 'purchase' else None,
                    'total': fake.random_int(min=500, max=10000) if event_type == 'purchase' else None
                }
            
            # Crear el registro
            PageAccess.objects.create(**page_data)
            
            total_created += 1
            
            if total_created % 10 == 0:
                self.stdout.write(f"✅ Creados {total_created} registros...")
        
        # Generar UserJourney
        self.stdout.write("Generando UserJourney...")
        journey_count = count // 10  # 1 journey por cada 10 page_access
        
        for i in range(journey_count):
            # Generar journey con múltiples páginas
            pages_in_journey = random.randint(2, 8)
            journey_pages = random.sample(urls, min(pages_in_journey, len(urls)))
            
            journey_start = start_date + timedelta(
                days=random.randint(0, days),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            journey_data = {
                'session_id': fake.uuid4(),
                'user_id': fake.uuid4() if random.random() > 0.5 else '',
                'entry_page': journey_pages[0],
                'exit_page': journey_pages[-1],
                'pages_visited': journey_pages,
                'total_pages': len(journey_pages),
                'total_time': random.randint(60, 1800),
                'conversion_goal': random.choice(['', 'purchase', 'lead', 'newsletter']),
                'started_at': journey_start,
                'ended_at': journey_start + timedelta(minutes=random.randint(5, 30))
            }
            
            UserJourney.objects.create(**journey_data)
        
        # Generar PagePerformance
        self.stdout.write("Generando PagePerformance...")
        end_date = timezone.now().date()
        start_date_perf = end_date - timedelta(days=days)
        
        for i in range(days):
            current_date = start_date_perf + timedelta(days=i)
            
            for url in urls[:5]:  # Solo las primeras 5 URLs para performance
                performance_data = {
                    'page_url': url,
                    'date': current_date,
                    'load_time_avg': random.uniform(500, 3000),
                    'load_time_p75': random.uniform(800, 4000),
                    'load_time_p95': random.uniform(1200, 6000),
                    'bounce_rate': random.uniform(20, 80),
                    'exit_rate': random.uniform(10, 50),
                    'avg_session_duration': random.uniform(60, 600),
                    'page_views': random.randint(10, 1000),
                    'unique_visitors': random.randint(5, 500),
                    'new_visitors': random.randint(2, 200),
                    'conversions': random.randint(0, 50),
                    'conversion_rate': random.uniform(0, 10)
                }
                
                PagePerformance.objects.get_or_create(
                    page_url=url,
                    date=current_date,
                    defaults=performance_data
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Se generaron {total_created} registros de PageAccess, "
                f"{journey_count} UserJourney y métricas de rendimiento para {days} días"
            )
        ) 