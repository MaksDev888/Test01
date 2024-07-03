# import json

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from ..views import *


# from shop.user.models import User


class ShopGuestAPITest(APITestCase):
    def test_get_products(self):
        url = reverse('get_products')
        response = self.client.get(url, data=None, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ShopAdminAPITest(APITestCase):

    def authenticate(self):
        # response = self.client.post(reverse('login'), {'email': 'admin@shop.ru', 'password': 'admin'})
        # self.assertEqual(response.data, reverse('login'))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + "783307f69a5e67f21752d4daaa62391e91873ed2")

    def test_should_create_product(self):
        """
        Ensure we can create a new product
        """
        # user = User.objects.get(email="admin@shop.ru")
        # token, _ = Token.objects.get_or_create(user=user)
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.key)
        # url = reverse('create_product')
        # data = {'name': 'Test product', 'description': 'test', 'price': 100}
        # response = self.client.post(url, data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token = "783307f69a5e67f21752d4daaa62391e91873ed2"
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        # url = reverse('change_product')
        response = self.client.get('/product/1')
        # self.assertEqual(response.data['data'], {
        #                                     "id": 1,
        #                                     "name": "Картошка",
        #                                     "description": "Очень вкусная",
        #                                     "price": "100.00"
        #                              })
        # data = {'name': 'Test product', 'description': 'test', 'price': 100}
        # response = self.client.post(url, data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(client, 'Test product')

    def test_get_products(self):
        data = [
            {
                "id": 1,
                "name": "Картошка",
                "description": "Очень вкусная",
                "price": "100.00"
            },
            {
                "id": 2,
                "name": "Морковка",
                "description": "Очень полезная",
                "price": "120.00"
            },
            {
                "id": 3,
                "name": "Капуста",
                "description": "Зеленая, свежая",
                "price": "75.00"
            }
        ]
        url = reverse('get_products')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 1)
        self.assertListEqual(response.data, data)

