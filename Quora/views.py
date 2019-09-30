from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm

def index(request, *args, **kwards):
    form_signup = RegistrationForm(request.POST)
    form_login = AuthenticationForm(request.POST)

    if request.method == "POST":
        print("debug1")

        if request.POST.get("submit") == "signup":
            
            print("debug2")
            if form_signup.is_valid():
                print("debug3")
                form_signup.save()
                # redirect somewhere OR show something
            
        elif request.POST.get("submit") == "login":
            

    context = {
        'form_signup': form_signup,
        'form_login': form_login
    }

    return render(request, 'auth.html', context)