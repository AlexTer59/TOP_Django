from django import forms
from .models import TaskStatus


class AddTaskForm(forms.Form):
    task = forms.CharField(max_length=1024, widget=forms.Textarea(attrs={'rows': 3, 'class': 'input_data'}))
    status = forms.ModelChoiceField(queryset=TaskStatus.objects.all())


class AddNoteForm(forms.Form):
    note = forms.CharField(max_length=1024, label='Заметка',
                           widget=forms.Textarea(attrs={'rows': 3, 'class': 'input_data'}))


class AddFeedbackForm(forms.Form):
    name = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'class': 'input_data'}))
    text = forms.CharField(max_length=1024,
                           widget=forms.Textarea(attrs={'rows': 4, 'class': 'input_data'}))

