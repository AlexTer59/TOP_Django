from django.shortcuts import render, redirect, HttpResponse
from .models import Task, TaskStatus


def main(request):
    status_tasks_dict = {}
    all_tasks = Task.objects.all()
    for task in all_tasks:
        status_tasks_dict.setdefault(task.status.status, []).append(task.task)
    return render(request, 'task_list.html', {'status_task_dict': status_tasks_dict})


def add_task(request):
    statuses = TaskStatus.objects.all()
    if request.method == 'POST':
        task = request.POST.get('task')
        status = TaskStatus.objects.get(id=request.POST.get('task_status'))

        if task == '' or not status:
            error = 'Заполните поле "Введите задачу"'
            return render(request, 'add_task.html',
                          {'statuses': statuses, 'error': error})
        Task.objects.create(status=status, task=task)
        return redirect('tasks')
    return render(request, 'add_task.html', {'statuses': statuses})
