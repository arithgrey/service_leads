from django.urls import path
from .views import fake_lead

urlpatterns = [
    path('fake_lead/', fake_lead, name='fake_lead'),
]
