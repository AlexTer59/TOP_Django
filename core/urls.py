from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='tasks'),
    path('task/add', add_task, name='add_task'),
    path('task/<int:task_id>', task_detail, name='task_detail'),
    path('feedback', add_feedback, name='add_feedback'),
    path('feedback/success', feedback_success, name='success'),
    path('task/<int:task_id>/note/<int:note_id>/like', note_like, name='note_like')
]