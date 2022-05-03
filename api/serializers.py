from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import TodoList, TodoItem


class TodoListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    status = serializers.ReadOnlyField()
    duration = serializers.DurationField(read_only=True)

    class Meta:
        model = TodoList
        fields = '__all__'


class TodoItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = TodoItem
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(TodoItemSerializer, self).to_representation(instance)
        representation['status'] = instance.get_status_display()
        representation['priority'] = instance.get_priority_display()
        return representation


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
