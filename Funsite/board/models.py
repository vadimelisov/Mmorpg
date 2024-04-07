from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    title = models.CharField(max_length=50)
    content = models.TextField()

    def __str__(self):
        return self.title


class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    is_allowed = models.BooleanField(default=False)

    def __str__(self):
        return self.author.username + ', ' + self.post.title

