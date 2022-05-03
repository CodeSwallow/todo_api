from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class TodoList(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TodoItem(models.Model):
    name = models.CharField(max_length=255)
    list = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.name
