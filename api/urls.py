from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import TodoItemViewSet, TodoListViewSet, user_view

router = DefaultRouter()
router.register(r'lists', TodoListViewSet, basename='list')
router.register(r'items', TodoItemViewSet, basename='item')

app_name = "api"
urlpatterns = [
    path('user', user_view),
    path('', include(router.urls)),
]
