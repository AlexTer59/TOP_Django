from django.shortcuts import render
from .models import Note


def main(request):
    completed_notes = Note.objects.filter(status=True)
    uncompleted_notes = Note.objects.filter(status=False)
    return render(request, 'index.html',
                  {'completed_notes': completed_notes, 'uncompleted_notes': uncompleted_notes})
