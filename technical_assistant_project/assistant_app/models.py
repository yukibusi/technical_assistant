from django.db import models
from django.contrib.auth.models import User

class GitIssue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    repo = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.repo



