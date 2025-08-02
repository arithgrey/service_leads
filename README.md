# Service Leads - Microservicio de Gestión de Leads

Este microservicio maneja la gestión de leads, métricas y analytics de páginas para el sistema Enid.

## 🚀 Inicio Rápido

### Requisitos
- Docker
- Docker Compose

### Levantar el servicio
```bash
# Desde la raíz del proyecto
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f microservice_enid
```

## 📊 Comandos de Analytics de Páginas (page_analytics)

### Generar datos de prueba
```bash
# Generar 100 registros de PageAccess (por defecto)
docker-compose exec microservice_enid python manage.py generate_page_analytics_data

# Generar cantidad personalizada
docker-compose exec microservice_enid python manage.py generate_page_analytics_data --count=500

# Generar datos para días específicos
docker-compose exec microservice_enid python manage.py generate_page_analytics_data --days=7
```

### Limpiar datos de prueba
```bash
# Limpiar todos los datos de analytics
docker-compose exec microservice_enid python manage.py clear_page_analytics_data

# Limpiar solo PageAccess y UserJourney (mantener secciones)
docker-compose exec microservice_enid python manage.py clear_page_analytics_data --keep-sections
```

### Ejecutar tests de page_analytics
```bash
# Ejecutar todos los tests
docker-compose exec microservice_enid python manage.py test page_analytics

# Ejecutar tests con verbosidad alta
docker-compose exec microservice_enid python manage.py test page_analytics --verbosity=2

# Ejecutar tests específicos
docker-compose exec microservice_enid python manage.py test page_analytics.tests.PageAccessModelTest
```

## 📈 Comandos de Métricas de Leads (lead_metrics)

### Generar datos de prueba para leads
```bash
# Generar leads realistas
docker-compose exec microservice_enid python manage.py generate_realistic_leads

# Generar leads para testing de tendencias
docker-compose exec microservice_enid python manage.py generate_test_trends

# Generar leads distribuidos
docker-compose exec microservice_enid python manage.py generate_distributed_leads
```

### Limpiar datos de leads
```bash
# Limpiar todos los leads de prueba
docker-compose exec microservice_enid python manage.py clear_test_leads
```

### Ejecutar tests de lead_metrics
```bash
# Ejecutar todos los tests
docker-compose exec microservice_enid python manage.py test lead_metrics

# Ejecutar tests con verbosidad alta
docker-compose exec microservice_enid python manage.py test lead_metrics --verbosity=2
```

## 🗄️ Comandos de Base de Datos

### Migraciones
```bash
# Crear migraciones
docker-compose exec microservice_enid python manage.py makemigrations

# Aplicar migraciones
docker-compose exec microservice_enid python manage.py migrate

# Ver estado de migraciones
docker-compose exec microservice_enid python manage.py showmigrations
```

### Shell de Django
```bash
# Abrir shell interactivo
docker-compose exec microservice_enid python manage.py shell

# Ejecutar comando específico en shell
docker-compose exec microservice_enid python manage.py shell -c "from page_analytics.models import PageAccess; print(PageAccess.objects.count())"
```

## 🔍 Comandos de Inspección

### Verificar datos
```bash
# Contar registros de PageAccess
docker-compose exec microservice_enid python manage.py shell -c "from page_analytics.models import PageAccess; print(f'Total PageAccess: {PageAccess.objects.count()}')"

# Contar registros de Lead
docker-compose exec microservice_enid python manage.py shell -c "from lead.models import Lead; print(f'Total Leads: {Lead.objects.count()}')"

# Ver URLs disponibles
docker-compose exec microservice_enid python manage.py shell -c "from django.urls import reverse; print('page-access-list:', reverse('page-access-list'))"
```

### Logs y debugging
```bash
# Ver logs del contenedor
docker-compose logs microservice_enid

# Ver logs en tiempo real
docker-compose logs -f microservice_enid

# Ver logs de PostgreSQL
docker-compose logs lead_postgres
```

## 🌐 Endpoints Disponibles

### Page Analytics
- **Listar PageAccess**: `GET /page-analytics/page-access/`
- **Resumen de Analytics**: `GET /page-analytics/page-access/summary/`
- **Tendencias**: `GET /page-analytics/page-access/trends/`
- **Secciones**: `GET /page-analytics/page-access/sections/`
- **Rendimiento**: `GET /page-analytics/page-access/performance/`
- **Secciones Activas**: `GET /page-analytics/page-sections/active/`
- **User Journey Analytics**: `GET /page-analytics/user-journey/analytics/`
- **Rendimiento por Fecha**: `GET /page-analytics/page-performance/by_date/`

### Lead Metrics
- **Resumen de Leads**: `GET /lead-metrics/overview/`
- **Métricas por Status**: `GET /lead-metrics/status/`
- **Métricas por Tipo**: `GET /lead-metrics/type/`
- **Tendencias**: `GET /lead-metrics/trends/`
- **Métricas Diarias**: `GET /lead-metrics/daily/`

### Leads
- **Listar Leads**: `GET /lead/`
- **Buscar Leads**: `GET /lead-search/?q=query&status=pending`

## 🧪 Testing

### Ejecutar todos los tests
```bash
docker-compose exec microservice_enid python manage.py test
```

### Ejecutar tests específicos
```bash
# Tests de page_analytics
docker-compose exec microservice_enid python manage.py test page_analytics

# Tests de lead_metrics
docker-compose exec microservice_enid python manage.py test lead_metrics

# Tests de lead
docker-compose exec microservice_enid python manage.py test lead

# Tests de lead_search
docker-compose exec microservice_enid python manage.py test lead_search
```

### Tests con cobertura
```bash
# Instalar pytest si no está disponible
docker-compose exec microservice_enid pip install pytest pytest-cov

# Ejecutar tests con cobertura
docker-compose exec microservice_enid python -m pytest page_analytics/tests.py --cov=page_analytics --cov-report=html
```

## 🔧 Mantenimiento

### Reiniciar servicios
```bash
# Reiniciar solo el microservicio
docker-compose restart microservice_enid

# Reiniciar todo el stack
docker-compose down && docker-compose up -d
```

### Limpiar contenedores
```bash
# Parar y eliminar contenedores
docker-compose down

# Parar y eliminar contenedores + volúmenes
docker-compose down -v

# Eliminar imágenes
docker-compose down --rmi all
```

### Backup de base de datos
```bash
# Crear backup
docker-compose exec lead_postgres pg_dump -U user_dev db_dev > backup.sql

# Restaurar backup
docker-compose exec -T lead_postgres psql -U user_dev db_dev < backup.sql
```

## 📝 Notas Importantes

### URLs de Desarrollo vs Producción
- **Desarrollo local**: Los endpoints están disponibles en `http://localhost:8086/`
- **Con reverse proxy**: Los endpoints usan el prefijo `/api/lead/`

### Ejemplos de URLs:
- **Desarrollo**: `http://localhost:8086/page-analytics/page-access/`
- **Producción**: `http://localhost:8086/api/lead/page-analytics/page-access/`

### Variables de Entorno
El servicio usa las siguientes variables de entorno (definidas en docker-compose.yml):
- `POSTGRES_DB`: db_dev
- `POSTGRES_USER`: user_dev
- `POSTGRES_PASSWORD`: password_dev
- `DEBUG`: True (desarrollo)

## 🚨 Troubleshooting

### Problemas comunes

1. **Error de conexión a base de datos**
   ```bash
   # Verificar que PostgreSQL esté corriendo
   docker-compose ps
   
   # Reiniciar PostgreSQL
   docker-compose restart lead_postgres
   ```

2. **Migraciones no aplicadas**
   ```bash
   # Aplicar migraciones manualmente
   docker-compose exec microservice_enid python manage.py migrate
   ```

3. **Tests fallando**
   ```bash
   # Verificar que las tablas existan
   docker-compose exec microservice_enid python manage.py showmigrations
   
   # Recrear base de datos de test
   docker-compose exec microservice_enid python manage.py test --keepdb
   ```

4. **Endpoints no responden**
   ```bash
   # Verificar que el servicio esté corriendo
   docker-compose ps
   
   # Ver logs del servicio
   docker-compose logs microservice_enid
   ```

## 📚 Documentación Adicional

- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django ORM](https://docs.djangoproject.com/en/4.2/topics/db/)
- [PostgreSQL](https://www.postgresql.org/docs/)
- [Docker Compose](https://docs.docker.com/compose/)

---

**Desarrollado para el sistema Enid**  
*Última actualización: Agosto 2025* 