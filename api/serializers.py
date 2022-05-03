from rest_framework import serializers

from api.models import TodoList, TodoItem


class TodoListSerializer(serializers.ModelSerializer):

    class Meta:
        model = TodoList
        fields = '__all__'


class TodoItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = TodoItem
        fields = '__all__'
