import xml.etree.ElementTree as ET
from django.urls import reverse
from rest_framework.test import APITestCase
from pizza.models import OrderMessageConfig,Crust,Order,Topping


class WelcomeTests(APITestCase):
    def setUp(self):
        OrderMessageConfig.objects.create(
            welcome_message="Hello and welcome to the pyPizza shop"
        )
        #create some crusts
        Crust.objects.create(size=1,price=400)
        Crust.objects.create(size=2,price=500)
        Crust.objects.create(size=3,price=600)
        Crust.objects.create(size=4,price=700)
        #create some toppings
        Topping.objects.create(name="pepperoni",price=300)
        Topping.objects.create(name="hawaiian",price=200)
        Topping.objects.create(name="BBQ chicken",price=500)


    def test_welcome_message(self):
        url = reverse('welcome')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        response_xml_as_text = response.content.decode('utf-8')
        with open('x_welcome.txt') as f:
            self.assertXMLEqual(response_xml_as_text,f.read())
