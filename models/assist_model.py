import bs4
from dotenv import dotenv_values
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from memo_rag import retriever, vectorstore, prompt


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


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

print(rag_chain.invoke(f"入力されたエラーの解決方法を表示してください\n{input("エラー：")}"))