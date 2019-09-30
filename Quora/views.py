from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm

def index(request, *args, **kwards):
    # We put both here as both sign up and login have to be in same page/view

    if request.method == "GET":
        form_signup = RegistrationForm()
        form_login = AuthenticationForm()

    if request.method == "POST":
        form_signup = RegistrationForm(data=request.POST)
        form_login = AuthenticationForm(data=request.POST)
        if request.POST.get("submit") == "signup":
            if form_signup.is_valid():
                form_signup.save()
                form_signup.clean()
                # redirect somewhere OR show something

        elif request.POST.get("submit") == "login":
            print("debug1")
            if form_login.is_valid():
                print("debug2")
                user_object = form_login.get_user()
                print("debug3")
                print(user_object)
                print("debug1")

    context = {
        'form_signup': form_signup,
        'form_login': form_login
    }

    return render(request, 'auth.html', context)