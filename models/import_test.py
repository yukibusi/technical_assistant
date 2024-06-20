from memo_rag import create_vectorstore_and_retriever, write_formatted_memo
from dotenv import dotenv_values
OPENAI_API_KEY = str(dotenv_values()["OPENAI_API_KEY"])


vectorstore, retriever = create_vectorstore_and_retriever(
    added_memo_file_names_dir="../added_memo_file_names",
    database_dir="../memo_database",
    formatted_memos_dir="../error_file_modify",
    openai_api_key=OPENAI_API_KEY
)

print(vectorstore._collection.count())
retrieved_docs = retriever.invoke('TypeError: can only concatenate list (not "str") to list')
print(retrieved_docs[0].page_content)


question="""Traceback (most recent call last):
  File "/home/ubuntu/group_1_work/technical_assistant/error_check_file_02.py", line 4, in <module>
    li[6]
    ~~^^^"""

result = write_formatted_memo(
    fewshot_path="./fewshot.txt",
    openai_api_key=OPENAI_API_KEY,
    question=question,
    add_to_database=True,
    added_memo_file_names_dir="../added_memo_file_names",
    database_dir="../memo_database",
    formatted_memos_dir="../error_file_modify",
)

print(result)

vectorstore, retriever = create_vectorstore_and_retriever(
    added_memo_file_names_dir="../added_memo_file_names",
    database_dir="../memo_database",
    formatted_memos_dir="../error_file_modify",
    openai_api_key=OPENAI_API_KEY
)

print(vectorstore._collection.count())