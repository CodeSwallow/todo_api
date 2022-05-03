# Generated by Django 4.0.4 on 2022-05-03 17:40

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TodoList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('last_modified', models.DateField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TodoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('FI', 'Finished'), ('PE', 'Pending')], default='PE', max_length=2)),
                ('priority', models.CharField(choices=[('H', 'High'), ('M', 'Medium'), ('L', 'Low')], default='L', max_length=1)),
                ('duration', models.DurationField(default=datetime.timedelta(0))),
                ('date_created', models.DateField(auto_now_add=True)),
                ('last_modified', models.DateField(auto_now=True)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='api.todolist')),
            ],
        ),
    ]
