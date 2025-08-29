# generate_expanded_content.py

import os
import sys
import json
import time
from pathlib import Path
import logging
from typing import Dict, List, Any

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent))

from segment_processor.expanded_content_generator import ExpandedContentGenerator
from segment_processor.expanded_segments import ExpandedSegmentDatabase
from config.settings import CHROMA_HOST, CHROMA_PORT

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/expanded_content_generation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def generate_expanded_content():
    """
    Genera contenido para todos los segmentos expandidos
    """
    try:
        logger.info("=== INICIANDO GENERACIÓN DE CONTENIDO EXPANDIDO ===")
        
        # Inicializar generador
        generator = ExpandedContentGenerator(
            chroma_host=CHROMA_HOST,
            chroma_port=CHROMA_PORT
        )
        
        # Mostrar información de segmentos disponibles
        segment_db = ExpandedSegmentDatabase()
        all_segments = segment_db.get_all_segments()
        
        logger.info(f"Segmentos disponibles: {len(all_segments)}")
        for segment_id, segment in all_segments.items():
            logger.info(f"  - {segment_id}: {segment.name} ({segment.category})")
        
        # Generar contenido para todos los segmentos
        result = generator.generate_content_for_all_expanded_segments()
        
        if result["success"]:
            logger.info("=== GENERACIÓN COMPLETADA EXITOSAMENTE ===")
            logger.info(f"Total de contenido generado: {result['total_content']}")
            logger.info(f"Archivo exportado: {result['export_path']}")
            
            # Mostrar estadísticas
            stats = result["statistics"]
            logger.info("=== ESTADÍSTICAS ===")
            logger.info(f"Total de piezas: {stats['total_pieces']}")
            logger.info(f"Distribución por prioridad:")
            logger.info(f"  - Alta (≥0.8): {stats['priority_distribution']['high']}")
            logger.info(f"  - Media (0.5-0.8): {stats['priority_distribution']['medium']}")
            logger.info(f"  - Baja (<0.5): {stats['priority_distribution']['low']}")
            
            logger.info("Por categoría:")
            for category, count in stats['by_category'].items():
                logger.info(f"  - {category}: {count}")
            
            logger.info("Por fase:")
            for phase, count in stats['by_phase'].items():
                logger.info(f"  - {phase}: {count}")
            
            logger.info("Por tipo de contenido:")
            for content_type, count in stats['by_content_type'].items():
                logger.info(f"  - {content_type}: {count}")
            
        else:
            logger.error("=== ERROR EN LA GENERACIÓN ===")
            logger.error(f"Error: {result['error']}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error en generación de contenido expandido: {e}")
        return False

def generate_content_for_specific_segment(segment_id: str, content_types: List[str] = None):
    """
    Genera contenido para un segmento específico
    """
    try:
        logger.info(f"=== GENERANDO CONTENIDO PARA SEGMENTO: {segment_id} ===")
        
        # Inicializar generador
        generator = ExpandedContentGenerator(
            chroma_host=CHROMA_HOST,
            chroma_port=CHROMA_PORT
        )
        
        # Obtener segmento
        segment_db = ExpandedSegmentDatabase()
        segment = segment_db.get_segment(segment_id)
        
        if not segment:
            logger.error(f"Segmento {segment_id} no encontrado")
            return False
        
        logger.info(f"Segmento encontrado: {segment.name}")
        logger.info(f"Categoría: {segment.category}")
        logger.info(f"Fase: {segment.phase}")
        logger.info(f"Estado emocional: {segment.emotional_primary}")
        
        # Tipos de contenido por defecto
        if not content_types:
            content_types = [
                "lesson_3min",
                "whats_happening", 
                "nutrition_guide",
                "chart_explanation"
            ]
        
        generated_content = []
        
        for content_type in content_types:
            logger.info(f"Generando {content_type}...")
            
            try:
                content = generator.generate_content_for_expanded_segment(
                    segment_id=segment_id,
                    content_type=content_type
                )
                
                if content:
                    content_data = {
                        "segment_id": segment_id,
                        "segment_name": segment.name,
                        "content_type": content_type,
                        "content": content,
                        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    generated_content.append(content_data)
                    logger.info(f"✓ {content_type}: Generado")
                else:
                    logger.warning(f"✗ {content_type}: No generado")
                    
            except Exception as e:
                logger.error(f"Error generando {content_type}: {e}")
                continue
        
        # Guardar resultados
        if generated_content:
            export_path = Path("data/exports") / f"{segment_id}_content_{int(time.time())}.json"
            export_path.parent.mkdir(exist_ok=True)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(generated_content, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✓ {len(generated_content)} piezas de contenido exportadas a: {export_path}")
            return True
        else:
            logger.error("No se generó contenido")
            return False
            
    except Exception as e:
        logger.error(f"Error generando contenido para segmento específico: {e}")
        return False

def list_available_segments():
    """
    Lista todos los segmentos disponibles
    """
    try:
        segment_db = ExpandedSegmentDatabase()
        all_segments = segment_db.get_all_segments()
        
        print("\n=== SEGMENTOS EXPANDIDOS DISPONIBLES ===\n")
        
        # Agrupar por categoría
        categories = {}
        for segment_id, segment in all_segments.items():
            if segment.category not in categories:
                categories[segment.category] = []
            categories[segment.category].append((segment_id, segment))
        
        for category, segments in categories.items():
            print(f"📁 {category.upper().replace('_', ' ')}")
            for segment_id, segment in segments:
                print(f"  • {segment_id}: {segment.name}")
                print(f"    Fase: {segment.phase}")
                if segment.emotional_primary:
                    print(f"    Estado emocional: {segment.emotional_primary}")
                if segment.intensity_level:
                    print(f"    Intensidad: {segment.intensity_level}")
                print()
        
        print(f"Total: {len(all_segments)} segmentos")
        
    except Exception as e:
        logger.error(f"Error listando segmentos: {e}")

def save_segments_database():
    """
    Guarda la base de datos de segmentos a un archivo JSON
    """
    try:
        segment_db = ExpandedSegmentDatabase()
        export_path = Path("data/exports") / "expanded_segments_database.json"
        export_path.parent.mkdir(exist_ok=True)
        
        segment_db.save_to_file(str(export_path))
        logger.info(f"✓ Base de datos de segmentos guardada en: {export_path}")
        
    except Exception as e:
        logger.error(f"Error guardando base de datos: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generador de contenido expandido para segmentos")
    parser.add_argument("--action", choices=["all", "segment", "list", "save"], default="all",
                       help="Acción a realizar")
    parser.add_argument("--segment-id", help="ID del segmento para generar contenido específico")
    parser.add_argument("--content-types", nargs="+", 
                       help="Tipos de contenido a generar")
    
    args = parser.parse_args()
    
    if args.action == "all":
        generate_expanded_content()
    elif args.action == "segment":
        if not args.segment_id:
            print("Error: --segment-id es requerido para la acción 'segment'")
            sys.exit(1)
        generate_content_for_specific_segment(args.segment_id, args.content_types)
    elif args.action == "list":
        list_available_segments()
    elif args.action == "save":
        save_segments_database()