# Generated by Django 4.0.4 on 2022-05-06 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_todoitem_last_modified_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todoitem',
            name='started',
        ),
    ]
