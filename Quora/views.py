from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.utils.safestring import mark_safe
from .forms import RegistrationForm, Post, PostForm, AnswerForm, PersonalInfoForm
from Quora.models import Answer, User, Follow


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
                followDB = Follow.objects.create()
                followDB.follower = user
                followDB.save()
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


def logout_page(request):
    logout(request)
    return redirect('/')


def landing(request):
    context = {'list': filtering(request, Post.objects.all().order_by(
        '-id')), 'username': request.user.email}
    if request.method == "POST":
        post = PostForm(request.POST)
        try:
            post.save()
        except:
            context['error'] = 'Please enter a question!'

    if not request.user.is_authenticated:
        return redirect('/')
    return render(request, 'index.html', context)


def question(request, id):
    post = Post.objects.get(id=id)
    answers = Answer.objects.filter(original_post=id)

    context = {
        'post': post,
        'answers': answers,
        'answer_form': AnswerForm()
    }

    if request.method == 'POST':
        if request.POST.get("submit") == "addAnswer":
            answer = AnswerForm(request.POST)
            try:
                answer.save()
            except:
                context['error'] = 'Please enter an answer!'

        elif request.POST.get("submit") == "addQuestion":
            post = PostForm(request.POST)
            try:
                post.save()
            except:
                context['error'] = 'Please enter a question!'

    return render(request, 'view_question.html', context)


def profile(request, username):

    current_user = None
    for user in User.objects.all():
        if str(user.email) == str(username):
            current_user = user

    posts = Post.objects.filter(user=current_user)

    if current_user == None:
        return redirect('/')
    context = {'username': username,
               'posts': posts,
               'form': PersonalInfoForm(instance=current_user)}

    if request.method == "POST":
        post = PersonalInfoForm(request.POST, instance=current_user)
        try:
            post.save()
        except:
            print("Error updating user info")

    return render(request, 'profile.html', context)


def about(request):
    context = {
        'username': request.user.email if request.user.is_authenticated else 'anonymous'}
    return render(request, 'about.html', context)


def filtering(request, posts):
    lista_post = []
    current_user = None
    for follow in Follow.objects.all():
        if str(follow.follower) == str(request.user.email):
            current_user = follow
    if current_user == None:
        return []
    for post in posts:
        if str(post.user.email) in str(current_user.following.all()):
            lista_post.append(post)
    return lista_post
