from django import forms
from .models import GitIssue
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Group, GroupItem

class GitIssueForm(forms.ModelForm):
    class Meta:
        model = GitIssue
        fields = ['repo']

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

class GroupForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,  # チェックボックス形式で複数選択
        label="ユーザー"  # フィールドのラベルを日本語に変更
    )

    class Meta:
        model = Group
        fields = ['name', 'users']
        labels = {
            'name': 'グループ名',  # フィールドのラベルを日本語に変更
        }

class GroupItemForm(forms.ModelForm):
    class Meta:
        model = GroupItem
        fields = ['name', 'description']

class AddMemberForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all())

class RemoveMemberForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        super(RemoveMemberForm, self).__init__(*args, **kwargs)
        if group:
            self.fields['users'].queryset = group.users.all()