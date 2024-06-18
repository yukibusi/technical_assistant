import os
import glob
import pickle
#import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
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