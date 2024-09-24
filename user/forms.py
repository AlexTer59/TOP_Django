from django import forms
from django.contrib.auth import authenticate, get_user_model
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

class RegisterForm(forms.Form):
    login = forms.CharField(max_length=250)
    name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100, required=False)
    password1 = forms.CharField(max_length=250, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=250, widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError('Введеные пароли не совпадают!')

        return password2

    def clean_login(self):
        login = self.cleaned_data.get('login')
        User = get_user_model()

        if User.objects.filter(username=login).exists():
            raise ValidationError('Пользователь с таким логином уже существует!')

        return login