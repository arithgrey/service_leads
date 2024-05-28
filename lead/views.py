from rest_framework import viewsets, status
from lead.serializers import LeadSerializer
from lead.models import Lead
from lead_type.models import LeadType
from rest_framework.decorators import action
from rest_framework.response import Response
import json

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    @action(detail=False, methods=['post'], url_path='existence')
    def existence(self, request):
        data = request.data
        store_id = request.headers.get('X-Store-Id')

        if store_id is None:
            return Response({'error': 'X-Store-Id header is missing'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LeadSerializer(data=data)
        if serializer.is_valid():
            email = data.get('email')
            name = data.get('name')
            phone_number = data.get('phone_number')
            lead_type = data.get('lead_type')
            products_interest = data.get('products_interest', [])

            defaults = {
                'lead_type': LeadType.objects.get(id=lead_type),
                'name': name,
                'phone_number': phone_number,
                'email': email,
                'store_id': store_id,
                'products_interest_ids': json.dumps(products_interest)
            }

            lead, created = Lead.objects.get_or_create(email=email, defaults=defaults)

            if created:
                serializer = LeadSerializer(lead)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return self.tryet_or_create(obj_lead=lead, data=defaults, new_lead_type=lead_type)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def tryet_or_create(self, obj_lead, data, new_lead_type):
        if obj_lead.lead_type.id != new_lead_type:
            new_lead = Lead.objects.create(**data)
            serializer = LeadSerializer(new_lead)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            for key, value in data.items():
                if key == 'products_interest':
                    value = json.dumps(value)
                    key = 'products_interest_ids'
                setattr(obj_lead, key, value)
            obj_lead.tryet += 1
            obj_lead.save()
            serializer = LeadSerializer(obj_lead)
            return Response(serializer.data, status=status.HTTP_200_OK)
