from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from backend.utils.vectorstore import add_text, add_file

router = APIRouter()

@router.post("/text")
async def ingest_text(texts: List[str]):
    try:
        count = add_text(texts)
        return {"ingested": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/file")
async def ingest_file(file: UploadFile = File(...)):
    try:
        contents = add_file(file)
        return {"ingested": contents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))