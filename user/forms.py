from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    login = forms.CharField(max_length=250)
    password = forms.CharField(max_length=250, widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None

        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def get_user(self):
        return self.user

    def clean(self):
        login = self.cleaned_data.get('login')
        password = self.cleaned_data.get('password')

        self.user = authenticate(self.request, username=login, password=password)

        if not self.user:
            raise ValidationError('Неверный логин или пароль!')