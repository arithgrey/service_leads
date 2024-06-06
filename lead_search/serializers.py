# serializers.py
from rest_framework import serializers
from lead.models import Lead
import json


class LeadSearchSerializer(serializers.ModelSerializer):
    
    products = serializers.SerializerMethodField() 

    class Meta:
        model = Lead
        fields = ['id', 'name', 'email', 'phone_number', 'status','created_at','products']
    
    def get_products(self, obj):
        if obj.products_interest_ids:
            return json.loads(obj.products_interest_ids)
        return []