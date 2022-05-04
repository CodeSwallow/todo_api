from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import TodoList, TodoItem


class TodoListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    status = serializers.ReadOnlyField()
    estimated_duration = serializers.DurationField(read_only=True)
    started = serializers.ReadOnlyField()
    finished = serializers.ReadOnlyField()
    item_count = serializers.ReadOnlyField()

    class Meta:
        model = TodoList
        fields = '__all__'


class TodoItemSerializer(serializers.ModelSerializer):
    finished = serializers.ReadOnlyField()

    class Meta:
        model = TodoItem
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(TodoItemSerializer, self).to_representation(instance)
        representation['status'] = instance.get_status_display()
        representation['priority'] = instance.get_priority_display()
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
        instance.started = validated_data.get('started', instance.started)
        instance.save()
        return instance


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
