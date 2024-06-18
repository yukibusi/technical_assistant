import bs4
from dotenv import dotenv_values
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from memo_rag import retriever, vectorstore


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def main(error):
    prompt = hub.pull("rlm/rag-prompt")

    OPENAI_API_KEY = dotenv_values()["OPENAI_API_KEY"]

    llm = ChatOpenAI(
        model="gpt-4o",
        api_key=OPENAI_API_KEY,
        # temperature=0,
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
    error = input("解決したいエラーを入力してください：")
    assist = main(error)
    print(assist)