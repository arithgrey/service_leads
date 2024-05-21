from django.test import TestCase
from rest_framework.test import APIClient
from lead.models import Lead
from lead_type.models import LeadType
from faker import Faker
from django.urls import reverse

class TestsLeadViewSet(TestCase):
    def setUp(self):
        self.fake = Faker('es_MX')
        self.client = APIClient()
        self.lead_type = LeadType.objects.create(name="En intento de compra")
        self.api_existence = reverse('lead-existence')
        self.api_lead =reverse('fake_lead')
        self.headers = {'HTTP_X_STORE_ID': 1}
        

    def test_success_create_lead(self):
        
        data = {'wjs':True}
        fake_lead = self.client.get(
            self.api_lead, data=data, format='json',**self.headers).json()
        
        
        response = self.client.post(self.api_existence, data=fake_lead, format='json', **self.headers)
        
        self.assertEqual(response.status_code, 201)        
        self.assertEqual(Lead.objects.count(),1)



    def test_success_create_lead_with_interest_products(self):
        
        data = {'wjs':True, 'products_interest_ids': [1,3,44,49]}
        fake_lead = self.client.get(
            self.api_lead, data=data, format='json',**self.headers).json()
        
        response = self.client.post(self.api_existence, data=fake_lead, format='json', **self.headers)
        self.assertEqual(response.status_code, 201)        
        self.assertEqual(Lead.objects.count(),1)

        self.assertGreaterEqual(len(response.data['products_interest_ids']), 1)
        self.assertEqual(response.data["products_interest_ids"], fake_lead['products_interest_ids'])
    


    def test_success_handler_response_400s(self):
                                
        response = self.client.post(
            self.api_existence, {}, format='json')                                            
        self.assertEqual(response.status_code, 400)        

    
    def test_success_create_lead_when_diferent_type(self):
        
        other_type = LeadType.objects.create(name="other type")

        fake_lead = self.client.get(
            self.api_lead, format='json',**self.headers).json()
        
        email = fake_lead['email']
        store_id = fake_lead['store_id']
        data = {
            'email': email,
            'lead_type':other_type.id,
            'name':fake_lead['name'] ,
            'phone_number':'5552967027',
            'store':store_id,
            }
                
        response = self.client.post(
            self.api_existence, data, format='json', **self.headers)          
        
        self.assertEqual(response.data["tryet"], 1)
        self.assertEqual(response.status_code, 201)        
        self.assertEqual(email, response.data["email"])
        self.assertEqual(Lead.objects.filter(email=email).count(), 2)


    def test_success_add_triet_lead(self):
        
        fake_lead = self.client.get(
            self.api_lead, format='json',**self.headers).json()     

        fake_lead = Lead.objects.get(id=fake_lead['id'])   
        self.assertEqual(fake_lead.tryet, 1)
        lead_type = fake_lead.lead_type.id

        data = {
            'email': fake_lead.email,
            'lead_type':lead_type,
            'name':fake_lead.name ,
            'phone_number':'5552967027',
            'store':fake_lead.store_id
            }

        response = self.client.post(
            self.api_existence, data, format='json', **self.headers)
        
        self.assertEqual(response.data["tryet"], 2)
        self.assertEqual(response.status_code, 200)        
        self.assertEqual(response.data["phone_number"], "5552967027")