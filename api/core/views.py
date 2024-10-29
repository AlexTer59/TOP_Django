from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from core.forms import AddFeedbackModelForm
from django.utils.timezone import localtime

from core.models import *


@login_required
def api_note_like(request, task_id, note_id):
    note = TaskNote.objects.get(id=note_id)
    profile = request.user.profile


    like, created = TaskNoteLike.objects.get_or_create(note=note, profile=profile)

    if not created:
        like.delete()

    count_likes = note.note_likes.count()
    return JsonResponse({
        'is_liked': created,
        'likes_count': count_likes
    })


def api_add_feedback(request):

    if request.method == 'POST':
        form = AddFeedbackModelForm(request.POST)

        if form.is_valid():
            form.save()

            return JsonResponse({})

        else:
            return JsonResponse({'errors': form.errors}, status=400)


def api_load_notes(request, task_id):
    task = Task.objects.get(id=task_id)
    notes = task.task_note.all()
    profile = request.user.profile
    liked_notes_ids = TaskNoteLike.objects.filter(profile=profile, note__in=notes).values_list('note_id', flat=True)

    my_task_notes = []

    for note in notes:
        likes_count = note.note_likes.count()
        my_task_notes.append({
            'id': note.id,
            'note': note.note,
            'profile': note.profile.user.username,
            'created_at': localtime(note.created_at).strftime('%d-%m-%Y %H:%M'),
            'likes_count': likes_count,
            'is_liked': note.id in liked_notes_ids,
        })

    return JsonResponse({'notes': my_task_notes}, safe=False)