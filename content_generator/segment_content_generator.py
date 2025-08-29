# python-scripts/content_generator/segment_content_generator.py

import chromadb
import requests
import logging
from typing import Dict, Optional
from config.settings import OLLAMA_HOST, OLLAMA_PORT, OLLAMA_MODEL

logger = logging.getLogger(__name__)

class SegmentContentGenerator:
    """
    Genera contenido personalizado para cada segmento usando Chroma DB y Ollama
    """
    
    def __init__(self, chroma_host: str = "localhost", chroma_port: int = 8000):
        self.chroma_client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        self.ollama_url = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"
        
        # Obtener colección de Chroma
        try:
            self.collection = self.chroma_client.get_collection("salud_femenina_knowledge")
            logger.info("✓ Conectado a Chroma DB")
        except:
            logger.error("No se pudo conectar a Chroma DB")
            raise
    
    def generate_content_for_segment(self, segment_id: str, content_type: str) -> Optional[str]:
        """
        Genera contenido específico para un segmento y tipo de contenido
        """
        try:
            # Buscar contenido relevante en Chroma para este segmento
            # Cambiar la consulta para usar operadores válidos de ChromaDB
            search_results = self.collection.query(
                query_texts=[f"contenido {content_type} {segment_id}"],
                # Usar $in en lugar de $contains, o buscar por texto directamente
                n_results=3
            )
            
            if not search_results['documents'] or not search_results['documents'][0]:
                logger.warning(f"No se encontró contenido para {segment_id} - {content_type}")
                return None
            
            # Construir prompt para Ollama
            prompt = self._build_content_prompt(segment_id, content_type, search_results)
            
            # Generar contenido con Ollama
            content = self._generate_with_ollama(prompt)
            
            return content
            
        except Exception as e:
            logger.error(f"Error generando contenido para {segment_id} - {content_type}: {e}")
            return None
    
    def _build_content_prompt(self, segment_id: str, content_type: str, search_results: Dict) -> str:
        """
        Construye el prompt específico para generar contenido
        """
        # Obtener información del segmento
        segment_info = self._get_segment_info(segment_id)
        
        # Obtener contenido relevante
        relevant_content = search_results['documents'][0][0] if search_results['documents'][0] else ""
        
        prompt = f"""
        TIPO DE CONTENIDO: {content_type}
        SEGMENTO: {segment_info['name']} - {segment_info['description']}
        
        CONTEXTO HORMONAL Y EMOCIONAL:
        - Fase del ciclo: {segment_info['phase']}
        - Estado emocional dominante: {segment_info['emotional_state']}
        - Desafíos típicos: {segment_info['common_challenges']}
        - Oportunidades de esta fase: {segment_info['opportunities']}
        
        INFORMACIÓN MÉDICA RELEVANTE:
        {relevant_content}
        
        INSTRUCCIONES:
        Genera contenido específico para este segmento y tipo de contenido.
        El contenido debe ser empático, científicamente preciso y accionable.
        
        CONTENIDO GENERADO:
        """
        
        return prompt
    
    def _get_segment_info(self, segment_id: str) -> Dict:
        """
        Obtiene información del segmento específico
        """
        # Mapeo de segmentos (puedes expandir esto)
        segment_mapping = {
            "SEG001": {
                "name": "Folicular Estresada",
                "description": "Estrógeno creciente pero cortisol alto",
                "phase": "folicular",
                "emotional_state": "estresada",
                "common_challenges": ["manejo del estrés", "aprovechamiento de energía"],
                "opportunities": ["reducción de cortisol", "optimización hormonal"]
            },
            "SEG003": {
                "name": "Folicular Energética", 
                "description": "Alineación óptima con aumento hormonal",
                "phase": "folicular",
                "emotional_state": "energética",
                "common_challenges": ["canalizar energía", "mantener enfoque"],
                "opportunities": ["nuevos proyectos", "optimización personal"]
            }
            # ... agregar para todos los 20 segmentos
        }
        
        return segment_mapping.get(segment_id, {
            "name": f"Segmento {segment_id}",
            "description": "Información no disponible",
            "phase": "desconocida",
            "emotional_state": "desconocida",
            "common_challenges": [],
            "opportunities": []
        })
    
    def _generate_with_ollama(self, prompt: str) -> str:
        """
        Genera contenido usando Ollama
        """
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
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