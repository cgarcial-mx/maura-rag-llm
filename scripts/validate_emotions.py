#!/usr/bin/env python3
"""
Script para validar la consistencia de emociones entre los archivos Python y JavaScript
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

from segment_processor.expanded_segments import ExpandedSegmentDatabase

def main():
    """Función principal de validación"""
    print("🔍 Validando consistencia de emociones...")
    print("=" * 50)
    
    # Inicializar la base de datos de segmentos
    try:
        segment_db = ExpandedSegmentDatabase()
        print("✅ Base de datos de segmentos inicializada correctamente")
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        return False
    
    # Validar emociones
    try:
        validation_results = segment_db.validate_emotions()
        
        print("\n📊 RESULTADOS DE VALIDACIÓN:")
        print("-" * 30)
        
        # Mostrar emociones válidas
        valid_count = len(set(validation_results["valid_emotions"]))
        print(f"✅ Emociones válidas: {valid_count}")
        
        # Mostrar emociones inválidas
        invalid_emotions = list(set(validation_results["invalid_emotions"]))
        if invalid_emotions:
            print(f"\n❌ Emociones NO encontradas en emotions.js ({len(invalid_emotions)}):")
            for emotion in invalid_emotions:
                print(f"   • {emotion}")
        else:
            print("✅ Todas las emociones están definidas en emotions.js")
        
        # Mostrar mapeo de emociones disponibles
        print(f"\n📝 EMOCIONES DISPONIBLES EN EL MAPEO ({len(segment_db.emotion_mapping)}):")
        print("-" * 40)
        
        categories = {
            "Estrés y ansiedad": ["ansiosa", "abrumada", "nerviosa", "impaciente", "tensa", "frustrada", "preocupada", "estresada", "cansada_mentalmente", "insegura"],
            "Ánimo bajo": ["triste", "vacía", "sensible", "desmotivada", "aislada", "lloro_fácil", "nostálgica", "melancólica", "incomprendida", "desesperanzada"],
            "Físico y energía": ["cansada_físicamente", "energética", "letárgica", "inflamada", "dolorida", "irritable_físicamente", "con_hambre_excesiva", "liviana", "activa", "aletargada"],
            "Autoestima": ["poderosa", "atractiva", "desconectada", "confiada", "inadecuada", "en_paz_conmigo", "con_culpa", "orgullosa_de_mí", "frágil"],
            "Relacional": ["amada", "ignorada", "conectada", "en_conflicto", "valorada", "sola", "cuidada", "rechazada", "agradecida", "acompañada"]
        }
        
        for category, emotions in categories.items():
            print(f"\n{category}:")
            for emotion in emotions:
                emotion_id = segment_db.get_emotion_id(emotion)
                print(f"   • {emotion} → {emotion_id}")
        
        # Mostrar estadísticas de segmentos
        all_segments = segment_db.get_all_segments()
        print(f"\n📈 ESTADÍSTICAS DE SEGMENTOS:")
        print("-" * 30)
        print(f"Total de segmentos: {len(all_segments)}")
        
        # Contar por categorías
        categories_count = {}
        phases_count = {}
        for segment in all_segments.values():
            categories_count[segment.category] = categories_count.get(segment.category, 0) + 1
            phases_count[segment.phase] = phases_count.get(segment.phase, 0) + 1
        
        print("\nPor categoría:")
        for cat, count in categories_count.items():
            print(f"   • {cat}: {count}")
        
        print("\nPor fase:")
        for phase, count in phases_count.items():
            print(f"   • {phase}: {count}")
        
        # Resultado final
        print("\n" + "=" * 50)
        if invalid_emotions:
            print(f"❌ VALIDACIÓN FALLIDA: {len(invalid_emotions)} emociones no están mapeadas")
            return False
        else:
            print("✅ VALIDACIÓN EXITOSA: Todas las emociones están correctamente mapeadas")
            return True
            
    except Exception as e:
        print(f"❌ Error durante la validación: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)