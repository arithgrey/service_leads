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

        # Parámetros predeterminados para crear el lead
        defaults = {
            "email": fake.email(), 
            "name": fake.name(),
            "phone_number": fake.phone_number().split('x')[0].strip(),
            "lead_type": LeadType.objects.create(name="En intento de compra"),
            "store_id": 1
        }

        lead_data = {**defaults, **request.query_params}        
        
        for key, value in lead_data.items():
            if isinstance(value, list):
                lead_data[key] = value[0]
    
        Lead.objects.create(**lead_data)
        serializer = LeadSerializer(lead_data)
        transaction.set_rollback(True)

        data = serializer.data
        data['products_interest_ids'] = [1,3,5]
        return Response(data, status=201)
    
    except Exception as e:
        return Response({'error': str(e)}, status=500)
