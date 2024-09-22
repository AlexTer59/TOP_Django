from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login as auth_login, logout as auth_logout

def login(request):
    login_form = LoginForm()

    if request.method == 'POST':
        login_form = LoginForm(request, request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, user)

            return redirect('tasks')

    return render(request, 'user/login.html', context={'login_form': login_form})


def logout(request):
    auth_logout(request)
    return redirect('tasks')