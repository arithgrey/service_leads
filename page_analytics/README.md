# Page Analytics API

Esta aplicación permite registrar y analizar accesos a páginas web y sus secciones para mejorar la experiencia del usuario día a día.

## Modelos

### PageAccess
Registra cada acceso a una página o sección específica.

**Campos principales:**
- `page_url`: URL de la página accedida
- `section`: Sección específica de la página
- `user_id`: ID del usuario (si está autenticado)
- `session_id`: ID de sesión del usuario
- `device_type`: Tipo de dispositivo (mobile, desktop, tablet)
- `browser`: Navegador utilizado
- `time_on_page`: Tiempo en la página en segundos
- `scroll_depth`: Profundidad de scroll en porcentaje
- `interactions`: Número de interacciones

### PageSection
Define secciones de páginas y sus métricas.

### UserJourney
Rastrea el journey del usuario a través de múltiples páginas.

### PagePerformance
Métricas de rendimiento de páginas por fecha.

## Endpoints

### PageAccess

#### GET `/page-analytics/page-access/`
Lista todos los registros de acceso a páginas.

#### POST `/page-analytics/page-access/`
Registra un nuevo acceso a página.

**Ejemplo:**
```json
{
  "page_url": "/productos",
  "page_title": "Productos - Tienda",
  "section": "productos-destacados",
  "user_id": "user123",
  "session_id": "session456",
  "device_type": "desktop",
  "browser": "Chrome",
  "time_on_page": 120,
  "scroll_depth": 75,
  "interactions": 5
}
```

#### GET `/page-analytics/page-access/summary/`
Obtiene resumen de analytics.

**Parámetros:**
- `days`: Número de días hacia atrás (default: 30)

**Respuesta:**
```json
{
  "total_page_views": 1500,
  "unique_visitors": 450,
  "avg_session_duration": 180.5,
  "bounce_rate": 35.2,
  "top_pages": [
    {"page_url": "/", "views": 300},
    {"page_url": "/productos", "views": 250}
  ],
  "top_sections": [
    {"section": "header", "views": 150},
    {"section": "hero", "views": 120}
  ],
  "device_distribution": {
    "desktop": 60,
    "mobile": 35,
    "tablet": 5
  },
  "browser_distribution": {
    "Chrome": 45,
    "Firefox": 25,
    "Safari": 20
  }
}
```

#### GET `/page-analytics/page-access/trends/`
Obtiene tendencias de analytics.

**Parámetros:**
- `days`: Número de días (default: 7)

**Respuesta:**
```json
[
  {
    "date": "2024-01-01",
    "page_views": 150,
    "unique_visitors": 45,
    "avg_time_on_page": 180.5,
    "bounce_rate": 35.2
  }
]
```

#### GET `/page-analytics/page-access/sections/`
Obtiene analytics por secciones.

**Parámetros:**
- `days`: Número de días (default: 30)

#### GET `/page-analytics/page-access/performance/`
Obtiene métricas de rendimiento.

**Parámetros:**
- `days`: Número de días (default: 30)

### PageSection

#### GET `/page-analytics/page-sections/`
Lista todas las secciones de página.

#### POST `/page-analytics/page-sections/`
Crea una nueva sección de página.

#### GET `/page-analytics/page-sections/active/`
Obtiene solo secciones activas.

### UserJourney

#### GET `/page-analytics/user-journey/`
Lista todos los user journeys.

#### POST `/page-analytics/user-journey/`
Crea un nuevo user journey.

#### GET `/page-analytics/user-journey/analytics/`
Obtiene analytics de user journey.

### PagePerformance

#### GET `/page-analytics/page-performance/`
Lista todas las métricas de rendimiento.

#### POST `/page-analytics/page-performance/`
Crea nuevas métricas de rendimiento.

#### GET `/page-analytics/page-performance/by_date/`
Obtiene rendimiento por fecha.

**Parámetros:**
- `date`: Fecha en formato YYYY-MM-DD

## Comandos de Gestión

### Generar datos de prueba
```bash
python manage.py generate_page_analytics_data --count 100 --days 30
```

### Limpiar datos
```bash
python manage.py clear_page_analytics_data
```

### Limpiar datos incluyendo secciones
```bash
python manage.py clear_page_analytics_data --sections
```

## Casos de Uso

### 1. Tracking de Páginas
Registrar cada acceso a una página para analizar:
- Páginas más visitadas
- Tiempo promedio en página
- Tasa de rebote
- Dispositivos más utilizados

### 2. Tracking de Secciones
Analizar el comportamiento en secciones específicas:
- Secciones más vistas
- Engagement por sección
- Conversiones por sección

### 3. User Journey
Rastrear el camino del usuario:
- Páginas de entrada más comunes
- Páginas de salida más comunes
- Flujo de navegación
- Metas de conversión alcanzadas

### 4. Rendimiento
Monitorear el rendimiento de las páginas:
- Tiempos de carga
- Tasas de conversión
- Métricas de tráfico

## Mejoras Continuas

Esta aplicación permite:

1. **Identificar páginas problemáticas** con alta tasa de rebote
2. **Optimizar secciones** con bajo engagement
3. **Mejorar user journey** analizando flujos de navegación
4. **Optimizar rendimiento** monitoreando tiempos de carga
5. **Personalizar experiencia** basándose en dispositivos y navegadores más utilizados 