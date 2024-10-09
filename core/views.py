from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.utils import timezone


from .models import *
from .forms import *
from datetime import datetime


def main(request):
    all_tasks = Task.objects.all()
    all_status = Task.STATUS_CHOICES
    status_tasks_dict = {}
    active_status_id = request.GET.get('status')
    text_filter = request.GET.get('text')

    if active_status_id:
        active_status_id = int(active_status_id)
        all_tasks = Task.objects.filter(status=active_status_id)

    if request.user.is_authenticated:
        profile = request.user.profile
        all_tasks = all_tasks.filter(id__in=profile.executor_profile.values_list('task', flat=True))

    if text_filter:
        all_tasks = all_tasks.filter(Q(task__icontains=text_filter)|
                                     Q(status__icontains=text_filter)|
                                     Q(deadline__icontains=text_filter)|
                                     Q(created_at__icontains=text_filter)|
                                     Q(updated_at__icontains=text_filter)|
                                     Q(profile_from__user__username__icontains=text_filter))




    for task in all_tasks:
        status_tasks_dict.setdefault(task.get_status_display(), []).append(task)
    return render(request, 'task_list.html',
                  {
                      'status_task_dict': status_tasks_dict,
                      'active_status_id': active_status_id,
                      'all_statuses': all_status,
                      'text_filter': text_filter
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

    my_task_notes =[]

    for note in notes:
        likes_count = note.note_likes.count()
        my_task_notes.append({
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
                   'notes': my_task_notes,
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


class TaskEditView(LoginRequiredMixin, FormView):
    template_name = 'edit_task.html'
    form_class = AddTaskForm


    def get_task(self):
        return get_object_or_404(Task, id=self.kwargs['task_id'])

    def dispatch(self, request, *args, **kwargs):
        task = self.get_task()

        # Проверка что текущий пользователь - это создатель задачи
        if task.profile_from != self.request.user.profile:
            return HttpResponseForbidden('Вы не можете редактировать эту задачу!')

        # Если пользователь имеет право на редактирование задачи
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'task_id': self.kwargs['task_id']})

    def get_initial(self):
        task = self.get_task()

        return {
            'task': task.task,
            'status': task.status,
            'deadline_date': task.deadline.date(),
            'deadline_time': task.deadline.time(),
            'executors': task.task_executor.values_list('profile', flat=True)
        }

    def form_valid(self, form):
        task = self.get_task()

        task.task = form.cleaned_data['task']
        task.status = form.cleaned_data['status']

        deadline_date = form.cleaned_data['deadline_date']
        deadline_time = form.cleaned_data['deadline_time']

        if deadline_date and deadline_time:
            task.deadline = timezone.make_aware(datetime.combine(deadline_date, deadline_time))
        task.save()

        current_executors = set(task.task_executor.values_list('profile', flat=True))

        new_executors = set(form.cleaned_data['executors'].values_list('id', flat=True))

        if current_executors != new_executors:
            TaskExecutor.objects.filter(task=self.kwargs['task_id']).delete() # Очищаем старых исполнителей
            for executor in form.cleaned_data['executors']:
                TaskExecutor.objects.create(task=task, profile=executor)

        return super().form_valid(form)


@login_required
def task_ready(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.user.profile.id in task.task_executor.values_list('profile', flat=True):
        task.status = 4
        task.save(update_fields=['status'])

    return redirect('task_detail', task_id)