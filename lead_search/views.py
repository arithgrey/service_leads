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
    
    
    def perform_search(self,request):
        
        q = request.query_params.get('q', None)        
        status = request.query_params.get('status', 'pending')        
        
        if q is None:            

            return Lead.objects.filter(
                status=status).order_by('-created_at')[:30]

        else:   
            
            return Lead.objects.filter(
                Q(name__icontains=q) |        
                Q(email__icontains=q) |            
                Q(phone_number__icontains=q),   
                status=status
            )