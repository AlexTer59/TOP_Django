from django import forms
from .models import TaskStatus


class AddTaskForm(forms.Form):
    task = forms.CharField(max_length=256, widget=forms.Textarea(attrs={'rows': 3, 'class': 'input_data'}))
    status = forms.ModelChoiceField(queryset=TaskStatus.objects.all())


class AddNoteForm(forms.Form):
    note = forms.CharField(max_length=1000, label='Заметка',
                           widget=forms.Textarea(attrs={'rows': 3, 'class': 'input_data'}))