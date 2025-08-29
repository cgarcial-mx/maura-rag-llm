# python-scripts/config/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Chroma configuration
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8000))

# Mistral OCR configuration (opcional)
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Ollama configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_PORT = int(os.getenv("OLLAMA_PORT", 11434))
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "salud-femenina")

# Processing configuration
MAX_CHUNK_SIZE = 400
MIN_CHUNK_SIZE = 100
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"