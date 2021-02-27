from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', related_name='followers')


class Post(models.Model):
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    time_created = models.DateTimeField(auto_now_add=True)
    user_likes = models.ManyToManyField(User, related_name='post_likes')

    class Meta:
        ordering = ['-time_created']

    def __str__(self):
        return f'{self.owner} has wrote this at {self.time_created}'
