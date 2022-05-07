from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

# Create your models here.


class TodoList(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def status(self):
        items = self.items.all()
        progress = {item.status for item in items}
        if progress:
            if 'PE' not in progress:
                return 'Finished'
            if 'FI' not in progress:
                return 'Not Started'
            return 'In Progress'
        return 'Empty'

    @property
    def estimated_duration(self):
        items = self.items.all()
        durations = [item.duration for item in items]
        total = sum(durations, timedelta())
        return total

    @property
    def finished(self):
        items = self.items.all().order_by('-finished')
        if items:
            progress = {item.status for item in items}
            if 'PE' not in progress:
                return items[0].finished.astimezone().strftime("%Y-%m-%d %H:%M")
        return None

    @property
    def item_count(self):
        return self.items.count()


class TodoItem(models.Model):

    class Progress(models.TextChoices):
        FINISHED = 'FI', _('Finished')
        PENDING = 'PE', _('Pending')

    class Priority(models.TextChoices):
        HIGH = 'H', _('High')
        MEDIUM = 'M', _('Medium')
        LOW = 'L', _('Low')

    name = models.CharField(max_length=255)
    list_id = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name='items')
    status = models.CharField(
        max_length=2,
        choices=Progress.choices,
        default=Progress.PENDING,
    )
    priority = models.CharField(
        max_length=1,
        choices=Priority.choices,
        default=Priority.LOW,
    )
    duration = models.DurationField(default=timedelta())
    date_created = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return self.name
