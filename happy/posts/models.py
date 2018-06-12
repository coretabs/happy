from django.db import models
from django.contrib.auth.models import User
# from accounts.models import CustomUser as User

# Create your models here.


class Post(models.Model):
    content = models.TextField(max_length=254)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="posts")
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    dislikes = models.ManyToManyField(User, related_name="dislikes", blank=True)
    
    def __str__(self):
        return self.content[:50]

    def likes_count(self):
        return self.likes.count()

    def dislikes_count(self):
        return self.dislikes.count()

