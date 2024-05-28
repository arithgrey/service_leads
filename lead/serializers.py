from rest_framework import serializers
from lead.models import Lead
import json

class LeadSerializer(serializers.ModelSerializer):
    products_interest = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_empty=True
    )

    class Meta:
        model = Lead
        fields = '__all__'
        extra_kwargs = {
            'products_interest_ids': {'write_only': True}
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['products_interest'] = instance.get_products_interest_ids()
        return representation

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        products_interest = data.get('products_interest', [])
        internal_value['products_interest_ids'] = json.dumps(products_interest)
        return internal_value
