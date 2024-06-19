from django import forms
from .models import GitIssue
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class GitIssueForm(forms.ModelForm):
    class Meta:
        model = GitIssue
        fields = ['repo', 'description']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')