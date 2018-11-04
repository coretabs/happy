from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from posts.models import Post


class PostReport(models.Model):

    REASON = (
            ('SPAM','spam'),
            ('VIOLENCE', 'violence'),
        )
    reason = models.CharField(
            max_length=255,
            choices=REASON,
            default= None,
        )
    created = models.DateTimeField(auto_now_add=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE,related_name="reports")
    #reason = models.TextField(max_length=256, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reports")


    class Meta:
        ordering =["-created"]
    
    def __str__(self):
        return f'the post with id:{self.post.id} is reported'