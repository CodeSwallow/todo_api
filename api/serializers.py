from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import TodoList, TodoItem


class TodoListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    status = serializers.ReadOnlyField()
    estimated_duration = serializers.DurationField(read_only=True)
    started = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")
    finished = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")
    item_count = serializers.ReadOnlyField()

    class Meta:
        model = TodoList
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(TodoListSerializer, self).to_representation(instance)
        representation['date_created'] = instance.date_created.astimezone().strftime("%Y-%m-%d %H:%M")
        return representation


class TodoItemSerializer(serializers.ModelSerializer):
    finished = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()

    class Meta:
        model = TodoItem
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(TodoItemSerializer, self).to_representation(instance)
        representation['status'] = instance.get_status_display()
        representation['priority'] = instance.get_priority_display()
        if instance.finished:
            representation['finished'] = instance.finished.astimezone().strftime("%Y-%m-%d %H:%M")
        representation['date_created'] = instance.date_created.astimezone().strftime("%Y-%m-%d %H:%M")
        return representation

    def update(self, instance, validated_data):
        item_status = validated_data.get('status', None)
        if item_status is not None:
            instance.status = validated_data.get('status', instance.status)
            if instance.status == 'FI':
                instance.finished = timezone.now()
            else:
                instance.finished = None
        instance.name = validated_data.get('name', instance.name)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.save()
        return instance

    def create(self, validated_data):
        todo_item = TodoItem.objects.create(**validated_data)
        finished = validated_data.get('status', None)
        if finished == 'FI':
            todo_item.finished = timezone.now()
            todo_item.save()
        return todo_item


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
