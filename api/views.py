from rest_framework.viewsets import ModelViewSet

from api.models import TodoList, TodoItem
from api.serializers import TodoListSerializer, TodoItemSerializer

# Create your views here.


class TodoListViewSet(ModelViewSet):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer


class TodoItemViewSet(ModelViewSet):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
