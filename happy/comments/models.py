from django.db import models

from django.contrib.auth.models import User
# from accounts.models import CustomUser as User
from posts.models import Post


# Create your models here.


class BaseComment(models.Model):
    content = models.TextField(max_length=254)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:50]


class Comment(BaseComment):
    parent = models.ForeignKey(Post, on_delete=models.CASCADE,
                               related_name="post_comments")


class Reply(BaseComment):
    parent = models.ForeignKey(Comment, on_delete=models.CASCADE,
                               related_name="comment_replies", null=True)

    def __str__(self):
        return self.content[:50]
