from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):

    LIKE = 1
    DISLIKE = -1
 
    VOTES = [
        (DISLIKE, 'Dislike'),
        (LIKE, 'Like')
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.SmallIntegerField(null=True, choices=VOTES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class UserLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_liked = models.DateField(auto_now=True)
    like_dislike = models.SmallIntegerField(default=0)
