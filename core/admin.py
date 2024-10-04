from django.contrib import admin

from .models import *

admin.site.register(Task)
admin.site.register(TaskNote)
admin.site.register(Feedback)
admin.site.register(TaskExecutor)
admin.site.register(TaskNoteLike)