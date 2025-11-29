# Sistema de Segmentación de Usuarios para API Node.js

## Contexto y Arquitectura

El sistema de segmentación funciona de manera desacoplada:

- **Generador de Contenidos (Python)**: Genera contenido personalizado basado en segmentos expandidos
- **API de Producción (Node.js/Express)**: Maneja la lógica de negocio, incluyendo el cálculo de segmentación en tiempo real
- **Base de Datos de Contenidos**: Almacena el contenido pre-generado por segmentos

## Archivo de Referencia: `docs/emotions.js`

```javascript
const emotionsData = {
  'Estrés y ansiedad': [
    { id: 'FEEL001', feeling: 'Ansiosa', score: -2 },
    { id: 'FEEL002', feeling: 'Abrumada', score: -2 },
    { id: 'FEEL003', feeling: 'Nerviosa', score: -1 },
    // ... más emociones
  ],
  'Ánimo bajo': [...],
  'Físico y energía': [...],
  'Autoestima': [...],
  'Relacional': [...]
}
```

## Sistema de Segmentación para la API Node.js

### 1. Estructura de Datos del Usuario

```javascript
// Modelo de Usuario con datos necesarios para segmentación
const userSegmentationData = {
  // Datos del ciclo menstrual
  cycle: {
    lastPeriodDate: "2024-01-15",
    averageCycleLength: 28,
    currentDay: 12,
    currentPhase: "folicular", // folicular, ovulatory, luteal, menstrual
    subPhase: "middle" // early, middle, late, peak, flow, recovery
  },
  
  // Datos demográficos
  demographics: {
    age: 25,
    ageGroup: "20-29", // 8-12, 13-19, 20-29, 30-39, 40-49, 50+
    lifeStage: "reproductiva_temprana"
  },
  
  // Estado emocional actual (últimos 7 días)
  currentEmotions: [
    { emotionId: "FEEL001", intensity: 3, timestamp: "2024-01-20" },
    { emotionId: "FEEL022", intensity: 2, timestamp: "2024-01-21" },
    // ... más registros emocionales
  ],
  
  // Historial de síntomas físicos (calculados desde registros emocionales)
  physicalSymptoms: [
    { symptom: "tension_muscular", intensity: 2, date: "2024-01-20" },
    { symptom: "fatiga", intensity: 1, date: "2024-01-21" }
  ],
  
  // Preferencias de contenido (aprendidas del comportamiento del usuario)
  contentPreferences: {
    preferredLength: "medium", // short, medium, long
    preferredTone: "empathetic", // empathetic, motivational, educational
    avoidTopics: ["medical_advice", "intense_exercises"]
  }
}
```

### 2. Cálculo de Síntomas Físicos y Preferencias

#### **Cálculo de Síntomas Físicos desde Emociones**

```javascript
// Los síntomas físicos se pueden inferir desde las emociones registradas
function calculatePhysicalSymptoms(emotionalHistory) {
  const recentEmotions = emotionalHistory.filter(e => 
    new Date() - new Date(e.timestamp) <= 7 * 24 * 60 * 60 * 1000
  );
  
  const symptomMapping = {
    // Estrés y ansiedad → síntomas físicos
    'FEEL001': ['tension_muscular', 'palpitaciones'], // Ansiosa
    'FEEL002': ['fatiga', 'dolores_cabeza'], // Abrumada
    'FEEL003': ['tension_muscular', 'problemas_sueño'], // Nerviosa
    'FEEL005': ['tension_muscular', 'rigidez'], // Tensa
    'FEEL006': ['tension_muscular', 'irritabilidad_fisica'], // Frustrada
    'FEEL008': ['fatiga', 'tension_muscular', 'problemas_sueño'], // Estresada
    
    // Ánimo bajo → síntomas físicos
    'FEEL011': ['fatiga', 'cambios_apetito'], // Triste
    'FEEL014': ['fatiga', 'letargia'], // Desmotivada
    'FEEL020': ['fatiga', 'problemas_sueño'], // Desesperanzada
    
    // Físico y energía → síntomas directos
    'FEEL021': ['fatiga'], // Cansada físicamente
    'FEEL023': ['letargia', 'fatiga'], // Letárgica
    'FEEL024': ['hinchazon', 'molestias'], // Inflamada
    'FEEL025': ['dolores_corporales'], // Dolorida
    'FEEL027': ['cambios_apetito'], // Con hambre excesiva
  };
  
  const symptomCounts = {};
  
  recentEmotions.forEach(emotion => {
    const symptoms = symptomMapping[emotion.emotionId] || [];
    symptoms.forEach(symptom => {
      if (!symptomCounts[symptom]) {
        symptomCounts[symptom] = { total: 0, count: 0, dates: [] };
      }
      symptomCounts[symptom].total += emotion.intensity;
      symptomCounts[symptom].count += 1;
      symptomCounts[symptom].dates.push(emotion.timestamp);
    });
  });
  
  // Convertir a formato de síntomas físicos
  return Object.entries(symptomCounts).map(([symptom, data]) => ({
    symptom,
    intensity: Math.round(data.total / data.count), // Intensidad promedio
    date: data.dates[data.dates.length - 1], // Fecha más reciente
    frequency: data.count // Frecuencia en los últimos 7 días
  }));
}
```

#### **Cálculo de Preferencias de Contenido**

```javascript
// Las preferencias se aprenden del comportamiento del usuario
async function calculateContentPreferences(userId) {
  // 1. Obtener historial de interacciones con contenido
  const interactions = await ContentInteraction.find({ 
    userId,
    createdAt: { $gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) } // últimos 30 días
  });
  
  // 2. Analizar patrones de consumo
  const lengthPreferences = analyzeLengthPreferences(interactions);
  const tonePreferences = analyzeTonePreferences(interactions);
  const topicAvoidance = analyzeTopicAvoidance(interactions);
  
  return {
    preferredLength: lengthPreferences.dominant,
    preferredTone: tonePreferences.dominant,
    avoidTopics: topicAvoidance,
    lastUpdated: new Date()
  };
}

function analyzeLengthPreferences(interactions) {
  const lengthStats = {
    short: { views: 0, completionRate: 0, totalTime: 0 },
    medium: { views: 0, completionRate: 0, totalTime: 0 },
    long: { views: 0, completionRate: 0, totalTime: 0 }
  };
  
  interactions.forEach(interaction => {
    const length = getContentLength(interaction.contentType);
    lengthStats[length].views++;
    lengthStats[length].completionRate += interaction.completionPercentage || 0;
    lengthStats[length].totalTime += interaction.timeSpent || 0;
  });
  
  // Calcular score por longitud (completion rate * engagement time)
  const scores = {};
  Object.keys(lengthStats).forEach(length => {
    const stats = lengthStats[length];
    if (stats.views > 0) {
      const avgCompletion = stats.completionRate / stats.views;
      const avgTime = stats.totalTime / stats.views;
      scores[length] = (avgCompletion / 100) * (avgTime / 60); // Score basado en completion y tiempo
    } else {
      scores[length] = 0;
    }
  });
  
  const dominant = Object.keys(scores).reduce((a, b) => scores[a] > scores[b] ? a : b);
  
  return {
    dominant,
    scores,
    stats: lengthStats
  };
}

function analyzeTonePreferences(interactions) {
  const toneStats = {
    empathetic: { positive: 0, negative: 0, neutral: 0 },
    motivational: { positive: 0, negative: 0, neutral: 0 },
    educational: { positive: 0, negative: 0, neutral: 0 }
  };
  
  interactions.forEach(interaction => {
    const tone = getContentTone(interaction.contentType, interaction.segmentId);
    const feedback = categorizeFeedback(interaction.rating, interaction.timeSpent, interaction.completionPercentage);
    
    toneStats[tone][feedback]++;
  });
  
  // Calcular score por tono
  const scores = {};
  Object.keys(toneStats).forEach(tone => {
    const stats = toneStats[tone];
    const total = stats.positive + stats.negative + stats.neutral;
    if (total > 0) {
      scores[tone] = (stats.positive * 2 + stats.neutral * 1 - stats.negative * 1) / total;
    } else {
      scores[tone] = 0;
    }
  });
  
  const dominant = Object.keys(scores).reduce((a, b) => scores[a] > scores[b] ? a : b);
  
  return {
    dominant,
    scores,
    stats: toneStats
  };
}

function analyzeTopicAvoidance(interactions) {
  const avoidTopics = [];
  const topicStats = {};
  
  interactions.forEach(interaction => {
    const topics = getContentTopics(interaction.contentType, interaction.focusAreas);
    topics.forEach(topic => {
      if (!topicStats[topic]) {
        topicStats[topic] = { negative: 0, positive: 0, total: 0 };
      }
      topicStats[topic].total++;
      
      const feedback = categorizeFeedback(interaction.rating, interaction.timeSpent, interaction.completionPercentage);
      if (feedback === 'negative') {
        topicStats[topic].negative++;
      } else if (feedback === 'positive') {
        topicStats[topic].positive++;
      }
    });
  });
  
  // Identificar temas con alta tasa de feedback negativo
  Object.entries(topicStats).forEach(([topic, stats]) => {
    const negativeRate = stats.negative / stats.total;
    if (negativeRate >= 0.6 && stats.total >= 3) { // 60% negativo con al menos 3 interacciones
      avoidTopics.push(topic);
    }
  });
  
  return avoidTopics;
}

// Funciones auxiliares
function getContentLength(contentType) {
  const lengthMap = {
    'lesson_3min': 'medium',
    'whats_happening': 'short',
    'nutrition_guide': 'medium',
    'cycle_day_info': 'short',
    'hormone_levels': 'long',
    'stress_levels': 'medium'
  };
  return lengthMap[contentType] || 'medium';
}

function categorizeFeedback(rating, timeSpent, completionPercentage) {
  // Combinar múltiples indicadores para determinar si el feedback fue positivo/negativo
  let score = 0;
  
  if (rating) {
    score += (rating - 3) * 0.4; // Rating de 1-5, neutral en 3
  }
  
  if (completionPercentage) {
    if (completionPercentage >= 80) score += 0.3;
    else if (completionPercentage <= 20) score -= 0.3;
  }
  
  if (timeSpent) {
    // Tiempo adecuado vs muy poco/mucho tiempo
    const expectedTime = getExpectedReadTime(contentType);
    const timeRatio = timeSpent / expectedTime;
    if (timeRatio >= 0.7 && timeRatio <= 1.5) score += 0.2;
    else if (timeRatio < 0.3) score -= 0.2;
  }
  
  if (score > 0.2) return 'positive';
  if (score < -0.2) return 'negative';
  return 'neutral';
}
```

#### **Esquema de Base de Datos para Tracking**

```javascript
// models/ContentInteraction.js
const contentInteractionSchema = {
  userId: String,
  contentId: String,
  contentType: String, // lesson_3min, whats_happening, etc.
  segmentId: String,
  focusAreas: [String],
  
  // Métricas de engagement
  timeSpent: Number, // segundos
  completionPercentage: Number, // 0-100
  rating: Number, // 1-5 si el usuario califica
  
  // Acciones del usuario
  shared: Boolean,
  bookmarked: Boolean,
  skipped: Boolean,
  
  // Contexto
  deviceType: String,
  timeOfDay: String,
  
  createdAt: Date,
  updatedAt: Date
};

// models/UserPreferences.js
const userPreferencesSchema = {
  userId: String,
  
  // Preferencias calculadas
  preferredLength: String, // short, medium, long
  preferredTone: String, // empathetic, motivational, educational
  avoidTopics: [String],
  
  // Métricas de aprendizaje
  totalInteractions: Number,
  learningConfidence: Number, // 0-1, qué tan confiables son las preferencias
  
  lastCalculated: Date,
  createdAt: Date,
  updatedAt: Date
};
```

### 3. Algoritmo de Cálculo de Segmentación

#### **Paso 1: Determinar Fase del Ciclo**

```javascript
function calculateCyclePhase(lastPeriodDate, averageCycleLength) {
  const today = new Date();
  const lastPeriod = new Date(lastPeriodDate);
  const daysSinceLastPeriod = Math.floor((today - lastPeriod) / (1000 * 60 * 60 * 24));
  const currentDay = (daysSinceLastPeriod % averageCycleLength) + 1;
  
  // Lógica de fases basada en ciclo de 28 días (ajustable)
  if (currentDay >= 1 && currentDay <= 5) {
    return { phase: "menstrual", subPhase: currentDay <= 3 ? "flow" : "recovery", day: currentDay };
  } else if (currentDay >= 6 && currentDay <= 13) {
    return { phase: "folicular", subPhase: getFollicularSubPhase(currentDay), day: currentDay };
  } else if (currentDay >= 14 && currentDay <= 16) {
    return { phase: "ovulatory", subPhase: "peak", day: currentDay };
  } else {
    return { phase: "luteal", subPhase: getLutealSubPhase(currentDay, averageCycleLength), day: currentDay };
  }
}
```

#### **Paso 2: Análizar Estado Emocional Dominante**

```javascript
function analyzeEmotionalState(emotionalHistory) {
  const recent = emotionalHistory.filter(e => 
    new Date() - new Date(e.timestamp) <= 7 * 24 * 60 * 60 * 1000 // últimos 7 días
  );
  
  // Calcular emociones dominantes por categoría
  const emotionsByCategory = groupEmotionsByCategory(recent);
  
  // Determinar emoción primaria y secundaria
  const primary = findDominantEmotion(emotionsByCategory);
  const secondary = findSecondaryEmotion(emotionsByCategory, primary);
  
  // Calcular intensidad promedio
  const averageIntensity = calculateAverageIntensity(recent);
  
  return {
    primary: primary,
    secondary: secondary,
    intensity: averageIntensity,
    volatility: calculateEmotionalVolatility(recent),
    trend: calculateEmotionalTrend(recent)
  };
}
```

#### **Paso 3: Calcular Intensidad de Síntomas**

```javascript
function calculateSymptomIntensity(physicalSymptoms, emotionalState) {
  const recentSymptoms = physicalSymptoms.filter(s => 
    new Date() - new Date(s.date) <= 3 * 24 * 60 * 60 * 1000 // últimos 3 días
  );
  
  const physicalScore = recentSymptoms.reduce((sum, s) => sum + s.intensity, 0);
  const emotionalScore = Math.abs(emotionalState.intensity) * 2;
  
  const totalScore = physicalScore + emotionalScore;
  
  if (totalScore >= 8) return "very_high";
  if (totalScore >= 6) return "high"; 
  if (totalScore >= 4) return "moderate";
  if (totalScore >= 2) return "low";
  return "very_low";
}
```

#### **Paso 4: Generar ID de Segmento**

```javascript
function generateSegmentId(cyclePhase, emotionalState, demographics, intensity) {
  // Formato: SEG_[FASE]_[EDAD]_[EMOCION_PRIMARIA]_[INTENSIDAD]
  const phaseAbbr = {
    "folicular": "FOL",
    "ovulatory": "OVU", 
    "luteal": "LUT",
    "menstrual": "MEN"
  }[cyclePhase.phase];
  
  const ageAbbr = demographics.ageGroup.replace("-", "_");
  const emotionAbbr = emotionalState.primary.toUpperCase();
  const intensityAbbr = intensity.toUpperCase();
  
  return `SEG_${phaseAbbr}_${ageAbbr}_${emotionAbbr}_${intensityAbbr}`;
}
```

### 3. Implementación del Endpoint de Segmentación

```javascript
// routes/segmentation.js
const express = require('express');
const router = express.Router();

router.post('/calculate-segment', async (req, res) => {
  try {
    const { userId } = req.body;
    
    // 1. Obtener datos básicos del usuario
    const userData = await getUserSegmentationData(userId);
    
    // 2. Calcular síntomas físicos desde emociones
    const physicalSymptoms = calculatePhysicalSymptoms(userData.currentEmotions);
    
    // 3. Obtener/calcular preferencias de contenido
    let contentPreferences = await getUserContentPreferences(userId);
    if (!contentPreferences || shouldRecalculatePreferences(contentPreferences)) {
      contentPreferences = await calculateContentPreferences(userId);
      await saveUserContentPreferences(userId, contentPreferences);
    }
    
    // 4. Combinar todos los datos
    const completeUserData = {
      ...userData,
      physicalSymptoms,
      contentPreferences
    };
    
    // 2. Calcular fase del ciclo
    const cyclePhase = calculateCyclePhase(
      userData.cycle.lastPeriodDate, 
      userData.cycle.averageCycleLength
    );
    
    // 3. Analizar estado emocional
    const emotionalState = analyzeEmotionalState(userData.currentEmotions);
    
    // 4. Calcular intensidad de síntomas
    const symptomIntensity = calculateSymptomIntensity(
      userData.physicalSymptoms, 
      emotionalState
    );
    
    // 5. Generar segmento
    const segmentId = generateSegmentId(
      cyclePhase, 
      emotionalState, 
      userData.demographics, 
      symptomIntensity
    );
    
    // 6. Obtener metadata del segmento
    const segmentMetadata = await getSegmentMetadata(segmentId);
    
    // 7. Personalizar contenido disponible
    const availableContent = await getPersonalizedContent(
      segmentId, 
      userData.contentPreferences
    );
    
    const result = {
      segmentId,
      cycleInfo: {
        phase: cyclePhase.phase,
        subPhase: cyclePhase.subPhase,
        day: cyclePhase.day,
        daysUntilNext: calculateDaysUntilNextPhase(cyclePhase, userData.cycle)
      },
      emotionalProfile: {
        primary: emotionalState.primary,
        secondary: emotionalState.secondary,
        intensity: emotionalState.intensity,
        trend: emotionalState.trend
      },
      symptomLevel: symptomIntensity,
      recommendedContent: availableContent,
      segmentMetadata
    };
    
    // 8. Guardar historial de segmentación
    await saveSegmentationHistory(userId, result);
    
    res.json({ success: true, data: result });
    
  } catch (error) {
    console.error('Error calculating segment:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});
// Funciones auxiliares para manejo de preferencias
async function getUserContentPreferences(userId) {
  return await UserPreferences.findOne({ userId });
}

async function saveUserContentPreferences(userId, preferences) {
  return await UserPreferences.findOneAndUpdate(
    { userId },
    { 
      ...preferences,
      totalInteractions: await getTotalInteractions(userId),
      learningConfidence: calculateLearningConfidence(preferences),
      lastCalculated: new Date()
    },
    { upsert: true, new: true }
  );
}

function shouldRecalculatePreferences(preferences) {
  const daysSinceLastUpdate = (new Date() - preferences.lastCalculated) / (1000 * 60 * 60 * 24);
  return daysSinceLastUpdate >= 7 || preferences.learningConfidence < 0.5;
}

async function getTotalInteractions(userId) {
  return await ContentInteraction.countDocuments({ userId });
}

function calculateLearningConfidence(preferences) {
  // La confianza aumenta con el número de interacciones y la consistencia de patrones
  const interactionCount = preferences.totalInteractions || 0;
  const baseConfidence = Math.min(interactionCount / 20, 1); // 20 interacciones = confianza máxima
  return Math.round(baseConfidence * 100) / 100;
}

function getExpectedReadTime(contentType) {
  const readingTimes = {
    'lesson_3min': 180, // 3 minutos
    'whats_happening': 30, // 30 segundos
    'nutrition_guide': 120, // 2 minutos
    'cycle_day_info': 45, // 45 segundos
    'hormone_levels': 150, // 2.5 minutos
    'stress_levels': 90 // 1.5 minutos
  };
  return readingTimes[contentType] || 120;
}
```

### 4. Funciones de Utilidad Necesarias

```javascript
// utils/emotionMapping.js
const EMOTION_MAPPING = {
  'FEEL001': { name: 'ansiosa', category: 'stress_anxiety', score: -2 },
  'FEEL002': { name: 'abrumada', category: 'stress_anxiety', score: -2 },
  'FEEL003': { name: 'nerviosa', category: 'stress_anxiety', score: -1 },
  // ... mapeo completo desde emotions.js
};

function groupEmotionsByCategory(emotions) {
  return emotions.reduce((groups, emotion) => {
    const mapping = EMOTION_MAPPING[emotion.emotionId];
    if (!groups[mapping.category]) groups[mapping.category] = [];
    groups[mapping.category].push({ ...emotion, ...mapping });
    return groups;
  }, {});
}

function findDominantEmotion(emotionsByCategory) {
  let maxScore = -Infinity;
  let dominantEmotion = null;
  
  Object.values(emotionsByCategory).flat().forEach(emotion => {
    const weightedScore = Math.abs(emotion.score) * emotion.intensity;
    if (weightedScore > maxScore) {
      maxScore = weightedScore;
      dominantEmotion = emotion.name;
    }
  });
  
  return dominantEmotion;
}
```

### 5. Base de Datos y Modelos

```javascript
// models/UserSegmentation.js
const userSegmentationSchema = {
  userId: String,
  segmentId: String,
  calculatedAt: Date,
  cycleDay: Number,
  phase: String,
  subPhase: String,
  primaryEmotion: String,
  secondaryEmotion: String,
  intensityLevel: String,
  metadata: Object,
  contentRecommendations: Array
};

// models/SegmentContent.js
const segmentContentSchema = {
  segmentId: String,
  contentType: String, // lesson_3min, whats_happening, nutrition_guide, etc.
  priority: Number,
  content: String,
  generatedAt: Date,
  focusAreas: Array,
  tone: String
};
```

### 6. Integración con el Sistema de Contenidos

```javascript
// services/contentService.js
async function getPersonalizedContent(segmentId, preferences) {
  // 1. Buscar contenido exacto del segmento
  let content = await SegmentContent.find({ segmentId });
  
  // 2. Si no hay contenido exacto, buscar segmentos similares
  if (content.length === 0) {
    const similarSegments = await findSimilarSegments(segmentId);
    content = await SegmentContent.find({ 
      segmentId: { $in: similarSegments } 
    });
  }
  
  // 3. Filtrar por preferencias del usuario
  content = filterContentByPreferences(content, preferences);
  
  // 4. Ordenar por prioridad
  content.sort((a, b) => b.priority - a.priority);
  
  return {
    lesson_3min: content.find(c => c.contentType === 'lesson_3min'),
    whats_happening: content.find(c => c.contentType === 'whats_happening'),
    nutrition_guide: content.find(c => c.contentType === 'nutrition_guide'),
    cycle_day_info: content.find(c => c.contentType === 'cycle_day_info'),
    hormone_levels: content.find(c => c.contentType === 'hormone_levels'),
    stress_levels: content.find(c => c.contentType === 'stress_levels')
  };
}
```

## Tareas para Cursor IDE/Cursor-Agent

### **Implementación Prioritaria:**

1. **Crear el sistema de mapeo de emociones** basado en `docs/emotions.js`
2. **Implementar las funciones de cálculo de fase del ciclo** con lógica médicamente precisa
3. **Desarrollar el algoritmo de análisis emocional** que procese el historial de la usuaria
4. **Crear el endpoint `/calculate-segment`** con toda la lógica de segmentación
5. **Implementar los modelos de base de datos** para almacenar segmentaciones y contenidos
6. **Desarrollar el servicio de contenido personalizado** que conecte segmentos con contenido generado

### **Consideraciones Técnicas:**

- **Performance**: Cache de segmentos calculados (válidos por 24h)
- **Fallback**: Sistema de segmentos similares cuando no hay match exacto
- **Personalización**: Aprendizaje de preferencias basado en interacciones
- **Privacidad**: Encriptación de datos sensibles del ciclo menstrual
- **Escalabilidad**: Queue system para cálculos complejos de segmentación

### **Testing Necesario:**

- Unit tests para cada función de cálculo
- Integration tests para el endpoint completo
- Tests de edge cases (ciclos irregulares, datos incompletos)
- Performance tests con volúmenes altos de usuarios

¿Te gustaría que Cursor implemente alguna parte específica de este sistema primero?