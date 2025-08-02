from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'page-access', views.PageAccessViewSet, basename='page-access')
router.register(r'page-sections', views.PageSectionViewSet, basename='page-sections')
router.register(r'user-journey', views.UserJourneyViewSet, basename='user-journey')
router.register(r'page-performance', views.PagePerformanceViewSet, basename='page-performance')

urlpatterns = router.urls 