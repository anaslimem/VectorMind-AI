from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from backend.utils.vectorstore import get_retriever
from backend.utils.embeddings import get_llm_chain

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    k: int = 2

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]

@router.post("/", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        retriever = get_retriever(k=request.k)
        llm_chain = get_llm_chain(retriever)
        result = llm_chain.invoke({"question": request.question})
        # Use the retriever and llm_chain to process the query
        answer = result.get("result", "")
        sources = result.get("source_documents", [])
        sources = [
            {"source": d.metadata.get("source", ""), "page": d.metadata.get("page"), "score": d.metadata.get("score")}
            for d in sources
        ]
        return QueryResponse(answer=answer, sources=sources)
    
    except Exception as e:
        print(f"Error in query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    