from django.contrib import admin

from .models import *

admin.site.register(Task)
# admin.site.register(TaskStatus)
admin.site.register(TaskNote)
admin.site.register(Feedback)
admin.site.register(TaskExecutor)