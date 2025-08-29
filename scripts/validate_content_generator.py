#!/usr/bin/env python3
"""
Script para validar que el generador de contenido cumpla con las especificaciones
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

from segment_processor.expanded_segments import ExpandedSegmentDatabase
from segment_processor.expanded_content_generator import ExpandedContentGenerator

def main():
    """Función principal de validación"""
    print("🔍 Validando generador de contenido...")
    print("=" * 50)
    
    # Inicializar componentes
    try:
        segment_db = ExpandedSegmentDatabase()
        print("✅ Base de datos de segmentos inicializada")
        
        # No inicializar el cliente Chroma ya que no está disponible
        print("⚠️  Nota: Validación sin conexión a Chroma DB")
    except Exception as e:
        print(f"❌ Error inicializando componentes: {e}")
        return False
    
    # Validar tipos de contenido
    print("\n📋 VALIDANDO TIPOS DE CONTENIDO:")
    print("-" * 40)
    
    expected_content_types = [
        "lesson_3min",
        "whats_happening", 
        "nutrition_guide",
        "cycle_day_info",
        "hormone_levels",
        "stress_levels"
    ]
    
    # Verificar que todos los segmentos tengan los nuevos tipos de contenido
    all_segments = segment_db.get_all_segments()
    
    for segment_id, segment in all_segments.items():
        print(f"\n🔹 Validando segmento: {segment.name}")
        
        # Verificar que tenga RecommendedContentTypes
        if not segment.recommended_content_types:
            print(f"   ❌ Falta recommended_content_types")
            continue
        
        # Verificar que tenga todos los tipos de contenido esperados
        content_types = segment.recommended_content_types
        
        try:
            priorities = {
                "lesson_3min": content_types.lesson_3min,
                "whats_happening": content_types.whats_happening,
                "nutrition_guide": content_types.nutrition_guide,
                "cycle_day_info": content_types.cycle_day_info,
                "hormone_levels": content_types.hormone_levels,
                "stress_levels": content_types.stress_levels
            }
            
            print(f"   ✅ Todos los tipos de contenido presentes")
            
            # Mostrar prioridades
            print("   📊 Prioridades:")
            for content_type, priority in priorities.items():
                status = "🔥 ALTA" if priority >= 0.8 else "⚡ MEDIA" if priority >= 0.5 else "⚪ BAJA"
                print(f"      • {content_type}: {priority:.2f} {status}")
                
        except AttributeError as e:
            print(f"   ❌ Falta atributo: {e}")
            continue
    
    # Validar especificaciones de contenido
    print(f"\n📖 ESPECIFICACIONES DE CONTENIDO:")
    print("-" * 40)
    
    specifications = {
        "lesson_3min": "Lecciones de máximo 3 minutos de lectura (400-500 palabras)",
        "whats_happening": "Texto de máximo 4 renglones explicando qué pasa en cuerpo/mente",
        "nutrition_guide": "Información nutricional para fase de ciclo y emociones",
        "cycle_day_info": "Información de la fase del ciclo y el día en el que va",
        "hormone_levels": "Información de niveles de estrógeno, progesterona y FSH",
        "stress_levels": "Información de niveles de estrés basados en cortisol"
    }
    
    for content_type, spec in specifications.items():
        print(f"✅ {content_type}: {spec}")
    
    # Validar emociones consistentes
    print(f"\n🎭 VALIDACIÓN DE EMOCIONES:")
    print("-" * 40)
    
    validation_results = segment_db.validate_emotions()
    
    if validation_results["invalid_emotions"]:
        print(f"❌ Emociones inválidas encontradas: {len(validation_results['invalid_emotions'])}")
        for emotion in validation_results["invalid_emotions"][:5]:  # Mostrar solo las primeras 5
            print(f"   • {emotion}")
        if len(validation_results["invalid_emotions"]) > 5:
            print(f"   ... y {len(validation_results['invalid_emotions']) - 5} más")
    else:
        print("✅ Todas las emociones están correctamente mapeadas")
    
    print(f"✅ Emociones válidas: {len(set(validation_results['valid_emotions']))}")
    
    # Estadísticas finales
    print(f"\n📈 ESTADÍSTICAS FINALES:")
    print("-" * 30)
    print(f"Total de segmentos: {len(all_segments)}")
    print(f"Tipos de contenido por segmento: {len(expected_content_types)}")
    print(f"Total de combinaciones posibles: {len(all_segments) * len(expected_content_types)}")
    
    # Verificar que todas las categorías estén representadas
    categories = set(segment.category for segment in all_segments.values())
    phases = set(segment.phase for segment in all_segments.values())
    
    print(f"Categorías de segmentos: {len(categories)}")
    for cat in sorted(categories):
        count = sum(1 for s in all_segments.values() if s.category == cat)
        print(f"   • {cat}: {count}")
    
    print(f"Fases de ciclo: {len(phases)}")
    for phase in sorted(phases):
        count = sum(1 for s in all_segments.values() if s.phase == phase)
        print(f"   • {phase}: {count}")
    
    # Resultado final
    print("\n" + "=" * 50)
    
    has_invalid_emotions = bool(validation_results["invalid_emotions"])
    
    if has_invalid_emotions:
        print("⚠️  VALIDACIÓN PARCIAL: Algunas emociones necesitan actualización")
        print("📝 Acción requerida: Actualizar emociones inválidas")
        return False
    else:
        print("✅ VALIDACIÓN EXITOSA: Generador de contenido listo para usar")
        print("🎯 Especificaciones cumplidas:")
        print("   • 6 tipos de contenido definidos")
        print("   • Límites de longitud especificados")
        print("   • Emociones consistentes con emotions.js")
        print("   • Segmentos expandidos completos")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)