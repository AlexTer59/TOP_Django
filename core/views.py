from django.shortcuts import render, redirect, HttpResponse
from .models import Note


def main(request):
    completed_notes = Note.objects.filter(status=True)
    uncompleted_notes = Note.objects.filter(status=False)
    return render(request, 'task_list.html',
                  {'completed_notes': completed_notes, 'uncompleted_notes': uncompleted_notes})


def add_task(request):
    return render(request, 'add_task.html')


def add_task_submit(request):
    task = request.POST.get('task')
    status = True if request.POST.get('is_completed') == 'on' else False
    Note.objects.create(text=task, status=status)
    return redirect('tasks')