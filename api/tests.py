from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from freezegun import freeze_time
from datetime import timedelta

from api.models import TodoList, TodoItem

# Create your tests here.

JWT_URL = 'http://localhost:8000/api/token/'
TODO_LIST_1 = {"name": "Todo List 1"}
TODO_LIST_2 = {"name": "Todo List 2"}
TODO_LIST_3 = {"name": "Todo List 3"}
TODO_LIST_4 = {"name": "Todo List 4"}
TODO_ITEMS_1 = [
    {"name": "Item 1 List 1", "list_id": "1", "status": "PE", "priority": "M", "duration": "00:45:00"},
    {"name": "Item 2 List 1", "list_id": "1", "status": "PE", "priority": "H", "duration": "15:00:00"},
    {"name": "Item 3 List 1", "list_id": "1", "status": "FI", "priority": "L", "duration": "03:00:00"}
]
TODO_ITEMS_2 = [
    {"name": "Item 1 List 2", "list_id": "2", "status": "PE", "priority": "L", "duration": "1 days"},
    {"name": "Item 2 List 2", "list_id": "2", "status": "PE", "priority": "H"}
]
TODO_ITEMS_3 = [
    {"name": "Item 1 List 3", "list_id": "3", "status": "FI", "priority": "M"},
    {"name": "Item 2 List 3", "list_id": "3", "status": "FI", "priority": "M"}
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
    username = "test_user", "second_user"
    email = "test@gmail.com", "second@gmail.com"
    password = "test77test", "second77second"

    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create_user(username=cls.username[0], email=cls.email[0], password=cls.password[0])
        cls.user_2 = User.objects.create_user(username=cls.username[1], email=cls.email[1], password=cls.password[1])

    def addListsAndItems(self):
        url = reverse('api:list-list')
        for todo_list in LISTS:
            self.client.post(url, todo_list, format='json')
        url = reverse('api:item-list')
        for todo_item in ITEMS:
            for item in todo_item:
                self.client.post(url, item, format='json')

    def authenticate_user_1(self):
        response = self.client.post(JWT_URL, {"username": self.username[0], "password": self.password[0]})
        assert response.status_code == status.HTTP_200_OK
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

    def authenticate_user_2(self):
        response = self.client.post(JWT_URL, {"username": self.username[1], "password": self.password[1]})
        assert response.status_code == status.HTTP_200_OK
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

    def test_addLists_and_addItems_work(self):
        self.authenticate_user_1()
        self.addListsAndItems()
        url = reverse('api:list-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['name'], 'Todo List 1')
        self.assertEqual(response.data[1]['id'], 2)
        self.assertEqual(response.data[1]['name'], 'Todo List 2')
        self.assertEqual(response.data[2]['id'], 3)
        self.assertEqual(response.data[2]['name'], 'Todo List 3')

        url = reverse('api:item-list') + "?list_id=2"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TodoItem.objects.count(), 7)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Item 1 List 2')
        self.assertEqual(response.data[0]['list_id'], 2)
        self.assertEqual(response.data[1]['name'], 'Item 2 List 2')
        self.assertEqual(response.data[1]['list_id'], 2)

    def test_can_create_todo_list(self):
        self.authenticate_user_1()
        url = reverse('api:list-list')
        response = self.client.post(url, TODO_LIST_1, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        self.assertEqual(TodoList.objects.count(), 1)
        self.client.post(url, TODO_LIST_2, format='json')
        self.assertEqual(TodoList.objects.count(), 2)
        self.assertEqual(TodoList.objects.first().name, "Todo List 1")
        self.assertEqual(TodoList.objects.first().owner.username, self.username[0])

    def test_can_create_todo_item(self):
        self.authenticate_user_1()
        url = reverse('api:list-list')
        response = self.client.post(url, TODO_LIST_1, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        url = reverse('api:item-list')
        response = self.client.post(url, TODO_ITEMS_1[0], format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TodoItem.objects.count(), 1)
        self.client.post(url, TODO_ITEMS_1[1], format='json')
        self.assertEqual(TodoItem.objects.count(), 2)
        self.assertEqual(TodoItem.objects.first().name, "Item 1 List 1")
        self.assertEqual(TodoItem.objects.first().list_id.owner.username, self.username[0])

    def test_user_views_own_lists(self):
        self.authenticate_user_2()
        url = reverse('api:list-list')
        response = self.client.post(url, TODO_LIST_1, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        self.authenticate_user_1()
        self.client.post(url, TODO_LIST_2, format='json')
        self.client.post(url, TODO_LIST_3, format='json')
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.assertEqual(TodoList.objects.count(), 3)
        self.assertEqual(len(response.data), 2)

    def test_user_views_own_items(self):
        self.authenticate_user_2()
        url = reverse('api:list-list')
        self.client.post(url, TODO_LIST_1, format='json')
        url = reverse('api:item-list')
        self.client.post(url, TODO_ITEMS_1[0], format='json')
        self.client.post(url, TODO_ITEMS_1[1], format='json')

        self.authenticate_user_1()
        url = reverse('api:list-list')
        self.client.post(url, TODO_LIST_2, format='json')
        url = reverse('api:item-list')
        self.client.post(url, TODO_ITEMS_2[0], format='json')
        self.client.post(url, TODO_ITEMS_2[1], format='json')

        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.assertEqual(TodoItem.objects.count(), 4)
        self.assertEqual(len(response.data), 2)
        print(response.data[0])
        todo_list = TodoList.objects.get(pk=response.data[0]['list_id'])
        self.assertEqual(todo_list.owner.username, 'test_user')

    def test_view_items_by_list_id(self):
        self.authenticate_user_1()
        self.addListsAndItems()
        url = reverse('api:item-list') + "?list_id=1"
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[2]['name'], 'Item 3 List 1')

        url = reverse('api:item-list') + "?list_id=5"
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.assertEqual(len(response.data), 0)

        url = reverse('api:item-list') + "?made_up_query=5"
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.assertEqual(len(response.data), 7)

    def test_finish_list_view(self):
        self.authenticate_user_1()
        self.addListsAndItems()
        url = reverse('api:list-list')
        initial_response = self.client.get(url, format='json')
        assert initial_response.status_code == status.HTTP_200_OK
        url = reverse('api:list-finish-list', args=['1'])
        self.assertEqual(initial_response.data[0]['status'], 'In Progress')
        response = self.client.post(url, format='json')
        self.assertEqual(response.data['status'], 'Finished')
        url = reverse('api:list-finish-list', args=['2'])
        self.assertEqual(initial_response.data[1]['status'], 'Not Started')
        response = self.client.post(url, format='json')
        self.assertEqual(response.data['status'], 'Finished')
        url = reverse('api:list-finish-list', args=['3'])
        self.assertEqual(initial_response.data[2]['status'], 'Finished')
        response = self.client.post(url, format='json')
        self.assertEqual(response.data['status'], 'Finished')
        url = reverse('api:list-finish-list', args=['4'])
        self.assertEqual(initial_response.data[3]['status'], 'Empty')
        response = self.client.post(url, format='json')
        self.assertEqual(response.data['status'], 'Empty')

    def test_estimated_duration_property(self):
        self.authenticate_user_1()
        self.addListsAndItems()
        url = reverse('api:list-list')
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.assertEqual(response.data[0]['estimated_duration'], '18:45:00')
        self.assertEqual(response.data[1]['estimated_duration'], '1 00:00:00')
        self.assertEqual(response.data[2]['estimated_duration'], '00:00:00')
        self.assertEqual(response.data[3]['estimated_duration'], '00:00:00')

    def test_item_count_property(self):
        self.authenticate_user_1()
        self.addListsAndItems()
        url = reverse('api:list-list')
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.assertEqual(response.data[0]['item_count'], 3)
        self.assertEqual(response.data[1]['item_count'], 2)
        self.assertEqual(response.data[2]['item_count'], 2)
        self.assertEqual(response.data[3]['item_count'], 0)

    def test_finished_property(self):
        with freeze_time("2022-05-06 10:30:00", tz_offset=+5) as frozen_datetime:
            self.authenticate_user_1()
            self.addListsAndItems()
            url = reverse('api:item-list') + '?list_id=2'
            items_response = self.client.get(url, format='json')
            self.assertEqual(items_response.status_code, status.HTTP_200_OK)

            url = reverse('api:list-detail', args=['2'])
            list_response = self.client.get(url, format='json')
            assert list_response.status_code == status.HTTP_200_OK
            self.assertEqual(list_response.data['status'], 'Not Started')

            patch_url = reverse('api:item-detail', args=['4'])
            self.client.patch(patch_url, {"status": "FI"}, format='json')
            response = self.client.get(url, format='json')
            assert items_response.status_code == status.HTTP_200_OK
            self.assertEqual(response.data['status'], 'In Progress')
            self.assertEqual(response.data['finished'], None)

            frozen_datetime.tick(delta=timedelta(days=3))
            self.authenticate_user_1()
            patch_url = reverse('api:item-detail', args=['5'])
            self.client.patch(patch_url, {"status": "FI"}, format='json')
            response = self.client.get(url, format='json')
            assert response.status_code == status.HTTP_200_OK
            self.assertEqual(response.data['status'], 'Finished')
            self.assertEqual(response.data['finished'], '2022-05-09 10:30')

