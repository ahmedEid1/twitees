import json

from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post
from .forms import PostCreateForm


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {'create_form': PostCreateForm(), 'posts': page_obj,
                                                  'page_num_range': range(page_obj.paginator.num_pages)})


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

            posts = Post.objects.all()
            paginator = Paginator(posts, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, "network/index.html", {'create_form': PostCreateForm(), 'posts': page_obj,
                                                          'page_num_range': range(page_obj.paginator.num_pages)})
        else:
            posts = Post.objects.all()
            paginator = Paginator(posts, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, "network/index.html", {'create_form': PostCreateForm(), 'posts': page_obj,
                                                          'page_num_range': range(page_obj.paginator.num_pages)})
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {'create_form': PostCreateForm(), 'posts': page_obj,
                                                  'page_num_range': range(page_obj.paginator.num_pages)})


def all_posts(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'network/posts/post_list.html', {'title': 'All', 'posts': page_obj,
                                                            'page_num_range': range(page_obj.paginator.num_pages)})


def user_profile(request, pk):
    profile_owner = User.objects.get(pk=pk)
    return render(request, 'network/profile.html', {'profile_owner': profile_owner})


def follow(request, user, user_to_follow):
    person = User.objects.get(pk=user)
    personToFollow = User.objects.get(pk=user_to_follow)

    person.following.add(personToFollow)

    return render(request, 'network/profile.html', {'profile_owner': personToFollow})


def unfollow(request, user, user_to_follow):
    person = User.objects.get(pk=user)
    personToFollow = User.objects.get(pk=user_to_follow)

    person.following.remove(personToFollow)

    return render(request, 'network/profile.html', {'profile_owner': personToFollow})


def following_posts(request):
    if not request.user.is_authenticated:
        return render(request, 'network/login.html')

    user = User.objects.get(pk=request.user.id)
    followed_users = user.following
    posts = Post.objects.filter(owner__in=followed_users.all())
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'network/posts/post_list.html', {'title': 'Following', 'posts': page_obj,
                                                            'page_num_range': range(page_obj.paginator.num_pages)})


def edit_post(request, post_id):
    if Post.objects.filter(pk=post_id).exists():
        post = Post.objects.get(pk=post_id)
    else:
        return HttpResponseRedirect(reverse('index'))

    if post.owner.id != request.user.id:
        return HttpResponseRedirect(reverse('index'))
    if not request.user.is_authenticated:
        return render(request, 'network/login.html')

    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        post.content = data['content']
        post.save()
        return HttpResponse("Success")
    else:
        return render(request, 'network/edit.html', {'edit_form': PostCreateForm(instance=post), 'post_id': post_id})