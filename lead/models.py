from django.db import models
from lead_type.models import LeadType
import json

class Lead(models.Model):
    
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('contacted', 'Contactado'),
        ('discarded', 'Descartado'),
        ('process', 'En proceso'),
        ('converted', 'Convertido'),        
    )   

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True, blank=True)    
    lead_type = models.ForeignKey(LeadType, related_name='leads', on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    tryet = models.IntegerField(default=1, null=False)
    products_interest_ids = models.TextField(null=True, blank=True)
    store_id = models.IntegerField(default=1,null=False, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')        

    def __str__(self):
        return self.name

    def set_products_interest_ids(self, ids):
        self.products_interest_ids = json.dumps(ids)
