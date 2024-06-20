import os
import glob
import pickle
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
OPENAI_API_KEY = str(dotenv_values()["OPENAI_API_KEY"])

#この四つは変えて大丈夫
database_dir = "../memo_database"
add_docs_from_formatted_memos = True
formatted_memos_dir = "../error_file_modify"
added_memo_file_names_dir = "../added_memo_file_names"
fewshot_path = "./fewshot.txt"

if len(os.listdir(added_memo_file_names_dir)) == 0:
    added_memo_file_names = set()
else:
    with open(added_memo_file_names_dir + '/added_memo_file_names.pickle', mode='rb') as f:
        added_memo_file_names = pickle.load(f)

embedding = OpenAIEmbeddings(
    model="text-embedding-3-large",
    openai_api_key=OPENAI_API_KEY
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

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 1})
retrieved_docs = retriever.invoke('TypeError: can only concatenate list (not "str") to list')

write_memo_llm = ChatOpenAI(model="gpt-4o",
                            openai_api_key=OPENAI_API_KEY,
                            temperature=0)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "あなたはソフトウェア開発者です。ユーザーのfewshotを参考に出力してください。"),
        ("human", "{human_prompt}"),
    ]
)

chain = (
    {"human_prompt": RunnablePassthrough()}
    | prompt
    | write_memo_llm
    | StrOutputParser()
)

with open(fewshot_path) as f:
    fewshot = f.read()

question = """Traceback (most recent call last):
  File "/home/ubuntu/group_1_work/technical_assistant/error_check_file_03.py", line 4, in <module>
    print(personal["mame"])
          ~~~~~~~~^^^^^^^^"""

result = chain.invoke(fewshot + f"""フォーマット化する前のメモ:\n{question}\n\nフォーマット化したメモ:""")
print(result)
print("==========================================================================================")
print(result.split("フォーマット化したメモ:")[1].split("フォーマット化する前のメモ:")[0])