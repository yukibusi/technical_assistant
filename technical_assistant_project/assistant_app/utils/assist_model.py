import bs4
import os
from dotenv import dotenv_values, load_dotenv
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from .memo_rag import create_vectorstore_and_retriever


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def main(error, OPENAI_API_KEY, added_memo_file_names_dir, database_dir, formatted_memos_dir):
    prompt = hub.pull("rlm/rag-prompt")

    llm = ChatOpenAI(
        model="gpt-4o",
        api_key=OPENAI_API_KEY,
        # temperature=0,
    )

    vectorstore, retriever = create_vectorstore_and_retriever(
    added_memo_file_names_dir=added_memo_file_names_dir,
    database_dir=database_dir,
    formatted_memos_dir=formatted_memos_dir,
    openai_api_key=OPENAI_API_KEY
    )

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    assist = rag_chain.invoke(f"以下のエラーの解決方法を教えてください。エラー:{error}")
    
    return assist

if __name__ == "__main__":
    env_path = os.path.join('..', '.env')
    print(env_path)
    load_dotenv(dotenv_path=env_path)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_API_KEY = dotenv_values()["OPENAI_API_KEY"]
    added_memo_file_names_dir="../added_memo_file_names"
    database_dir="../memo_database"
    formatted_memos_dir="../error_file_modify"
    error = input("解決したいエラーを入力してください：")
    assist = main(error, OPENAI_API_KEY, added_memo_file_names_dir, database_dir, formatted_memos_dir)
    print(assist)