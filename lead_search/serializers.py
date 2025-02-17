# serializers.py
from rest_framework import serializers
from lead.models import Lead
import json


class LeadSearchSerializer(serializers.ModelSerializer):
    
    products = serializers.SerializerMethodField() 
    status_choices = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Lead
        fields = ['id', 'name', 'email', 'phone_number', 'status', 'status_display', 
                 'created_at', 'products', 'status_choices']
    
    def get_products(self, obj):
        if obj.products_interest_ids:
            return json.loads(obj.products_interest_ids)
        return []
    
    
    def get_status_choices(self, obj):
        return [
            {'value': status[0], 'label': status[1]} 
            for status in Lead.STATUS_CHOICES
        ]