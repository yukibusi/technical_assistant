from memo_rag import retriever, vectorstore

print(vectorstore._collection.count())
#retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 1})
retrieved_docs = retriever.invoke('TypeError: can only concatenate list (not "str") to list')
print(retrieved_docs[0].page_content)