# Page Analytics - Arquitectura Técnica

## Descripción General

La aplicación `page_analytics` es un sistema completo para registrar, analizar y medir el comportamiento de los usuarios en páginas web y sus secciones específicas. Permite mejorar continuamente la experiencia del usuario mediante datos cuantitativos.

## Arquitectura de Modelos

### 1. PageAccess (Registro de Accesos)
**Propósito:** Registra cada interacción del usuario con una página.

**Campos Clave:**
- `page_url`: URL de la página accedida
- `section`: Sección específica dentro de la página
- `user_id`: Identificador del usuario (si está autenticado)
- `session_id`: Identificador de sesión único
- `device_type`: Tipo de dispositivo (mobile/desktop/tablet)
- `time_on_page`: Tiempo de permanencia en segundos
- `scroll_depth`: Profundidad de scroll (0-100%)
- `interactions`: Número de interacciones (clicks, etc.)

**Índices de Base de Datos:**
```sql
CREATE INDEX ON page_analytics_access (page_url);
CREATE INDEX ON page_analytics_access (section);
CREATE INDEX ON page_analytics_access (created_at);
CREATE INDEX ON page_analytics_access (user_id);
CREATE INDEX ON page_analytics_access (device_type);
```

### 2. PageSection (Definición de Secciones)
**Propósito:** Define secciones de páginas para análisis granular.

**Campos Clave:**
- `name`: Nombre único de la sección
- `page_url_pattern`: Patrón para identificar páginas
- `section_selector`: Selector CSS de la sección
- `is_active`: Si está activa para tracking
- `priority`: Prioridad para análisis

### 3. UserJourney (Journey del Usuario)
**Propósito:** Rastrea el camino completo del usuario a través del sitio.

**Campos Clave:**
- `session_id`: Identificador de sesión
- `entry_page`: Página de entrada
- `exit_page`: Página de salida
- `pages_visited`: Lista ordenada de páginas visitadas
- `total_pages`: Número total de páginas visitadas
- `total_time`: Tiempo total en segundos
- `conversion_goal`: Meta de conversión alcanzada

### 4. PagePerformance (Rendimiento de Páginas)
**Propósito:** Métricas agregadas de rendimiento por página y fecha.

**Campos Clave:**
- `page_url`: URL de la página
- `date`: Fecha de las métricas
- `load_time_avg`: Tiempo de carga promedio
- `bounce_rate`: Tasa de rebote
- `page_views`: Vistas de página
- `unique_visitors`: Visitantes únicos
- `conversion_rate`: Tasa de conversión

## API Endpoints

### PageAccessViewSet
```python
# Endpoints principales
GET    /page-analytics/page-access/          # Listar todos
POST   /page-analytics/page-access/          # Crear nuevo
GET    /page-analytics/page-access/{id}/     # Obtener específico
PUT    /page-analytics/page-access/{id}/     # Actualizar
DELETE /page-analytics/page-access/{id}/     # Eliminar

# Endpoints de analytics
GET    /page-analytics/page-access/summary/      # Resumen general
GET    /page-analytics/page-access/trends/       # Tendencias temporales
GET    /page-analytics/page-access/sections/     # Analytics por secciones
GET    /page-analytics/page-access/performance/  # Métricas de rendimiento
```

### PageSectionViewSet
```python
GET    /page-analytics/page-sections/        # Listar todas
POST   /page-analytics/page-sections/        # Crear nueva
GET    /page-analytics/page-sections/active/ # Solo activas
```

### UserJourneyViewSet
```python
GET    /page-analytics/user-journey/         # Listar todos
POST   /page-analytics/user-journey/         # Crear nuevo
GET    /page-analytics/user-journey/analytics/ # Analytics de journey
```

### PagePerformanceViewSet
```python
GET    /page-analytics/page-performance/     # Listar todos
POST   /page-analytics/page-performance/     # Crear nuevo
GET    /page-analytics/page-performance/by_date/ # Por fecha
```

## Algoritmos de Análisis

### 1. Cálculo de Tasa de Rebote
```python
def calculate_bounce_rate(queryset):
    total_sessions = queryset.values('session_id').distinct().count()
    bounce_sessions = queryset.values('session_id').annotate(
        page_count=Count('id')
    ).filter(page_count=1).count()
    
    return (bounce_sessions / total_sessions * 100) if total_sessions > 0 else 0
```

### 2. Análisis de Tendencias
```python
def generate_trends_data(days, queryset):
    trends_data = []
    start_date = timezone.now() - timedelta(days=days)
    
    for i in range(days):
        date = start_date + timedelta(days=i)
        day_queryset = queryset.filter(created_at__date=date.date())
        
        # Calcular métricas del día
        page_views = day_queryset.count()
        unique_visitors = day_queryset.values('session_id').distinct().count()
        avg_time = day_queryset.aggregate(avg_time=Avg('time_on_page'))['avg_time'] or 0
        bounce_rate = calculate_bounce_rate(day_queryset)
        
        trends_data.append({
            'date': date.date(),
            'page_views': page_views,
            'unique_visitors': unique_visitors,
            'avg_time_on_page': round(avg_time, 2),
            'bounce_rate': round(bounce_rate, 2)
        })
    
    return trends_data
```

### 3. Análisis de Secciones
```python
def analyze_sections(queryset):
    return queryset.exclude(section='').values('section').annotate(
        total_views=Count('id'),
        avg_time_on_section=Avg('time_on_page'),
        engagement_rate=Avg('scroll_depth'),
        conversion_rate=Avg('interactions')
    ).order_by('-total_views')
```

## Optimizaciones de Rendimiento

### 1. Índices de Base de Datos
- Índices en campos de consulta frecuente
- Índices compuestos para consultas complejas
- Índices de fecha para análisis temporal

### 2. Agregación de Datos
- Cálculo de métricas en tiempo real
- Cache de resultados frecuentes
- Paginación para grandes volúmenes

### 3. Consultas Optimizadas
```python
# Ejemplo de consulta optimizada
queryset = PageAccess.objects.filter(
    created_at__gte=start_date
).select_related().prefetch_related()

# Agregación eficiente
metrics = queryset.aggregate(
    total_views=Count('id'),
    unique_visitors=Count('session_id', distinct=True),
    avg_time=Avg('time_on_page')
)
```

## Escalabilidad

### 1. Particionamiento
- Particionamiento por fecha para PageAccess
- Particionamiento por página para PagePerformance

### 2. Cache
- Cache de resúmenes diarios
- Cache de tendencias semanales
- Cache de métricas de secciones

### 3. Archivo de Datos
- Archivo de datos históricos (> 1 año)
- Compresión de datos antiguos
- Backup automático

## Seguridad

### 1. Validación de Datos
```python
def validate_page_url(self, value):
    if not value or value.strip() == '':
        raise serializers.ValidationError("La URL de la página es requerida")
    return value
```

### 2. Sanitización
- Limpieza de datos de entrada
- Validación de tipos de datos
- Escape de caracteres especiales

### 3. Privacidad
- Anonimización de IPs
- Respeto a GDPR/CCPA
- Consentimiento de tracking

## Monitoreo

### 1. Métricas de Aplicación
- Tiempo de respuesta de API
- Tasa de errores
- Uso de memoria y CPU

### 2. Métricas de Negocio
- Volumen de datos registrados
- Calidad de datos
- Tendencias de uso

### 3. Alertas
- Errores de API
- Caída de rendimiento
- Anomalías en datos

## Integración con Frontend

### 1. JavaScript Tracking
```javascript
// Ejemplo de tracking automático
window.addEventListener('load', function() {
    trackPageAccess({
        page_url: window.location.pathname,
        page_title: document.title,
        section: getCurrentSection(),
        time_on_page: 0,
        scroll_depth: 0,
        interactions: 0
    });
});
```

### 2. Eventos de Usuario
```javascript
// Tracking de scroll
window.addEventListener('scroll', function() {
    updateScrollDepth();
});

// Tracking de interacciones
document.addEventListener('click', function() {
    incrementInteractions();
});
```

### 3. User Journey
```javascript
// Inicio de journey
startUserJourney({
    entry_page: window.location.pathname,
    session_id: generateSessionId()
});

// Actualización de journey
updateUserJourney({
    page_url: window.location.pathname,
    time_on_page: calculateTimeOnPage()
});
```

## Roadmap

### Fase 1 (Actual)
- ✅ Registro básico de accesos
- ✅ Análisis de secciones
- ✅ Métricas de rendimiento
- ✅ User journey básico

### Fase 2 (Próxima)
- 🔄 Análisis de cohortes
- 🔄 Heatmaps de secciones
- 🔄 A/B testing integration
- 🔄 Machine learning para predicciones

### Fase 3 (Futura)
- 📋 Real-time analytics
- 📋 Personalización automática
- 📋 Integración con CRM
- 📋 API para terceros 