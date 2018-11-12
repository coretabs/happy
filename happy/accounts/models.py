from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='link')
    SOCIAL_APP = (
            ('FB','Facebook'),
            ('IG','Instagram'),
            ('YT','Youtube'),
            ('TW','Twitter'),
        )
    social_app = models.CharField(
            max_length=2,
            choices=SOCIAL_APP,
            default= None,
            blank= True
        )
    social_link = models.URLField(
            max_length=255,
            blank=True
            )
    def __str__(self):
        return self.social_app