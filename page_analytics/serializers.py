from rest_framework import serializers
from .models import PageAccess, PageSection, UserJourney, PagePerformance


class PageAccessSerializer(serializers.ModelSerializer):
    """
    Serializer para PageAccess
    """
    class Meta:
        model = PageAccess
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class PageAccessCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear PageAccess (con validación)
    """
    class Meta:
        model = PageAccess
        fields = [
            'page_url', 'page_title', 'section', 'user_id', 'session_id',
            'user_agent', 'device_type', 'browser', 'os', 'ip_address',
            'country', 'city', 'time_on_page', 'scroll_depth', 'interactions',
            'referrer', 'utm_source', 'utm_medium', 'utm_campaign', 'metadata'
        ]

    def validate_page_url(self, value):
        """
        Validar que la URL no esté vacía
        """
        if not value or value.strip() == '':
            raise serializers.ValidationError("La URL de la página es requerida")
        return value


class PageSectionSerializer(serializers.ModelSerializer):
    """
    Serializer para PageSection
    """
    class Meta:
        model = PageSection
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class UserJourneySerializer(serializers.ModelSerializer):
    """
    Serializer para UserJourney
    """
    class Meta:
        model = UserJourney
        fields = '__all__'
        read_only_fields = ['started_at', 'ended_at']


class PagePerformanceSerializer(serializers.ModelSerializer):
    """
    Serializer para PagePerformance
    """
    class Meta:
        model = PagePerformance
        fields = '__all__'


class PageAnalyticsSummarySerializer(serializers.Serializer):
    """
    Serializer para resumen de analytics
    """
    total_page_views = serializers.IntegerField()
    unique_visitors = serializers.IntegerField()
    avg_session_duration = serializers.FloatField()
    bounce_rate = serializers.FloatField()
    top_pages = serializers.ListField()
    top_sections = serializers.ListField()
    device_distribution = serializers.DictField()
    browser_distribution = serializers.DictField()


class PageAnalyticsTrendSerializer(serializers.Serializer):
    """
    Serializer para tendencias de analytics
    """
    date = serializers.DateField()
    page_views = serializers.IntegerField()
    unique_visitors = serializers.IntegerField()
    avg_time_on_page = serializers.FloatField()
    bounce_rate = serializers.FloatField()


class SectionAnalyticsSerializer(serializers.Serializer):
    """
    Serializer para analytics de secciones
    """
    section_name = serializers.CharField()
    total_views = serializers.IntegerField()
    avg_time_on_section = serializers.FloatField()
    engagement_rate = serializers.FloatField()
    conversion_rate = serializers.FloatField()


class UserJourneyAnalyticsSerializer(serializers.Serializer):
    """
    Serializer para analytics de user journey
    """
    session_id = serializers.CharField()
    entry_page = serializers.CharField()
    exit_page = serializers.CharField()
    total_pages = serializers.IntegerField()
    total_time = serializers.IntegerField()
    conversion_goal = serializers.CharField(allow_blank=True)
    pages_visited = serializers.ListField()


class PagePerformanceAnalyticsSerializer(serializers.Serializer):
    """
    Serializer para analytics de rendimiento
    """
    page_url = serializers.CharField()
    load_time_avg = serializers.FloatField()
    load_time_p75 = serializers.FloatField()
    load_time_p95 = serializers.FloatField()
    page_views = serializers.IntegerField()
    unique_visitors = serializers.IntegerField()
    conversion_rate = serializers.FloatField() 