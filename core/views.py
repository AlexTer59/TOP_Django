from django.shortcuts import render
from .models import Note


def main(request):
    notes = Note.objects.all()
    return render(request, 'index.html', {'notes': notes})
