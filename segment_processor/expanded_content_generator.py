# segment_processor/expanded_content_generator.py

import os
import sys
import json
import time
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent.parent))

from segment_processor.expanded_segments import ExpandedSegmentDatabase, ExpandedSegment
from content_generator.ollama_client import OllamaClient
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

class ExpandedContentGenerator:
    """
    Generador de contenido basado en segmentos expandidos con metadata detallada
    """
    
    def __init__(self, chroma_host: str = CHROMA_HOST, chroma_port: int = CHROMA_PORT):
        self.chroma_host = chroma_host
        self.chroma_port = chroma_port
        self.segment_db = ExpandedSegmentDatabase()
        self.ollama_client = OllamaClient()
        
        # Inicializar cliente de Chroma
        try:
            import chromadb
            self.chroma_client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
            self.collection = self.chroma_client.get_collection("medical_documents")
            logger.info("✓ Conectado a Chroma DB")
        except Exception as e:
            logger.error(f"Error conectando a Chroma DB: {e}")
            self.chroma_client = None
            self.collection = None
    
    def generate_content_for_expanded_segment(
        self, 
        segment_id: str, 
        content_type: str,
        custom_prompt: Optional[str] = None
    ) -> Optional[str]:
        """
        Genera contenido para un segmento expandido específico
        """
        try:
            # Obtener segmento
            segment = self.segment_db.get_segment(segment_id)
            if not segment:
                logger.error(f"Segmento {segment_id} no encontrado")
                return None
            
            # Verificar si el tipo de contenido es recomendado para este segmento
            content_priority = self._get_content_priority(segment, content_type)
            if content_priority < 0.5:
                logger.warning(f"Tipo de contenido {content_type} no recomendado para {segment_id} (prioridad: {content_priority})")
            
            # Obtener contexto relevante
            context = self._get_relevant_context(segment, content_type)
            
            # Generar prompt personalizado
            if custom_prompt:
                prompt = custom_prompt
            else:
                prompt = self._build_content_prompt(segment, content_type, context)
            
            # Generar contenido
            content = self.ollama_client.generate_content(prompt)
            
            if content:
                logger.info(f"✓ Contenido generado para {segment_id} - {content_type}")
                return content
            else:
                logger.error(f"Error generando contenido para {segment_id} - {content_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error en generación de contenido: {e}")
            return None
    
    def _get_content_priority(self, segment: ExpandedSegment, content_type: str) -> float:
        """Obtiene la prioridad de un tipo de contenido para un segmento"""
        content_types = segment.recommended_content_types
        
        priority_map = {
            "lesson_3min": content_types.lesson_3min,
            "whats_happening": content_types.whats_happening,
            "nutrition_guide": content_types.nutrition_guide,
            "cycle_day_info": content_types.cycle_day_info,
            "hormone_levels": content_types.hormone_levels,
            "stress_levels": content_types.stress_levels
        }
        
        return priority_map.get(content_type, 0.0)
    
    def _get_relevant_context(self, segment: ExpandedSegment, content_type: str) -> str:
        """Obtiene contexto relevante de la base de datos para el segmento"""
        if not self.collection:
            return ""
        
        try:
            # Construir query basada en el segmento
            query_terms = self._build_query_terms(segment, content_type)
            
            # Buscar en Chroma DB
            results = self.collection.query(
                query_texts=query_terms,
                n_results=5
            )
            
            # Combinar resultados
            context_parts = []
            if results['documents'] and results['documents'][0]:
                for doc in results['documents'][0]:
                    context_parts.append(doc)
            
            return "\n\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Error obteniendo contexto: {e}")
            return ""
    
    def _build_query_terms(self, segment: ExpandedSegment, content_type: str) -> List[str]:
        """Construye términos de búsqueda basados en el segmento"""
        query_terms = []
        
        # Fase + emociones principales
        if segment.emotional_primary:
            query_terms.append(f"{segment.phase} {segment.emotional_primary}")
        
        # Síntomas físicos comunes
        if segment.physical_symptoms and segment.physical_symptoms.common:
            query_terms.append(" ".join(segment.physical_symptoms.common[:3]))
        
        # Áreas de enfoque del contenido
        if segment.content_preferences.focus_areas:
            query_terms.append(" ".join(segment.content_preferences.focus_areas[:2]))
        
        # Tipo de contenido específico
        content_type_queries = {
            "lesson_3min": ["lección", "educación", "aprendizaje", "consejos"],
            "whats_happening": ["qué está pasando", "explicación", "cambios", "cuerpo", "mente"],
            "nutrition_guide": ["nutrición", "alimentación", "dieta", "vitaminas", "minerales"],
            "cycle_day_info": ["ciclo menstrual", "fase", "día", "duración", "timing"],
            "hormone_levels": ["hormonas", "estrógeno", "progesterona", "FSH", "hormonal"],
            "stress_levels": ["estrés", "cortisol", "ansiedad", "tensión", "calma"]
        }
        
        if content_type in content_type_queries:
            query_terms.extend(content_type_queries[content_type])
        
        return query_terms
    
    def _build_content_prompt(
        self, 
        segment: ExpandedSegment, 
        content_type: str, 
        context: str
    ) -> str:
        """Construye el prompt para generar contenido específico"""
        
        # Información del segmento
        segment_info = f"""
SEGMENTO: {segment.name} ({segment.id})
FASE: {segment.phase}
CATEGORÍA: {segment.category}
ESTADO EMOCIONAL: {segment.emotional_primary or 'N/A'}
INTENSIDAD: {segment.intensity_level or 'N/A'}
TONO RECOMENDADO: {segment.content_preferences.tone}
URGENCIA: {segment.content_preferences.urgency}
ÁREAS DE ENFOQUE: {', '.join(segment.content_preferences.focus_areas)}
TEMAS A EVITAR: {', '.join(segment.content_preferences.avoid_topics)}
"""
        
        # Características emocionales
        emotional_info = f"""
CARACTERÍSTICAS EMOCIONALES:
- Emociones principales: {', '.join(segment.emotional_characteristics.primary_emotions)}
- Emociones secundarias: {', '.join(segment.emotional_characteristics.secondary_emotions)}
- Rango emocional: {segment.emotional_characteristics.emotional_range}
- Volatilidad: {segment.emotional_characteristics.volatility}
- Tiempo de recuperación: {segment.emotional_characteristics.recovery_time}
"""
        
        # Perfil hormonal
        hormonal_info = f"""
PERFIL HORMONAL:
- Estradiol: {segment.hormonal_profile.estrogen_level}
- Progesterona: {segment.hormonal_profile.progesterone_level}
- Cortisol: {segment.hormonal_profile.cortisol_level or 'N/A'}
- Factores de sensibilidad: {', '.join(segment.hormonal_profile.sensitivity_factors)}
"""
        
        # Síntomas físicos
        physical_info = ""
        if segment.physical_symptoms:
            physical_info = f"""
SÍNTOMAS FÍSICOS:
- Comunes: {', '.join(segment.physical_symptoms.common)}
- Moderados: {', '.join(segment.physical_symptoms.moderate)}
- Severos: {', '.join(segment.physical_symptoms.severe)}
"""
        
        # Demografía
        demographics_info = f"""
DEMOGRAFÍA:
- Grupos de edad: {', '.join(segment.demographics.age_groups)}
- Etapas de vida: {', '.join(segment.demographics.life_stages)}
- Desencadenantes comunes: {', '.join(segment.demographics.common_triggers)}
"""
        
        # Prioridades de intervención
        intervention_info = f"""
PRIORIDADES DE INTERVENCIÓN:
{', '.join(segment.intervention_priorities)}
"""
        
        # Contexto de la base de datos
        context_info = f"""
CONTEXTO MÉDICO RELEVANTE:
{context}
"""
        
        # Instrucciones específicas por tipo de contenido
        content_instructions = self._get_content_type_instructions(content_type, segment)
        
        # Construir prompt completo
        prompt = f"""
Eres una experta en salud femenina y bienestar menstrual. Tu tarea es generar contenido personalizado y empático para mujeres en diferentes fases de su ciclo menstrual.

{segment_info}
{emotional_info}
{hormonal_info}
{physical_info}
{demographics_info}
{intervention_info}
{context_info}

INSTRUCCIONES ESPECÍFICAS PARA {content_type.upper()}:
{content_instructions}

REQUISITOS OBLIGATORIOS:
1. Usa un tono {segment.content_preferences.tone}
2. Mantén un nivel de profundidad {segment.content_preferences.depth}
3. Enfócate en: {', '.join(segment.content_preferences.focus_areas)}
4. EVITA: {', '.join(segment.content_preferences.avoid_topics)}
5. RESPETA ESTRICTAMENTE los límites de longitud especificados para cada tipo de contenido
6. Incluye consejos prácticos y validación emocional
7. NO hagas diagnósticos médicos
8. Usa lenguaje empático y comprensivo
9. Basa el contenido en la información médica proporcionada
10. Dirige el contenido directamente a la usuaria usando "tú" y "tu"

Genera el contenido ahora:
"""
        
        return prompt
    
    def _get_content_type_instructions(self, content_type: str, segment: ExpandedSegment) -> str:
        """Obtiene instrucciones específicas para cada tipo de contenido"""
        
        instructions = {
            "lesson_3min": f"""
Crea una lección educativa de MÁXIMO 3 MINUTOS DE LECTURA (aproximadamente 400-500 palabras) que explique:
- Qué está pasando hormonalmente en la fase {segment.phase}
- Cómo se relaciona con sentirse {segment.emotional_primary}
- Estrategias prácticas para manejar los síntomas
- Validación de las emociones y experiencias
- Consejos específicos para {', '.join(segment.demographics.age_groups)}
- Incluye ejemplos prácticos y accionables

FORMATO: Texto corrido, divídelo en párrafos cortos para facilitar la lectura.
""",
            
            "whats_happening": f"""
Crea un texto de MÁXIMO 4 RENGLONES que explique brevemente:
- Qué está pasando en tu cuerpo durante la fase {segment.phase}
- Por qué te sientes {segment.emotional_primary}
- Cómo los cambios hormonales afectan tu mente y cuerpo
- Que es completamente normal sentirse así

FORMATO: Máximo 4 líneas de texto, directo y empático. Usa "tú" para dirigirte directamente a la usuaria.
EJEMPLO DE FORMATO:
"Durante la fase folicular, tus niveles de estrógeno están aumentando...
Esto hace que te sientas más enérgica pero también puede generar ansiedad...
Tu cuerpo se está preparando para la ovulación y es normal que experimentes...
Estos cambios son parte natural de tu ciclo y pasarán en unos días."
""",
            
            "nutrition_guide": f"""
Proporciona información nutricional específica para la fase {segment.phase} y para manejar sentirse {segment.emotional_primary}:

Incluye:
- 5-7 alimentos específicos recomendados para esta fase y estado emocional
- Nutrientes clave que tu cuerpo necesita ahora (vitaminas, minerales)
- 3-4 alimentos que debes evitar o limitar
- Horarios de comida recomendados para esta fase
- Consejos de hidratación específicos
- 1-2 suplementos que podrían ayudar (si aplica)

FORMATO: Lista organizada con explicaciones breves de por qué cada recomendación es importante para tu fase actual.
""",
            
            "cycle_day_info": f"""
Proporciona información específica sobre la fase del ciclo y el día:

Incluye:
- En qué día del ciclo típicamente ocurre la fase {segment.phase}
- Duración normal de esta fase (rango de días)
- Qué esperar en los próximos días
- Cómo puede variar entre mujeres (rangos normales)
- Señales físicas y emocionales típicas de esta fase
- Cuándo esta fase debería terminar y qué sigue

FORMATO: Información clara y estructurada sobre el timing y progresión de la fase actual.
""",
            
            "hormone_levels": f"""
Proporciona información detallada sobre los niveles hormonales durante la fase {segment.phase}:

Incluye información sobre:
- Niveles de ESTRÓGENO: {segment.hormonal_profile.estrogen_level} - qué significa y cómo afecta tu cuerpo y emociones
- Niveles de PROGESTERONA: {segment.hormonal_profile.progesterone_level} - su función y efectos actuales
- Niveles de FSH (Hormona Folículo Estimulante) - qué está haciendo ahora y por qué
- Cómo estos niveles se relacionan con sentirse {segment.emotional_primary}
- Qué cambios hormonales esperar en los próximos días
- Cómo estas hormonas afectan tu energía, estado de ánimo y síntomas físicos

FORMATO: Explicación educativa pero accesible de la actividad hormonal actual.
""",
            
            "stress_levels": f"""
Proporciona información sobre los niveles de estrés basados en el cortisol durante la fase {segment.phase}:

Incluye:
- Niveles actuales de CORTISOL: {segment.hormonal_profile.cortisol_level or 'variable'} - qué significa esto
- Cómo el cortisol interactúa con tus hormonas sexuales en esta fase
- Por qué te sientes {segment.emotional_primary} en relación al estrés
- Señales físicas de estrés que puedes estar experimentando
- Estrategias específicas para reducir el cortisol en esta fase
- Cómo el estrés puede afectar tu ciclo menstrual
- Técnicas de manejo del estrés más efectivas para ti ahora

FORMATO: Información práctica sobre la relación entre estrés, cortisol y tu fase menstrual actual.
""",
            

            

        }
        
        return instructions.get(content_type, "Genera contenido relevante y útil para este segmento.")
    
    def generate_content_for_all_expanded_segments(self) -> Dict[str, Any]:
        """Genera contenido para todos los segmentos expandidos"""
        try:
            all_segments = self.segment_db.get_all_segments()
            content_types = [
                "lesson_3min",
                "whats_happening", 
                "nutrition_guide",
                "cycle_day_info",
                "hormone_levels",
                "stress_levels"
            ]
            
            generated_content = []
            total_segments = len(all_segments)
            total_content_types = len(content_types)
            total_combinations = total_segments * total_content_types
            
            logger.info(f"Generando contenido para {total_segments} segmentos expandidos...")
            logger.info(f"Total de combinaciones: {total_combinations}")
            
            current_combination = 0
            
            for segment_id, segment in all_segments.items():
                logger.info(f"Procesando segmento: {segment.name} ({segment_id})")
                
                for content_type in content_types:
                    current_combination += 1
                    logger.info(f"Progreso: {current_combination}/{total_combinations} - {segment_id} - {content_type}")
                    
                    try:
                        # Generar contenido
                        content = self.generate_content_for_expanded_segment(
                            segment_id=segment_id,
                            content_type=content_type
                        )
                        
                        if content:
                            content_data = {
                                "segment_id": segment_id,
                                "segment_name": segment.name,
                                "segment_category": segment.category,
                                "segment_phase": segment.phase,
                                "content_type": content_type,
                                "content_priority": self._get_content_priority(segment, content_type),
                                "content": content,
                                "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                                "segment_metadata": self.segment_db.get_segment_metadata(segment_id)
                            }
                            generated_content.append(content_data)
                            
                            logger.info(f"✓ {segment_id} - {content_type}: Generado (prioridad: {content_data['content_priority']:.2f})")
                        else:
                            logger.warning(f"✗ {segment_id} - {content_type}: No generado")
                    
                    except Exception as e:
                        logger.error(f"Error generando {content_type} para {segment_id}: {e}")
                        continue
            
            # Guardar resultados
            if generated_content:
                export_path = Path("data/exports") / f"expanded_content_{int(time.time())}.json"
                export_path.parent.mkdir(exist_ok=True)
                
                with open(export_path, 'w', encoding='utf-8') as f:
                    json.dump(generated_content, f, ensure_ascii=False, indent=2)
                
                logger.info(f"✓ {len(generated_content)} piezas de contenido expandido exportadas a: {export_path}")
                
                # Estadísticas
                stats = self._generate_statistics(generated_content)
                logger.info(f"Estadísticas: {stats}")
                
                return {
                    "success": True,
                    "total_content": len(generated_content),
                    "export_path": str(export_path),
                    "statistics": stats
                }
            else:
                logger.error("No se generó contenido")
                return {"success": False, "error": "No se generó contenido"}
                
        except Exception as e:
            logger.error(f"Error en generación de contenido expandido: {e}")
            return {"success": False, "error": str(e)}
    
    def _generate_statistics(self, generated_content: List[Dict]) -> Dict[str, Any]:
        """Genera estadísticas del contenido generado"""
        stats = {
            "total_pieces": len(generated_content),
            "by_segment": {},
            "by_content_type": {},
            "by_category": {},
            "by_phase": {},
            "priority_distribution": {"high": 0, "medium": 0, "low": 0}
        }
        
        for content in generated_content:
            # Por segmento
            segment_id = content["segment_id"]
            stats["by_segment"][segment_id] = stats["by_segment"].get(segment_id, 0) + 1
            
            # Por tipo de contenido
            content_type = content["content_type"]
            stats["by_content_type"][content_type] = stats["by_content_type"].get(content_type, 0) + 1
            
            # Por categoría
            category = content["segment_category"]
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
            
            # Por fase
            phase = content["segment_phase"]
            stats["by_phase"][phase] = stats["by_phase"].get(phase, 0) + 1
            
            # Distribución de prioridades
            priority = content["content_priority"]
            if priority >= 0.8:
                stats["priority_distribution"]["high"] += 1
            elif priority >= 0.5:
                stats["priority_distribution"]["medium"] += 1
            else:
                stats["priority_distribution"]["low"] += 1
        
        return stats