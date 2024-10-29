from django.urls import path
from .views import *

urlpatterns = [
    path('tasks/<int:task_id>/notes/<int:note_id>/like', api_note_like, name='api_note_like'),
    path('feedback', api_add_feedback, name='api_add_feedback'),
    path('tasks/<int:task_id>/notes', api_load_notes, name='api_load_notes')
]