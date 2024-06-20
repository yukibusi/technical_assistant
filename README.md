# テクニカルアシスタントアプリ(開発時のトラブル早期解決)

これまで様々なエンジニアが経験したエラーへの対処法がまとまっているメモ等を有効活用して、取り組むべき業務に集中できることを目標とします。

# 実演例

実際にアプリを使ってトラブルを解決している出力の結果のスクショみたいなものを載せる(完成したあとで適宜埋める)


# モチベーションと概要

* ある程度のサポートは可能だが、各々のチーム毎にあった環境に対応するサービスは少ない上、Chat GPT等に質問しても完全な解答がかえってくるとは限りません。
* そこで開発時のトラブルをGitHubのissueなどを有効的に参照することで、より迅速かつ正確な解答をエンジニアに提供可能になります。
* そのためにRAGという技術を用います。

# 必要なライブラリ

動かすのに必要なライブラリなどを列挙する（適宜埋めていく）

* langchain
* langchain_chroma
* langchain_community
* langchain_core
* langchain_openai
* langchain_text_splitters
* dotenv 

# インストール方法

Requirementで列挙したライブラリなどのインストール方法を説明する（適宜埋めていく）


```bash
pip install langchain
pip install langchain_chroma
pip install langchain_community.document_loaders
pip install langchain_core.output_parsers
pip install langchain_core.runnables
pip install langchain_core.prompts
pip install langchain_openai
pip install langchain_openai
pip install langchain_text_splitters
pip install dotenv 
```

# 使用方法

実行方法など、基本的な使い方を説明する(適宜埋めていく)

コードの例

```bash
git clone https://github.com/hoge/~
cd examples
python demo.py
```

# 注意

使用の際に注意点などがあれば書く

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