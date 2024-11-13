from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import *
from .serializers import TaskNoteSerializer
import random


@api_view(['GET'])
def get_notes_rest(request, task_id):

    notes = TaskNote.objects.filter(task__id=task_id)
    serializer = TaskNoteSerializer(notes, many=True, context={'request': request})
    return Response({'notes': serializer.data})

@api_view(['POST'])
def set_notes_rest(request, task_id):

    task = Task.objects.get(id=task_id)
    profile = request.user.profile
    serializer = TaskNoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(task=task, profile=profile)
        return Response(status=200)
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like_rest(request, task_id, note_id):
    note = TaskNote.objects.get(id=note_id)
    profile = request.user.profile

    like, created = TaskNoteLike.objects.get_or_create(note=note, profile=profile)

    if not created:
        like.delete()

    return Response(data={'is_liked': created},
                    status=200)


@api_view(['GET'])
def get_random_clicks(request):
    return Response({'clicks': random.randint(1, 100)})


