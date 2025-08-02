from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils import timezone
from datetime import datetime, timedelta
from io import StringIO
from .models import PageAccess, PageSection, UserJourney, PagePerformance


class GeneratePageAnalyticsDataCommandTest(TestCase):
    """Tests para el comando generate_page_analytics_data"""
    
    def test_generate_page_analytics_data_default(self):
        """Test: Generar datos con parámetros por defecto"""
        out = StringIO()
        
        # Verificar que no hay datos al inicio
        self.assertEqual(PageAccess.objects.count(), 0)
        self.assertEqual(PageSection.objects.count(), 0)
        self.assertEqual(UserJourney.objects.count(), 0)
        self.assertEqual(PagePerformance.objects.count(), 0)
        
        # Ejecutar comando
        call_command('generate_page_analytics_data', stdout=out)
        
        # Verificar que se crearon datos
        self.assertGreater(PageAccess.objects.count(), 0)
        self.assertGreater(PageSection.objects.count(), 0)
        self.assertGreater(UserJourney.objects.count(), 0)
        self.assertGreater(PagePerformance.objects.count(), 0)
        
        # Verificar output
        output = out.getvalue()
        self.assertIn('Generando 100 registros', output)
        self.assertIn('Se generaron', output)
    
    def test_generate_page_analytics_data_custom_count(self):
        """Test: Generar datos con count personalizado"""
        out = StringIO()
        
        # Ejecutar comando con count personalizado
        call_command('generate_page_analytics_data', count=50, stdout=out)
        
        # Verificar que se crearon 50 registros de PageAccess
        self.assertEqual(PageAccess.objects.count(), 50)
        
        # Verificar output
        output = out.getvalue()
        self.assertIn('Generando 50 registros', output)
    
    def test_generate_page_analytics_data_custom_days(self):
        """Test: Generar datos con días personalizados"""
        out = StringIO()
        
        # Ejecutar comando con días personalizados
        call_command('generate_page_analytics_data', days=7, stdout=out)
        
        # Verificar que se crearon datos
        self.assertGreater(PageAccess.objects.count(), 0)
        
        # Verificar que las fechas están en el rango correcto
        start_date = timezone.now() - timedelta(days=7)
        page_accesses = PageAccess.objects.all()
        
        for access in page_accesses:
            self.assertGreaterEqual(access.created_at, start_date)
            self.assertLessEqual(access.created_at, timezone.now())
    
    def test_generate_page_analytics_data_sections_created(self):
        """Test: Verificar que se crean las secciones correctamente"""
        out = StringIO()
        
        # Ejecutar comando
        call_command('generate_page_analytics_data', stdout=out)
        
        # Verificar que se crearon secciones
        sections = PageSection.objects.all()
        self.assertGreater(len(sections), 0)
        
        # Verificar que las secciones tienen los campos correctos
        for section in sections:
            self.assertIsNotNone(section.name)
            self.assertIsNotNone(section.page_url_pattern)
            self.assertIsNotNone(section.section_selector)
            self.assertIsNotNone(section.is_active)
            self.assertIsNotNone(section.priority)
    
    def test_generate_page_analytics_data_user_journeys_created(self):
        """Test: Verificar que se crean user journeys correctamente"""
        out = StringIO()
        
        # Ejecutar comando
        call_command('generate_page_analytics_data', stdout=out)
        
        # Verificar que se crearon user journeys
        journeys = UserJourney.objects.all()
        self.assertGreater(len(journeys), 0)
        
        # Verificar que los journeys tienen los campos correctos
        for journey in journeys:
            self.assertIsNotNone(journey.session_id)
            self.assertIsNotNone(journey.entry_page)
            self.assertIsNotNone(journey.exit_page)
            self.assertIsInstance(journey.pages_visited, list)
            self.assertGreater(journey.total_pages, 0)
            self.assertGreater(journey.total_time, 0)
    
    def test_generate_page_analytics_data_performance_created(self):
        """Test: Verificar que se crean métricas de rendimiento correctamente"""
        out = StringIO()
        
        # Ejecutar comando
        call_command('generate_page_analytics_data', stdout=out)
        
        # Verificar que se crearon métricas de rendimiento
        performances = PagePerformance.objects.all()
        self.assertGreater(len(performances), 0)
        
        # Verificar que las métricas tienen los campos correctos
        for performance in performances:
            self.assertIsNotNone(performance.page_url)
            self.assertIsNotNone(performance.date)
            self.assertGreaterEqual(performance.load_time_avg, 0)
            self.assertGreaterEqual(performance.bounce_rate, 0)
            self.assertGreaterEqual(performance.page_views, 0)
            self.assertGreaterEqual(performance.unique_visitors, 0)


class ClearPageAnalyticsDataCommandTest(TestCase):
    """Tests para el comando clear_page_analytics_data"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear datos de prueba
        self.page_access = PageAccess.objects.create(
            page_url='/test',
            session_id='test-session',
            device_type='desktop'
        )
        
        self.section = PageSection.objects.create(
            name='test-section',
            page_url_pattern='*test*'
        )
        
        self.journey = UserJourney.objects.create(
            session_id='test-journey',
            entry_page='/',
            exit_page='/test',
            pages_visited=['/', '/test'],
            total_pages=2,
            total_time=60
        )
        
        self.performance = PagePerformance.objects.create(
            page_url='/test',
            date=timezone.now().date(),
            page_views=100
        )
    
    def test_clear_page_analytics_data_basic(self):
        """Test: Limpiar datos básicos"""
        out = StringIO()
        
        # Verificar que hay datos al inicio
        self.assertEqual(PageAccess.objects.count(), 1)
        self.assertEqual(PageSection.objects.count(), 1)
        self.assertEqual(UserJourney.objects.count(), 1)
        self.assertEqual(PagePerformance.objects.count(), 1)
        
        # Ejecutar comando
        call_command('clear_page_analytics_data', stdout=out)
        
        # Verificar que se eliminaron los datos
        self.assertEqual(PageAccess.objects.count(), 0)
        self.assertEqual(UserJourney.objects.count(), 0)
        self.assertEqual(PagePerformance.objects.count(), 0)
        
        # Verificar que las secciones NO se eliminaron (por defecto)
        self.assertEqual(PageSection.objects.count(), 1)
        
        # Verificar output
        output = out.getvalue()
        self.assertIn('Limpiando datos de page_analytics', output)
        self.assertIn('Se eliminaron 1 registros de PageAccess', output)
    
    def test_clear_page_analytics_data_with_sections(self):
        """Test: Limpiar datos incluyendo secciones"""
        out = StringIO()
        
        # Verificar que hay datos al inicio
        self.assertEqual(PageSection.objects.count(), 1)
        
        # Ejecutar comando con --sections
        call_command('clear_page_analytics_data', sections=True, stdout=out)
        
        # Verificar que se eliminaron todos los datos incluyendo secciones
        self.assertEqual(PageAccess.objects.count(), 0)
        self.assertEqual(PageSection.objects.count(), 0)
        self.assertEqual(UserJourney.objects.count(), 0)
        self.assertEqual(PagePerformance.objects.count(), 0)
        
        # Verificar output
        output = out.getvalue()
        self.assertIn('Eliminadas 1 secciones de página', output)
    
    def test_clear_page_analytics_data_empty_database(self):
        """Test: Limpiar base de datos vacía"""
        out = StringIO()
        
        # Eliminar todos los datos primero
        PageAccess.objects.all().delete()
        PageSection.objects.all().delete()
        UserJourney.objects.all().delete()
        PagePerformance.objects.all().delete()
        
        # Verificar que no hay datos
        self.assertEqual(PageAccess.objects.count(), 0)
        self.assertEqual(PageSection.objects.count(), 0)
        self.assertEqual(UserJourney.objects.count(), 0)
        self.assertEqual(PagePerformance.objects.count(), 0)
        
        # Ejecutar comando
        call_command('clear_page_analytics_data', stdout=out)
        
        # Verificar que no hay errores
        output = out.getvalue()
        self.assertIn('Se eliminaron 0 registros de PageAccess', output)
    
    def test_clear_page_analytics_data_multiple_records(self):
        """Test: Limpiar múltiples registros"""
        out = StringIO()
        
        # Crear múltiples registros
        for i in range(5):
            PageAccess.objects.create(
                page_url=f'/test-{i}',
                session_id=f'test-session-{i}',
                device_type='desktop'
            )
        
        # Verificar que hay múltiples registros
        self.assertEqual(PageAccess.objects.count(), 6)  # 1 del setUp + 5 nuevos
        
        # Ejecutar comando
        call_command('clear_page_analytics_data', stdout=out)
        
        # Verificar que se eliminaron todos
        self.assertEqual(PageAccess.objects.count(), 0)
        
        # Verificar output
        output = out.getvalue()
        self.assertIn('Se eliminaron 6 registros de PageAccess', output)


class CommandIntegrationTest(TestCase):
    """Tests de integración para comandos"""
    
    def test_generate_and_clear_cycle(self):
        """Test: Ciclo completo de generar y limpiar datos"""
        out = StringIO()
        
        # Paso 1: Generar datos
        call_command('generate_page_analytics_data', count=10, stdout=out)
        
        # Verificar que se crearon datos
        self.assertGreater(PageAccess.objects.count(), 0)
        self.assertGreater(PageSection.objects.count(), 0)
        self.assertGreater(UserJourney.objects.count(), 0)
        self.assertGreater(PagePerformance.objects.count(), 0)
        
        # Paso 2: Limpiar datos
        call_command('clear_page_analytics_data', stdout=out)
        
        # Verificar que se eliminaron los datos
        self.assertEqual(PageAccess.objects.count(), 0)
        self.assertEqual(UserJourney.objects.count(), 0)
        self.assertEqual(PagePerformance.objects.count(), 0)
        
        # Verificar que las secciones permanecen (por defecto)
        self.assertGreater(PageSection.objects.count(), 0)
        
        # Paso 3: Limpiar incluyendo secciones
        call_command('clear_page_analytics_data', sections=True, stdout=out)
        
        # Verificar que se eliminaron todos los datos
        self.assertEqual(PageSection.objects.count(), 0)
    
    def test_data_quality_after_generation(self):
        """Test: Calidad de datos después de la generación"""
        out = StringIO()
        
        # Generar datos
        call_command('generate_page_analytics_data', count=20, days=5, stdout=out)
        
        # Verificar calidad de datos de PageAccess
        page_accesses = PageAccess.objects.all()
        for access in page_accesses:
            # Verificar campos requeridos
            self.assertIsNotNone(access.page_url)
            self.assertIsNotNone(access.session_id)
            self.assertIsNotNone(access.device_type)
            
            # Verificar rangos válidos
            self.assertGreaterEqual(access.time_on_page, 0)
            self.assertGreaterEqual(access.scroll_depth, 0)
            self.assertLessEqual(access.scroll_depth, 100)
            self.assertGreaterEqual(access.interactions, 0)
            
            # Verificar fechas
            self.assertGreaterEqual(access.created_at, timezone.now() - timedelta(days=5))
            self.assertLessEqual(access.created_at, timezone.now())
        
        # Verificar calidad de datos de UserJourney
        journeys = UserJourney.objects.all()
        for journey in journeys:
            # Verificar campos requeridos
            self.assertIsNotNone(journey.session_id)
            self.assertIsNotNone(journey.entry_page)
            self.assertIsNotNone(journey.exit_page)
            
            # Verificar datos válidos
            self.assertGreater(journey.total_pages, 0)
            self.assertGreater(journey.total_time, 0)
            self.assertIsInstance(journey.pages_visited, list)
            self.assertGreater(len(journey.pages_visited), 0)
        
        # Verificar calidad de datos de PagePerformance
        performances = PagePerformance.objects.all()
        for performance in performances:
            # Verificar campos requeridos
            self.assertIsNotNone(performance.page_url)
            self.assertIsNotNone(performance.date)
            
            # Verificar rangos válidos
            self.assertGreaterEqual(performance.load_time_avg, 0)
            self.assertGreaterEqual(performance.bounce_rate, 0)
            self.assertLessEqual(performance.bounce_rate, 100)
            self.assertGreaterEqual(performance.page_views, 0)
            self.assertGreaterEqual(performance.unique_visitors, 0) 