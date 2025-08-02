from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import PageAccess, PageSection, UserJourney, PagePerformance
from .serializers import (
    PageAccessSerializer, PageAccessCreateSerializer, PageSectionSerializer,
    UserJourneySerializer, PagePerformanceSerializer, PageAnalyticsSummarySerializer,
    PageAnalyticsTrendSerializer, SectionAnalyticsSerializer, UserJourneyAnalyticsSerializer,
    PagePerformanceAnalyticsSerializer
)


class PageAccessViewSet(viewsets.ModelViewSet):
    """
    ViewSet para PageAccess
    """
    queryset = PageAccess.objects.all()
    serializer_class = PageAccessSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PageAccessCreateSerializer
        return PageAccessSerializer
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Obtener resumen de analytics
        """
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        queryset = self.queryset.filter(
            created_at__gte=start_date
        )
        
        # Métricas básicas
        total_page_views = queryset.count()
        unique_visitors = queryset.values('session_id').distinct().count()
        avg_time = queryset.aggregate(avg_time=Avg('time_on_page'))['avg_time'] or 0
        
        # Calcular tasa de rebote
        total_sessions = queryset.values('session_id').distinct().count()
        bounce_sessions = queryset.values('session_id').annotate(
            page_count=Count('id')
        ).filter(page_count=1).count()
        bounce_rate = (bounce_sessions / total_sessions * 100) if total_sessions > 0 else 0
        
        # Páginas más visitadas
        top_pages = queryset.values('page_url').annotate(
            views=Count('id')
        ).order_by('-views')[:10]
        
        # Secciones más visitadas
        top_sections = queryset.exclude(section='').values('section').annotate(
            views=Count('id')
        ).order_by('-views')[:10]
        
        # Distribución por dispositivo
        device_distribution = queryset.values('device_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Distribución por navegador
        browser_distribution = queryset.values('browser').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Eventos de ecommerce
        ecommerce_events = {}
        
        # Contar eventos específicos de ecommerce desde metadata
        product_views = queryset.filter(metadata__has_key='event_type').filter(metadata__event_type='product_view').count()
        add_to_cart = queryset.filter(metadata__has_key='event_type').filter(metadata__event_type='add_to_cart').count()
        begin_checkout = queryset.filter(metadata__has_key='event_type').filter(metadata__event_type='begin_checkout').count()
        purchases = queryset.filter(metadata__has_key='event_type').filter(metadata__event_type='purchase').count()
        
        ecommerce_events = {
            'product_views': product_views,
            'add_to_cart': add_to_cart,
            'begin_checkout': begin_checkout,
            'purchases': purchases
        }
        
        data = {
            'total_page_views': total_page_views,
            'unique_visitors': unique_visitors,
            'avg_session_duration': avg_time,
            'bounce_rate': round(bounce_rate, 2),
            'top_pages': list(top_pages),
            'top_sections': list(top_sections),
            'device_distribution': {item['device_type']: item['count'] for item in device_distribution},
            'browser_distribution': {item['browser']: item['count'] for item in browser_distribution},
            'ecommerce_events': ecommerce_events
        }
        
        serializer = PageAnalyticsSummarySerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def trends(self, request):
        """
        Obtener tendencias de analytics
        """
        days = int(request.query_params.get('days', 7))
        start_date = timezone.now() - timedelta(days=days)
        
        # Generar fechas para el rango
        dates = []
        trends_data = []
        
        for i in range(days):
            date = start_date + timedelta(days=i)
            dates.append(date.date())
            
            # Filtrar por fecha
            day_queryset = self.queryset.filter(
                created_at__date=date.date()
            )
            
            page_views = day_queryset.count()
            unique_visitors = day_queryset.values('session_id').distinct().count()
            avg_time = day_queryset.aggregate(avg_time=Avg('time_on_page'))['avg_time'] or 0
            
            # Calcular tasa de rebote para el día
            total_sessions = day_queryset.values('session_id').distinct().count()
            bounce_sessions = day_queryset.values('session_id').annotate(
                page_count=Count('id')
            ).filter(page_count=1).count()
            bounce_rate = (bounce_sessions / total_sessions * 100) if total_sessions > 0 else 0
            
            trends_data.append({
                'date': date.date(),
                'page_views': page_views,
                'unique_visitors': unique_visitors,
                'avg_time_on_page': round(avg_time, 2),
                'bounce_rate': round(bounce_rate, 2)
            })
        
        serializer = PageAnalyticsTrendSerializer(trends_data, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def sections(self, request):
        """
        Obtener analytics por secciones
        """
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        queryset = self.queryset.filter(
            created_at__gte=start_date
        ).exclude(section='')
        
        sections_data = queryset.values('section').annotate(
            total_views=Count('id'),
            avg_time_on_section=Avg('time_on_page'),
            engagement_rate=Avg('scroll_depth'),
            conversion_rate=Avg('interactions')
        ).order_by('-total_views')
        
        # Formatear datos
        formatted_data = []
        for item in sections_data:
            formatted_data.append({
                'section_name': item['section'],
                'total_views': item['total_views'],
                'avg_time_on_section': round(item['avg_time_on_section'] or 0, 2),
                'engagement_rate': round(item['engagement_rate'] or 0, 2),
                'conversion_rate': round(item['conversion_rate'] or 0, 2)
            })
        
        serializer = SectionAnalyticsSerializer(formatted_data, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def performance(self, request):
        """
        Obtener métricas de rendimiento
        """
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        queryset = self.queryset.filter(created_at__gte=start_date)
        
        # Agrupar por página
        pages_data = queryset.values('page_url').annotate(
            page_views=Count('id'),
            unique_visitors=Count('session_id', distinct=True),
            load_time_avg=Avg('time_on_page'),
            load_time_p75=Avg('time_on_page'),  # Simplificado
            load_time_p95=Avg('time_on_page'),  # Simplificado
            conversion_rate=Avg('interactions')
        ).order_by('-page_views')
        
        # Formatear datos
        formatted_data = []
        for item in pages_data:
            formatted_data.append({
                'page_url': item['page_url'],
                'load_time_avg': round(item['load_time_avg'] or 0, 2),
                'load_time_p75': round(item['load_time_p75'] or 0, 2),
                'load_time_p95': round(item['load_time_p95'] or 0, 2),
                'page_views': item['page_views'],
                'unique_visitors': item['unique_visitors'],
                'conversion_rate': round(item['conversion_rate'] or 0, 2)
            })
        
        serializer = PagePerformanceAnalyticsSerializer(formatted_data, many=True)
        return Response(serializer.data)


class PageSectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para PageSection
    """
    queryset = PageSection.objects.all()
    serializer_class = PageSectionSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Obtener solo secciones activas
        """
        queryset = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserJourneyViewSet(viewsets.ModelViewSet):
    """
    ViewSet para UserJourney
    """
    queryset = UserJourney.objects.all()
    serializer_class = UserJourneySerializer
    
    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """
        Obtener analytics de user journey
        """
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        queryset = self.queryset.filter(started_at__gte=start_date)
        
        # Métricas de journey
        total_journeys = queryset.count()
        avg_pages_per_journey = queryset.aggregate(avg_pages=Avg('total_pages'))['avg_pages'] or 0
        avg_time_per_journey = queryset.aggregate(avg_time=Avg('total_time'))['avg_time'] or 0
        
        # Journeys más largos
        top_journeys = queryset.order_by('-total_pages')[:10]
        
        # Páginas de entrada más comunes
        entry_pages = queryset.values('entry_page').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        # Páginas de salida más comunes
        exit_pages = queryset.values('exit_page').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        data = {
            'total_journeys': total_journeys,
            'avg_pages_per_journey': round(avg_pages_per_journey, 2),
            'avg_time_per_journey': round(avg_time_per_journey, 2),
            'top_journeys': UserJourneySerializer(top_journeys, many=True).data,
            'entry_pages': list(entry_pages),
            'exit_pages': list(exit_pages)
        }
        
        return Response(data)


class PagePerformanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para PagePerformance
    """
    queryset = PagePerformance.objects.all()
    serializer_class = PagePerformanceSerializer
    
    @action(detail=False, methods=['get'])
    def by_date(self, request):
        """
        Obtener rendimiento por fecha
        """
        date_str = request.query_params.get('date')
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                queryset = self.queryset.filter(date=date)
            except ValueError:
                return Response(
                    {'error': 'Formato de fecha inválido. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # Últimos 7 días por defecto
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=7)
            queryset = self.queryset.filter(date__range=[start_date, end_date])
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data) 