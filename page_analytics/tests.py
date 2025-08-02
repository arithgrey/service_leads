from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta
from .models import PageAccess, PageSection, UserJourney, PagePerformance


class PageAccessModelTest(TestCase):
    """Tests para el modelo PageAccess"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.page_access_data = {
            'page_url': '/productos',
            'page_title': 'Productos - Tienda',
            'section': 'productos-destacados',
            'user_id': 'user123',
            'session_id': 'session456',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'device_type': 'desktop',
            'browser': 'Chrome',
            'os': 'Windows',
            'ip_address': '192.168.1.1',
            'country': 'México',
            'city': 'Ciudad de México',
            'time_on_page': 120,
            'scroll_depth': 75,
            'interactions': 5,
            'referrer': 'https://google.com',
            'utm_source': 'google',
            'utm_medium': 'cpc',
            'utm_campaign': 'summer_sale',
            'metadata': {
                'screen_resolution': '1920x1080',
                'language': 'es',
                'timezone': 'America/Mexico_City'
            }
        }
    
    def test_create_page_access(self):
        """Test: Crear un registro de PageAccess"""
        page_access = PageAccess.objects.create(**self.page_access_data)
        
        self.assertEqual(page_access.page_url, '/productos')
        self.assertEqual(page_access.device_type, 'desktop')
        self.assertEqual(page_access.time_on_page, 120)
        self.assertEqual(page_access.scroll_depth, 75)
        self.assertIsNotNone(page_access.created_at)
        self.assertIsNotNone(page_access.updated_at)
    
    def test_page_access_str_representation(self):
        """Test: Representación string del modelo"""
        page_access = PageAccess.objects.create(**self.page_access_data)
        expected_str = f"/productos - {page_access.created_at.strftime('%Y-%m-%d %H:%M')}"
        self.assertEqual(str(page_access), expected_str)
    
    def test_page_access_ordering(self):
        """Test: Ordenamiento por fecha de creación (más reciente primero)"""
        # Crear dos registros con fechas diferentes
        old_access = PageAccess.objects.create(**self.page_access_data)
        old_access.created_at = timezone.now() - timedelta(hours=1)
        old_access.save()
        
        new_access = PageAccess.objects.create(**self.page_access_data)
        new_access.created_at = timezone.now()
        new_access.save()
        
        # Verificar ordenamiento
        accesses = PageAccess.objects.all()
        self.assertEqual(accesses[0], new_access)
        self.assertEqual(accesses[1], old_access)
    
    def test_page_access_metadata_json(self):
        """Test: Campo metadata como JSON"""
        page_access = PageAccess.objects.create(**self.page_access_data)
        
        self.assertIsInstance(page_access.metadata, dict)
        self.assertEqual(page_access.metadata['screen_resolution'], '1920x1080')
        self.assertEqual(page_access.metadata['language'], 'es')


class PageSectionModelTest(TestCase):
    """Tests para el modelo PageSection"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.section_data = {
            'name': 'header',
            'description': 'Sección de navegación principal',
            'page_url_pattern': '*header*',
            'section_selector': '.header',
            'total_views': 100,
            'avg_time_on_section': 30.5,
            'engagement_rate': 85.2,
            'is_active': True,
            'priority': 1
        }
    
    def test_create_page_section(self):
        """Test: Crear una sección de página"""
        section = PageSection.objects.create(**self.section_data)
        
        self.assertEqual(section.name, 'header')
        self.assertEqual(section.is_active, True)
        self.assertEqual(section.priority, 1)
        self.assertIsNotNone(section.created_at)
    
    def test_page_section_str_representation(self):
        """Test: Representación string del modelo"""
        section = PageSection.objects.create(**self.section_data)
        self.assertEqual(str(section), 'header')
    
    def test_page_section_ordering(self):
        """Test: Ordenamiento por prioridad y nombre"""
        # Crear secciones con diferentes prioridades
        low_priority = PageSection.objects.create(
            name='footer',
            priority=3,
            page_url_pattern='*footer*'
        )
        
        high_priority = PageSection.objects.create(
            name='hero',
            priority=1,
            page_url_pattern='*hero*'
        )
        
        medium_priority = PageSection.objects.create(
            name='sidebar',
            priority=2,
            page_url_pattern='*sidebar*'
        )
        
        # Verificar ordenamiento
        sections = PageSection.objects.all()
        self.assertEqual(sections[0], high_priority)  # priority=1
        self.assertEqual(sections[1], medium_priority)  # priority=2
        self.assertEqual(sections[2], low_priority)  # priority=3


class UserJourneyModelTest(TestCase):
    """Tests para el modelo UserJourney"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.journey_data = {
            'session_id': 'session123',
            'user_id': 'user456',
            'entry_page': '/',
            'exit_page': '/checkout',
            'pages_visited': ['/', '/productos', '/carrito', '/checkout'],
            'total_pages': 4,
            'total_time': 600,
            'conversion_goal': 'purchase'
        }
    
    def test_create_user_journey(self):
        """Test: Crear un user journey"""
        journey = UserJourney.objects.create(**self.journey_data)
        
        self.assertEqual(journey.session_id, 'session123')
        self.assertEqual(journey.entry_page, '/')
        self.assertEqual(journey.exit_page, '/checkout')
        self.assertEqual(journey.total_pages, 4)
        self.assertEqual(journey.total_time, 600)
        self.assertEqual(journey.conversion_goal, 'purchase')
        self.assertIsNotNone(journey.started_at)
        self.assertIsNone(journey.ended_at)
    
    def test_user_journey_str_representation(self):
        """Test: Representación string del modelo"""
        journey = UserJourney.objects.create(**self.journey_data)
        expected_str = f"Journey session123 - 4 páginas"
        self.assertEqual(str(journey), expected_str)
    
    def test_user_journey_pages_visited_json(self):
        """Test: Campo pages_visited como JSON"""
        journey = UserJourney.objects.create(**self.journey_data)
        
        self.assertIsInstance(journey.pages_visited, list)
        self.assertEqual(len(journey.pages_visited), 4)
        self.assertEqual(journey.pages_visited[0], '/')
        self.assertEqual(journey.pages_visited[-1], '/checkout')
    
    def test_user_journey_ordering(self):
        """Test: Ordenamiento por fecha de inicio (más reciente primero)"""
        # Crear journeys con fechas diferentes
        old_journey = UserJourney.objects.create(**self.journey_data)
        old_journey.started_at = timezone.now() - timedelta(hours=1)
        old_journey.save()
        
        new_journey = UserJourney.objects.create(**self.journey_data)
        new_journey.started_at = timezone.now()
        new_journey.save()
        
        # Verificar ordenamiento
        journeys = UserJourney.objects.all()
        self.assertEqual(journeys[0], new_journey)
        self.assertEqual(journeys[1], old_journey)


class PagePerformanceModelTest(TestCase):
    """Tests para el modelo PagePerformance"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.performance_data = {
            'page_url': '/productos',
            'date': timezone.now().date(),
            'load_time_avg': 1500.5,
            'load_time_p75': 2000.0,
            'load_time_p95': 3500.0,
            'bounce_rate': 25.5,
            'exit_rate': 15.2,
            'avg_session_duration': 180.0,
            'page_views': 1000,
            'unique_visitors': 450,
            'new_visitors': 200,
            'conversions': 25,
            'conversion_rate': 5.5
        }
    
    def test_create_page_performance(self):
        """Test: Crear métricas de rendimiento"""
        performance = PagePerformance.objects.create(**self.performance_data)
        
        self.assertEqual(performance.page_url, '/productos')
        self.assertEqual(performance.load_time_avg, 1500.5)
        self.assertEqual(performance.bounce_rate, 25.5)
        self.assertEqual(performance.page_views, 1000)
        self.assertEqual(performance.conversion_rate, 5.5)
    
    def test_page_performance_str_representation(self):
        """Test: Representación string del modelo"""
        performance = PagePerformance.objects.create(**self.performance_data)
        expected_str = f"/productos - {performance.date}"
        self.assertEqual(str(performance), expected_str)
    
    def test_page_performance_unique_constraint(self):
        """Test: Restricción única de page_url y date"""
        # Crear primer registro
        PagePerformance.objects.create(**self.performance_data)
        
        # Intentar crear otro con la misma URL y fecha debería fallar
        with self.assertRaises(Exception):
            PagePerformance.objects.create(**self.performance_data)
    
    def test_page_performance_ordering(self):
        """Test: Ordenamiento por fecha y URL"""
        # Crear registros con diferentes fechas
        old_date = timezone.now().date() - timedelta(days=1)
        new_date = timezone.now().date()
        
        old_performance = PagePerformance.objects.create(
            page_url='/old-page',
            date=old_date,
            load_time_avg=1000.0,
            page_views=100
        )
        
        new_performance = PagePerformance.objects.create(
            page_url='/new-page',
            date=new_date,
            load_time_avg=2000.0,
            page_views=200
        )
        
        # Verificar ordenamiento
        performances = PagePerformance.objects.all()
        self.assertEqual(performances[0], new_performance)  # fecha más reciente
        self.assertEqual(performances[1], old_performance)  # fecha más antigua 