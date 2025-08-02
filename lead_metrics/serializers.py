from rest_framework import serializers
from lead.models import Lead
from lead_type.models import LeadType
from django.db.models import Count
from django.utils import timezone
from datetime import datetime, timedelta

class LeadMetricsSerializer(serializers.Serializer):
    """Serializer para métricas generales de leads"""
    total_leads = serializers.IntegerField()
    new_leads_today = serializers.IntegerField()
    new_leads_week = serializers.IntegerField()
    new_leads_month = serializers.IntegerField()
    conversion_rate = serializers.FloatField()
    
class LeadStatusMetricsSerializer(serializers.Serializer):
    """Serializer para métricas por estado"""
    status = serializers.CharField()
    count = serializers.IntegerField()
    percentage = serializers.FloatField()
    
class LeadTypeMetricsSerializer(serializers.Serializer):
    """Serializer para métricas por tipo de lead"""
    lead_type = serializers.CharField()
    count = serializers.IntegerField()
    percentage = serializers.FloatField()
    
class LeadTrendSerializer(serializers.Serializer):
    """Serializer para tendencias temporales"""
    date = serializers.DateField()
    new_leads = serializers.IntegerField()
    converted_leads = serializers.IntegerField()
    
class LeadDailyMetricsSerializer(serializers.Serializer):
    """Serializer para métricas diarias"""
    date = serializers.DateField()
    total_leads = serializers.IntegerField()
    new_leads = serializers.IntegerField()
    pending_leads = serializers.IntegerField()
    contacted_leads = serializers.IntegerField()
    discarded_leads = serializers.IntegerField()
    process_leads = serializers.IntegerField()
    converted_leads = serializers.IntegerField() 