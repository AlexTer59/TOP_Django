from django.urls import path

from .views import *

urlpatterns = [
    path('task/<int:task_id>/note/<int:note_id>/like', api_note_like, name='api_note_like'),
]