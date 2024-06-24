# テクニカルアシスタントアプリ(開発時のトラブル早期解決)

これまで様々なエンジニアが経験したエラーへの対処法がまとまっているメモ等を有効活用して、取り組むべき業務に集中できることを目標とします。

# 実演例

実際にアプリを使ってトラブルを解決している出力の結果のスクショみたいなものを載せる(完成したあとで適宜埋める)


# モチベーションと概要

* ある程度のサポートは可能だが、各々のチーム毎にあった環境に対応するサービスは少ない上、Chat GPT等に質問しても完全な解答がかえってくるとは限りません。
* そこで開発時のトラブルをGitHubのissueなどを有効的に参照することで、より迅速かつ正確な解答をエンジニアに提供可能になります。
* そのためにRAGとLang Chainいう技術を用います。
* また、これらの実装のためにwebアプリケーションのフレームワークであるDjangoを使用しました。

# 必要なライブラリ

必要なライブラリは以下の通りです（適宜埋めていく）

* bs4
* langchain
* langchain_chroma
* langchain_community
* langchain_core
* langchain_openai
* langchain_text_splitters
* dotenv 
* requests
* Django

# インストール方法

（適宜埋めていく）


```bash
pip install bs4
pip install langchain
pip install langchain_chroma
pip install langchain_community
pip install langchain_core
pip install langchain_openai
pip install langchain_text_splitters
pip install dotenv 
pip install requests
pip install Django
```

# 使用方法
アプリを立ち上げる場合

```bash
git clone https://github.com/hoge/~
cd technical_assistant_project/
mkdir added_memo_file_names
mkdir formatted_memos
python manage.py runserver
```

アプリ上で使われている機能は
technical_assistant_project/assistant_app/utils/
にpythonファイルが保存されています。

# 注意

git issueからメモを作成する際、git issueの数が多い場合、エラーが出る可能性があります。

# 著者

作成情報を列挙する

* 作成者
* 所属
* E-mail

# ライセンス
ライセンスを明示する

"hoge" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).

社内向けなら社外秘であることを明示してる

"hoge" is Confidential.