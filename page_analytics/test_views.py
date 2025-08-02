from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import PageAccess, PageSection, UserJourney, PagePerformance
from .serializers import PageAccessSerializer, PageSectionSerializer


class PageAccessViewSetTest(APITestCase):
    """Tests para PageAccessViewSet"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        
        # Crear datos de prueba
        self.page_access_data = {
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
        
        # Crear múltiples registros para testing
        for i in range(5):
            data = self.page_access_data.copy()
            data['page_url'] = f'/page-{i}'
            data['session_id'] = f'session-{i}'
            data['created_at'] = timezone.now() - timedelta(days=i)
            page_access = PageAccess.objects.create(**data)
            page_access.created_at = data['created_at']
            page_access.save(update_fields=['created_at'])
    
    def test_list_page_access(self):
        """Test: Listar todos los registros de PageAccess"""
        url = reverse('page-access-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
    
    def test_create_page_access(self):
        """Test: Crear un nuevo registro de PageAccess"""
        url = reverse('page-access-list')
        data = self.page_access_data.copy()
        data['page_url'] = '/new-page'
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PageAccess.objects.count(), 6)
        self.assertEqual(response.data['page_url'], '/new-page')
    
    def test_create_page_access_invalid_data(self):
        """Test: Crear PageAccess con datos inválidos"""
        url = reverse('page-access-list')
        data = self.page_access_data.copy()
        data['page_url'] = ''  # URL vacía
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('page_url', response.data)
    
    def test_retrieve_page_access(self):
        """Test: Obtener un registro específico de PageAccess"""
        page_access = PageAccess.objects.first()
        url = reverse('page-access-detail', args=[page_access.id])
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['page_url'], page_access.page_url)
    
    def test_update_page_access(self):
        """Test: Actualizar un registro de PageAccess"""
        page_access = PageAccess.objects.first()
        url = reverse('page-access-detail', args=[page_access.id])
        data = self.page_access_data.copy()
        data['time_on_page'] = 200
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['time_on_page'], 200)
    
    def test_delete_page_access(self):
        """Test: Eliminar un registro de PageAccess"""
        page_access = PageAccess.objects.first()
        url = reverse('page-access-detail', args=[page_access.id])
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PageAccess.objects.count(), 4)
    
    def test_summary_action(self):
        """Test: Endpoint summary de PageAccess"""
        url = reverse('page-access-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_page_views', response.data)
        self.assertIn('unique_visitors', response.data)
        self.assertIn('avg_session_duration', response.data)
        self.assertIn('bounce_rate', response.data)
        self.assertIn('top_pages', response.data)
        self.assertIn('top_sections', response.data)
        self.assertIn('device_distribution', response.data)
        self.assertIn('browser_distribution', response.data)
    
    def test_summary_action_with_days_parameter(self):
        """Test: Endpoint summary con parámetro days"""
        url = reverse('page-access-summary')
        response = self.client.get(url, {'days': 7})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_page_views', response.data)
    
    def test_trends_action(self):
        """Test: Endpoint trends de PageAccess"""
        url = reverse('page-access-trends')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        
        if response.data:  # Si hay datos
            trend_data = response.data[0]
            self.assertIn('date', trend_data)
            self.assertIn('page_views', trend_data)
            self.assertIn('unique_visitors', trend_data)
            self.assertIn('avg_time_on_page', trend_data)
            self.assertIn('bounce_rate', trend_data)
    
    def test_trends_action_with_days_parameter(self):
        """Test: Endpoint trends con parámetro days"""
        url = reverse('page-access-trends')
        response = self.client.get(url, {'days': 3})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_sections_action(self):
        """Test: Endpoint sections de PageAccess"""
        url = reverse('page-access-sections')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_performance_action(self):
        """Test: Endpoint performance de PageAccess"""
        url = reverse('page-access-performance')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)


class PageSectionViewSetTest(APITestCase):
    """Tests para PageSectionViewSet"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        
        # Crear secciones de prueba
        self.section_data = {
            'name': 'header',
            'description': 'Sección de navegación principal',
            'page_url_pattern': '*header*',
            'section_selector': '.header',
            'is_active': True,
            'priority': 1
        }
        
        self.section = PageSection.objects.create(**self.section_data)
    
    def test_list_page_sections(self):
        """Test: Listar todas las secciones"""
        url = reverse('page-sections-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_page_section(self):
        """Test: Crear una nueva sección"""
        url = reverse('page-sections-list')
        data = {
            'name': 'footer',
            'description': 'Sección de pie de página',
            'page_url_pattern': '*footer*',
            'section_selector': '.footer',
            'is_active': True,
            'priority': 2
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PageSection.objects.count(), 2)
        self.assertEqual(response.data['name'], 'footer')
    
    def test_retrieve_page_section(self):
        """Test: Obtener una sección específica"""
        url = reverse('page-sections-detail', args=[self.section.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'header')
    
    def test_update_page_section(self):
        """Test: Actualizar una sección"""
        url = reverse('page-sections-detail', args=[self.section.id])
        data = self.section_data.copy()
        data['priority'] = 5
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['priority'], 5)
    
    def test_delete_page_section(self):
        """Test: Eliminar una sección"""
        url = reverse('page-sections-detail', args=[self.section.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PageSection.objects.count(), 0)
    
    def test_active_action(self):
        """Test: Endpoint active de PageSection"""
        url = reverse('page-sections-active')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Solo la sección activa
        
        # Crear una sección inactiva
        inactive_section = PageSection.objects.create(
            name='inactive',
            page_url_pattern='*inactive*',
            is_active=False
        )
        
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)  # Solo las activas


class UserJourneyViewSetTest(APITestCase):
    """Tests para UserJourneyViewSet"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        
        # Crear journey de prueba
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
    
    def test_list_user_journeys(self):
        """Test: Listar todos los user journeys"""
        url = reverse('user-journey-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_user_journey(self):
        """Test: Crear un nuevo user journey"""
        url = reverse('user-journey-list')
        data = self.journey_data.copy()
        data['session_id'] = 'session789'
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserJourney.objects.count(), 2)
        self.assertEqual(response.data['session_id'], 'session789')
    
    def test_retrieve_user_journey(self):
        """Test: Obtener un user journey específico"""
        url = reverse('user-journey-detail', args=[self.journey.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['session_id'], 'session123')
    
    def test_analytics_action(self):
        """Test: Endpoint analytics de UserJourney"""
        url = reverse('user-journey-analytics')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_journeys', response.data)
        self.assertIn('avg_pages_per_journey', response.data)
        self.assertIn('avg_time_per_journey', response.data)
        self.assertIn('top_journeys', response.data)
        self.assertIn('entry_pages', response.data)
        self.assertIn('exit_pages', response.data)


class PagePerformanceViewSetTest(APITestCase):
    """Tests para PagePerformanceViewSet"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        
        # Crear performance de prueba
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
    
    def test_list_page_performances(self):
        """Test: Listar todas las métricas de rendimiento"""
        url = reverse('page-performance-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_page_performance(self):
        """Test: Crear nuevas métricas de rendimiento"""
        url = reverse('page-performance-list')
        data = self.performance_data.copy()
        data['page_url'] = '/nueva-pagina'
        data['date'] = (timezone.now().date() + timedelta(days=1)).isoformat()
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PagePerformance.objects.count(), 2)
        self.assertEqual(response.data['page_url'], '/nueva-pagina')
    
    def test_retrieve_page_performance(self):
        """Test: Obtener métricas específicas de rendimiento"""
        url = reverse('page-performance-detail', args=[self.performance.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['page_url'], '/productos')
    
    def test_by_date_action(self):
        """Test: Endpoint by_date de PagePerformance"""
        url = reverse('page-performance-by-date')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_by_date_action_with_date_parameter(self):
        """Test: Endpoint by_date con parámetro date"""
        url = reverse('page-performance-by-date')
        today = timezone.now().date().isoformat()
        response = self.client.get(url, {'date': today})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_by_date_action_invalid_date_format(self):
        """Test: Endpoint by_date con formato de fecha inválido"""
        url = reverse('page-performance-by-date')
        response = self.client.get(url, {'date': 'invalid-date'})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data) 