from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from core.forms import AddFeedbackModelForm

from core.models import TaskNote, TaskNoteLike, Feedback


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