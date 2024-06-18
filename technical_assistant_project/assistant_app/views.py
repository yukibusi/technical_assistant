from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

from django.shortcuts import render
from django.http import HttpResponse

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
    
