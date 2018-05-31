from django.contrib import admin
from .models import Post, Like, Dislike, Comment, Profile

# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Comment)
admin.site.register(Profile)