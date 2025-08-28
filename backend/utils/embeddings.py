from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import retrieval_qa
from langchain_core.prompts import PromptTemplate
from backend.utils.vectorstore import get_vectorstore
from backend.utils.config import LLM_PROVIDER, OLLAMA_MODEL
from langchain_ollama import OllamaLLM

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
    if _llm is not None:
        return _llm
    _llm = OllamaLLM(model_name=OLLAMA_MODEL, temperature=0.2)
    return _llm

RAG_PROMPT = PromptTemplate.from_template(
    """
    You are a helpful AI assistant. Use the following context to answer the question.
    If the answer is not in the context, say you don't know.
    Context:\n{context}\n\nQuestion: {question}
    """
)
def get_llm_chain(retriever):
    llm = get_llm()
    chain = retrieval_qa.RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": RAG_PROMPT},
        return_source_documents=True
    )
    return chain


