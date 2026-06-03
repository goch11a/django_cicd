from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from .views import OrderItemViewset, OrderViewset, ProductViewset
from rest_framework.authtoken.models import Token
from .models import Product, Order, OrderItem


class ProductTest(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username='zuka', password='zuka')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.product = Product.objects.create(name='item1', description='good item', price=8.15, stock=5)


    def test_product_list(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_created_product_authenticated(self):
        data = {'name':'new_product', 'description':'bad quality', 'price':1.20, 'stock':1200}
        response = self.client.post(reverse('product-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

    def test_created_product_unauthenticated(self):
        self.client.credentials()
        data = {'name':'new_product', 'description':'bad quality', 'price':1.20, 'stock':1200}
        response = self.client.post(reverse('product-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        

class OrderTest(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username='deme', password='deme')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.product = Product.objects.create(name='item2', description='nice item', price=10.30, stock=3)
        

    def test_created_order_authenticated(self):
        response = self.client.post(reverse('order-list'), {'user':self.user.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_order_unauthenticated(self):
        self.client.credentials()
        response = self.client.post(reverse('order-list'), {'user':self.user.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticationTest(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username='zuka', password='zuka')
        self.token = Token.objects.create(user=self.user)

    def test_acces_protected_endpoint_with_authentification(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_acces_protected_endpoint_without_authentification(self):
        self.client.credentials()
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
