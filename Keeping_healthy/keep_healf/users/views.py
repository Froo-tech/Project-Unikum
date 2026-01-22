from django.shortcuts import render, redirect
import hashlib
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, CreateView, DetailView
from .models import *
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/users/account/")
        else:
            return render(request, "users/login.html", {"error": "Неправильный логин или пароль"})
    return render(request, "users/login.html")


def account(request):
    contex = {}
    if request.user.is_authenticated:
        username = request.user.username

        email = request.user.email
        contex = {"username":username,
                  "email":email}
    else:
        contex = {'anom':"User is not authenticated"}
    return render(request, 'users/account.html', contex)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_')


        if password != password_confirm:

            return render(request, 'users/register.html',{"error" : "Пожалуйста введите одинаковый пароль"})

        if User.objects.filter(username=username).exists():
            return render(request, 'users/register.html', {"error" : "Пользователь с таким username уже сушествует "})

        if User.objects.filter(email=email).exists():
            return render(request, 'users/register.html', {"error" : "Пользователь с таким email уже сушествует"})


        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('/users/account/')


        except Exception as e:
            return render(request, 'users/register.html')

    return render(request, 'users/register.html')

def logout(request):
    auth_logout(request)
    return redirect('/users/register/')
def main(request):
    return render(request, 'users/main-page.html')