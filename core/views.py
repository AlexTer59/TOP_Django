from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from datetime import datetime


def main(request):
    all_tasks = Task.objects.all()
    all_status = Task.STATUS_CHOICES
    status_tasks_dict = {}
    active_status_id = request.GET.get('status')

    if active_status_id:
        active_status_id = int(active_status_id)
        all_tasks = Task.objects.filter(status=active_status_id)

    if request.user.is_authenticated:
        profile = request.user.profile
        all_tasks = all_tasks.filter(id__in=profile.executor_profile.values_list('task', flat=True))

    for task in all_tasks:
        status_tasks_dict.setdefault(task.get_status_display(), []).append(task)
    return render(request, 'task_list.html',
                  {
                      'status_task_dict': status_tasks_dict,
                      'active_status_id': active_status_id,
                      'all_statuses': all_status
                  })


@login_required
def add_task(request):
    statuses = Task.STATUS_CHOICES
    add_task_form = AddTaskForm()

    if request.method == 'POST':
        add_task_form = AddTaskForm(request.POST)

        if add_task_form.is_valid():
            data = add_task_form.cleaned_data
            profile = request.user.profile
            date = data['deadline_date']
            time = data['deadline_time']

            if date and time:
                deadline = datetime.combine(data['deadline_date'], data['deadline_time'])
                task = Task.objects.create(status=data['status'],
                                           task=data['task'],
                                           deadline=deadline,
                                           profile_from=profile,
                                           )
            else:
                task = Task.objects.create(status=data['status'],
                                           task=data['task'],
                                           profile_from=profile,
                                           )

            for executor in data['executors']:
                TaskExecutor.objects.create(task=task,
                                            profile=executor)
            return redirect('tasks')
    return render(request, 'add_task.html',
                  {'statuses': statuses,
                   'add_task_form': add_task_form})


@login_required
def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    executors = [executor.profile.user for executor in task.task_executor.all()]
    notes = task.task_note.all()
    add_note_form = AddNoteModelForm()
    profile = request.user.profile

    liked_notes_ids = TaskNoteLike.objects.filter(profile=profile, note__in=notes).values_list('note_id', flat=True)

    task_notes_with_likes =[]

    for note in notes:
        likes_count = note.note_likes.count()
        task_notes_with_likes.append({
            'id': note.id,
            'note': note.note,
            'profile': note.profile,
            'created_at': note.created_at,
            'likes_count': likes_count,
            'is_liked': note.id in liked_notes_ids,
        })

    if request.method == 'POST':
        add_note_form = AddNoteModelForm(request.POST)
        if add_note_form.is_valid():
            note = add_note_form.cleaned_data['note']
            TaskNote.objects.create(note=note, task=task, profile=profile)
            return redirect(task_detail, task_id)
    return render(request, 'task_detail.html',
                  {'task': task,
                   'notes': task_notes_with_likes,
                   'add_note_form': add_note_form,
                   'executors': executors
                   })


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

@login_required
def note_like(request, task_id, note_id):
    note = TaskNote.objects.get(id=note_id)
    profile = request.user.profile

    like, created = TaskNoteLike.objects.get_or_create(note=note, profile=profile)

    if not created:
        like.delete()

    return redirect('task_detail', task_id)

