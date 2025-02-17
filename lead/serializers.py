from rest_framework import serializers
from lead.models import Lead
import json

class LeadSerializer(serializers.ModelSerializer):
    products_interest = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    status_choices = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = ['id', 'name', 'email', 'phone_number', 'lead_type', 'created_at', 
                 'status', 'status_display', 'status_choices', 'products_interest', 
                 'products_interest_ids']
        extra_kwargs = {
            'products_interest_ids': {'write_only': True}
        }

    def get_products_interest(self, obj):
        if obj.products_interest_ids:
            return json.loads(obj.products_interest_ids)
        return []

    def get_status_choices(self, obj):
        return [
            {'value': status[0], 'label': status[1]} 
            for status in Lead.STATUS_CHOICES
        ]

class LeadSearchSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    status_choices = serializers.SerializerMethodField()
    lead_type_name = serializers.CharField(source='lead_type.name', read_only=True)

    class Meta:
        model = Lead
        fields = ['id', 'name', 'email', 'phone_number', 'lead_type', 'lead_type_name', 
                 'created_at', 'status', 'status_display', 'status_choices']

    def get_status_choices(self, obj):
        return [
            {'value': status[0], 'label': status[1]} 
            for status in Lead.STATUS_CHOICES
        ]
