from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta
from .models import PageAccess, PageSection, UserJourney, PagePerformance
from .serializers import (
    PageAccessSerializer, PageAccessCreateSerializer, PageSectionSerializer,
    UserJourneySerializer, PagePerformanceSerializer, PageAnalyticsSummarySerializer,
    PageAnalyticsTrendSerializer, SectionAnalyticsSerializer, UserJourneyAnalyticsSerializer,
    PagePerformanceAnalyticsSerializer
)


class PageAccessSerializerTest(TestCase):
    """Tests para PageAccessSerializer"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.page_access_data = {
            'page_url': '/productos',
            'page_title': 'Productos - Tienda',
            'section': 'productos-destacados',
            'user_id': 'user123',
            'session_id': 'session456',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
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
        self.page_access = PageAccess.objects.create(**self.page_access_data)
    
    def test_page_access_serializer_fields(self):
        """Test: Verificar campos del serializer"""
        serializer = PageAccessSerializer(self.page_access)
        data = serializer.data
        
        self.assertEqual(data['page_url'], '/productos')
        self.assertEqual(data['page_title'], 'Productos - Tienda')
        self.assertEqual(data['section'], 'productos-destacados')
        self.assertEqual(data['device_type'], 'desktop')
        self.assertEqual(data['time_on_page'], 120)
        self.assertEqual(data['scroll_depth'], 75)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
    
    def test_page_access_serializer_read_only_fields(self):
        """Test: Verificar campos de solo lectura"""
        serializer = PageAccessSerializer(self.page_access)
        data = serializer.data
        
        # Estos campos no deberían estar en el serializer de entrada
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)


class PageAccessCreateSerializerTest(TestCase):
    """Tests para PageAccessCreateSerializer"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.valid_data = {
            'page_url': '/productos',
            'page_title': 'Productos - Tienda',
            'section': 'productos-destacados',
            'user_id': 'user123',
            'session_id': 'session456',
            'device_type': 'desktop',
            'browser': 'Chrome',
            'time_on_page': 120,
            'scroll_depth': 75,
            'interactions': 5
        }
    
    def test_page_access_create_serializer_valid_data(self):
        """Test: Serializer con datos válidos"""
        serializer = PageAccessCreateSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
    
    def test_page_access_create_serializer_invalid_url(self):
        """Test: Validación de URL requerida"""
        invalid_data = self.valid_data.copy()
        invalid_data['page_url'] = ''
        
        serializer = PageAccessCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('page_url', serializer.errors)
    
    def test_page_access_create_serializer_missing_url(self):
        """Test: Validación de URL faltante"""
        invalid_data = self.valid_data.copy()
        del invalid_data['page_url']
        
        serializer = PageAccessCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('page_url', serializer.errors)
    
    def test_page_access_create_serializer_create_object(self):
        """Test: Crear objeto desde serializer"""
        serializer = PageAccessCreateSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        
        page_access = serializer.save()
        self.assertEqual(page_access.page_url, '/productos')
        self.assertEqual(page_access.device_type, 'desktop')
        self.assertEqual(page_access.time_on_page, 120)


class PageSectionSerializerTest(TestCase):
    """Tests para PageSectionSerializer"""
    
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
        self.section = PageSection.objects.create(**self.section_data)
    
    def test_page_section_serializer_fields(self):
        """Test: Verificar campos del serializer"""
        serializer = PageSectionSerializer(self.section)
        data = serializer.data
        
        self.assertEqual(data['name'], 'header')
        self.assertEqual(data['description'], 'Sección de navegación principal')
        self.assertEqual(data['page_url_pattern'], '*header*')
        self.assertEqual(data['is_active'], True)
        self.assertEqual(data['priority'], 1)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
    
    def test_page_section_serializer_create(self):
        """Test: Crear sección desde serializer"""
        new_data = {
            'name': 'footer',
            'description': 'Sección de pie de página',
            'page_url_pattern': '*footer*',
            'section_selector': '.footer',
            'is_active': True,
            'priority': 2
        }
        
        serializer = PageSectionSerializer(data=new_data)
        self.assertTrue(serializer.is_valid())
        
        section = serializer.save()
        self.assertEqual(section.name, 'footer')
        self.assertEqual(section.priority, 2)


class UserJourneySerializerTest(TestCase):
    """Tests para UserJourneySerializer"""
    
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
        self.journey = UserJourney.objects.create(**self.journey_data)
    
    def test_user_journey_serializer_fields(self):
        """Test: Verificar campos del serializer"""
        serializer = UserJourneySerializer(self.journey)
        data = serializer.data
        
        self.assertEqual(data['session_id'], 'session123')
        self.assertEqual(data['entry_page'], '/')
        self.assertEqual(data['exit_page'], '/checkout')
        self.assertEqual(data['total_pages'], 4)
        self.assertEqual(data['total_time'], 600)
        self.assertEqual(data['conversion_goal'], 'purchase')
        self.assertIn('started_at', data)
        self.assertIsNone(data['ended_at'])
    
    def test_user_journey_serializer_pages_visited(self):
        """Test: Verificar campo pages_visited como JSON"""
        serializer = UserJourneySerializer(self.journey)
        data = serializer.data
        
        self.assertIsInstance(data['pages_visited'], list)
        self.assertEqual(len(data['pages_visited']), 4)
        self.assertEqual(data['pages_visited'][0], '/')
        self.assertEqual(data['pages_visited'][-1], '/checkout')


class PagePerformanceSerializerTest(TestCase):
    """Tests para PagePerformanceSerializer"""
    
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
        self.performance = PagePerformance.objects.create(**self.performance_data)
    
    def test_page_performance_serializer_fields(self):
        """Test: Verificar campos del serializer"""
        serializer = PagePerformanceSerializer(self.performance)
        data = serializer.data
        
        self.assertEqual(data['page_url'], '/productos')
        self.assertEqual(data['load_time_avg'], 1500.5)
        self.assertEqual(data['bounce_rate'], 25.5)
        self.assertEqual(data['page_views'], 1000)
        self.assertEqual(data['conversion_rate'], 5.5)


class AnalyticsSerializersTest(TestCase):
    """Tests para serializers de analytics"""
    
    def test_page_analytics_summary_serializer(self):
        """Test: PageAnalyticsSummarySerializer"""
        data = {
            'total_page_views': 1500,
            'unique_visitors': 450,
            'avg_session_duration': 180.5,
            'bounce_rate': 35.2,
            'top_pages': [
                {'page_url': '/', 'views': 300},
                {'page_url': '/productos', 'views': 250}
            ],
            'top_sections': [
                {'section': 'header', 'views': 150},
                {'section': 'hero', 'views': 120}
            ],
            'device_distribution': {
                'desktop': 60,
                'mobile': 35,
                'tablet': 5
            },
            'browser_distribution': {
                'Chrome': 45,
                'Firefox': 25,
                'Safari': 20
            }
        }
        
        serializer = PageAnalyticsSummarySerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_page_analytics_trend_serializer(self):
        """Test: PageAnalyticsTrendSerializer"""
        data = {
            'date': timezone.now().date(),
            'page_views': 150,
            'unique_visitors': 45,
            'avg_time_on_page': 180.5,
            'bounce_rate': 35.2
        }
        
        serializer = PageAnalyticsTrendSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_section_analytics_serializer(self):
        """Test: SectionAnalyticsSerializer"""
        data = {
            'section_name': 'header',
            'total_views': 100,
            'avg_time_on_section': 30.5,
            'engagement_rate': 85.2,
            'conversion_rate': 5.5
        }
        
        serializer = SectionAnalyticsSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_user_journey_analytics_serializer(self):
        """Test: UserJourneyAnalyticsSerializer"""
        data = {
            'session_id': 'session123',
            'entry_page': '/',
            'exit_page': '/checkout',
            'total_pages': 4,
            'total_time': 600,
            'conversion_goal': 'purchase',
            'pages_visited': ['/', '/productos', '/carrito', '/checkout']
        }
        
        serializer = UserJourneyAnalyticsSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_page_performance_analytics_serializer(self):
        """Test: PagePerformanceAnalyticsSerializer"""
        data = {
            'page_url': '/productos',
            'load_time_avg': 1500.5,
            'load_time_p75': 2000.0,
            'load_time_p95': 3500.0,
            'page_views': 1000,
            'unique_visitors': 450,
            'conversion_rate': 5.5
        }
        
        serializer = PagePerformanceAnalyticsSerializer(data=data)
        self.assertTrue(serializer.is_valid()) 