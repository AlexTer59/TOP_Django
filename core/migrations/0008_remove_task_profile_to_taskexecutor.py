# Generated by Django 5.1 on 2024-09-26 21:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_task_profile_from_task_profile_to_tasknote_profile'),
        ('user', '0002_alter_profile_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='profile_to',
        ),
        migrations.CreateModel(
            name='TaskExecutor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='executor_profile', to='user.profile')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_executor', to='core.task')),
            ],
        ),
    ]