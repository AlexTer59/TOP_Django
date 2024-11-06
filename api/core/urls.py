from django.urls import path
from .views import *
from .rest_views import *

urlpatterns = [
    path('tasks/<int:task_id>/notes/<int:note_id>/like', api_note_like, name='api_note_like'),
    path('feedback', api_add_feedback, name='api_add_feedback'),
    path('rest/tasks/<int:task_id>/notes', get_notes_rest, name='get_notes_rest'),
    path('rest/tasks/<int:task_id>/notes/add', set_notes_rest, name='set_notes_rest'),
    path('rest/clicks', get_random_clicks, name='get_random_clicks')
]