from django.contrib import admin
from .models import PageAccess, PageSection, UserJourney, PagePerformance


@admin.register(PageAccess)
class PageAccessAdmin(admin.ModelAdmin):
    list_display = ['page_url', 'section', 'user_id', 'device_type', 'created_at']
    list_filter = ['device_type', 'browser', 'os', 'created_at']
    search_fields = ['page_url', 'page_title', 'section', 'user_id']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('page_url', 'page_title', 'section')
        }),
        ('Usuario', {
            'fields': ('user_id', 'session_id')
        }),
        ('Dispositivo', {
            'fields': ('user_agent', 'device_type', 'browser', 'os')
        }),
        ('Ubicación', {
            'fields': ('ip_address', 'country', 'city')
        }),
        ('Métricas', {
            'fields': ('time_on_page', 'scroll_depth', 'interactions')
        }),
        ('Marketing', {
            'fields': ('referrer', 'utm_source', 'utm_medium', 'utm_campaign')
        }),
        ('Metadatos', {
            'fields': ('metadata',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'page_url_pattern', 'total_views', 'is_active', 'priority']
    list_filter = ['is_active', 'priority', 'created_at']
    search_fields = ['name', 'description', 'page_url_pattern']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'description', 'page_url_pattern', 'section_selector')
        }),
        ('Métricas', {
            'fields': ('total_views', 'avg_time_on_section', 'engagement_rate')
        }),
        ('Configuración', {
            'fields': ('is_active', 'priority')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(UserJourney)
class UserJourneyAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'entry_page', 'exit_page', 'total_pages', 'total_time', 'started_at']
    list_filter = ['started_at', 'ended_at']
    search_fields = ['session_id', 'user_id', 'entry_page', 'exit_page']
    readonly_fields = ['started_at', 'ended_at']
    date_hierarchy = 'started_at'
    
    fieldsets = (
        ('Información de Sesión', {
            'fields': ('session_id', 'user_id')
        }),
        ('Journey', {
            'fields': ('entry_page', 'exit_page', 'pages_visited', 'total_pages', 'total_time')
        }),
        ('Conversión', {
            'fields': ('conversion_goal',)
        }),
        ('Timestamps', {
            'fields': ('started_at', 'ended_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(PagePerformance)
class PagePerformanceAdmin(admin.ModelAdmin):
    list_display = ['page_url', 'date', 'page_views', 'unique_visitors', 'conversion_rate']
    list_filter = ['date']
    search_fields = ['page_url']
    readonly_fields = ['date']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Página', {
            'fields': ('page_url', 'date')
        }),
        ('Rendimiento', {
            'fields': ('load_time_avg', 'load_time_p75', 'load_time_p95')
        }),
        ('Engagement', {
            'fields': ('bounce_rate', 'exit_rate', 'avg_session_duration')
        }),
        ('Tráfico', {
            'fields': ('page_views', 'unique_visitors', 'new_visitors')
        }),
        ('Conversión', {
            'fields': ('conversions', 'conversion_rate')
        })
    ) 