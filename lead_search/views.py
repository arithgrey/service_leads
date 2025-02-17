from rest_framework import viewsets, status
from rest_framework.response import Response
from lead.models import Lead
from lead_search.serializers import LeadSearchSerializer
from django.db.models import Q
from rest_framework.decorators import action

class LeadSearchViewSet(viewsets.ViewSet):
        
    def search(self, request):
        leads = self.perform_search(request)        
        serializer = LeadSearchSerializer(leads, many=True)
        return Response(serializer.data)
    
    def perform_search(self, request):
        q = request.query_params.get('q', '')
        status = request.query_params.get('status', 'pending')
        limit = request.query_params.get('limit', 30)
        
        # Si status es 'all', comenzamos con todos los leads
        if status == 'all':
            queryset = Lead.objects.all()
        else:
            # Si no, filtramos por el status específico
            queryset = Lead.objects.filter(status=status)

        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |        
                Q(email__icontains=q) |            
                Q(phone_number__icontains=q)
            )
            
        return queryset.order_by('-created_at')[:int(limit)]