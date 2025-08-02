from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lead_metrics import views

router = DefaultRouter()
router.register(r'', views.LeadMetricsViewSet, basename="lead-metrics")

urlpatterns = router.urls 