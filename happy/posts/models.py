import os 
from django.db import models
from hashlib import md5
from django.utils import timezone
from django.utils.dateformat import format
from django.contrib.auth.models import User

from .validators import validate_file_extension_and_size
# from accounts.models import CustomUser as User
 
def content_file_name(instance, filename):
    now = timezone.now()
    file_path = '{author_username}/uploads/{date}/{filename}'.format(
         author_username=md5(str(instance.author).encode()).hexdigest(),
         user_id=instance.id,
         date=format(now, 'd-m-Y'),
         filename=filename) 
    return file_path


class Post(models.Model):
    time_since = models.DateTimeField(auto_now=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="posts")
    content = models.TextField(max_length=1024, 
                                blank=True)
    likes = models.ManyToManyField(User,
                               related_name="likes",
                               blank=True)
    dislikes = models.ManyToManyField(User, related_name="dislikes", blank=True)
    mediafile = models.FileField(upload_to=content_file_name,
                            validators=[validate_file_extension_and_size],
                            blank=True,
                            null=True)
    class Meta:
       ordering = ('-created',)

    def __str__(self):
        return self.content[:50]

    def FORMAT(self):
        from django.utils.timesince import timesince
        if timesince(self.created).find("week"):
            return timesince(self.created).split(',')[0]
        return timesince(self.created)

    def likes_count(self):
        return self.likes.count()

    def dislikes_count(self):
        return self.dislikes.count()