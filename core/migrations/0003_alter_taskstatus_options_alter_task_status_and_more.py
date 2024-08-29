# Generated by Django 5.1 on 2024-08-29 07:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_task_taskstatus_delete_note_task_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskstatus',
            options={'verbose_name': 'Статус задачи', 'verbose_name_plural': 'Статусы задач'},
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks_status', to='core.taskstatus', verbose_name='Статус задачи'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task',
            field=models.CharField(max_length=256, verbose_name='Задача'),
        ),
        migrations.AlterField(
            model_name='taskstatus',
            name='status',
            field=models.CharField(max_length=100, verbose_name='Статус задачи'),
        ),
        migrations.CreateModel(
            name='TaskNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(max_length=1000, verbose_name='Заметка')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_note', to='core.task', verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'Заметка',
                'verbose_name_plural': 'Заметка',
            },
        ),
    ]
