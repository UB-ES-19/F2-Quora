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
                follow(request, username)
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
    post_list = filtering(request, Post.objects.all().order_by(
        '-id'))

    posts = []

    for p in post_list:
        num_answers = Answer.objects.filter(original_post=p.id).count()
        posts.append([p, p.topic.split(','), num_answers])

    context = {'list': posts}
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
    topics = post.topic.split(',')

    context = {
        'post': post,
        'topics': topics,
        'answers': answers,
        'answer_form': AnswerForm(),
        'username': post.user
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

    current_user = User.objects.get(email=username)
    post_list = Post.objects.filter(user=current_user).order_by('-id')
    is_following = False

    posts = []

    for p in post_list:
        num_answers = Answer.objects.filter(original_post=p.id).count()
        posts.append([p, p.topic.split(','), num_answers])

    try:
        follows = Follow.objects.get(follower=request.user)
        is_following = current_user in follows.following.all()
    except:
        pass

    if current_user == None:
        return redirect('/')

    if request.method == "POST":
        if request.POST.get("submit") == "editProfile":
            post = PersonalInfoForm(request.POST, instance=current_user)
            try:
                post.save()
            except:
                print("Error updating user info")
        elif request.POST.get("submit") == "addQuestion":
            post = PostForm(request.POST)
            try:
                post.save()
            except:
                context['error'] = 'Please enter a question!'
        elif request.POST.get("submit") == "follow":
            follows = Follow.objects.filter(follower=request.user)
            if not follows.exists():
                print("Follows doesn't exist, creating")
                follows = Follow(follower=request.user)
                follows.save()
            follows = follows.first()
            if not is_following:
                follow(request, current_user)
                is_following = True
            else:
                unfollow(request, current_user)
                is_following = False

    context = {'user': current_user,
               'posts': posts,
               'form': PersonalInfoForm(instance=current_user),
               'is_following': is_following}

    return render(request, 'profile.html', context)


def about(request):
    context = {
        'username': request.user.email if request.user.is_authenticated else 'anonymous'}
    if request.POST.get("submit") == "addQuestion":
        post = PostForm(request.POST)
        try:
            post.save()
        except:
            context['error'] = 'Please enter a question!'
    return render(request, 'about.html', context)


def ajaxSearch(request, str):
    result = ""
    for user in search(str):
        result += '<a href="/profile/' + user.email + '"><div class="userResult"><b>' + user.first_name + ' ' + \
            user.last_name + '</b><br>' + user.email + '</div></a>'
    return HttpResponse(result)


def filtering(request, posts):
    following = []

    try:
        follows = Follow.objects.get(follower=request.user)
        following = [f.email for f in follows.following.all()]
        posts = Post.objects.filter(user__email__in=following).order_by('-id')
    except:
        # User is following no one. Return empty list.
        posts = []

    return posts


def follow(request, userToFollow):
    obj = Follow.objects.get(follower=request.user)
    followed = User.objects.get(email=userToFollow)
    obj.following.add(followed.id)
    obj.save()


def unfollow(request, userToUnfollow):
    obj = Follow.objects.get(follower=request.user)
    followed = User.objects.get(email=userToUnfollow)
    if userToUnfollow != request.user.email:
        obj.following.remove(followed.id)
        obj.save()


def search(word):

    user_list = []
    for userObject in User.objects.all():
        if word == userObject.email or word in userObject.first_name or word in userObject.last_name:
            user_list.append(userObject)
    return user_list


def saveImageDB(request, url):
    request.user.photo = url
    request.user.save()
