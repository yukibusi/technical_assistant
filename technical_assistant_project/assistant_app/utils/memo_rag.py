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
#database_dir = "../memo_database"
#add_docs_from_formatted_memos = True
#formatted_memos_dir = "../error_file_modify"
#added_memo_file_names_dir = "../added_memo_file_names"
#fewshot_path = "./fewshot.txt"

def create_vectorstore_and_retriever(added_memo_file_names_dir, database_dir, formatted_memos_dir, openai_api_key):
    if len(os.listdir(added_memo_file_names_dir)) == 0:
        added_memo_file_names = set()
    else:
        with open(added_memo_file_names_dir + '/added_memo_file_names.pickle', mode='rb') as f:
            added_memo_file_names = pickle.load(f)

    embedding = OpenAIEmbeddings(
        model="text-embedding-3-large",
        openai_api_key=openai_api_key
    )

    vectorstore = Chroma(persist_directory=database_dir, embedding_function=embedding)

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

    return vectorstore, retriever

def write_formatted_memo(fewshot_path, openai_api_key, question, add_to_database=False, added_memo_file_names_dir=None, database_dir=None, formatted_memos_dir=None):
    write_memo_llm = ChatOpenAI(model="gpt-4o",
                                openai_api_key=OPENAI_API_KEY,
                                temperature=0)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "あなたはソフトウェア開発者です。ユーザーのfewshotを参考に出力してください。ただし、fewshotの部分は出力しないで下さい。"),
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

    result = chain.invoke(fewshot + f"""フォーマット化する前のメモ:\n{question}\n\nフォーマット化したメモ:""")

    if add_to_database:
        if len(os.listdir(added_memo_file_names_dir)) == 0:
            added_memo_file_names = set()
        else:
            with open(added_memo_file_names_dir + '/added_memo_file_names.pickle', mode='rb') as f:
                added_memo_file_names = pickle.load(f)

        embedding = OpenAIEmbeddings(
            model="text-embedding-3-large",
            openai_api_key=openai_api_key
        )

        vectorstore = Chroma(persist_directory=database_dir, embedding_function=embedding)

        filename = question[:50].replace("/","").replace('"',"").replace(" ","").replace("\n","").replace("[","").replace("]","").replace(",","").replace("<","").replace(">","").replace(":","") + ".txt"
        if filename not in added_memo_file_names:
            vectorstore._collection.add(
                ids=[str(vectorstore._collection.count()+1)],
                embeddings=[embedding.embed_query(result)],
                metadatas=[{"filename": filename}],
                documents=[result]
            )
            added_memo_file_names.add(filename)

        with open(added_memo_file_names_dir + '/added_memo_file_names.pickle', mode='wb') as f:
            pickle.dump(added_memo_file_names, f)
        with open(formatted_memos_dir + f"/{filename}", mode='w') as f:
            f.write(result)

    return result