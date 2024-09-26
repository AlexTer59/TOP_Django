from django import forms
from .models import *
from django.core.exceptions import ValidationError


class AddTaskForm(forms.Form):
    task = forms.CharField(max_length=1024,
                           widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}))
    status = forms.ModelChoiceField(queryset=TaskStatus.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    executors = forms.ModelMultipleChoiceField(queryset=Profile.objects.all(),
                                               widget=forms.SelectMultiple(attrs={'size': 3, 'class': 'form-control'}))

    # def __init__(self, *args, **kwargs):
    #     super(AddTaskForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'

    def clean_task(self):
        forbidden_words = ('дурак', 'дура', 'fuck')
        task = self.cleaned_data['task']
        for word in task.lower().split():
            if word in forbidden_words:
                raise ValidationError('Задача не прошла цензуру! Попробуйте еще раз...')
        return task

    def clean_status(self):
        status = self.cleaned_data['status']
        if not status:
            raise ValidationError('Статус не может быть пустым! Выберите из списка...')
        return status

    def clean_executors(self):
        profile = self.cleaned_data['executors']
        if not profile:
            raise ValidationError('Статус не может быть пустым! Выберите из списка...')
        return profile


class AddNoteModelForm(forms.ModelForm):
    class Meta:
        model = TaskNote
        fields = ['note']

    def __init__(self, *args, **kwargs):
        super(AddNoteModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

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
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name.split()) < 2:
            raise ValidationError('Введите имя и фамилию!')
        return name
