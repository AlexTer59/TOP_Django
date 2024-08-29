from django.contrib import admin

from .models import Task, TaskStatus, TaskNote

admin.site.register(Task)
admin.site.register(TaskStatus)
admin.site.register(TaskNote)
