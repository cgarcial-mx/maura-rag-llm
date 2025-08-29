# content_generator/ollama_client.py
import requests
import logging
from typing import Optional
from config.settings import OLLAMA_HOST, OLLAMA_PORT

logger = logging.getLogger(__name__)

class OllamaClient:
    """
    Cliente para comunicarse con Ollama
    """
    
    def __init__(self):
        self.base_url = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"
    
    def generate_content(self, prompt: str, model: str = "salud-femenina") -> Optional[str]:
        """
        Genera contenido usando Ollama
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                logger.error(f"Error en Ollama: {response.status_code}")
                return ""
                
        except Exception as e:
            logger.error(f"Error comunicándose con Ollama: {e}")
            return ""
    
    def test_connection(self) -> bool:
        """
        Prueba la conexión con Ollama
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            return response.status_code == 200
        except:
            return False