from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import query, ingest
from langchain_community.cache import RedisCache
import langchain
from backend.utils.cache import get_redis_client

print("Initializing Redis client for LLM caching...")
try:
    redis_client = get_redis_client()
    cache = RedisCache(redis_client)
    langchain.llm_cache = cache
    print("Redis LLM cache initialized.")
except Exception as e:
    print(f"Failed to initialize Redis LLM cache: {e}")


app = FastAPI(title="VectorMind AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router, prefix="/query", tags=["query"])
app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])

@app.get("/")
def root():
    return {"service": "VectorMind AI", "status": "ok"}

