import os
import glob
import pickle
#import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import dotenv_values

#この四つは変えて大丈夫
database_dir = "../memo_database"
add_docs_from_formatted_memos = True
formatted_memos_dir = "../error_file_modify"
added_memo_file_names_dir = "../added_memo_file_names"

if len(os.listdir(added_memo_file_names_dir)) == 0:
    added_memo_file_names = set()
else:
    with open(added_memo_file_names_dir + '/added_memo_file_names.pickle', mode='rb') as f:
        added_memo_file_names = pickle.load(f)

#OPENAI_API_KEY=str(dotenv_values()["OPENAI_API_KEY"])
embedding = OpenAIEmbeddings(
    model="text-embedding-3-large",
    #openai_api_key=OPENAI_API_KEY
)

vectorstore = Chroma(persist_directory=database_dir, embedding_function=embedding)

if add_docs_from_formatted_memos:
    for path in glob.glob(formatted_memos_dir + '/*.txt'):
        filename = path.split("/")[-1]
        if filename not in added_memo_file_names:
            with open(path) as f:
                doc = f.read()
            vectorstore._collection.add(
                ids=[str(vectorstore._collection.count()+1)],
                embeddings=[embedding.embed_query(doc)],
                metadatas=[{"filename": filename}],
                documents=[doc]
            )
            added_memo_file_names.add(filename)

with open(added_memo_file_names_dir + '/added_memo_file_names.pickle', mode='wb') as f:
    pickle.dump(added_memo_file_names, f)

print(vectorstore._collection.count())
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 1})
retrieved_docs = retriever.invoke('TypeError: can only concatenate list (not "str") to list')
print(retrieved_docs[0].page_content)


memo_rag_llm = ChatOpenAI(model="gpt-4o")


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "あなたはソフトウェア開発者です。ユーザーのfewshotを参考に出力してください。"),
        ("human", "{question}"),
    ]
)

question = """フォーマット化する前のメモ:
MNISTをダウンロード・表示させるプログラムである，ch3/mnist_show.pyを実行すると以下のエラーを吐きます．urllib.error.HTTPError: HTTP Error 403: Forbiddendataset/mnist.py内の関数_downloadを以下に変更することで解決しました．def _download(file_name):
file_path = dataset_dir + "/" + file_name

if os.path.exists(file_path):
    return

print("Downloading " + file_name + " ... ")
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
    }
request = urllib.request.Request(url_base+file_name, headers=headers)
response = urllib.request.urlopen(request).read()
with open(file_path, mode='wb') as f:
    f.write(response)
print("Done")DL先のサイトhttp://yann.lecun.com/へのアクセス権限がないことが原因のようです．「ブラウザからのアクセスだよ」と伝えてあげる必要があります．私の場合はヘッダーをFirefoxと偽装することで解決しました．ありがとうございます。コード修正しました。f549a18

フォーマット化したメモ:
生原因:
なし

生エラー:
urllib.error.HTTPError: HTTP Error 403: Forbidden

要約原因:
DL先のサイトhttp://yann.lecun.com/ へのアクセス権限がないことが原因です。

要約エラー:
アクセス権限がないためHTTP Error 403が発生しました。

解決策:
dataset/mnist.py内の関数_downloadを以下に変更することで解決しました．

def _download(file_name):
    file_path = dataset_dir + "/" + file_name

    if os.path.exists(file_path):
        return

    print("Downloading " + file_name + " ... ")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
        }
    request = urllib.request.Request(url_base+file_name, headers=headers)
    response = urllib.request.urlopen(request).read()
    with open(file_path, mode='wb') as f:
        f.write(response)
    print("Done")


フォーマット化する前のメモ:
3章のMNIST画像（手書き数字認識のサンプル画像）を表示する部分ですがmnist_show.pyを実行すると% python mnist_show.py
Traceback (most recent call last):
  File "mnist_show.py", line 6, in <module>
    from PIL import Image
ModuleNotFoundError: No module named 'PIL'PILのライブラリが存在しないと言うエラーになります。こちらですがpillowをインストールで解決致しました。pip3 install pillowどこかに補足など頂けると幸いでございます。参考にさせていただたURLhttps://qiita.com/ukwksk/items/483d1b9e525667b77187
@3panda私も引っかかりissueにあがってないか確認したら、同じように困ってる方がいて自分だけではないということに安心しました。笑どうやら、PIL は開発が中止されてしまい、代わりにそこから枝分かれした、Pillowが使われているようです。https://note.nkmk.me/python-pillow-basic/

フォーマット化したメモ:
生原因:
Traceback (most recent call last):
  File "mnist_show.py", line 6, in <module>
    from PIL import Image

生エラー:
ModuleNotFoundError: No module named 'PIL'

要約原因:
PILのライブラリがインストールされていないことが原因です。

要約エラー:
PILが存在しないためインポートができない。

解決策:
PIL は開発が中止されているので、代わりにそこから枝分かれした、Pillowをインストールして使用してください。


フォーマット化する前のメモ:
sys.path.append(os.pardir)だと、下記のエラーが出ました。Traceback (most recent call last):
  File "ch05/gradient_check.py", line 5, in <module>
    from dataset.mnist import load_mnist
ModuleNotFoundError: No module named 'dataset'os.pardirのところをフルパス (e.g.Users/user_name/deep-learning-from-scratch)にしたところ動きました。環境はmacOS High SierraPython 3.6.2anaconda 1.6.5です。
import os
import sys
sys.path.append(os.path.abspath('..'))とすれば，自動的にフルパスで展開してくれます．私の手元の環境は，Ubuntu 16.04Python 3.5.2です．
from dataset.mnist import load_mnistImportError: No module named 'dataset.mnist'

フォーマット化したメモ:
生原因:
Traceback (most recent call last):
  File "ch05/gradient_check.py", line 5, in <module>
    from dataset.mnist import load_mnist

生エラー:
ModuleNotFoundError: No module named 'dataset'

要約原因:
sys.path.append(os.pardir)と相対パスで指定していることが原因。

要約エラー:
datasetディレクトリを見つけることができませんでした。

解決策:
絶対パスで指定してimportしてください。
import os
import sys
sys.path.append(os.path.abspath('..'))
のようにすれば自動的に絶対パスで展開できます。


"""



rag_chain = (
    {"question": RunnablePassthrough()}
    | prompt
    | memo_rag_llm
    | StrOutputParser()
)

result = rag_chain.invoke(question + """"フォーマット化する前のメモ:
Traceback (most recent call last):
  File "/home/ubuntu/group_1_work/technical_assistant/error_check_file_05.py", line 3, in <module>
    with open("nonexistent_file.txt", "r") as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
フォーマット化したメモ:
""")
print(result)