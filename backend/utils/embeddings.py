from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from backend.utils.config import OLLAMA_MODEL
from langchain_ollama import OllamaLLM
import os 

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL")
_embeddings = None

def get_embedding():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return _embeddings
# LLM
_llm = None
def get_llm():
    global _llm
    if _llm is None:
        _llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_URL)
    return _llm

RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    You are a helpful AI assistant. Use the following context to answer the question.
    If the answer is not in the context, say you don't know.

    Context:
    {context}

    Query:
    {question}
    """
)
def get_llm_chain(retriever):
    llm = get_llm()
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": RAG_PROMPT}, 
        return_source_documents=True,
        input_key="question"
    )
    return chain


