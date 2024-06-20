from django import forms
from .models import GitIssue
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class GitIssueForm(forms.ModelForm):
    class Meta:
        model = GitIssue
        fields = ['repo', 'description']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['email'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''