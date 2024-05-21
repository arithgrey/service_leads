from django.test import TestCase
from django.urls import reverse
from rest_framework import status

class TestsLeadSearchViewSet(TestCase):
        
    def setUp(self):
        super().setUp()
        self.api = reverse('lead_search:lead-search')
        self.headers = {'HTTP_X_STORE_ID': 1}
        self.api_lead =reverse('fake_lead')


    def test_success_on_simple_search(self):
            
        response = self.client.get(self.api, {},format='json')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_success_search_by_email(self):

        email="jmedrano@9006.com"
        data = {'email':email}
        self.client.get(self.api_lead, data=data, format='json', **self.headers).json()
       
        response = self.client.get(
            self.api, {"q":email, 'status':'pending'},
            format='json',  
            **self.headers
            )    
            
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)



    def test_success_search_by_name(self):

        name="jonathan Medrano"
        data = {'name':name}
        self.client.get(self.api_lead, data=data, format='json', **self.headers).json()

        response = self.client.get(
            self.api, {"q":name, 'status':'pending'},
            format='json',  
            **self.headers
            )        
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    
    
    def test_success_search_by_phone_number(self):

        phone_number="5552967027"
        data = {'phone_number':phone_number}

        self.client.get(self.api_lead, data=data, format='json', **self.headers).json()

        response = self.client.get(
            self.api, {"q":phone_number, 'status':'pending'},
            format='json',  
            **self.headers
            )        
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    def test_success_search_by_10_results(self):    

        for _ in range(10):
            self.client.get(self.api_lead, format='json', **self.headers).json()

        response = self.client.get(
            self.api, {'status':'pending'},
            format='json',  
            **self.headers
            )        
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 10)


    def test_by_status(self):

        data = {'status':'discarded'}

        self.client.get(self.api_lead, data=data, format='json', **self.headers).json()

        response = self.client.get(
            self.api, {'status':'discarded'},
            format='json',  
            **self.headers
            )                
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 1)
