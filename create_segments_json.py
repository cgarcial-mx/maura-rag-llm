# create_segments_json.py

import json
from pathlib import Path
from segment_processor.expanded_segments import ExpandedSegmentDatabase

def create_segments_json():
    """
    Crea un archivo JSON con todos los segmentos expandidos
    """
    try:
        # Crear base de datos de segmentos
        segment_db = ExpandedSegmentDatabase()
        
        # Obtener todos los segmentos
        all_segments = segment_db.get_all_segments()
        
        # Convertir a diccionario para JSON
        segments_data = {}
        
        for segment_id, segment in all_segments.items():
            segments_data[segment_id] = {
                "id": segment.id,
                "name": segment.name,
                "category": segment.category,
                "phase": segment.phase,
                "emotional_primary": segment.emotional_primary,
                "emotional_secondary": segment.emotional_secondary,
                "emotional_combination": segment.emotional_combination,
                "intensity_level": segment.intensity_level,
                "duration_pattern": segment.duration_pattern,
                "age_range": segment.age_range,
                "life_stage": segment.life_stage,
                "symptom_count": segment.symptom_count,
                
                "demographics": {
                    "age_groups": segment.demographics.age_groups,
                    "life_stages": segment.demographics.life_stages,
                    "common_triggers": segment.demographics.common_triggers,
                    "development_stage": segment.demographics.development_stage,
                    "common_concerns": segment.demographics.common_concerns
                },
                
                "hormonal_profile": {
                    "estrogen_level": segment.hormonal_profile.estrogen_level,
                    "progesterone_level": segment.hormonal_profile.progesterone_level,
                    "cortisol_level": segment.hormonal_profile.cortisol_level,
                    "development_stage": segment.hormonal_profile.development_stage,
                    "sensitivity_factors": segment.hormonal_profile.sensitivity_factors
                },
                
                "emotional_characteristics": {
                    "primary_emotions": segment.emotional_characteristics.primary_emotions,
                    "secondary_emotions": segment.emotional_characteristics.secondary_emotions,
                    "emotional_range": segment.emotional_characteristics.emotional_range,
                    "volatility": segment.emotional_characteristics.volatility,
                    "recovery_time": segment.emotional_characteristics.recovery_time
                },
                
                "physical_symptoms": {
                    "common": segment.physical_symptoms.common if segment.physical_symptoms else [],
                    "moderate": segment.physical_symptoms.moderate if segment.physical_symptoms else [],
                    "severe": segment.physical_symptoms.severe if segment.physical_symptoms else []
                },
                
                "content_preferences": {
                    "tone": segment.content_preferences.tone,
                    "depth": segment.content_preferences.depth,
                    "urgency": segment.content_preferences.urgency,
                    "focus_areas": segment.content_preferences.focus_areas,
                    "avoid_topics": segment.content_preferences.avoid_topics
                },
                
                "recommended_content_types": {
                    "lesson_3min": segment.recommended_content_types.lesson_3min,
                    "whats_happening": segment.recommended_content_types.whats_happening,
                    "nutrition_guide": segment.recommended_content_types.nutrition_guide,
                    "chart_explanation": segment.recommended_content_types.chart_explanation,
                    "breathing_exercises": segment.recommended_content_types.breathing_exercises,
                    "educational_videos": segment.recommended_content_types.educational_videos,
                    "productivity_tips": segment.recommended_content_types.productivity_tips,
                    "crisis_support": segment.recommended_content_types.crisis_support
                },
                
                "intervention_priorities": segment.intervention_priorities,
                "related_segments": segment.related_segments
            }
        
        # Crear directorio de exports si no existe
        export_dir = Path("data/exports")
        export_dir.mkdir(parents=True, exist_ok=True)
        
        # Guardar archivo JSON
        json_path = export_dir / "expanded_segments_database.json"
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(segments_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Archivo JSON creado exitosamente: {json_path}")
        print(f"✓ Total de segmentos: {len(segments_data)}")
        
        # Mostrar resumen por categoría
        categories = {}
        for segment_id, segment_data in segments_data.items():
            category = segment_data["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(segment_id)
        
        print("\n=== RESUMEN POR CATEGORÍA ===")
        for category, segment_ids in categories.items():
            print(f"{category}: {len(segment_ids)} segmentos")
            for segment_id in segment_ids:
                segment_data = segments_data[segment_id]
                print(f"  - {segment_id}: {segment_data['name']}")
        
        return str(json_path)
        
    except Exception as e:
        print(f"Error creando archivo JSON: {e}")
        return None

if __name__ == "__main__":
    create_segments_json()