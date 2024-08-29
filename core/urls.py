from django.urls import path
from .views import main, add_task, task_detail

urlpatterns = [
    path('', main, name='tasks'),
    path('task/add', add_task, name='add_task'),
    path('task/<int:task_id>', task_detail, name='task_detail'),
]