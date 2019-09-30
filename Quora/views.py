# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm



def index(request, *args, **kwards):
    form_reg = RegistrationForm(request.POST)
    form_login = LoginForm(request.POST)

    if request.method == "POST":
        # print("debug1")

        if request.POST.get("submit") == "sign_up":
            
            # print("debug2")
            if form_reg.is_valid():
                # print("debug3")
                form_reg.save()
                # redirect somewhere OR show something
            
        elif request.POST.get("submit") == "login":
            pass

    context = {
        'form_reg': form_reg,
        'form_login': form_login
    }

    return render(request, 'auth.html', context)