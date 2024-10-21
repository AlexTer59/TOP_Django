# Generated by Django 5.1 on 2024-09-27 21:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_task_profile_to_taskexecutor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Активная'), (2, 'Срочная'), (3, 'Просроченая'), (4, 'Выполненая')], verbose_name='Статус'),
        ),
        migrations.AlterModelOptions(
            name='taskexecutor',
            options={'verbose_name': 'Назначение', 'verbose_name_plural': 'Назначения'},
        ),
        migrations.AddField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 4, 20, 59, 58, 960295, tzinfo=datetime.timezone.utc)),
        ),
        migrations.DeleteModel(
            name='TaskStatus',
        ),
    ]