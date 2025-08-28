import os 
from typing import List
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from backend.utils.embeddings import get_embedding
from backend.utils.config import PERSIST_DIR

_vs = None
_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)

def get_vectorstore() -> Chroma:
    global _vs
    if _vs is None:
        os.makedirs(PERSIST_DIR, exist_ok=True)
        _vs = Chroma(
            embedding_function=get_embedding(),
            persist_directory=PERSIST_DIR
        )
    return _vs

def get_retriever(k: int = 4 ) -> Chroma:
    return get_vectorstore().as_retriever(search_kwargs={"k": k})

def add_text(texts: List[str]) -> int:
    docs = _splitter.create_documents(texts, metadatas=[{"source": "api:text"}] * len(texts))
    get_vectorstore().add_documents(docs)
    get_vectorstore().persist()
    return len(docs)

def add_file(upload_file) -> int:
    suffix = (upload_file.filename or "").lower()
    if suffix.endswith(".pdf"):
        # Save temp
        tmp_path = f"/tmp/{upload_file.filename}"
        with open(tmp_path, "wb") as f:
            f.write(upload_file.file.read())
        loader = PyPDFLoader(tmp_path)
    else:
        tmp_path = f"/tmp/{upload_file.filename}"
        with open(tmp_path, "wb") as f:
            f.write(upload_file.file.read())
        loader = TextLoader(tmp_path)

    pages = loader.load()
    # Split and store 
    chunks = _splitter.split_documents(pages)
    get_vectorstore().add_documents(chunks)
    get_vectorstore().persist()
    return len(chunks)
