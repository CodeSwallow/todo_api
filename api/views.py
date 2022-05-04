from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from api.models import TodoList, TodoItem
from api.serializers import TodoListSerializer, TodoItemSerializer, UserSerializer
from api.permissions import IsOwner, IsListOwner

# Create your views here.


@api_view(['GET', 'POST'])
def user_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    user = get_object_or_404(User, pk=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


class TodoListViewSet(ModelViewSet):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.request.user.id)
        filters = {"owner": user}
        self.queryset = self.queryset.filter(**filters)
        return self.queryset

    def perform_create(self, serializer):
        user = get_object_or_404(User, pk=self.request.user.id)
        serializer.save(owner=user)

    @action(detail=True, methods=['post'])
    def finish_list(self, request, pk=None):
        instance = self.get_object()
        items = TodoItem.objects.filter(list_id=instance)
        for item in items:
            item.status = 'FI'
            item.finished = timezone.now()
            item.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TodoItemViewSet(ModelViewSet):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = [IsAuthenticated, IsListOwner]

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.request.user.id)
        filters = {"list_id__owner": user}
        list_id = self.request.query_params.get('list_id', None)
        if list_id is not None:
            filters['list_id_id'] = list_id
        self.queryset = self.queryset.filter(**filters)
        return self.queryset
