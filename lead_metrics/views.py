from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from lead.models import Lead
from lead_type.models import LeadType
from lead_metrics.serializers import (
    LeadMetricsSerializer,
    LeadStatusMetricsSerializer,
    LeadTypeMetricsSerializer,
    LeadTrendSerializer,
    LeadDailyMetricsSerializer
)

class LeadMetricsViewSet(viewsets.ViewSet):
    """
    ViewSet para métricas de leads para dashboards
    """
    
    @action(detail=False, methods=['get'], url_path='overview')
    def overview(self, request):
        """
        Obtiene métricas generales de leads para dashboard principal
        """
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Métricas básicas
        total_leads = Lead.objects.count()
        new_leads_today = Lead.objects.filter(created_at__date=today).count()
        new_leads_week = Lead.objects.filter(created_at__date__gte=week_ago).count()
        new_leads_month = Lead.objects.filter(created_at__date__gte=month_ago).count()
        
        # Tasa de conversión (convertidos / total)
        converted_leads = Lead.objects.filter(status='converted').count()
        conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
        
        data = {
            'total_leads': total_leads,
            'new_leads_today': new_leads_today,
            'new_leads_week': new_leads_week,
            'new_leads_month': new_leads_month,
            'conversion_rate': round(conversion_rate, 2)
        }
        
        serializer = LeadMetricsSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='by-status')
    def by_status(self, request):
        """
        Obtiene métricas de leads agrupados por estado
        """
        total_leads = Lead.objects.count()
        
        status_counts = Lead.objects.values('status').annotate(
            count=Count('id')
        ).order_by('-count')
        
        metrics = []
        for item in status_counts:
            percentage = (item['count'] / total_leads * 100) if total_leads > 0 else 0
            metrics.append({
                'status': item['status'],
                'count': item['count'],
                'percentage': round(percentage, 2)
            })
        
        serializer = LeadStatusMetricsSerializer(metrics, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='by-type')
    def by_type(self, request):
        """
        Obtiene métricas de leads agrupados por tipo
        """
        total_leads = Lead.objects.count()
        
        type_counts = Lead.objects.values('lead_type__name').annotate(
            count=Count('id')
        ).order_by('-count')
        
        metrics = []
        for item in type_counts:
            percentage = (item['count'] / total_leads * 100) if total_leads > 0 else 0
            metrics.append({
                'lead_type': item['lead_type__name'],
                'count': item['count'],
                'percentage': round(percentage, 2)
            })
        
        serializer = LeadTypeMetricsSerializer(metrics, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='trends')
    def trends(self, request):
        """
        Obtiene tendencias de leads por día (últimos 30 días)
        """
        days = int(request.query_params.get('days', 30))
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        trends = []
        current_date = start_date
        
        while current_date <= end_date:
            new_leads = Lead.objects.filter(created_at__date=current_date).count()
            converted_leads = Lead.objects.filter(
                status='converted',
                created_at__date=current_date
            ).count()
            
            trends.append({
                'date': current_date,
                'new_leads': new_leads,
                'converted_leads': converted_leads
            })
            
            current_date += timedelta(days=1)
        
        serializer = LeadTrendSerializer(trends, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='daily-metrics')
    def daily_metrics(self, request):
        """
        Obtiene métricas diarias detalladas (últimos 7 días)
        """
        days = int(request.query_params.get('days', 7))
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        daily_metrics = []
        current_date = start_date
        
        while current_date <= end_date:
            leads_for_date = Lead.objects.filter(created_at__date=current_date)
            
            metrics = {
                'date': current_date,
                'total_leads': leads_for_date.count(),
                'new_leads': leads_for_date.count(),  # Todos los creados en esa fecha son nuevos
                'pending_leads': leads_for_date.filter(status='pending').count(),
                'contacted_leads': leads_for_date.filter(status='contacted').count(),
                'discarded_leads': leads_for_date.filter(status='discarded').count(),
                'process_leads': leads_for_date.filter(status='process').count(),
                'converted_leads': leads_for_date.filter(status='converted').count(),
            }
            
            daily_metrics.append(metrics)
            current_date += timedelta(days=1)
        
        serializer = LeadDailyMetricsSerializer(daily_metrics, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='recent-activity')
    def recent_activity(self, request):
        """
        Obtiene actividad reciente de leads (últimos leads creados)
        """
        limit = int(request.query_params.get('limit', 10))
        
        recent_leads = Lead.objects.select_related('lead_type').order_by('-created_at')[:limit]
        
        activity = []
        for lead in recent_leads:
            activity.append({
                'id': lead.id,
                'name': lead.name,
                'email': lead.email,
                'status': lead.status,
                'lead_type': lead.lead_type.name,
                'created_at': lead.created_at,
                'tryet': lead.tryet
            })
        
        return Response(activity)
    
    @action(detail=False, methods=['get'], url_path='conversion-funnel')
    def conversion_funnel(self, request):
        """
        Obtiene métricas del funnel de conversión
        """
        total_leads = Lead.objects.count()
        
        funnel_data = {
            'total_leads': total_leads,
            'pending_leads': Lead.objects.filter(status='pending').count(),
            'contacted_leads': Lead.objects.filter(status='contacted').count(),
            'process_leads': Lead.objects.filter(status='process').count(),
            'converted_leads': Lead.objects.filter(status='converted').count(),
            'discarded_leads': Lead.objects.filter(status='discarded').count(),
        }
        
        # Calcular porcentajes del funnel
        if total_leads > 0:
            funnel_data['pending_percentage'] = round((funnel_data['pending_leads'] / total_leads) * 100, 2)
            funnel_data['contacted_percentage'] = round((funnel_data['contacted_leads'] / total_leads) * 100, 2)
            funnel_data['process_percentage'] = round((funnel_data['process_leads'] / total_leads) * 100, 2)
            funnel_data['converted_percentage'] = round((funnel_data['converted_leads'] / total_leads) * 100, 2)
            funnel_data['discarded_percentage'] = round((funnel_data['discarded_leads'] / total_leads) * 100, 2)
        else:
            funnel_data.update({
                'pending_percentage': 0,
                'contacted_percentage': 0,
                'process_percentage': 0,
                'converted_percentage': 0,
                'discarded_percentage': 0
            })
        
        return Response(funnel_data) 