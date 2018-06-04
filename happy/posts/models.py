from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    content = models.TextField(max_length=254)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="posts")

    def __str__(self):
        return self.content[:50]


class Like(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="likes"
                             )

    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name="likes"
                             )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} likes {self.post}"


class Dislike(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="dislikes"
                             )

    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name="dislikes"
                             )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} dislikes {self.post}"
