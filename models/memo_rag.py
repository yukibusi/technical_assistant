import os
import glob
import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import dotenv_values

database_dir = "../memo_database"
add_docs_from_formatted_memos = False
formatted_memos_dir = "../formatted_memos"

#OPENAI_API_KEY=str(dotenv_values()["OPENAI_API_KEY"])
embedding = OpenAIEmbeddings(
    model="text-embedding-3-large",
    #openai_api_key=OPENAI_API_KEY
)

vectorstore = Chroma(persist_directory=database_dir, embedding_function=embedding)

if add_docs_from_formatted_memos:
    for path in glob.glob(formatted_memos_dir + '/*'):
        with open(path) as f:
            doc = f.read()
        vectorstore._collection.add(
            ids=[str(vectorstore._collection.count()+1)],
            embeddings=[embedding.embed_query(doc)],
            metadatas=[{"key": "value"}],
            documents=[doc]
        )

retriever = vectorstore.as_retriever()