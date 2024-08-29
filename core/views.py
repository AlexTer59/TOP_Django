from django.shortcuts import render, redirect, HttpResponse
from .models import Task, TaskStatus, TaskNote


def main(request):
    all_tasks = Task.objects.all()
    all_status = TaskStatus.objects.all()
    status_tasks_dict = {}
    active_status_obj = None
    active_status_id = request.GET.get('status')
    if active_status_id:
        active_status_obj = TaskStatus.objects.get(id=active_status_id)
        all_tasks = active_status_obj.tasks_status.all()
    for task in all_tasks:
        status_tasks_dict.setdefault(task.status, []).append(task)
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


def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    notes = TaskNote.objects.filter(task=task)

    return render(request, 'task_detail.html',
                  {'task': task,
                   'notes': notes})


def add_note(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        note = request.POST.get('note')
        notes = TaskNote.objects.filter(task=task)
        if note == '':
            error = 'Заполните поле "Заметка"'
            return render(request, 'task_detail.html',
                          {'task': task,
                           'error': error,
                           'notes': notes})
        TaskNote.objects.create(note=note, task=task)
        return redirect(task_detail, task_id)

    return redirect(task_detail, task_id)