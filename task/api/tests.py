import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class TestSetUp(APITestCase):

    def setUp(self) -> None:

        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.tasks_api = reverse('tasks')
        self.create_task_api = reverse('create_task')

        self.task_data = {
            "title": "string",
            "text": "string",
            "date": "2020-12-04"
        }

        # reg + auth
        data = {
            "email": "testmail@mail.com",
            "password": "password12345"
        }
        self.client.post(self.register_url, data=data, format='json')
        response = self.client.post(self.login_url, data=data, format='json')
        tokens = json.loads(response.data['tokens'].replace('\'', '\"'))
        self.token = 'Token ' + tokens['access']
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()


class TaskTests(TestSetUp):
    def test_tasks(self):
        response = self.client.get(self.tasks_api, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        response = self.client.post(self.create_task_api, data=self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.task_data['title'])
        self.assertEqual(response.data['text'], self.task_data['text'])
        self.assertEqual(response.data['date'], self.task_data['date'])

    def test_create_task_with_none_data(self):
        response = self.client.post(self.create_task_api, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_task_with_invalid_data(self):
        data = {
            "title": "",
            "text": "",
            "date": "dalsjdl2020-12-04"
        }
        response = self.client.post(self.create_task_api, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_task_by_id_api(self):
        create = self.client.post(self.create_task_api, data=self.task_data, format='json')
        response = self.client.get(reverse('task_by_id', kwargs={'pk': 1}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], create.data['title'])
        self.assertEqual(response.data['text'], create.data['text'])
        self.assertEqual(response.data['date'], create.data['date'])

        response = self.client.get(reverse('task_by_id', kwargs={'pk': 100}), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_set_as_complete(self):
        create = self.client.post(self.create_task_api, data=self.task_data, format='json')
        response = self.client.get(reverse('set_as_complete', kwargs={'pk': 1}), format='json')
        get_by_id = self.client.get(reverse('task_by_id', kwargs={'pk': 1}), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_by_id.data['is_complete'], True)

        response = self.client.get(reverse('set_as_complete', kwargs={'pk': 100}), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task(self):
        self.client.post(self.create_task_api, data=self.task_data, format='json')
        response = self.client.delete(reverse('delete_task', kwargs={'pk': 1}), format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        response = self.client.delete(reverse('delete_task', kwargs={'pk': 1}), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
