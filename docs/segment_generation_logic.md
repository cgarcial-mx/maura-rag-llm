# Lógica de Generación de Segmentos Expandidos

## Resumen Ejecutivo

Este documento explica la lógica detrás de la generación de 120 segmentos expandidos para el sistema RAG de salud femenina. Los segmentos se crean combinando sistemáticamente diferentes dimensiones del ciclo menstrual, grupos de edad, estados emocionales e intensidades.

## Estructura de Datos Base

### 1. Fases del Ciclo Menstrual

```json
{
  "folicular": {
    "early": {"days": [6, 7, 8, 9], "description": "Primera fase de renovación hormonal"},
    "middle": {"days": [10, 11, 12, 13], "description": "Estrógeno en niveles medios"},
    "late": {"days": [14, 15, 16, 17], "description": "Estrógeno en pico, preparación para ovulación"}
  },
  "ovulatory": {
    "peak": {"days": [18, 19, 20, 21], "description": "Pico de estrógeno, ovulación"}
  },
  "luteal": {
    "early": {"days": [22, 23, 24, 25], "description": "Progesterona aumentando"},
    "middle": {"days": [26, 27, 28, 29], "description": "Progesterona en pico"},
    "late": {"days": [30, 31, 32, 33], "description": "Progesterona disminuyendo"}
  },
  "menstrual": {
    "flow": {"days": [1, 2, 3, 4], "description": "Flujo menstrual activo"},
    "recovery": {"days": [5, 6], "description": "Recuperación post-menstrual"}
  }
}
```

**Total de subfases**: 9 subfases únicas

### 2. Grupos de Edad

```json
{
  "8-12": {"stage": "pre_menarca", "characteristics": ["desarrollo_pubertad", "curiosidad_natural"]},
  "13-19": {"stage": "adolescente", "characteristics": ["ciclo_estableciendose", "energia_social_alta"]},
  "20-29": {"stage": "reproductiva_temprana", "characteristics": ["ciclo_estable", "responsabilidades_adultas"]},
  "30-39": {"stage": "reproductiva_media", "characteristics": ["ciclo_estable", "responsabilidades_familia"]},
  "40-49": {"stage": "perimenopausia", "characteristics": ["cambios_hormonales", "síntomas_variables"]},
  "50+": {"stage": "post_menopausia", "characteristics": ["estabilidad_hormonal", "enfoque_salud"]}
}
```

**Total de grupos de edad**: 6 grupos

### 3. Estados Emocionales

#### Emociones Positivas
- `energy`: Energía física y mental alta
- `confidence`: Confianza en capacidades y decisiones
- `creativity`: Creatividad y expresión artística
- `social_connection`: Conexión social y networking
- `productivity`: Productividad y rendimiento
- `optimism`: Optimismo y perspectiva positiva
- `motivation`: Motivación y determinación
- `resilience`: Resiliencia y capacidad de adaptación

#### Emociones Negativas
- `anxiety`: Ansiedad y preocupación
- `stress`: Estrés y sobrecarga
- `sadness`: Tristeza y melancolía
- `melancholy`: Melancolía suave y reflexión
- `insecurity`: Inseguridad y dudas
- `irritability`: Irritabilidad y frustración
- `fatigue`: Fatiga y agotamiento
- `overwhelm`: Abrumación y sobrecarga

#### Emociones Neutrales
- `sensitivity`: Sensibilidad aumentada
- `reflection`: Reflexión e introspección
- `curiosity`: Curiosidad y aprendizaje
- `adaptability`: Adaptabilidad y flexibilidad
- `introspection`: Introspección y autoconocimiento
- `calmness`: Calma y tranquilidad
- `balance`: Equilibrio y estabilidad
- `patience`: Paciencia y tolerancia

**Total de emociones**: 24 emociones únicas

### 4. Niveles de Intensidad

```json
{
  "very_low": {"score_range": [0.0, 0.5], "description": "Intensidad muy baja, síntomas mínimos"},
  "low": {"score_range": [0.5, 1.0], "description": "Intensidad baja, síntomas leves"},
  "moderate": {"score_range": [1.0, 1.5], "description": "Intensidad moderada, síntomas notables"},
  "high": {"score_range": [1.5, 2.0], "description": "Intensidad alta, síntomas significativos"},
  "very_high": {"score_range": [2.0, 2.5], "description": "Intensidad muy alta, síntomas intensos"}
}
```

## Algoritmo de Generación

### Fórmula de Combinación

```
Total de segmentos = Fases × Grupos de Edad × Variaciones por Combinación
Total de segmentos = 9 × 6 × 5 = 270 segmentos teóricos
```

Sin embargo, se generan **120 segmentos** siguiendo esta lógica:

### Lógica de Variaciones por Combinación

Para cada combinación de fase-edad, se generan exactamente **5 segmentos** con diferentes patrones emocionales:

#### Patrón 1: Muy Alta Intensidad (Positivo)
- **Emoción primaria**: Positiva (energy, confidence, creativity, etc.)
- **Emoción secundaria**: Positiva (diferente a la primaria)
- **Intensidad**: `very_high`
- **Scores**: Primaria = 2.0, Secundaria = 2.0
- **Conflicto**: `null`
- **Resolución necesaria**: `false`

#### Patrón 2: Alta Intensidad (Mixto)
- **Emoción primaria**: Negativa (anxiety, stress, sadness, etc.)
- **Emoción secundaria**: Positiva (energy, confidence, etc.)
- **Intensidad**: `high`
- **Scores**: Primaria = -1.5, Secundaria = 1.0
- **Conflicto**: `{primaria}_{secundaria}_conflict`
- **Resolución necesaria**: `true`

#### Patrón 3: Moderada Intensidad (Neutral)
- **Emoción primaria**: Neutral (sensitivity, reflection, curiosity, etc.)
- **Emoción secundaria**: Neutral (diferente a la primaria)
- **Intensidad**: `moderate`
- **Scores**: Primaria = 0.5, Secundaria = 1.0
- **Conflicto**: `null`
- **Resolución necesaria**: `false`

#### Patrón 4: Moderada Intensidad (Mixto)
- **Emoción primaria**: Negativa (diferente a la del patrón 2)
- **Emoción secundaria**: Positiva (diferente a la del patrón 2)
- **Intensidad**: `moderate`
- **Scores**: Primaria = -1.0, Secundaria = 1.0
- **Conflicto**: `{primaria}_{secundaria}_conflict`
- **Resolución necesaria**: `true`

#### Patrón 5: Baja Intensidad (Positivo)
- **Emoción primaria**: Positiva (diferente a la del patrón 1)
- **Emoción secundaria**: Positiva (diferente a la primaria)
- **Intensidad**: `low`
- **Scores**: Primaria = 1.0, Secundaria = 1.0
- **Conflicto**: `null`
- **Resolución necesaria**: `false`

## Generación de Contexto Hormonal

### Mapeo Fase → Perfil Hormonal

```python
def get_hormonal_context(phase, subphase, primary_emotion):
    contexts = {
        "folicular": {
            "early": {"estrogen": "beginning_increase", "progesterone": "very_low"},
            "middle": {"estrogen": "medium", "progesterone": "low"},
            "late": {"estrogen": "high", "progesterone": "low"}
        },
        "ovulatory": {
            "peak": {"estrogen": "peak", "progesterone": "beginning_increase"}
        },
        "luteal": {
            "early": {"estrogen": "medium", "progesterone": "increasing"},
            "middle": {"estrogen": "medium", "progesterone": "high"},
            "late": {"estrogen": "decreasing", "progesterone": "decreasing"}
        },
        "menstrual": {
            "flow": {"estrogen": "low", "progesterone": "very_low"},
            "recovery": {"estrogen": "beginning_increase", "progesterone": "very_low"}
        }
    }
```

### Ajuste por Emoción Primaria

El nivel de cortisol se ajusta según la emoción primaria:
- **Emociones positivas** (energy, confidence, creativity): `cortisol = "low"`
- **Emociones negativas** (anxiety, stress, sadness): `cortisol = "moderate"` o `"high"`
- **Emociones neutrales**: `cortisol = "low"` o `"moderate"`

## Generación de Necesidades de Contenido

### Mapeo Emoción → Necesidades Primarias

```python
primary_needs = {
    "energy": ["aprovechamiento_energia", "actividades_energeticas", "proyectos_nuevos"],
    "confidence": ["desarrollo_confianza", "liderazgo", "proyectos_importantes"],
    "anxiety": ["manejo_ansiedad", "tecnicas_calma", "validacion_emocional"],
    "stress": ["manejo_estres", "tecnicas_autocuidado", "balance_hormonal"],
    "sadness": ["apoyo_emocional", "validacion_tristeza", "conexion_emocional"],
    # ... más mapeos
}
```

### Mapeo Emoción → Necesidades Secundarias

```python
secondary_needs = {
    "energy": ["ejercicio_moderado", "nutricion_energetica", "descanso_adecuado"],
    "confidence": ["desarrollo_habilidades", "networking", "proyectos_colaborativos"],
    "anxiety": ["tecnicas_respiracion", "nutricion_estabilizadora", "ejercicio_suave"],
    # ... más mapeos
}
```

### Mapeo Emoción → Temas a Evitar

```python
avoid_topics = {
    "anxiety": ["presion_adicional", "informacion_abrumadora", "expectativas_altas"],
    "stress": ["presion_adicional", "optimizacion_excesiva", "comparaciones"],
    "sadness": ["presion_alegria", "minimizacion_emociones", "estimulacion_excesiva"],
    # ... más mapeos
}
```

## Generación de Estilo de Presentación

### Mapeo Emoción → Tono

```python
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
```

### Mapeo Edad → Longitud de Contenido

```python
length_map = {
    "8-12": "corta",      # Contenido más conciso para niños
    "13-19": "media",     # Contenido moderado para adolescentes
    "20-29": "media",     # Contenido moderado para adultos jóvenes
    "30-39": "media",     # Contenido moderado para adultos
    "40-49": "media",     # Contenido moderado para perimenopausia
    "50+": "media"        # Contenido moderado para post-menopausia
}
```

### Mapeo Intensidad → Urgencia

```python
urgency_map = {
    "very_low": "baja",
    "low": "baja",
    "moderate": "moderada",
    "high": "moderada",
    "very_high": "alta"
}
```

## Ejemplo de Segmento Generado con Metadata Completa

```json
{
  "id": "SEG_FOL_20_29_001",
  "name": "Folicular Temprana - Ansiosa pero Energética - Alta Intensidad",
  "phase": {
    "main": "folicular",
    "subphase": "early",
    "days": [6, 7, 8, 9],
    "description": "Primera fase de renovación hormonal, estrógeno comenzando a aumentar"
  },
  "age_group": {
    "range": "20-29",
    "stage": "reproductiva_temprana",
    "characteristics": ["ciclo_estable", "responsabilidades_adultas", "buscando_equilibrio", "presion_social"]
  },
  "emotional_profile": {
    "primary": {
      "emotion": "anxiety",
      "intensity": 1,
      "score": -1.5,
      "description": "Ansiedad relacionada con responsabilidades y expectativas"
    },
    "secondary": {
      "emotion": "energy",
      "intensity": 1,
      "score": 1.0,
      "description": "Energía optimizada para actividades y proyectos"
    },
    "conflict": "anxiety_energy_conflict",
    "resolution_needed": true
  },
  "hormonal_context": {
    "estrogen": "increasing",
    "progesterone": "low",
    "cortisol": "moderate",
    "optimal_balance": false,
    "description": "Contexto hormonal de folicular early con anxiety como emoción primaria"
  },
  "content_needs": {
    "primary": ["manejo_ansiedad", "aprovechamiento_energia", "balance_hormonal"],
    "secondary": ["tecnicas_respiracion", "ejercicio_moderado", "nutricion_estabilizadora"],
    "avoid": ["presion_adicional", "optimizacion_excesiva", "informacion_abrumadora"]
  },
  "presentation_style": {
    "tone": "calmante_animador",
    "structure": "balance_emocional",
    "length": "media",
    "urgency": "moderada",
    "language": "español_adaptado"
  },
  
  "segment_metadata": {
    "id": "SEG_FOL_20_29_001",
    "name": "Folicular Temprana - Ansiosa pero Energética - Alta Intensidad",
    "category": "folicular_20-29",
    "phase": "folicular",
    "subphase": "early",
    "emotional_primary": "anxiety",
    "emotional_secondary": "energy",
    "intensity_level": "high",
    "age_range": "20-29",
    "life_stage": "reproductiva_temprana",
    
    "applicable_content": {
      "lesson_3min": {
        "priority": 0.8,
        "focus_areas": ["manejo_ansiedad", "técnicas_calma", "validación_emocional"],
        "tone": "empático_tranquilizador"
      },
      "whats_happening": {
        "priority": 0.95,
        "focus_areas": ["validación_emocional", "explicación_hormonal", "normalización_síntomas"],
        "tone": "empático_tranquilizador"
      },
      "nutrition_guide": {
        "priority": 0.7,
        "focus_areas": ["alimentos_calma", "reducción_cortisol", "nutrición_estabilizadora"],
        "tone": "práctico_tranquilizador"
      },
      "breathing_exercises": {
        "priority": 0.9,
        "focus_areas": ["técnicas_respiración", "calma_inmediata", "reducción_ansiedad"],
        "tone": "calmante_empático"
      },
      "crisis_support": {
        "priority": 0.8,
        "focus_areas": ["apoyo_crisis_ansiedad", "técnicas_emergencia", "calma_inmediata"],
        "tone": "urgente_tranquilizador"
      }
    },
    
    "search_keywords": [
      "folicular temprana anxiety",
      "anxiety energy",
      "ansiedad",
      "preocupación",
      "estrógeno",
      "energía",
      "crecimiento",
      "adulto_joven"
    ],
    
    "related_segments": [
      "SEG_FOL_8_12_XXX",
      "SEG_FOL_13_19_XXX",
      "SEG_FOL_30_39_XXX",
      "SEG_OVU_20_29_XXX",
      "SEG_LUT_20_29_XXX"
    ],
    
    "content_generation_rules": {
      "max_length": 800,
      "min_validation": true,
      "include_practical_tips": true,
      "avoid_medical_diagnosis": true,
      "tone": "calmante_animador",
      "urgency": "moderada",
      "language": "español_adaptado",
      "structure": "balance_emocional"
    }
  }
}
```

## Metadata para Mistral (Sistema RAG)

### Estructura de Metadata

Cada segmento incluye una sección `segment_metadata` específicamente diseñada para que Mistral pueda consultar y generar contenido apropiado:

#### 1. **Información Básica del Segmento**
```json
{
  "id": "SEG_FOL_20_29_001",
  "name": "Folicular Temprana - Ansiosa pero Energética - Alta Intensidad",
  "category": "folicular_20-29",
  "phase": "folicular",
  "subphase": "early",
  "emotional_primary": "anxiety",
  "emotional_secondary": "energy",
  "intensity_level": "high",
  "age_range": "20-29",
  "life_stage": "reproductiva_temprana"
}
```

#### 2. **Contenido Aplicable (`applicable_content`)**

Define qué tipos de contenido son apropiados para cada segmento con:
- **Prioridad** (0.0 - 1.0): Qué tan relevante es el tipo de contenido
- **Focus Areas**: Áreas específicas de enfoque para el contenido
- **Tone**: Tono específico para cada tipo de contenido

```json
"applicable_content": {
  "lesson_3min": {
    "priority": 0.8,
    "focus_areas": ["manejo_ansiedad", "técnicas_calma", "validación_emocional"],
    "tone": "empático_tranquilizador"
  },
  "breathing_exercises": {
    "priority": 0.9,
    "focus_areas": ["técnicas_respiración", "calma_inmediata", "reducción_ansiedad"],
    "tone": "calmante_empático"
  }
}
```

#### 3. **Palabras Clave de Búsqueda (`search_keywords`)**

Generadas automáticamente basadas en:
- Fase + emoción primaria
- Emociones combinadas
- Síntomas específicos por emoción
- Contexto hormonal
- Contexto de edad

```json
"search_keywords": [
  "folicular temprana anxiety",
  "anxiety energy",
  "ansiedad",
  "preocupación",
  "estrógeno",
  "energía",
  "crecimiento",
  "adulto_joven"
]
```

#### 4. **Segmentos Relacionados (`related_segments`)**

Identifica segmentos similares basados en:
- Misma fase, diferentes edades
- Misma emoción primaria, diferentes fases
- Emociones similares o complementarias

```json
"related_segments": [
  "SEG_FOL_8_12_XXX",
  "SEG_FOL_13_19_XXX",
  "SEG_FOL_30_39_XXX",
  "SEG_OVU_20_29_XXX",
  "SEG_LUT_20_29_XXX"
]
```

#### 5. **Reglas de Generación de Contenido (`content_generation_rules`)**

Define parámetros específicos para la generación:
- **max_length**: Longitud máxima según edad e intensidad
- **tone**: Tono general del contenido
- **urgency**: Nivel de urgencia del contenido
- **language**: Nivel de complejidad del lenguaje
- **structure**: Estructura recomendada del contenido

```json
"content_generation_rules": {
  "max_length": 800,
  "min_validation": true,
  "include_practical_tips": true,
  "avoid_medical_diagnosis": true,
  "tone": "calmante_animador",
  "urgency": "moderada",
  "language": "español_adaptado",
  "structure": "balance_emocional"
}
```

### Lógica de Priorización de Contenido

#### Ajuste por Emoción Primaria
- **Ansiedad/Estrés**: Prioriza `breathing_exercises` (0.9) y `crisis_support` (0.8)
- **Energía/Confianza**: Prioriza `productivity_tips` (0.9) y `lesson_3min` (0.9)
- **Tristeza/Melancolía**: Prioriza `whats_happening` (0.95) y `crisis_support` (0.7)
- **Curiosidad**: Prioriza `educational_videos` (0.9) y `lesson_3min` (0.9)

#### Ajuste por Intensidad
- **Alta/Very High**: Aumenta prioridad de `crisis_support` y `breathing_exercises`
- **Baja/Very Low**: Reduce prioridad de contenido de crisis

#### Ajuste por Edad
- **8-12 años**: Prioriza `educational_videos` y `lesson_3min`, reduce `productivity_tips`
- **Adultos**: Mantiene balance entre todos los tipos de contenido

### Generación de Focus Areas

Cada tipo de contenido tiene áreas de enfoque específicas por emoción:

#### Para `lesson_3min`:
- **Ansiedad**: ["manejo_ansiedad", "técnicas_calma", "validación_emocional"]
- **Energía**: ["aprovechamiento_energía", "actividades_energéticas", "proyectos_nuevos"]
- **Confianza**: ["desarrollo_confianza", "liderazgo", "proyectos_importantes"]

#### Para `nutrition_guide`:
- **Ansiedad**: ["alimentos_calma", "reducción_cortisol", "nutrición_estabilizadora"]
- **Estrés**: ["alimentos_antiestrés", "balance_hormonal", "nutrición_equilibrada"]
- **Energía**: ["alimentos_energéticos", "nutrición_optimizada", "combustible_corporal"]

### Generación de Tono

El tono se ajusta según:
1. **Tipo de contenido**: `lesson_3min` vs `crisis_support`
2. **Emoción primaria**: `anxiety` → `tranquilizador`
3. **Intensidad**: `high` → `muy_tranquilizador`

### Longitud Máxima del Contenido

```python
base_length = {
  "8-12": 400,    # Contenido más conciso para niños
  "13-19": 500,   # Contenido moderado para adolescentes
  "20-29": 600,   # Contenido completo para adultos jóvenes
  "30-39": 600,   # Contenido completo para adultos
  "40-49": 600,   # Contenido completo para perimenopausia
  "50+": 500      # Contenido moderado para post-menopausia
}

# Ajuste por intensidad
if intensity in ["very_high", "high"]:
    length = min(800, length + 200)  # Más extenso para alta intensidad
elif intensity in ["very_low", "low"]:
    length = max(300, length - 100)  # Más conciso para baja intensidad
```

## Ventajas del Sistema

### 1. **Cobertura Completa**
- Cubre todas las fases del ciclo menstrual
- Incluye todos los grupos de edad relevantes
- Abarca el espectro completo de estados emocionales

### 2. **Personalización Granular**
- Cada segmento tiene necesidades específicas de contenido
- Estilos de presentación adaptados a la edad y estado emocional
- Prioridades de intervención claramente definidas

### 3. **Metadata Inteligente para RAG**
- Palabras clave específicas para búsqueda contextual
- Prioridades de contenido calculadas dinámicamente
- Reglas de generación adaptadas a cada segmento
- Segmentos relacionados para recomendaciones

### 4. **Escalabilidad**
- Fácil agregar nuevas emociones o fases
- Sistema modular que permite modificaciones
- Base de datos estructurada para consultas eficientes

### 5. **Consistencia**
- Lógica predecible para generación de contenido
- Mapeos consistentes entre emociones y necesidades
- Estructura uniforme en todos los segmentos

## Casos de Uso

### 1. **Generación de Contenido Personalizado**
- El sistema RAG puede usar la metadata del segmento para generar contenido específico
- Las necesidades de contenido guían el tipo de información a incluir
- El estilo de presentación determina el tono y formato

### 2. **Recomendaciones de Intervención**
- Las prioridades de intervención sugieren acciones específicas
- Los temas a evitar previenen contenido contraproducente
- La urgencia determina la prioridad de entrega

### 3. **Análisis y Reporting**
- Estadísticas por fase, edad, emoción e intensidad
- Identificación de patrones en el comportamiento del usuario
- Optimización continua del sistema

## Conclusiones

El sistema de generación de segmentos expandidos proporciona una base sólida para la personalización de contenido en salud femenina. La combinación sistemática de dimensiones relevantes asegura que cada usuario reciba contenido apropiado para su situación específica, mejorando la efectividad del sistema RAG y la experiencia del usuario.