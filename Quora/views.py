from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.utils.safestring import mark_safe
from .forms import RegistrationForm, Post, PostForm


def index(request, *args, **kwards):
    # We put both here as both sign up and login have to be in same page/view
    # logout(request)
    if request.method == "GET":
        form_signup = RegistrationForm()
        form_login = AuthenticationForm()

    if request.method == "POST":
        if request.POST.get("submit") == "signup":
            form_signup = RegistrationForm(data=request.POST)
            form_login = AuthenticationForm()

            if form_signup.is_valid():
                form_signup.save()
                username = form_signup.cleaned_data.get('email')
                password = form_signup.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/homepage/')

        elif request.POST.get("submit") == "login":
            form_signup = RegistrationForm()
            form_login = AuthenticationForm(data=request.POST)

            print("\t[DEBUG] LOGIN VALID: ", form_login.is_valid())
            if form_login.is_valid():
                user_object = form_login.get_user()
                print("\t[DEBUG] LOGIN USER: ", user_object)

                username = form_login.cleaned_data.get('username')
                password = form_login.cleaned_data.get('password')

                print("\t[DEBUG] username, password: ", username, password)

                user = authenticate(username=username, password=password)

                if user is not None:
                    print("\t[DEBUG] user: ", user.email)
                    print(user)
                    login(request, user)
                    return redirect('/homepage/')

                form_login = AuthenticationForm()

    context = {
        'form_signup': form_signup,
        'form_login': form_login
    }

    return render(request, 'auth.html', context)


def pagelogout(request):
    logout(request)
    return redirect('/')


def landing(request):
    context = {'list': Post.objects.all()}
    if request.method == "POST":
        post = PostForm(request.POST)
        post.save()

    if not request.user.is_authenticated:
        return redirect('/')
    return render(request, 'index.html', context)
