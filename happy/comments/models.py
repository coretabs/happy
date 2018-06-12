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
    likes = models.ManyToManyField(User, blank=True, related_name="like")
    dislikes = models.ManyToManyField(User, blank=True, related_name="dislike")

    def __str__(self):
        return self.content[:50]

    def likes_count(self):
        return self.likes.count()

    def dislikes_count(self):
      return self.dislikes.count()


class Comment(BaseComment):
    parent = models.ForeignKey(Post, on_delete=models.CASCADE,
                               related_name="post_comments")


class Reply(BaseComment):
    parent = models.ForeignKey(Comment, on_delete=models.CASCADE,
                               related_name="comment_replies", null=True)

    def __str__(self):
        return self.content[:50]
