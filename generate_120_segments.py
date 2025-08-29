# generate_120_segments.py

import json
from pathlib import Path

def generate_120_segments():
    """
    Genera 120 segmentos expandidos basados en la estructura existente
    """
    
    # Definir las categorías base
    phases = {
        "folicular": {
            "early": {"days": [6, 7, 8, 9], "description": "Primera fase de renovación hormonal, estrógeno comenzando a aumentar"},
            "middle": {"days": [10, 11, 12, 13], "description": "Estrógeno en niveles medios, energía y creatividad aumentando"},
            "late": {"days": [14, 15, 16, 17], "description": "Estrógeno en pico, preparación para ovulación"}
        },
        "ovulatory": {
            "peak": {"days": [18, 19, 20, 21], "description": "Pico de estrógeno, ovulación, máxima fertilidad"}
        },
        "luteal": {
            "early": {"days": [22, 23, 24, 25], "description": "Progesterona aumentando, fase lútea temprana"},
            "middle": {"days": [26, 27, 28, 29], "description": "Progesterona en pico, fase lútea media"},
            "late": {"days": [30, 31, 32, 33], "description": "Progesterona disminuyendo, fase lútea tardía"}
        },
        "menstrual": {
            "flow": {"days": [1, 2, 3, 4], "description": "Flujo menstrual activo, renovación del ciclo"},
            "recovery": {"days": [5, 6], "description": "Recuperación post-menstrual, preparación para nuevo ciclo"}
        }
    }
    
    age_groups = {
        "8-12": {"stage": "pre_menarca", "characteristics": ["desarrollo_pubertad", "curiosidad_natural", "energia_alta", "aprendizaje_acelerado"]},
        "13-19": {"stage": "adolescente", "characteristics": ["ciclo_estableciendose", "energia_social_alta", "buscando_identidad", "influencia_grupo"]},
        "20-29": {"stage": "reproductiva_temprana", "characteristics": ["ciclo_estable", "responsabilidades_adultas", "buscando_equilibrio", "presion_social"]},
        "30-39": {"stage": "reproductiva_media", "characteristics": ["ciclo_estable", "responsabilidades_familia", "equilibrio_vida", "presion_tiempo"]},
        "40-49": {"stage": "perimenopausia", "characteristics": ["cambios_hormonales", "síntomas_variables", "transición_vida", "autocuidado_prioritario"]},
        "50+": {"stage": "post_menopausia", "characteristics": ["estabilidad_hormonal", "enfoque_salud", "sabiduría_experiencia", "nuevas_prioridades"]}
    }
    
    emotions = {
        "positive": ["energética", "confiada", "poderosa", "activa", "orgullosa_de_mí", "en_paz_conmigo", "conectada", "valorada"],
        "negative": ["ansiosa", "estresada", "triste", "frustrada", "insegura", "abrumada", "cansada_físicamente", "desesperanzada"],
        "neutral": ["sensible", "nerviosa", "melancólica", "nostálgica", "frágil", "desconectada", "impaciente", "tensa"]
    }
    
    intensity_levels = {
        "very_low": {"score_range": [0.0, 0.5], "description": "Intensidad muy baja, síntomas mínimos"},
        "low": {"score_range": [0.5, 1.0], "description": "Intensidad baja, síntomas leves"},
        "moderate": {"score_range": [1.0, 1.5], "description": "Intensidad moderada, síntomas notables"},
        "high": {"score_range": [1.5, 2.0], "description": "Intensidad alta, síntomas significativos"},
        "very_high": {"score_range": [2.0, 2.5], "description": "Intensidad muy alta, síntomas intensos"}
    }
    
    segments = []
    segment_counter = 1
    
    # Generar segmentos para cada combinación
    for phase_name, subphases in phases.items():
        for subphase_name, phase_info in subphases.items():
            for age_range, age_info in age_groups.items():
                # Generar 5 segmentos por combinación fase-edad
                for i in range(5):
                    # Seleccionar emociones primaria y secundaria
                    if i == 0:  # Muy alta intensidad - emociones positivas
                        primary_emotion = emotions["positive"][i % len(emotions["positive"])]
                        secondary_emotion = emotions["positive"][(i + 1) % len(emotions["positive"])]
                        intensity = "very_high"
                        primary_score = 2.0
                        secondary_score = 2.0
                        conflict = None
                        resolution_needed = False
                    elif i == 1:  # Alta intensidad - emociones mixtas
                        primary_emotion = emotions["negative"][i % len(emotions["negative"])]
                        secondary_emotion = emotions["positive"][i % len(emotions["positive"])]
                        intensity = "high"
                        primary_score = -1.5
                        secondary_score = 1.0
                        conflict = f"{primary_emotion}_{secondary_emotion}_conflict"
                        resolution_needed = True
                    elif i == 2:  # Moderada intensidad - emociones neutrales
                        primary_emotion = emotions["neutral"][i % len(emotions["neutral"])]
                        secondary_emotion = emotions["neutral"][(i + 1) % len(emotions["neutral"])]
                        intensity = "moderate"
                        primary_score = 0.5
                        secondary_score = 1.0
                        conflict = None
                        resolution_needed = False
                    elif i == 3:  # Moderada intensidad - emociones mixtas
                        primary_emotion = emotions["negative"][(i + 1) % len(emotions["negative"])]
                        secondary_emotion = emotions["positive"][(i + 1) % len(emotions["positive"])]
                        intensity = "moderate"
                        primary_score = -1.0
                        secondary_score = 1.0
                        conflict = f"{primary_emotion}_{secondary_emotion}_conflict"
                        resolution_needed = True
                    else:  # Baja intensidad - emociones positivas
                        primary_emotion = emotions["positive"][(i + 2) % len(emotions["positive"])]
                        secondary_emotion = emotions["positive"][(i + 3) % len(emotions["positive"])]
                        intensity = "low"
                        primary_score = 1.0
                        secondary_score = 1.0
                        conflict = None
                        resolution_needed = False
                    
                    # Crear ID del segmento
                    phase_abbr = phase_name[:3].upper()
                    age_abbr = age_range.replace("-", "_")
                    segment_id = f"SEG_{phase_abbr}_{age_abbr}_{segment_counter:03d}"
                    
                    # Crear nombre del segmento
                    primary_emotion_spanish = get_emotion_spanish(primary_emotion)
                    secondary_emotion_spanish = get_emotion_spanish(secondary_emotion)
                    phase_spanish = get_phase_spanish(phase_name, subphase_name)
                    intensity_spanish = get_intensity_spanish(intensity)
                    
                    segment_name = f"{phase_spanish} - {primary_emotion_spanish} y {secondary_emotion_spanish} - {intensity_spanish}"
                    
                    # Determinar perfil hormonal
                    hormonal_context = get_hormonal_context(phase_name, subphase_name, primary_emotion)
                    
                    # Determinar necesidades de contenido
                    content_needs = get_content_needs(primary_emotion, secondary_emotion, age_range, intensity)
                    
                    # Determinar estilo de presentación
                    presentation_style = get_presentation_style(primary_emotion, secondary_emotion, intensity, age_range)
                    
                    # Crear segmento
                    segment = {
                        "id": segment_id,
                        "name": segment_name,
                        "phase": {
                            "main": phase_name,
                            "subphase": subphase_name,
                            "days": phase_info["days"],
                            "description": phase_info["description"]
                        },
                        "age_group": {
                            "range": age_range,
                            "stage": age_info["stage"],
                            "characteristics": age_info["characteristics"]
                        },
                        "emotional_profile": {
                            "primary": {
                                "emotion": primary_emotion,
                                "intensity": 2 if intensity in ["very_high", "high"] else 1,
                                "score": primary_score,
                                "description": get_emotion_description(primary_emotion, age_range)
                            },
                            "secondary": {
                                "emotion": secondary_emotion,
                                "intensity": 2 if intensity in ["very_high", "high"] else 1,
                                "score": secondary_score,
                                "description": get_emotion_description(secondary_emotion, age_range)
                            },
                            "conflict": conflict,
                            "resolution_needed": resolution_needed
                        },
                        "hormonal_context": hormonal_context,
                        "content_needs": content_needs,
                        "presentation_style": presentation_style,
                        
                        # METADATA PARA MISTRAL
                        "segment_metadata": {
                            "id": segment_id,
                            "name": segment_name,
                            "category": f"{phase_name}_{age_range}",
                            "phase": phase_name,
                            "subphase": subphase_name,
                            "emotional_primary": primary_emotion,
                            "emotional_secondary": secondary_emotion,
                            "intensity_level": intensity,
                            "age_range": age_range,
                            "life_stage": age_info["stage"],
                            
                            "applicable_content": get_applicable_content(primary_emotion, secondary_emotion, intensity, age_range),
                            
                            "search_keywords": get_search_keywords(phase_name, subphase_name, primary_emotion, secondary_emotion, age_range),
                            
                            "related_segments": get_related_segments(phase_name, primary_emotion, secondary_emotion, age_range),
                            
                            "content_generation_rules": {
                                "max_length": get_max_length(age_range, intensity),
                                "min_validation": True,
                                "include_practical_tips": True,
                                "avoid_medical_diagnosis": True,
                                "tone": presentation_style["tone"],
                                "urgency": presentation_style["urgency"],
                                "language": presentation_style["language"],
                                "structure": presentation_style["structure"]
                            }
                        }
                    }
                    
                    segments.append(segment)
                    segment_counter += 1
    
    return segments

def get_emotion_spanish(emotion):
    """Convierte emociones a formato de visualización"""
    # Las emociones ya están en español, solo necesitamos formatearlas para visualización
    display_names = {
        "energética": "Energética",
        "confiada": "Confiada", 
        "poderosa": "Poderosa",
        "activa": "Activa",
        "orgullosa_de_mí": "Orgullosa de mí",
        "en_paz_conmigo": "En paz conmigo",
        "conectada": "Conectada",
        "valorada": "Valorada",
        "ansiosa": "Ansiosa",
        "estresada": "Estresada",
        "triste": "Triste",
        "frustrada": "Frustrada",
        "insegura": "Insegura",
        "abrumada": "Abrumada",
        "cansada_físicamente": "Cansada físicamente",
        "desesperanzada": "Desesperanzada",
        "sensible": "Sensible",
        "nerviosa": "Nerviosa",
        "melancólica": "Melancólica",
        "nostálgica": "Nostálgica",
        "frágil": "Frágil",
        "desconectada": "Desconectada",
        "impaciente": "Impaciente",
        "tensa": "Tensa"
    }
    return display_names.get(emotion, emotion.replace("_", " ").title())

def get_phase_spanish(phase, subphase):
    """Convierte fases a español"""
    phase_translations = {
        "folicular": {
            "early": "Folicular Temprana",
            "middle": "Folicular Media",
            "late": "Folicular Tardía"
        },
        "ovulatory": {
            "peak": "Ovulatoria"
        },
        "luteal": {
            "early": "Lútea Temprana",
            "middle": "Lútea Media",
            "late": "Lútea Tardía"
        },
        "menstrual": {
            "flow": "Menstrual",
            "recovery": "Recuperación"
        }
    }
    return phase_translations.get(phase, {}).get(subphase, f"{phase.title()} {subphase.title()}")

def get_intensity_spanish(intensity):
    """Convierte intensidad a español"""
    translations = {
        "very_low": "Muy Baja Intensidad",
        "low": "Baja Intensidad",
        "moderate": "Moderada Intensidad",
        "high": "Alta Intensidad",
        "very_high": "Muy Alta Intensidad"
    }
    return translations.get(intensity, intensity.title())

def get_emotion_description(emotion, age_range):
    """Genera descripción de la emoción según la edad"""
    descriptions = {
        "energética": f"Energía física alta, ganas de explorar y aprender" if age_range == "8-12" else "Energía optimizada para actividades y proyectos",
        "confiada": f"Confianza natural en sus capacidades" if age_range == "8-12" else "Confianza en habilidades y decisiones",
        "ansiosa": f"Ansiedad por cambios corporales y hormonales nuevos" if age_range == "8-12" else "Ansiedad relacionada con responsabilidades y expectativas",
        "estresada": "Estrés por responsabilidades y presiones externas",
        "triste": "Tristeza relacionada con cambios hormonales o circunstancias",
        "melancólica": "Melancolía suave, reflexión sobre experiencias",
        "insegura": f"Inseguridad sobre cambios corporales" if age_range == "8-12" else "Inseguridad sobre capacidades o decisiones",
        "sensible": "Sensibilidad aumentada a estímulos emocionales y físicos",
        "nerviosa": f"Nerviosismo natural sobre cambios corporales y hormonales" if age_range == "8-12" else "Nerviosismo sobre nuevas experiencias y responsabilidades",
        "frustrada": "Frustración con situaciones que no se pueden controlar",
        "abrumada": "Sensación de tener demasiadas cosas que manejar",
        "cansada_físicamente": "Fatiga física relacionada with cambios hormonales"
    }
    return descriptions.get(emotion, f"Estado emocional: {get_emotion_spanish(emotion)}")

def get_hormonal_context(phase, subphase, primary_emotion):
    """Determina el contexto hormonal según la fase y emoción"""
    contexts = {
        "folicular": {
            "early": {"estrogen": "beginning_increase", "progesterone": "very_low", "cortisol": "low" if primary_emotion in ["energética", "confiada"] else "moderate"},
            "middle": {"estrogen": "medium", "progesterone": "low", "cortisol": "low" if primary_emotion in ["energética", "confiada"] else "moderate"},
            "late": {"estrogen": "high", "progesterone": "low", "cortisol": "low" if primary_emotion in ["energética", "confiada"] else "moderate"}
        },
        "ovulatory": {
            "peak": {"estrogen": "peak", "progesterone": "beginning_increase", "cortisol": "low" if primary_emotion in ["energética", "confiada"] else "moderate"}
        },
        "luteal": {
            "early": {"estrogen": "medium", "progesterone": "increasing", "cortisol": "moderate" if primary_emotion in ["ansiosa", "estresada"] else "low"},
            "middle": {"estrogen": "medium", "progesterone": "high", "cortisol": "moderate" if primary_emotion in ["ansiosa", "estresada"] else "low"},
            "late": {"estrogen": "decreasing", "progesterone": "decreasing", "cortisol": "high" if primary_emotion in ["ansiosa", "estresada"] else "moderate"}
        },
        "menstrual": {
            "flow": {"estrogen": "low", "progesterone": "very_low", "cortisol": "moderate"},
            "recovery": {"estrogen": "beginning_increase", "progesterone": "very_low", "cortisol": "low"}
        }
    }
    
    base_context = contexts.get(phase, {}).get(subphase, {"estrogen": "medium", "progesterone": "medium", "cortisol": "moderate"})
    
    return {
        "estrogen": base_context["estrogen"],
        "progesterone": base_context["progesterone"],
        "cortisol": base_context["cortisol"],
        "optimal_balance": base_context["cortisol"] == "low" and primary_emotion in ["energética", "confiada", "poderosa"],
        "description": f"Contexto hormonal de {phase} {subphase} con {primary_emotion} como emoción primaria"
    }

def get_content_needs(primary_emotion, secondary_emotion, age_range, intensity):
    """Determina las necesidades de contenido según las emociones y edad"""
    
    # Necesidades primarias basadas en la emoción primaria
    primary_needs = {
        "energética": ["aprovechamiento_energia", "actividades_energeticas", "proyectos_nuevos"],
        "confiada": ["desarrollo_confianza", "liderazgo", "proyectos_importantes"],
        "ansiosa": ["manejo_ansiedad", "tecnicas_calma", "validacion_emocional"],
        "estresada": ["manejo_estres", "tecnicas_autocuidado", "balance_hormonal"],
        "triste": ["apoyo_emocional", "validacion_tristeza", "conexion_emocional"],
        "melancólica": ["validacion_melancolia", "reflexion_personal", "actividades_suaves"],
        "insegura": ["construccion_confianza", "desarrollo_autoestima", "apoyo_emocional"],
        "sensible": ["validacion_sensibilidad", "autocuidado_emocional", "actividades_suaves"],
        "nerviosa": ["manejo_nerviosismo", "tecnicas_calma", "validacion_emocional"],
        "frustrada": ["manejo_frustracion", "canalizacion_energia", "validacion_emocional"],
        "abrumada": ["organizacion_tareas", "tecnicas_simplificacion", "apoyo_emocional"]
    }
    
    # Necesidades secundarias
    secondary_needs = {
        "energética": ["ejercicio_moderado", "nutricion_energetica", "descanso_adecuado"],
        "confiada": ["desarrollo_habilidades", "networking", "proyectos_colaborativos"],
        "ansiosa": ["tecnicas_respiracion", "nutricion_estabilizadora", "ejercicio_suave"],
        "estresada": ["nutricion_estabilizadora", "ejercicio_adaptativo", "tecnicas_relajacion"],
        "triste": ["nutricion_animo", "actividades_suaves", "conexion_social"],
        "melancólica": ["nutricion_animo", "actividades_reflexivas", "conexion_emocional"],
        "insegura": ["tecnicas_autocuidado", "proyectos_moderados", "apoyo_social"],
        "sensible": ["nutricion_equilibrada", "actividades_suaves", "desarrollo_emocional"],
        "nerviosa": ["actividades_calmantes", "nutricion_equilibrada", "autocuidado_basico"],
        "frustrada": ["ejercicio_liberador", "actividades_creativas", "apoyo_social"],
        "abrumada": ["organizacion_simple", "descanso_prioritario", "apoyo_practico"]
    }
    
    # Temas a evitar
    avoid_topics = {
        "ansiosa": ["presion_adicional", "informacion_abrumadora", "expectativas_altas"],
        "estresada": ["presion_adicional", "optimizacion_excesiva", "comparaciones"],
        "triste": ["presion_alegria", "minimizacion_emociones", "estimulacion_excesiva"],
        "insegura": ["presion_rendimiento", "comparaciones", "expectativas_altas"],
        "sensible": ["estimulacion_excesiva", "presion_rendimiento", "critica"],
        "energética": ["limitaciones", "restricciones", "precauciones_excesivas"],
        "confiada": ["limitaciones", "subestimacion_capacidad", "restricciones"],
        "nerviosa": ["presion_adicional", "estimulacion_excesiva", "comparaciones"],
        "frustrada": ["minimizacion_emociones", "presion_paciencia", "invalidacion"],
        "abrumada": ["tareas_adicionales", "presion_organizacion", "expectativas_altas"]
    }
    
    return {
        "primary": primary_needs.get(primary_emotion, ["apoyo_emocional", "validacion", "autocuidado"]),
        "secondary": secondary_needs.get(secondary_emotion, ["nutricion_equilibrada", "actividades_suaves", "autocuidado"]),
        "avoid": avoid_topics.get(primary_emotion, ["presion_adicional", "informacion_abrumadora"])
    }

def get_presentation_style(primary_emotion, secondary_emotion, intensity, age_range):
    """Determina el estilo de presentación según las emociones e intensidad"""
    
    # Tono basado en la emoción primaria
    tone_map = {
        "energy": "motivacional_energico",
        "confidence": "empoderador_optimista",
        "anxiety": "calmante_empatico",
        "stress": "validador_empoderador",
        "sadness": "empatico_animador",
        "melancholy": "validador_reflexivo",
        "insecurity": "empoderador_empatico",
        "sensitivity": "validador_suave",
        "curiosity": "educativo_empatico"
    }
    
    # Estructura basada en la combinación de emociones
    structure_map = {
        ("anxiety", "energy"): "balance_emocional",
        ("stress", "resilience"): "reconocimiento_estrategia",
        ("sadness", "curiosity"): "validacion_esperanza",
        ("melancholy", "energy"): "validacion_oportunidad",
        ("insecurity", "confidence"): "validacion_crecimiento",
        ("sensitivity", "reflection"): "sensibilidad_reflexion"
    }
    
    # Longitud basada en la edad
    length_map = {
        "8-12": "corta",
        "13-19": "media",
        "20-29": "media",
        "30-39": "media",
        "40-49": "media",
        "50+": "media"
    }
    
    # Urgencia basada en la intensidad
    urgency_map = {
        "very_low": "baja",
        "low": "baja",
        "moderate": "moderada",
        "high": "moderada",
        "very_high": "alta"
    }
    
    return {
        "tone": tone_map.get(primary_emotion, "empatico_educativo"),
        "structure": structure_map.get((primary_emotion, secondary_emotion), "validacion_aprendizaje"),
        "length": length_map.get(age_range, "media"),
        "urgency": urgency_map.get(intensity, "moderada"),
        "language": "simple_español" if age_range == "8-12" else "español_adaptado"
    }

def get_applicable_content(primary_emotion, secondary_emotion, intensity, age_range):
    """Genera metadata de contenido aplicable para Mistral"""
    
    # Prioridades base por tipo de contenido (nuevos 6 tipos específicos)
    content_priorities = {
        "lesson_3min": 0.8,
        "whats_happening": 0.9,
        "nutrition_guide": 0.7,
        "cycle_day_info": 0.6,
        "hormone_levels": 0.7,
        "stress_levels": 0.6
    }
    
    # Ajustar prioridades según emociones
    if primary_emotion in ["ansiosa", "estresada"]:
        content_priorities["stress_levels"] = 0.95
        content_priorities["whats_happening"] = 0.95
        content_priorities["hormone_levels"] = 0.8
    elif primary_emotion in ["energética", "confiada"]:
        content_priorities["lesson_3min"] = 0.9
        content_priorities["cycle_day_info"] = 0.8
        content_priorities["hormone_levels"] = 0.85
    elif primary_emotion in ["triste", "melancólica"]:
        content_priorities["whats_happening"] = 0.95
        content_priorities["stress_levels"] = 0.8
        content_priorities["nutrition_guide"] = 0.8
    elif primary_emotion in ["nerviosa", "sensible"]:
        content_priorities["whats_happening"] = 0.9
        content_priorities["lesson_3min"] = 0.8
    
    # Ajustar según intensidad
    if intensity in ["very_high", "high"]:
        content_priorities["stress_levels"] = min(0.95, content_priorities["stress_levels"] + 0.3)
        content_priorities["whats_happening"] = min(0.95, content_priorities["whats_happening"] + 0.2)
    
    # Ajustar según edad
    if age_range == "8-12":
        content_priorities["lesson_3min"] = min(0.95, content_priorities["lesson_3min"] + 0.3)
        content_priorities["whats_happening"] = min(0.95, content_priorities["whats_happening"] + 0.2)
        content_priorities["cycle_day_info"] = min(0.95, content_priorities["cycle_day_info"] + 0.2)
    
    # Generar focus_areas y tone para cada tipo de contenido
    applicable_content = {}
    
    for content_type, priority in content_priorities.items():
        if priority > 0.3:  # Solo incluir contenido con prioridad significativa
            applicable_content[content_type] = {
                "priority": round(priority, 2),
                "focus_areas": get_focus_areas_for_content(content_type, primary_emotion, secondary_emotion, age_range),
                "tone": get_tone_for_content(content_type, primary_emotion, intensity)
            }
    
    return applicable_content

def get_focus_areas_for_content(content_type, primary_emotion, secondary_emotion, age_range):
    """Genera áreas de enfoque específicas para cada tipo de contenido"""
    
    focus_areas_map = {
        "lesson_3min": {
            "ansiosa": ["manejo_ansiedad", "técnicas_calma", "validación_emocional"],
            "estresada": ["manejo_estrés", "técnicas_autocuidado", "balance_hormonal"],
            "energética": ["aprovechamiento_energía", "actividades_energéticas", "proyectos_nuevos"],
            "confiada": ["desarrollo_confianza", "liderazgo", "proyectos_importantes"],
            "triste": ["apoyo_emocional", "validación_tristeza", "conexión_emocional"],
            "nerviosa": ["manejo_nerviosismo", "explicaciones_claras", "validación_emocional"],
            "sensible": ["validación_sensibilidad", "autocuidado_emocional", "comprensión_cambios"]
        },
        "whats_happening": {
            "ansiosa": ["validación_emocional", "explicación_hormonal", "normalización_síntomas"],
            "estresada": ["explicación_cortisol", "validación_estrés", "estrategias_manejo"],
            "energética": ["explicación_estrógeno", "aprovechamiento_energía", "optimización_rendimiento"],
            "confiada": ["explicación_hormonal", "desarrollo_confianza", "liderazgo_natural"],
            "triste": ["explicación_hormonal", "validación_emocional", "apoyo_emocional"],
            "nerviosa": ["educación_básica", "explicaciones_simples", "normalización_cambios"],
            "sensible": ["explicación_sensibilidad", "validación_emocional", "comprensión_cambios"]
        },
        "nutrition_guide": {
            "ansiosa": ["alimentos_calma", "reducción_cortisol", "nutrición_estabilizadora"],
            "estresada": ["alimentos_antiestrés", "balance_hormonal", "nutrición_equilibrada"],
            "energética": ["alimentos_energéticos", "nutrición_optimizada", "combustible_corporal"],
            "confiada": ["nutrición_optimizada", "alimentos_cerebro", "rendimiento_mental"],
            "triste": ["alimentos_ánimo", "nutrición_emocional", "conexión_alimentación"],
            "nerviosa": ["nutrición_calmante", "alimentos_estabilizadores", "balance_nutricional"],
            "sensible": ["nutrición_suave", "alimentos_reconfortantes", "balance_delicado"]
        },
        "cycle_day_info": {
            "ansiosa": ["timing_fase", "duración_normal", "qué_esperar"],
            "estresada": ["planificación_ciclo", "preparación_fase", "manejo_expectativas"],
            "energética": ["optimización_timing", "aprovechamiento_fase", "planificación_actividades"],
            "confiada": ["comprensión_ciclo", "planificación_estratégica", "optimización_personal"],
            "triste": ["normalización_timing", "comprensión_cambios", "validación_experiencia"],
            "nerviosa": ["educación_básica", "explicación_timing", "normalización_proceso"],
            "sensible": ["timing_delicado", "preparación_suave", "comprensión_personal"]
        },
        "hormone_levels": {
            "ansiosa": ["explicación_cortisol", "interacción_hormonas", "efectos_ansiedad"],
            "estresada": ["niveles_cortisol", "impacto_estrógeno", "balance_hormonal"],
            "energética": ["pico_estrógeno", "niveles_óptimos", "aprovechamiento_hormonal"],
            "confiada": ["balance_hormonal", "niveles_estables", "optimización_natural"],
            "triste": ["fluctuaciones_hormonales", "impacto_emocional", "comprensión_cambios"],
            "nerviosa": ["educación_hormonal", "explicación_simple", "normalización_niveles"],
            "sensible": ["sensibilidad_hormonal", "fluctuaciones_delicadas", "comprensión_personal"]
        },
        "stress_levels": {
            "ansiosa": ["manejo_cortisol_elevado", "técnicas_reducción_estrés", "estrategias_calma"],
            "estresada": ["niveles_cortisol", "técnicas_antiestrés", "balance_hormonal"],
            "energética": ["optimización_cortisol", "balance_energético", "prevención_sobreestimulación"],
            "confiada": ["mantenimiento_balance", "técnicas_equilibrio", "prevención_estrés"],
            "triste": ["cortisol_depresión", "manejo_estrés_emocional", "técnicas_apoyo"],
            "nerviosa": ["reducción_nerviosismo", "técnicas_calma", "manejo_básico_estrés"],
            "sensible": ["manejo_delicado_estrés", "técnicas_suaves", "balance_sensible"]
        }
    }
    
    # Obtener áreas de enfoque específicas
    content_focus = focus_areas_map.get(content_type, {}).get(primary_emotion, ["apoyo_emocional", "validación", "autocuidado"])
    
    # Ajustar según edad
    if age_range == "8-12":
        content_focus = [area.replace("liderazgo", "desarrollo_habilidades") for area in content_focus]
        content_focus = [area.replace("carrera", "futuro") for area in content_focus]
    
    return content_focus

def get_tone_for_content(content_type, primary_emotion, intensity):
    """Genera el tono específico para cada tipo de contenido"""
    
    tone_map = {
        "lesson_3min": {
            "ansiosa": "empático_tranquilizador",
            "estresada": "validador_empoderador",
            "energética": "motivacional_energético",
            "confiada": "empoderador_optimista",
            "triste": "empático_animador",
            "nerviosa": "educativo_empático",
            "sensible": "delicado_empático"
        },
        "whats_happening": {
            "ansiosa": "empático_tranquilizador",
            "estresada": "validador_empoderador",
            "energética": "motivacional_energético",
            "confiada": "empoderador_optimista",
            "triste": "empático_animador",
            "nerviosa": "educativo_empático",
            "sensible": "delicado_empático"
        },
        "nutrition_guide": {
            "ansiosa": "práctico_tranquilizador",
            "estresada": "práctico_empoderador",
            "energética": "práctico_motivador",
            "confiada": "práctico_optimista",
            "triste": "práctico_animador",
            "nerviosa": "práctico_educativo",
            "sensible": "práctico_delicado"
        },
        "cycle_day_info": {
            "ansiosa": "claro_tranquilizador",
            "estresada": "claro_empoderador",
            "energética": "claro_motivador",
            "confiada": "claro_optimista",
            "triste": "claro_animador",
            "nerviosa": "claro_educativo",
            "sensible": "claro_delicado"
        },
        "hormone_levels": {
            "ansiosa": "educativo_tranquilizador",
            "estresada": "educativo_empoderador",
            "energética": "educativo_motivador",
            "confiada": "educativo_optimista",
            "triste": "educativo_animador",
            "nerviosa": "educativo_empático",
            "sensible": "educativo_delicado"
        },
        "stress_levels": {
            "ansiosa": "urgente_tranquilizador",
            "estresada": "urgente_empoderador",
            "energética": "urgente_equilibrador",
            "confiada": "urgente_preventivo",
            "triste": "urgente_consolador",
            "nerviosa": "urgente_educativo",
            "sensible": "urgente_delicado"
        }
    }
    
    base_tone = tone_map.get(content_type, {}).get(primary_emotion, "empático_educativo")
    
    # Ajustar según intensidad
    if intensity in ["very_high", "high"]:
        if "tranquilizador" in base_tone:
            base_tone = base_tone.replace("tranquilizador", "muy_tranquilizador")
        elif "empoderador" in base_tone:
            base_tone = base_tone.replace("empoderador", "muy_empoderador")
    
    return base_tone

def get_search_keywords(phase_name, subphase_name, primary_emotion, secondary_emotion, age_range):
    """Genera palabras clave de búsqueda para el sistema RAG"""
    
    keywords = []
    
    # Fase + emoción primaria
    phase_spanish = get_phase_spanish(phase_name, subphase_name)
    keywords.append(f"{phase_spanish.lower()} {primary_emotion}")
    
    # Emociones combinadas
    if secondary_emotion and secondary_emotion != primary_emotion:
        keywords.append(f"{primary_emotion} {secondary_emotion}")
    
    # Síntomas específicos por emoción
    emotion_symptoms = {
        "anxiety": ["ansiedad", "preocupación", "nerviosismo", "tensión"],
        "stress": ["estrés", "sobrecarga", "presión", "agotamiento"],
        "energy": ["energía", "vitalidad", "motivación", "actividad"],
        "confidence": ["confianza", "seguridad", "autoestima", "liderazgo"],
        "sadness": ["tristeza", "melancolía", "desánimo", "apoyo"],
        "curiosity": ["curiosidad", "aprendizaje", "educación", "comprensión"]
    }
    
    if primary_emotion in emotion_symptoms:
        keywords.extend(emotion_symptoms[primary_emotion][:2])
    
    # Contexto hormonal
    if phase_name == "folicular":
        keywords.extend(["estrógeno", "energía", "crecimiento"])
    elif phase_name == "ovulatory":
        keywords.extend(["ovulación", "fertilidad", "pico_hormonal"])
    elif phase_name == "luteal":
        keywords.extend(["progesterona", "síntomas", "cambios"])
    elif phase_name == "menstrual":
        keywords.extend(["menstruación", "renovación", "recuperación"])
    
    # Contexto de edad
    if age_range == "8-12":
        keywords.extend(["pubertad", "desarrollo", "educación"])
    elif age_range == "13-19":
        keywords.extend(["adolescencia", "cambio", "identidad"])
    elif age_range == "20-29":
        keywords.extend(["adulto_joven", "responsabilidades", "equilibrio"])
    elif age_range == "30-39":
        keywords.extend(["adulto", "familia", "carrera"])
    elif age_range == "40-49":
        keywords.extend(["perimenopausia", "transición", "cambios"])
    elif age_range == "50+":
        keywords.extend(["post_menopausia", "estabilidad", "salud"])
    
    return keywords[:8]  # Limitar a 8 palabras clave

def get_related_segments(phase_name, primary_emotion, secondary_emotion, age_range):
    """Genera segmentos relacionados basados en similitudes"""
    
    related = []
    
    # Misma fase, diferentes edades
    for age in ["8-12", "13-19", "20-29", "30-39", "40-49", "50+"]:
        if age != age_range:
            related.append(f"SEG_{phase_name[:3].upper()}_{age.replace('-', '_')}_XXX")
    
    # Misma emoción primaria, diferentes fases
    phase_abbr_map = {
        "folicular": "FOL",
        "ovulatory": "OVU", 
        "luteal": "LUT",
        "menstrual": "MEN"
    }
    
    for phase, abbr in phase_abbr_map.items():
        if phase != phase_name:
            related.append(f"SEG_{abbr}_{age_range.replace('-', '_')}_XXX")
    
    # Emociones similares
    emotion_groups = {
        "anxiety": ["stress", "insecurity"],
        "stress": ["anxiety", "overwhelm"],
        "energy": ["confidence", "motivation"],
        "confidence": ["energy", "optimism"],
        "sadness": ["melancholy", "fatigue"],
        "curiosity": ["creativity", "motivation"]
    }
    
    if primary_emotion in emotion_groups:
        for similar_emotion in emotion_groups[primary_emotion]:
            related.append(f"SEG_{phase_abbr_map.get(phase_name, 'XXX')}_{age_range.replace('-', '_')}_{similar_emotion.upper()}_XXX")
    
    return related[:5]  # Limitar a 5 segmentos relacionados

def get_max_length(age_range, intensity):
    """Determina la longitud máxima del contenido según edad e intensidad"""
    
    base_length = {
        "8-12": 400,
        "13-19": 500,
        "20-29": 600,
        "30-39": 600,
        "40-49": 600,
        "50+": 500
    }
    
    length = base_length.get(age_range, 600)
    
    # Ajustar según intensidad
    if intensity in ["very_high", "high"]:
        length = min(800, length + 200)  # Contenido más extenso para alta intensidad
    elif intensity in ["very_low", "low"]:
        length = max(300, length - 100)  # Contenido más conciso para baja intensidad
    
    return length

def main():
    """Función principal para generar los 120 segmentos"""
    print("Generando 120 segmentos expandidos...")
    
    segments = generate_120_segments()
    
    # Crear directorio de exports si no existe
    export_dir = Path("data/exports")
    export_dir.mkdir(parents=True, exist_ok=True)
    
    # Guardar archivo JSON
    json_path = export_dir / "120_expanded_segments.json"
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Archivo JSON creado exitosamente: {json_path}")
    print(f"✓ Total de segmentos generados: {len(segments)}")
    
    # Mostrar estadísticas
    print("\n=== ESTADÍSTICAS ===")
    
    # Por fase
    phases_count = {}
    for segment in segments:
        phase = segment["phase"]["main"]
        phases_count[phase] = phases_count.get(phase, 0) + 1
    
    print("Por fase:")
    for phase, count in phases_count.items():
        print(f"  - {phase}: {count} segmentos")
    
    # Por grupo de edad
    ages_count = {}
    for segment in segments:
        age = segment["age_group"]["range"]
        ages_count[age] = ages_count.get(age, 0) + 1
    
    print("\nPor grupo de edad:")
    for age, count in ages_count.items():
        print(f"  - {age}: {count} segmentos")
    
    # Por intensidad
    intensity_count = {}
    for segment in segments:
        intensity = segment["presentation_style"]["urgency"]
        intensity_count[intensity] = intensity_count.get(intensity, 0) + 1
    
    print("\nPor urgencia:")
    for urgency, count in intensity_count.items():
        print(f"  - {urgency}: {count} segmentos")
    
    # Por emoción primaria
    emotions_count = {}
    for segment in segments:
        emotion = segment["emotional_profile"]["primary"]["emotion"]
        emotions_count[emotion] = emotions_count.get(emotion, 0) + 1
    
    print("\nPor emoción primaria:")
    for emotion, count in emotions_count.items():
        print(f"  - {emotion}: {count} segmentos")
    
    return str(json_path)

if __name__ == "__main__":
    main()