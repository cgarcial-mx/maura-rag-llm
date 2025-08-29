# python-scripts/generate_content.py

import os
import sys
import json
import time
from pathlib import Path
import logging
from typing import Dict, List

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent))

from content_generator.segment_content_generator import SegmentContentGenerator
from config.settings import CHROMA_HOST, CHROMA_PORT

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/content_generation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def generate_content_for_all_segments():
    """
    Genera contenido para todos los segmentos y lo exporta como JSON
    """
    try:
        # Inicializar generador de contenido
        generator = SegmentContentGenerator(
            chroma_host=CHROMA_HOST,
            chroma_port=CHROMA_PORT
        )
        
        # Definir los 20 segmentos
        segments = [
            "SEG001", "SEG002", "SEG003", "SEG004", "SEG005",  # Folicular
            "SEG006", "SEG007", "SEG008", "SEG009", "SEG010",  # Ovulatoria
            "SEG011", "SEG012", "SEG013", "SEG014", "SEG015",  # Lútea
            "SEG016", "SEG017", "SEG018", "SEG019", "SEG020"   # Menstrual
        ]
        
        # Tipos de contenido a generar
        content_types = [
            "lesson_3min",
            "whats_happening", 
            "nutrition_guide",
            "chart_explanation"
        ]
        
        generated_content = []
        
        for segment_id in segments:
            logger.info(f"Generando contenido para segmento: {segment_id}")
            
            for content_type in content_types:
                try:
                    # Generar contenido
                    content = generator.generate_content_for_segment(
                        segment_id=segment_id,
                        content_type=content_type
                    )
                    
                    if content:
                        content_data = {
                            "segment_id": segment_id,
                            "content_type": content_type,
                            "content": content,
                            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
                        }
                        generated_content.append(content_data)
                        
                        logger.info(f"✓ {segment_id} - {content_type}: Generado")
                    
                except Exception as e:
                    logger.error(f"Error generando {content_type} para {segment_id}: {e}")
                    continue
        
        # Guardar como JSON
        if generated_content:
            export_path = Path("data/exports") / f"generated_content_{int(time.time())}.json"
            export_path.parent.mkdir(exist_ok=True)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(generated_content, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✓ {len(generated_content)} piezas de contenido exportadas a: {export_path}")
        
    except Exception as e:
        logger.error(f"Error en generación de contenido: {e}")
        raise

if __name__ == "__main__":
    generate_content_for_all_segments()