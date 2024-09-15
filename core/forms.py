from django import forms
from .models import *
from django.core.exceptions import ValidationError


class AddTaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task', 'status']

    def __init__(self, *args, **kwargs):
        super(AddTaskModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input_data'

    def clean_task(self):
        forbidden_words = ('дурак', 'дура', 'fuck')
        task = self.cleaned_data['task']
        for word in task.lower().split():
            if word in forbidden_words:
                raise ValidationError('Задача не прошла цензуру! Попробуйте еще раз...')
        return task


class AddNoteModelForm(forms.ModelForm):
    class Meta:
        model = TaskNote
        fields = ['note']

    def __init__(self, *args, **kwargs):
        super(AddNoteModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input_data'

    def clean_note(self):
        forbidden_words = ('дурак', 'дура', 'fuck')
        note = self.cleaned_data['note']
        for word in note.lower().split():
            if word in forbidden_words:
                raise ValidationError('Заметка не прошла цензуру! Попробуйте еще раз...')
        return note


class AddFeedbackModelForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'text']

    def __init__(self, *args, **kwargs):
        super(AddFeedbackModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input_data'

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name.split()) < 2:
            raise ValidationError('Введите имя и фамилию!')
        return name
