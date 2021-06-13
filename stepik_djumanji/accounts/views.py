from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import login, logout


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('main')
