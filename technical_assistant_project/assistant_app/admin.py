from django.contrib import admin
from .models import Group, GroupItem, GitIssue

# Register your models here.
admin.site.register(GitIssue)
admin.site.register(Group)
admin.site.register(GroupItem)