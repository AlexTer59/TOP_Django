from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from .forms import *


def main(request):
    all_tasks = Task.objects.all()
    all_status = TaskStatus.objects.all()
    status_tasks_dict = {}
    active_status_obj = None
    active_status_id = request.GET.get('status')

    if active_status_id:
        active_status_obj = TaskStatus.objects.get(id=active_status_id)
        all_tasks = active_status_obj.tasks_status.all()

    if request.user.is_authenticated:
        profile = request.user.profile
        all_tasks = all_tasks.filter(profile_to=profile)

    for task in all_tasks:
        status_tasks_dict.setdefault(task.status, []).append(task)
    return render(request, 'task_list.html',
                  {
                      'status_task_dict': status_tasks_dict,
                      'active_status': active_status_obj,
                      'all_statuses': all_status
                  })


@login_required
def add_task(request):
    statuses = TaskStatus.objects.all()
    add_task_form = AddTaskModelForm()
    if request.method == 'POST':
        add_task_form = AddTaskModelForm(request.POST)
        if add_task_form.is_valid():
            data = add_task_form.cleaned_data
            profile = request.user.profile
            Task.objects.create(status=data['status'],
                                task=data['task'],
                                profile_from=profile,
                                profile_to=data['profile_to']
                                )
            return redirect('tasks')
        return render(request, 'add_task.html',
                      {'statuses': statuses,
                       'add_task_form': add_task_form})
    return render(request, 'add_task.html',
                  {'statuses': statuses,
                   'add_task_form': add_task_form})


@login_required
def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    notes = task.task_note.all()
    add_note_form = AddNoteModelForm()
    if request.method == 'POST':
        add_note_form = AddNoteModelForm(request.POST)
        if add_note_form.is_valid():
            note = add_note_form.cleaned_data['note']
            profile = request.user.profile
            TaskNote.objects.create(note=note, task=task, profile=profile)
            return redirect(task_detail, task_id)
    return render(request, 'task_detail.html',
                  {'task': task,
                   'notes': notes,
                   'add_note_form': add_note_form})


@login_required
def add_feedback(request):
    add_feedback_form = AddFeedbackModelForm()
    if request.method == 'POST':
        add_feedback_form = AddFeedbackModelForm(request.POST)
        if add_feedback_form.is_valid():
            data = add_feedback_form.cleaned_data
            Feedback.objects.create(name=data['name'], text=data['text'])
            return redirect('success')
    return render(request, 'add_feedback.html',
                  {'add_feedback_form': add_feedback_form})


@login_required
def feedback_success(request):
    return render(request, 'success_page.html')
