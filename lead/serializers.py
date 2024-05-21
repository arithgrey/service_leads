from rest_framework import serializers
from lead.models import Lead

class LeadSerializer(serializers.ModelSerializer):
    products_interest_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    class Meta:
        model = Lead
        fields = '__all__'