from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from posts.models import Post


class PostReport(models.Model):

    REASON = (
            ('SPAM','Spam'),
            ('VIOLENCE', 'Violence Content'),
        )
    reason = models.CharField(
            max_length=255,
            choices=REASON,
            default= None,
        )
    created = models.DateTimeField(auto_now_add=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE,related_name="reports")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reports")


    class Meta:
        ordering =["-created"]
    
    def __str__(self):
        return f'post:{self.post.id} reported by: {self.reporter.username}'