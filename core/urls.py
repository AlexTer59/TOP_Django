from django.urls import path
from .views import main, add_task, add_task_submit

urlpatterns = [
    path('', main, name='tasks'),
    path('add_task', add_task, name='add_task'),
    path('add_task_submit', add_task_submit, name='add_task_and_submit')
]