from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import TodoList, TodoItem

# Create your tests here.

JWT_URL = 'http://localhost:8000/api/token/'
TODO_LIST_1 = {"name": "Friday Reunion"}
TODO_LIST_2 = {"name": "Home Chores"}
TODO_LIST_3 = {"name": "Backyard Renovation"}
TODO_LIST_4 = {"name": "Kitchen Makeover"}
TODO_ITEMS_1 = [
    {"name": "Buy Coke", "list_id": "1", "status": "PE", "priority": "M"},
    {"name": "Buy Sauce", "list_id": "1", "status": "PE", "priority": "H"},
    {"name": "Broom Floor", "list_id": "1", "status": "FI", "priority": "L"}
]
TODO_ITEMS_2 = [
    {"name": "Wash Windows", "list_id": "2", "status": "PE", "priority": "L"},
    {"name": "Vacuum", "list_id": "2", "status": "PE", "priority": "H"}
]
TODO_ITEMS_3 = [
    {"name": "Cut Grass", "list_id": "3", "status": "FI", "priority": "M"},
    {"name": "Remove Weeds", "list_id": "3", "status": "FI", "priority": "M"}
]
TODO_ITEMS_4 = []

LISTS = [TODO_LIST_1, TODO_LIST_2, TODO_LIST_3, TODO_LIST_4]
ITEMS = [TODO_ITEMS_1, TODO_ITEMS_2, TODO_ITEMS_3, TODO_ITEMS_4]


class RegisterUserTest(APITestCase):

    def test_register_user(self):
        url = 'http://localhost:8000/api/user'
        data = {"username": "test_user", "email": "test@gmail.com", "password": "test77test", "first_name": "Test",
                "last_name": "Case"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test_user')

    def test_view_my_info(self):
        url = 'http://localhost:8000/api/user'
        data = {"username": "test_user", "email": "test@gmail.com", "password": "test77test", "first_name": "Test",
                "last_name": "Case"}
        self.client.post(url, data, format='json')
        response = self.client.post(JWT_URL, {"username": "test_user", "password": "test77test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        url = 'http://localhost:8000/api/user'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test_user')
        self.assertEqual(User.objects.get().first_name, 'Test')


class ExpenseViewSetTest(APITestCase):
    username = "test_user"
    email = "test@gmail.com"
    password = "test77test"

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username=cls.username, email=cls.email, password=cls.password)

    def addLists(self):
        url = reverse('api:list-list')
        for todo_list in LISTS:
            self.client.post(url, todo_list, format='json')

    def addItems(self):
        url = reverse('api:item-list')
        for todo_item in ITEMS:
            for item in todo_item:
                self.client.post(url, item, format='json')

    def authenticate(self):
        response = self.client.post(JWT_URL, {"username": self.username, "password": self.password})
        assert response.status_code == status.HTTP_200_OK
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

    def test_can_create_todo_list(self):
        self.authenticate()
        url = reverse('api:list-list')
        response = self.client.post(url, TODO_LIST_1, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        self.assertEqual(TodoList.objects.count(), 1)
        self.client.post(url, TODO_LIST_2, format='json')
        self.assertEqual(TodoList.objects.count(), 2)
        self.assertEqual(TodoList.objects.first().name, "Friday Reunion")
        self.assertEqual(TodoList.objects.first().owner.username, self.username)

    def test_can_create_todo_item(self):
        self.authenticate()
        self.addLists()
        url = reverse('api:item-list')
        response = self.client.post(url, TODO_ITEMS_1[0], format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TodoItem.objects.count(), 1)
        self.client.post(url, TODO_ITEMS_1[1], format='json')
        self.assertEqual(TodoItem.objects.count(), 2)
        self.assertEqual(TodoItem.objects.first().name, "Buy Coke")
        self.assertEqual(TodoItem.objects.first().list_id.owner.username, self.username)
