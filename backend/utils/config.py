import os 
from dotenv import load_dotenv

load_dotenv()

# Directories
DATA_DIR = os.getenv("DATA_DIR", "./data")
PERSIST_DIR = os.getenv("PERSIST_DIR", "./.chroma")

# LLM provider: Ollama
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "OLLAMA").upper()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

# Redis, used by worker for caching
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")