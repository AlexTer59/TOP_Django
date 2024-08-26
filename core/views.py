from django.shortcuts import render, redirect, HttpResponse
from .models import Task, TaskStatus


def main(request):
    all_tasks = Task.objects.all()
    all_status = TaskStatus.objects.all()
    status_tasks_dict = {}
    active_status_obj = None
    active_status_id = request.GET.get('status')
    if active_status_id:
        active_status_obj = TaskStatus.objects.get(id=active_status_id)
        all_tasks = all_tasks.filter(status__id=active_status_id)
    for task in all_tasks:
        status_tasks_dict.setdefault(task.status, []).append(task.task)
    return render(request, 'task_list.html',
                  {
                      'status_task_dict': status_tasks_dict,
                      'active_status': active_status_obj,
                      'all_statuses': all_status
                  })


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
