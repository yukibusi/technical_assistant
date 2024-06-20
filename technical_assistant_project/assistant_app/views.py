from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import GitIssueForm, SignUpForm
from .models import GitIssue
from django.contrib.auth import login, authenticate
from django.views.generic import ListView

# Create your views here.
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
        input_text = request.POST.get('input_text', '')  # Retrieve input text from POST data
        
        # ここで入力テキストのバリデーションや必要な処理を行う（例：データベースへの保存など）
        
        # テンプレートに入力テキストを渡してmemo.htmlを再レンダリング
        return render(request, 'memo.html', {'input_text': input_text})
    
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
            input_text = txt_file.read().decode('utf-8')
            
            # ここで必要な処理を行う（例：入力テキストのバリデーション、データベースへの保存など）
            
            # テンプレートに入力テキストを渡してmemo.htmlを再レンダリング
            return render(request, 'memo_file.html', {'input_text': input_text})
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
        
        # ここで入力テキストのバリデーションや必要な処理を行う（例：データベースへの保存など）
        
        # テンプレートに入力テキストを渡してmemo.htmlを再レンダリング
        return render(request, 'support.html', {'input_text': input_text})
    
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
            git_issue.user = request.user
            git_issue.save()
            output_text = '保存が完了しました'
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

class Issues_List(ListView):
    template_name = 'issues_list.html'
    model = GitIssue
