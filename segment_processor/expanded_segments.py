# segment_processor/expanded_segments.py

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
from pathlib import Path

@dataclass
class Demographics:
    age_groups: List[str]
    life_stages: List[str]
    common_triggers: List[str] = None
    development_stage: Optional[str] = None
    common_concerns: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.common_triggers is None:
            self.common_triggers = []

@dataclass
class HormonalProfile:
    estrogen_level: str
    progesterone_level: str
    cortisol_level: Optional[str] = None
    development_stage: Optional[str] = None
    sensitivity_factors: List[str] = None

@dataclass
class EmotionalCharacteristics:
    primary_emotions: List[str]
    secondary_emotions: List[str]
    emotional_range: List[float]
    volatility: str
    recovery_time: str

@dataclass
class PhysicalSymptoms:
    common: List[str]
    moderate: List[str]
    severe: List[str]

@dataclass
class ContentPreferences:
    tone: str
    depth: str
    urgency: str
    focus_areas: List[str]
    avoid_topics: List[str]

@dataclass
class RecommendedContentTypes:
    lesson_3min: float
    whats_happening: float
    nutrition_guide: float
    cycle_day_info: float
    hormone_levels: float
    stress_levels: float

@dataclass
class ExpandedSegment:
    id: str
    name: str
    category: str
    phase: str
    emotional_primary: Optional[str] = None
    emotional_secondary: Optional[str] = None
    emotional_combination: Optional[str] = None
    intensity_level: Optional[str] = None
    duration_pattern: Optional[str] = None
    age_range: Optional[str] = None
    life_stage: Optional[str] = None
    symptom_count: Optional[str] = None
    
    demographics: Demographics = None
    hormonal_profile: HormonalProfile = None
    emotional_characteristics: EmotionalCharacteristics = None
    physical_symptoms: Optional[PhysicalSymptoms] = None
    content_preferences: ContentPreferences = None
    recommended_content_types: RecommendedContentTypes = None
    intervention_priorities: List[str] = None
    related_segments: List[str] = None

class ExpandedSegmentDatabase:
    """
    Base de datos de segmentos expandidos con metadata detallada
    """
    
    def __init__(self):
        self.segments = {}
        self.emotion_mapping = self._create_emotion_mapping()
        self._initialize_segments()
    
    def _create_emotion_mapping(self):
        """
        Mapeo de emociones consistente con docs/emotions.js
        """
        return {
            # Estrés y ansiedad
            "ansiosa": "FEEL001",
            "abrumada": "FEEL002", 
            "nerviosa": "FEEL003",
            "impaciente": "FEEL004",
            "tensa": "FEEL005",
            "frustrada": "FEEL006",
            "preocupada": "FEEL007",
            "estresada": "FEEL008",
            "cansada_mentalmente": "FEEL009",
            "insegura": "FEEL010",
            
            # Ánimo bajo
            "triste": "FEEL011",
            "vacía": "FEEL012",
            "sensible": "FEEL013",
            "desmotivada": "FEEL014",
            "aislada": "FEEL015",
            "lloro_fácil": "FEEL016",
            "nostálgica": "FEEL017",
            "melancólica": "FEEL018",
            "incomprendida": "FEEL019",
            "desesperanzada": "FEEL020",
            
            # Físico y energía
            "cansada_físicamente": "FEEL021",
            "energética": "FEEL022",
            "letárgica": "FEEL023",
            "inflamada": "FEEL024",
            "dolorida": "FEEL025",
            "irritable_físicamente": "FEEL026",
            "con_hambre_excesiva": "FEEL027",
            "liviana": "FEEL028",
            "activa": "FEEL029",
            "aletargada": "FEEL030",
            
            # Autoestima
            "poderosa": "FEEL031",
            "atractiva": "FEEL032",
            "desconectada": "FEEL034",
            "confiada": "FEEL035",
            "inadecuada": "FEEL036",
            "en_paz_conmigo": "FEEL037",
            "con_culpa": "FEEL038",
            "orgullosa_de_mí": "FEEL039",
            "frágil": "FEEL040",
            
            # Relacional
            "amada": "FEEL041",
            "ignorada": "FEEL042",
            "conectada": "FEEL043",
            "en_conflicto": "FEEL044",
            "valorada": "FEEL045",
            "sola": "FEEL046",
            "cuidada": "FEEL047",
            "rechazada": "FEEL048",
            "agradecida": "FEEL049",
            "acompañada": "FEEL050"
        }
    
    def _initialize_segments(self):
        """Inicializa todos los segmentos expandidos"""
        
        # SEGMENTOS BASE POR FASE EMOCIONAL
        self._add_base_phase_emotional_segments()
        
        # SEGMENTOS POR EDAD
        self._add_age_specific_segments()
        
        # SEGMENTOS MIXTOS (COMBINACIÓN EMOCIONAL)
        self._add_mixed_emotional_segments()
        
        # SEGMENTOS POR INTENSIDAD DE SÍNTOMAS
        self._add_symptom_intensity_segments()
    
    def _add_base_phase_emotional_segments(self):
        """Segmentos base por fase y estado emocional"""
        
        # FOLICULAR ESTRESADA CRÓNICA
        self.segments["SEG001_FOL_STRESS_CHRONIC"] = ExpandedSegment(
            id="SEG001_FOL_STRESS_CHRONIC",
            name="Folicular Estresada Crónica",
            category="base_phase_emotional",
            phase="folicular",
            emotional_primary="ansiosa",
            emotional_secondary="cansada_mentalmente",
            intensity_level="alta",
            duration_pattern="crónica",
            
            demographics=Demographics(
                age_groups=["20-29", "30-39", "40-49"],
                life_stages=["reproductiva", "perimenopausia"],
                common_triggers=["trabajo", "relaciones", "finanzas"]
            ),
            
            hormonal_profile=HormonalProfile(
                estrogen_level="creciente",
                progesterone_level="bajo",
                cortisol_level="elevado",
                sensitivity_factors=["cortisol_estrogen_interaction", "stress_amplification"]
            ),
            
            emotional_characteristics=EmotionalCharacteristics(
                primary_emotions=["ansiosa", "preocupada", "abrumada"],
                secondary_emotions=["frustrada", "impaciente", "cansada_mentalmente"],
                emotional_range=[-2.0, -0.5],
                volatility="alta",
                recovery_time="lento"
            ),
            
            physical_symptoms=PhysicalSymptoms(
                common=["tensión_muscular", "dolores_cabeza", "fatiga"],
                moderate=["problemas_sueño", "cambios_apetito", "palpitaciones"],
                severe=["ataques_pánico", "agotamiento_extremo"]
            ),
            
            content_preferences=ContentPreferences(
                tone="empático_tranquilizador",
                depth="intermedio",
                urgency="alta",
                focus_areas=["manejo_estres", "técnicas_calma", "validación"],
                avoid_topics=["presión_adicional", "optimización_excesiva"]
            ),
            
            recommended_content_types=RecommendedContentTypes(
                lesson_3min=0.9,
                whats_happening=0.95,
                nutrition_guide=0.8,
                cycle_day_info=0.85,
                hormone_levels=0.9,
                stress_levels=0.95
            ),
            
            intervention_priorities=[
                "reducción_cortisol",
                "técnicas_respiración",
                "validación_emocional",
                "estrategias_manejo_estres"
            ],
            
            related_segments=[
                "SEG001_FOL_STRESS_ACUTE",
                "SEG011_LUT_ANXIOUS",
                "SEG016_MEN_IRRITABLE"
            ]
        )
        
        # FOLICULAR ENERGÉTICA
        self.segments["SEG002_FOL_ENERGETIC"] = ExpandedSegment(
            id="SEG002_FOL_ENERGETIC",
            name="Folicular Energética",
            category="base_phase_emotional",
            phase="folicular",
            emotional_primary="energética",
            emotional_secondary="confiada",
            intensity_level="moderada",
            duration_pattern="estable",
            
            demographics=Demographics(
                age_groups=["20-29", "30-39"],
                life_stages=["reproductiva"],
                common_triggers=["proyectos_nuevos", "oportunidades", "metas"]
            ),
            
            hormonal_profile=HormonalProfile(
                estrogen_level="creciente",
                progesterone_level="bajo",
                cortisol_level="normal",
                sensitivity_factors=["estrogen_energy_boost", "motivation_amplification"]
            ),
            
            emotional_characteristics=EmotionalCharacteristics(
                primary_emotions=["energética", "activa", "confiada"],
                secondary_emotions=["poderosa", "orgullosa_de_mí", "en_paz_conmigo"],
                emotional_range=[0.5, 2.0],
                volatility="baja",
                recovery_time="rápido"
            ),
            
            content_preferences=ContentPreferences(
                tone="motivacional_optimista",
                depth="intermedio",
                urgency="baja",
                focus_areas=["optimización_energía", "productividad", "metas"],
                avoid_topics=["limitaciones", "obstáculos"]
            ),
            
            recommended_content_types=RecommendedContentTypes(
                lesson_3min=0.8,
                whats_happening=0.7,
                nutrition_guide=0.9,
                cycle_day_info=0.8,
                hormone_levels=0.85,
                stress_levels=0.6
            ),
            
            intervention_priorities=[
                "canalización_energía",
                "optimización_rendimiento",
                "mantenimiento_motivación",
                "gestión_proyectos"
            ],
            
            related_segments=[
                "SEG_MIX_001",
                "SEG003_FOL_BALANCED"
            ]
        )
        
        # LÚTEA ANSIOSA
        self.segments["SEG011_LUT_ANXIOUS"] = ExpandedSegment(
            id="SEG011_LUT_ANXIOUS",
            name="Lútea Ansiosa",
            category="base_phase_emotional",
            phase="luteal",
            emotional_primary="ansiosa",
            emotional_secondary="frustrada",
            intensity_level="alta",
            duration_pattern="cíclica",
            
            demographics=Demographics(
                age_groups=["20-29", "30-39", "40-49"],
                life_stages=["reproductiva", "perimenopausia"],
                common_triggers=["cambios_hormonales", "estrés", "expectativas"]
            ),
            
            hormonal_profile=HormonalProfile(
                estrogen_level="variable",
                progesterone_level="alto",
                cortisol_level="elevado",
                sensitivity_factors=["progesterone_anxiety", "hormonal_fluctuation"]
            ),
            
            emotional_characteristics=EmotionalCharacteristics(
                primary_emotions=["ansiosa", "tensa", "preocupada"],
                secondary_emotions=["frustrada", "estresada", "cansada_físicamente"],
                emotional_range=[-2.0, 0.0],
                volatility="alta",
                recovery_time="lento"
            ),
            
            physical_symptoms=PhysicalSymptoms(
                common=["tensión_muscular", "problemas_sueño", "cambios_apetito"],
                moderate=["palpitaciones", "dolores_cabeza", "fatiga"],
                severe=["ataques_pánico", "agotamiento_emocional"]
            ),
            
            content_preferences=ContentPreferences(
                tone="empático_tranquilizador",
                depth="básico",
                urgency="alta",
                focus_areas=["manejo_ansiedad", "técnicas_calma", "validación"],
                avoid_topics=["presión_adicional", "optimización"]
            ),
            
            recommended_content_types=RecommendedContentTypes(
                lesson_3min=0.7,
                whats_happening=0.9,
                nutrition_guide=0.8,
                cycle_day_info=0.8,
                hormone_levels=0.9,
                stress_levels=0.95
            ),
            
            intervention_priorities=[
                "reducción_ansiedad",
                "técnicas_respiración",
                "validación_emocional",
                "manejo_síntomas"
            ],
            
            related_segments=[
                "SEG001_FOL_STRESS_CHRONIC",
                "SEG_INT_001"
            ]
        )
    
    def _add_age_specific_segments(self):
        """Segmentos específicos por edad"""
        
        # PRE-MENARCA CURIOSA
        self.segments["SEG_PREMEN_001"] = ExpandedSegment(
            id="SEG_PREMEN_001",
            name="Pre-menarca Curiosa",
            category="age_specific",
            phase="pre_menstrual",
            age_range="10-14",
            life_stage="pre_menarca",
            
            demographics=Demographics(
                age_groups=["10-12", "13-14"],
                life_stages=["pre_menarca"],
                development_stage="pubertad_temprana",
                common_concerns=["cambios_corporales", "expectativas_sociales", "preparación"]
            ),
            
            hormonal_profile=HormonalProfile(
                estrogen_level="inicial",
                progesterone_level="mínimo",
                development_stage="pre_ovulatorio",
                sensitivity_factors=["cambios_corporales", "expectativas", "comparación_social"]
            ),
            
            emotional_characteristics=EmotionalCharacteristics(
                primary_emotions=["nerviosa", "insegura", "sensible"],
                secondary_emotions=["impaciente", "frágil", "desconectada"],
                emotional_range=[-0.5, 1.5],
                volatility="moderada",
                recovery_time="rápido"
            ),
            
            content_preferences=ContentPreferences(
                tone="educativo_empático",
                depth="básico",
                urgency="baja",
                focus_areas=["educación_básica", "normalización", "preparación"],
                avoid_topics=["síntomas_graves", "complicaciones", "presión_temporal"]
            ),
            
            recommended_content_types=RecommendedContentTypes(
                lesson_3min=0.8,
                whats_happening=0.9,
                nutrition_guide=0.7,
                cycle_day_info=0.9,
                hormone_levels=0.8,
                stress_levels=0.5
            ),
            
            intervention_priorities=[
                "educación_básica",
                "normalización_cambios",
                "preparación_emocional",
                "apoyo_familiar"
            ],
            
            related_segments=[]
        )
        
        # PERIMENOPAUSIA INTENSA
        self.segments["SEG_PERI_001"] = ExpandedSegment(
            id="SEG_PERI_001",
            name="Perimenopausia Intensa",
            category="age_specific",
            phase="perimenopausia",
            age_range="45-55",
            life_stage="perimenopausia",
            
            demographics=Demographics(
                age_groups=["45-49", "50-55"],
                life_stages=["perimenopausia"],
                common_triggers=["cambios_hormonales", "estrés", "expectativas_vida"]
            ),
            
            hormonal_profile=HormonalProfile(
                estrogen_level="variable",
                progesterone_level="variable",
                cortisol_level="elevado",
                sensitivity_factors=["hormonal_fluctuation", "estrogen_decline", "stress_amplification"]
            ),
            
            emotional_characteristics=EmotionalCharacteristics(
                primary_emotions=["ansiosa", "frustrada", "abrumada"],
                secondary_emotions=["triste", "vacía", "cansada_físicamente"],
                emotional_range=[-2.0, 0.5],
                volatility="muy_alta",
                recovery_time="lento"
            ),
            
            physical_symptoms=PhysicalSymptoms(
                common=["sofocos", "problemas_sueño", "cambios_apetito", "fatiga"],
                moderate=["palpitaciones", "dolores_cabeza", "tensión_muscular"],
                severe=["ataques_pánico", "depresión", "agotamiento_extremo"]
            ),
            
            content_preferences=ContentPreferences(
                tone="empático_tranquilizador",
                depth="intermedio",
                urgency="alta",
                focus_areas=["manejo_síntomas", "validación", "estrategias_calma"],
                avoid_topics=["presión_adicional", "optimización_excesiva"]
            ),
            
            recommended_content_types=RecommendedContentTypes(
                lesson_3min=0.8,
                whats_happening=0.9,
                nutrition_guide=0.8,
                cycle_day_info=0.8,
                hormone_levels=0.85,
                stress_levels=0.9
            ),
            
            intervention_priorities=[
                "manejo_síntomas_perimenopausia",
                "validación_emocional",
                "estrategias_calma",
                "apoyo_transición"
            ],
            
            related_segments=[
                "SEG_INT_001",
                "SEG011_LUT_ANXIOUS"
            ]
        )
    
    def _add_mixed_emotional_segments(self):
        """Segmentos con combinaciones emocionales mixtas"""
        
        # ANSIOSA-ENERGÉTICA
        self.segments["SEG_MIX_001"] = ExpandedSegment(
            id="SEG_MIX_001",
            name="Ansiosa-Energética",
            category="mixed_emotional",
            phase="folicular",
            emotional_combination="ansiosa_energetica",
            
            demographics=Demographics(
                age_groups=["20-29", "30-39"],
                life_stages=["reproductiva"],
                common_triggers=["proyectos_nuevos", "deadlines", "oportunidades"]
            ),
            
            hormonal_profile=HormonalProfile(
                estrogen_level="creciente",
                progesterone_level="bajo",
                cortisol_level="moderado",
                sensitivity_factors=["estrogen_energy_boost", "cortisol_anxiety"]
            ),
            
            emotional_characteristics=EmotionalCharacteristics(
                primary_emotions=["ansiosa", "energética", "activa"],
                secondary_emotions=["nerviosa", "preocupada", "confiada"],
                emotional_range=[-1.0, 2.0],
                volatility="alta",
                recovery_time="variable"
            ),
            
            content_preferences=ContentPreferences(
                tone="motivacional_equilibrado",
                depth="intermedio",
                urgency="moderada",
                focus_areas=["canalización_energía", "manejo_ansiedad", "optimización"],
                avoid_topics=["sobreestimulación", "presión_excesiva"]
            ),
            
            recommended_content_types=RecommendedContentTypes(
                lesson_3min=0.8,
                whats_happening=0.7,
                nutrition_guide=0.8,
                cycle_day_info=0.7,
                hormone_levels=0.8,
                stress_levels=0.7
            ),
            
            intervention_priorities=[
                "canalización_energía",
                "manejo_ansiedad",
                "optimización_rendimiento",
                "equilibrio_emocional"
            ],
            
            related_segments=[
                "SEG002_FOL_ENERGETIC",
                "SEG001_FOL_STRESS_CHRONIC"
            ]
        )
    
    def _add_symptom_intensity_segments(self):
        """Segmentos por intensidad de síntomas"""
        
        # LÚTEA INTENSA
        self.segments["SEG_INT_001"] = ExpandedSegment(
            id="SEG_INT_001",
            name="Lútea Intensa",
            category="symptom_intensity",
            phase="luteal",
            intensity_level="alta",
            symptom_count="7+",
            
            demographics=Demographics(
                age_groups=["20-29", "30-39", "40-49"],
                life_stages=["reproductiva", "perimenopausia"],
                common_triggers=["estrés", "cambios_alimentarios", "falta_sueño"]
            ),
            
            hormonal_profile=HormonalProfile(
                estrogen_level="variable",
                progesterone_level="alto",
                cortisol_level="elevado",
                sensitivity_factors=["progesterone_sensitivity", "cortisol_amplification"]
            ),
            
            emotional_characteristics=EmotionalCharacteristics(
                primary_emotions=["frustrada", "ansiosa", "triste"],
                secondary_emotions=["abrumada", "desesperanzada", "cansada_físicamente"],
                emotional_range=[-2.0, 0.0],
                volatility="muy_alta",
                recovery_time="lento"
            ),
            
            physical_symptoms=PhysicalSymptoms(
                common=["hinchazón", "dolores_cabeza", "fatiga", "cambios_apetito"],
                moderate=["problemas_sueño", "tensión_muscular", "palpitaciones"],
                severe=["ataques_pánico", "depresión", "agotamiento_extremo"]
            ),
            
            content_preferences=ContentPreferences(
                tone="empático_tranquilizador",
                depth="básico",
                urgency="muy_alta",
                focus_areas=["manejo_síntomas", "validación", "estrategias_calma"],
                avoid_topics=["optimización", "presión_adicional", "complicaciones"]
            ),
            
            recommended_content_types=RecommendedContentTypes(
                lesson_3min=0.7,
                whats_happening=0.9,
                nutrition_guide=0.8,
                cycle_day_info=0.7,
                hormone_levels=0.85,
                stress_levels=0.95
            ),
            
            intervention_priorities=[
                "manejo_síntomas_graves",
                "validación_emocional",
                "estrategias_calma",
                "apoyo_crisis"
            ],
            
            related_segments=[
                "SEG011_LUT_ANXIOUS",
                "SEG_PERI_001"
            ]
        )
    
    def get_segment(self, segment_id: str) -> Optional[ExpandedSegment]:
        """Obtiene un segmento por ID"""
        return self.segments.get(segment_id)
    
    def get_segments_by_category(self, category: str) -> List[ExpandedSegment]:
        """Obtiene todos los segmentos de una categoría"""
        return [seg for seg in self.segments.values() if seg.category == category]
    
    def get_segments_by_phase(self, phase: str) -> List[ExpandedSegment]:
        """Obtiene todos los segmentos de una fase"""
        return [seg for seg in self.segments.values() if seg.phase == phase]
    
    def get_all_segments(self) -> Dict[str, ExpandedSegment]:
        """Obtiene todos los segmentos"""
        return self.segments
    
    def validate_emotions(self) -> Dict[str, List[str]]:
        """
        Valida que todas las emociones usadas estén en el mapeo
        """
        validation_results = {
            "valid_emotions": [],
            "invalid_emotions": [],
            "missing_emotions": []
        }
        
        for segment_id, segment in self.segments.items():
            # Validar emociones primarias y secundarias
            if segment.emotional_primary:
                if segment.emotional_primary in self.emotion_mapping:
                    validation_results["valid_emotions"].append(f"{segment_id}: {segment.emotional_primary}")
                else:
                    validation_results["invalid_emotions"].append(f"{segment_id}: {segment.emotional_primary}")
            
            if segment.emotional_secondary:
                if segment.emotional_secondary in self.emotion_mapping:
                    validation_results["valid_emotions"].append(f"{segment_id}: {segment.emotional_secondary}")
                else:
                    validation_results["invalid_emotions"].append(f"{segment_id}: {segment.emotional_secondary}")
            
            # Validar emociones en características emocionales
            if segment.emotional_characteristics:
                for emotion in segment.emotional_characteristics.primary_emotions:
                    if emotion in self.emotion_mapping:
                        validation_results["valid_emotions"].append(f"{segment_id} (primary): {emotion}")
                    else:
                        validation_results["invalid_emotions"].append(f"{segment_id} (primary): {emotion}")
                
                for emotion in segment.emotional_characteristics.secondary_emotions:
                    if emotion in self.emotion_mapping:
                        validation_results["valid_emotions"].append(f"{segment_id} (secondary): {emotion}")
                    else:
                        validation_results["invalid_emotions"].append(f"{segment_id} (secondary): {emotion}")
        
        return validation_results
    
    def get_emotion_id(self, emotion_name: str) -> Optional[str]:
        """Obtiene el ID de una emoción del mapeo"""
        return self.emotion_mapping.get(emotion_name)
    
    def get_segment_metadata(self, segment_id: str) -> Dict[str, Any]:
        """Obtiene metadata de un segmento para el sistema RAG"""
        segment = self.get_segment(segment_id)
        if not segment:
            return {}
        
        return {
            "segment_metadata": {
                "id": segment.id,
                "name": segment.name,
                "category": segment.category,
                "phase": segment.phase,
                "emotional_primary": segment.emotional_primary,
                "intensity_level": segment.intensity_level,
                
                "applicable_content": {
                    "lesson_3min": {
                        "priority": segment.recommended_content_types.lesson_3min,
                        "focus_areas": segment.content_preferences.focus_areas,
                        "tone": segment.content_preferences.tone
                    },
                    "whats_happening": {
                        "priority": segment.recommended_content_types.whats_happening,
                        "focus_areas": segment.content_preferences.focus_areas,
                        "tone": segment.content_preferences.tone
                    },
                    "nutrition_guide": {
                        "priority": segment.recommended_content_types.nutrition_guide,
                        "focus_areas": segment.content_preferences.focus_areas,
                        "tone": segment.content_preferences.tone
                    }
                },
                
                "search_keywords": self._generate_search_keywords(segment),
                
                "related_segments": segment.related_segments or [],
                
                "content_generation_rules": {
                    "max_length": 600,
                    "min_validation": True,
                    "include_practical_tips": True,
                    "avoid_medical_diagnosis": True,
                    "tone": segment.content_preferences.tone,
                    "urgency": segment.content_preferences.urgency
                }
            }
        }
    
    def _generate_search_keywords(self, segment: ExpandedSegment) -> List[str]:
        """Genera palabras clave de búsqueda para un segmento"""
        keywords = []
        
        # Fase + emociones
        if segment.emotional_primary:
            keywords.append(f"{segment.phase} {segment.emotional_primary}")
        
        # Síntomas físicos
        if segment.physical_symptoms:
            keywords.extend(segment.physical_symptoms.common[:3])
        
        # Características emocionales
        if segment.emotional_characteristics:
            keywords.extend(segment.emotional_characteristics.primary_emotions[:2])
        
        # Factores de sensibilidad hormonal
        if segment.hormonal_profile and segment.hormonal_profile.sensitivity_factors:
            keywords.extend(segment.hormonal_profile.sensitivity_factors[:2])
        
        return keywords
    
    def save_to_file(self, file_path: str):
        """Guarda todos los segmentos a un archivo JSON"""
        segments_data = {}
        for segment_id, segment in self.segments.items():
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
                    "cycle_day_info": segment.recommended_content_types.cycle_day_info,
                    "hormone_levels": segment.recommended_content_types.hormone_levels,
                    "stress_levels": segment.recommended_content_types.stress_levels
                },
                
                "intervention_priorities": segment.intervention_priorities,
                "related_segments": segment.related_segments
            }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(segments_data, f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, file_path: str):
        """Carga segmentos desde un archivo JSON"""
        with open(file_path, 'r', encoding='utf-8') as f:
            segments_data = json.load(f)
        
        self.segments = {}
        for segment_id, data in segments_data.items():
            # Reconstruir objetos dataclass
            demographics = Demographics(**data["demographics"])
            hormonal_profile = HormonalProfile(**data["hormonal_profile"])
            emotional_characteristics = EmotionalCharacteristics(**data["emotional_characteristics"])
            
            physical_symptoms = None
            if data["physical_symptoms"]["common"]:
                physical_symptoms = PhysicalSymptoms(**data["physical_symptoms"])
            
            content_preferences = ContentPreferences(**data["content_preferences"])
            recommended_content_types = RecommendedContentTypes(**data["recommended_content_types"])
            
            segment = ExpandedSegment(
                id=data["id"],
                name=data["name"],
                category=data["category"],
                phase=data["phase"],
                emotional_primary=data.get("emotional_primary"),
                emotional_secondary=data.get("emotional_secondary"),
                emotional_combination=data.get("emotional_combination"),
                intensity_level=data.get("intensity_level"),
                duration_pattern=data.get("duration_pattern"),
                age_range=data.get("age_range"),
                life_stage=data.get("life_stage"),
                symptom_count=data.get("symptom_count"),
                demographics=demographics,
                hormonal_profile=hormonal_profile,
                emotional_characteristics=emotional_characteristics,
                physical_symptoms=physical_symptoms,
                content_preferences=content_preferences,
                recommended_content_types=recommended_content_types,
                intervention_priorities=data["intervention_priorities"],
                related_segments=data["related_segments"]
            )
            
            self.segments[segment_id] = segment