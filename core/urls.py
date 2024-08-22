from django.urls import path
from .views import main, add_task

urlpatterns = [
    path('', main, name='tasks'),
    path('add_task', add_task, name='add_task'),
]