from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import TodoItemViewSet, TodoListViewSet

router = DefaultRouter()
router.register(r'lists', TodoListViewSet, basename='list')
router.register(r'items', TodoItemViewSet, basename='item')

urlpatterns = [
    path('', include(router.urls)),
]
