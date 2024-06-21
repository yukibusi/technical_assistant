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

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, related_name='created_groups', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='custom_groups')

    def __str__(self):
        return self.name

class GroupItem(models.Model):
    group = models.ForeignKey(Group, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name



