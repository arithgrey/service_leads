from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from lead.models import Lead, LeadType
from lead.serializers import LeadSerializer
from faker import Faker

@transaction.atomic
@api_view(['GET'])
def fake_lead(request):
    try:
        fake = Faker('es_MX')
        wjs = request.query_params.get('wjs', '').lower() == 'true'
        lead_type = LeadType.objects.create(name="En intento de compra")
        
        if wjs:
            lead_type = lead_type.id

        defaults = {
            "email": fake.email(), 
            "name": fake.name(),
            "phone_number": fake.phone_number().split('x')[0].strip(),
            "lead_type": lead_type,
            "store_id": 1,
            'products_interest_ids':[1,3,5],
        }

        query_params_copy = request.query_params.copy()
        lead_data = {**defaults, **query_params_copy}

        for key, value in lead_data.items():
            if isinstance(value, list) and key == 'products_interest_ids':
                lead_data[key] = value
            elif isinstance(value, list):
                lead_data[key] = value[0]
    
        
        if wjs:
            serializer = LeadSerializer(data=lead_data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data
            return Response(data, status=201)
        
        lead = Lead.objects.create(**lead_data)
        serializer = LeadSerializer(lead)
        data = serializer.data        
        return Response(data, status=201)
    
    except Exception as e:
        return Response({'error': str(e)}, status=500)
