from django.db import models
from django.utils import timezone


class PageAccess(models.Model):
    """
    Modelo para registrar accesos a páginas y secciones
    """
    # Información básica del acceso
    page_url = models.CharField(max_length=500, help_text="URL de la página accedida")
    page_title = models.CharField(max_length=200, blank=True, help_text="Título de la página")
    section = models.CharField(max_length=100, blank=True, help_text="Sección específica de la página")
    
    # Información del usuario
    user_id = models.CharField(max_length=100, blank=True, help_text="ID del usuario (si está autenticado)")
    session_id = models.CharField(max_length=100, blank=True, help_text="ID de sesión del usuario")
    
    # Información del dispositivo y navegador
    user_agent = models.TextField(blank=True, help_text="User Agent del navegador")
    device_type = models.CharField(max_length=50, blank=True, help_text="Tipo de dispositivo (mobile, desktop, tablet)")
    browser = models.CharField(max_length=50, blank=True, help_text="Navegador utilizado")
    os = models.CharField(max_length=50, blank=True, help_text="Sistema operativo")
    
    # Información geográfica
    ip_address = models.GenericIPAddressField(blank=True, null=True, help_text="Dirección IP del usuario")
    country = models.CharField(max_length=100, blank=True, help_text="País del usuario")
    city = models.CharField(max_length=100, blank=True, help_text="Ciudad del usuario")
    
    # Métricas de comportamiento
    time_on_page = models.IntegerField(default=0, help_text="Tiempo en la página en segundos")
    scroll_depth = models.IntegerField(default=0, help_text="Profundidad de scroll en porcentaje")
    interactions = models.IntegerField(default=0, help_text="Número de interacciones (clicks, etc.)")
    
    # Información adicional
    referrer = models.CharField(max_length=500, blank=True, help_text="Página de origen")
    utm_source = models.CharField(max_length=100, blank=True, help_text="Fuente UTM")
    utm_medium = models.CharField(max_length=100, blank=True, help_text="Medio UTM")
    utm_campaign = models.CharField(max_length=100, blank=True, help_text="Campaña UTM")
    
    # Metadatos adicionales
    metadata = models.JSONField(default=dict, blank=True, help_text="Metadatos adicionales en formato JSON")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora del acceso")
    updated_at = models.DateTimeField(auto_now=True, help_text="Fecha y hora de última actualización")
    
    class Meta:
        db_table = 'page_analytics_access'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['page_url']),
            models.Index(fields=['section']),
            models.Index(fields=['created_at']),
            models.Index(fields=['user_id']),
            models.Index(fields=['device_type']),
        ]
    
    def __str__(self):
        return f"{self.page_url} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class PageSection(models.Model):
    """
    Modelo para definir secciones de páginas y sus métricas
    """
    name = models.CharField(max_length=100, unique=True, help_text="Nombre de la sección")
    description = models.TextField(blank=True, help_text="Descripción de la sección")
    page_url_pattern = models.CharField(max_length=200, help_text="Patrón de URL para identificar la página")
    section_selector = models.CharField(max_length=200, blank=True, help_text="Selector CSS de la sección")
    
    # Métricas de la sección
    total_views = models.IntegerField(default=0, help_text="Total de vistas de la sección")
    avg_time_on_section = models.FloatField(default=0.0, help_text="Tiempo promedio en la sección")
    engagement_rate = models.FloatField(default=0.0, help_text="Tasa de engagement de la sección")
    
    # Configuración
    is_active = models.BooleanField(default=True, help_text="Si la sección está activa para tracking")
    priority = models.IntegerField(default=0, help_text="Prioridad de la sección para análisis")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'page_analytics_sections'
        ordering = ['priority', 'name']
    
    def __str__(self):
        return self.name


class UserJourney(models.Model):
    """
    Modelo para rastrear el journey del usuario a través de múltiples páginas
    """
    session_id = models.CharField(max_length=100, db_index=True, help_text="ID de sesión del usuario")
    user_id = models.CharField(max_length=100, blank=True, help_text="ID del usuario (si está autenticado)")
    
    # Journey information
    entry_page = models.CharField(max_length=500, help_text="Página de entrada")
    exit_page = models.CharField(max_length=500, blank=True, help_text="Página de salida")
    pages_visited = models.JSONField(default=list, help_text="Lista de páginas visitadas en orden")
    
    # Journey metrics
    total_pages = models.IntegerField(default=0, help_text="Total de páginas visitadas")
    total_time = models.IntegerField(default=0, help_text="Tiempo total en segundos")
    conversion_goal = models.CharField(max_length=100, blank=True, help_text="Meta de conversión alcanzada")
    
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True, help_text="Inicio del journey")
    ended_at = models.DateTimeField(blank=True, null=True, help_text="Fin del journey")
    
    class Meta:
        db_table = 'page_analytics_user_journey'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"Journey {self.session_id} - {self.total_pages} páginas"


class PagePerformance(models.Model):
    """
    Modelo para métricas de rendimiento de páginas
    """
    page_url = models.CharField(max_length=500, help_text="URL de la página")
    date = models.DateField(help_text="Fecha de las métricas")
    
    # Métricas de rendimiento
    load_time_avg = models.FloatField(default=0.0, help_text="Tiempo de carga promedio en ms")
    load_time_p75 = models.FloatField(default=0.0, help_text="Tiempo de carga percentil 75")
    load_time_p95 = models.FloatField(default=0.0, help_text="Tiempo de carga percentil 95")
    
    # Métricas de engagement
    bounce_rate = models.FloatField(default=0.0, help_text="Tasa de rebote")
    exit_rate = models.FloatField(default=0.0, help_text="Tasa de salida")
    avg_session_duration = models.FloatField(default=0.0, help_text="Duración promedio de sesión")
    
    # Métricas de tráfico
    page_views = models.IntegerField(default=0, help_text="Vistas de página")
    unique_visitors = models.IntegerField(default=0, help_text="Visitantes únicos")
    new_visitors = models.IntegerField(default=0, help_text="Nuevos visitantes")
    
    # Métricas de conversión
    conversions = models.IntegerField(default=0, help_text="Conversiones")
    conversion_rate = models.FloatField(default=0.0, help_text="Tasa de conversión")
    
    class Meta:
        db_table = 'page_analytics_performance'
        unique_together = ['page_url', 'date']
        ordering = ['-date', 'page_url']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['page_url']),
        ]
    
    def __str__(self):
        return f"{self.page_url} - {self.date}" 