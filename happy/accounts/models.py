from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from posts.models import Post


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)    
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


    def __str__(self):
        return f"{self.user} Profile"

    def displayed_name(self):
        return (f"{self.first_name} {self.last_name}")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Link(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    facebook = models.URLField(max_length=50, blank=True, null=True, default=None)
    instagram = models.URLField(max_length=50, blank=True, null=True, default=None)
    youtube = models.URLField(max_length=50, blank=True, null=True, default=None) 
    twitter = models.URLField(max_length=50, blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.user} links"

@receiver(post_save, sender=Profile)
def create_profile_links(sender, instance, created, **kwargs):
    if created:
        Link.objects.create(user_id=instance.id)


@receiver(post_save, sender=Profile)
def save_profile_links(sender, instance, **kwargs):
    instance.link.save()

class Wall(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post, blank=True)

    def __str__(self):
        return f"{self.user} wall"

@receiver(post_save, sender=User)
def create_user_wall(sender, instance, created, **kwargs):
    if created:
        Wall.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_wall(sender, instance, **kwargs):
    instance.wall.save()