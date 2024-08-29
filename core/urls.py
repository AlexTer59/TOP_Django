from django.urls import path
from .views import main, add_task, task_detail, add_note

urlpatterns = [
    path('', main, name='tasks'),
    path('task/add', add_task, name='add_task'),
    path('task/<int:task_id>', task_detail, name='task_detail'),
    path('task/<int:task_id>/note/add', add_note, name='add_note')
]