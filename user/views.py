from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model, authenticate
from .models import Profile


def login(request):
    login_form = LoginForm()

    if request.method == 'POST':
        login_form = LoginForm(request, request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, user)

            return redirect('tasks')

    return render(request, 'user/login.html', context={'login_form': login_form})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('tasks')

def register(request):
    register_form = RegisterForm()

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():

            login = register_form.cleaned_data['login']
            name = register_form.cleaned_data['name']
            surname = register_form.cleaned_data['surname']
            password = register_form.cleaned_data['password1']
            avatar = register_form.cleaned_data['avatar']


            User = get_user_model()
            user = User.objects.create(username=login)
            user.set_password(password)
            user.save()

            Profile.objects.create(user=user, name=name, surname=surname, avatar=avatar)

            user = authenticate(request, username=login, password=password)
            auth_login(request, user=user)

            return redirect('tasks')

    return render(request, 'user/register.html', context={'register_form': register_form})
