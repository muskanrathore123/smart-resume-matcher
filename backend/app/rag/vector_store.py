# ChromaDB setup
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
import os

# Here is configure chroma
embeddings = OllamaEmbeddings(model="nomic-embed-text")

def get_vectorstore(collection_name: str = "resume_matcher", persist_dir="./chroma_db"):
    os.makedirs(persist_dir, exist_ok=True)
    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_dir
    )

def add_documents_to_store(docs, collection_name: str = "resume_matcher"):
    vectorstore = get_vectorstore(collection_name)
    vectorstore.add_documents(docs)
    return vectorstore
    '''
   collection = vectorstore._collection
   print(collection.count())
    data = collection.get()
    print(data.keys())
    print(data["documents"])
    '''
   