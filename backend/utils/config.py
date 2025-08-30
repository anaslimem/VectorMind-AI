import os 
from dotenv import load_dotenv


# LLM provider: Ollama
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "OLLAMA").upper()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
