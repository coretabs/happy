from django.contrib import admin


from .models import Profile, Link, Wall

admin.site.register(Link)
admin.site.register(Profile)
admin.site.register(Wall)

