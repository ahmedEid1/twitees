
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create', views.create_post, name='create_post'),
    path('all', views.all_posts, name='all_posts'),
    path('profile/<int:pk>', views.user_profile, name='user_profile'),
    path('follow/<int:user>/<int:user_to_follow>', views.follow, name='follow'),
    path('unfollow/<int:user>/<int:user_to_follow>', views.unfollow, name='unfollow'),
    path('following', views.following_posts, name='following'),
    path('edit/<int:post_id>', views.edit_post, name='edit_post'),
]
