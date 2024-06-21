import sys
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import GitIssueForm, SignUpForm, GroupForm, GroupItemForm, AddMemberForm, RemoveMemberForm
from .models import GitIssue, Group, GroupItem
from django.contrib.auth import login, authenticate
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
sys.path.append(os.path.join(os.path.dirname(__file__), 'package'))
from .utils.assist_model import main
from .utils.memo_rag import write_formatted_memo
from .utils.issues import get_text_from_issue
from dotenv import load_dotenv, dotenv_values
from technical_assistant_project.settings import BASE_DIR


# Create your views here.
class Issues_List(LoginRequiredMixin, ListView):
    template_name = 'issues_list.html'
    model = GitIssue

@login_required
def index(request):
    return render(request, 'index.html')

from django.shortcuts import render
from django.http import HttpResponse

@login_required
def memo(request):
    if request.method == 'GET':
        return render(request, 'memo.html')
    
    elif request.method == 'POST':
        question =  request.POST.get('input_text', '')  # Retrieve input text from POST data
        
        api_key = str(dotenv_values()["OPENAI_API_KEY"])

        few_shot_path = os.path.join(BASE_DIR, 'assistant_app/utils/fewshot.txt')
        added_memo_file_names_dir = os.path.join(BASE_DIR, 'added_memo_file_names')
        database_dir = os.path.join(BASE_DIR, 'database')
        formatted_memos_dir = os.path.join(BASE_DIR, 'formatted_memos')
    
        output_text = write_formatted_memo(few_shot_path, api_key, question, True, added_memo_file_names_dir, database_dir, formatted_memos_dir)
        # テンプレートに入力テキストを渡してmemo.htmlを再レンダリング
        return render(request, 'memo.html', {'output_text': output_text})
    
    else:
        return HttpResponse('Method Not Allowed', status=405)

@login_required
def memo_file(request):
    if request.method == 'GET':
        return render(request, 'memo_file.html')
    
    elif request.method == 'POST':
        # ファイルがアップロードされたか確認
        if 'txt_file' in request.FILES:
            txt_file = request.FILES['txt_file']
            # ファイルの内容を読み込む
            input_text = txt_file.read().decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')
            
            input_list = input_text.split('\n\n\n')

            api_key = str(dotenv_values()["OPENAI_API_KEY"])

            few_shot_path = os.path.join(BASE_DIR, 'assistant_app/utils/fewshot.txt')
            added_memo_file_names_dir = os.path.join(BASE_DIR, 'added_memo_file_names')
            database_dir = os.path.join(BASE_DIR, 'database')
            formatted_memos_dir = os.path.join(BASE_DIR, 'formatted_memos')
            output_list = []
            for question in input_list:
                output_text = write_formatted_memo(few_shot_path, api_key, question, True, added_memo_file_names_dir, database_dir, formatted_memos_dir)
                output_list.append(output_text)
            output = '<br><br><br>'.join(output_list)
            output = output.replace('\n', '<br>')
            # テンプレートに入力テキストを渡してmemo.htmlを再レンダリング
            return render(request, 'memo_file.html', {'input_text': output})
        else:
            return HttpResponse('ファイルがアップロードされていません。', status=400)
    
    else:
        return HttpResponse('Method Not Allowed', status=405)

@login_required
def support(request):
    if request.method == 'GET':
        return render(request, 'support.html')
    
    elif request.method == 'POST':
        input_text = request.POST.get('input_text', '')  # Retrieve input text from POST data
        # env_path = os.path.join('BASE_DIR', 'assistant_app', '.env')
        # load_dotenv(dotenv_path=env_path)
        # api_key = os.getenv("OPENAI_API_KEY")
        api_key = str(dotenv_values()["OPENAI_API_KEY"])
        added_memo_file_names_dir = os.path.join(BASE_DIR, 'added_memo_file_names')
        database_dir = os.path.join(BASE_DIR, 'database')
        formatted_memos_dir = os.path.join(BASE_DIR, 'formatted_memos')
        error = input_text
        output_text = main(error, api_key, added_memo_file_names_dir, database_dir, formatted_memos_dir)
        # テンプレートに入力テキストを渡してmemo.htmlを再レンダリング
        return render(request, 'support.html', {'output_text': output_text})
    
    else:
        return HttpResponse('Method Not Allowed', status=405)


@login_required
def git_issues(request):
    if request.method == 'GET':
        form = GitIssueForm()
        return render(request, 'git_issues.html', {'form': form})
    
    elif request.method == 'POST':
        form = GitIssueForm(request.POST)
        if form.is_valid():
            git_issue = form.save(commit=False)
            repo = git_issue.repo
            git_issue.description = f"https://github.com/{repo}/issues"
            issues = get_text_from_issue(repo)
            api_key = str(dotenv_values()["OPENAI_API_KEY"])
            few_shot_path = os.path.join(BASE_DIR, 'assistant_app/utils/fewshot.txt')
            added_memo_file_names_dir = os.path.join(BASE_DIR, 'added_memo_file_names')
            database_dir = os.path.join(BASE_DIR, 'database')
            formatted_memos_dir = os.path.join(BASE_DIR, 'formatted_memos')
            for question in issues:
                output_text = write_formatted_memo(few_shot_path, api_key, question[0], True, added_memo_file_names_dir, database_dir, formatted_memos_dir)

            git_issue.user = request.user
            git_issue.save()
            output_text = '保存が完了しました'
            repo = git_issue.repo
            return render(request, 'git_issues.html', {'output_text': output_text})
        else:
            return render(request, 'git_issues.html', {'form': form})
    
    else:
        return HttpResponse('Method Not Allowed', status=405)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('index')  # ログイン後にリダイレクトするURL
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            form.save_m2m()
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'create_group.html', {'form': form})

@login_required
def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.users.all():
        return redirect('group_list')
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = GroupForm(instance=group)
    return render(request, 'edit_group.html', {'form': form})

@login_required
def group_list(request):
    groups = Group.objects.filter(users=request.user)
    return render(request, 'group_list.html', {'groups': groups})

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    items = group.items.all()
    return render(request, 'group_detail.html', {'group': group, 'items': items})

@login_required
def add_group_item(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = GroupItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.group = group
            item.save()
            return redirect('group_detail', group_id=group_id)
    else:
        form = GroupItemForm()
    return render(request, 'add_group_item.html', {'form': form, 'group': group})

@login_required
def add_member(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            users = form.cleaned_data['users']
            group.users.add(*users)
            return redirect('group_detail', group_id=group_id)
    else:
        form = AddMemberForm()
    return render(request, 'add_member.html', {'form': form, 'group': group})

@login_required
def remove_member(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.user != group.created_by:
        return HttpResponseForbidden("You are not allowed to remove members from this group.")

    if request.method == 'POST':
        form = RemoveMemberForm(request.POST, group=group)
        if form.is_valid():
            users = form.cleaned_data['users']
            group.users.remove(*users)
            return redirect('group_detail', group_id=group_id)
    else:
        form = RemoveMemberForm(group=group)
    return render(request, 'remove_member.html', {'form': form, 'group': group})



