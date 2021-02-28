from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post
from .forms import PostCreateForm


def index(request):
    return render(request, "network/index.html", {'create_form': PostCreateForm()})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def create_post(request):
    if not request.user.is_authenticated:
        return render(request, "network/index.html", {'create_form': PostCreateForm()})

    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            Post.objects.create(content=content, owner=request.user)

            return render(request, 'network/index.html', {'create_form': PostCreateForm()})
        else:
            return render(request, 'network/index.html', {'create_form': PostCreateForm(request.POST)})

    return render(request, 'network/index.html', {'create_form': PostCreateForm()})


def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'network/posts/post_list.html', {'posts': posts})


def user_profile(request, pk):
    profile_owner = User.objects.get(pk=pk)
    return render(request, 'network/profile.html', {'profile_owner': profile_owner})