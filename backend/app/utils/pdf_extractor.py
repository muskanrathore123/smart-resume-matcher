import fitz  # PyMuPDF
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def load_and_split_documents(file_paths: list[str], chunk_size=1200, chunk_overlap=180):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?"]
    )
    all_docs = []
    for path in file_paths:
        loader = PyMuPDFLoader(path)
        docs = loader.load()
        all_docs.extend(docs)
    return splitter.split_documents(all_docs)