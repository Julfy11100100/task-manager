from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker


class TestSetUp(APITestCase):

    def setUp(self) -> None:

        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.fake = Faker()

        self.user_data = {
            "email": self.fake.email(),
            "password": self.fake.password(),
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()


class AccountTests(TestSetUp):
    def test_register_with_none_data(self):
        data = {}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_valid_data(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_twice(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_none_data(self):
        data = {}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_valid_data(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user_data['email'])

