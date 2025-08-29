## Plan de Implementación Completo

### Resumen Ejecutivo

Desarrollaremos un sistema RAG (Retrieval-Augmented Generation) para proporcionar contenido educativo personalizado sobre salud femenina y cuidado hormonal. El sistema utilizará herramientas open source y de bajo costo para segmentar usuarias según su fase menstrual, edad y estado emocional, generando respuestas contextualizadas basadas en una base de conocimientos especializada.

---

## 1. Arquitectura General del Sistema

### 1.1 Componentes Principales

El sistema estará compuesto por cinco componentes fundamentales que trabajarán de manera integrada:

**Frontend (React Native App)**

- Interfaz de usuario para el tracker menstrual
- Sistema de registro de emociones diarias (50 tipos)
- Input para preguntas sobre el ciclo menstrual
- Visualización de contenido personalizado

**Backend API (Node.js + Express)**

- Manejo de autenticación y perfiles de usuario
- Lógica de negocio para cálculo de fases menstruales
- API endpoints para comunicación con el sistema RAG
- Procesamiento de datos de ciclos y emociones

**Sistema RAG (Chroma + Embeddings)**

- Base de datos vectorial con contenido segmentado
- Motor de búsqueda semántica
- Sistema de filtrado por metadata (fase, edad, emociones)

**Procesador de Documentos**

- Pipeline para procesar PDFs y documentos médicos
- Generación de embeddings y metadata
- Segmentación y categorización automática de contenido

**LLM Local (Ollama + Mistral)**

- Generación de respuestas personalizadas
- Procesamiento de queries de usuarias
- Síntesis de información de múltiples fuentes

### 1.2 Flujo de Datos Completo

El flujo de información sigue un patrón específico que garantiza respuestas precisas y contextualizadas. Cuando una usuaria registra sus datos diarios (emociones, síntomas, fechas), el sistema actualiza su perfil y recalcula su segmento actual. Al hacer una pregunta, el sistema busca en la base de conocimientos contenido relevante para su segmento específico y genera una respuesta personalizada que considera toda su información contextual.

---

## 2. Definición del Sistema de Segmentación

### 2.1 Sistema de Segmentación Basado en Scores Emocionales

**Fases del Ciclo Menstrual (4 categorías principales)**

- Menstrual (días 1-5): Sangrado, niveles hormonales bajos, introspección natural
- Folicular (días 6-13): Aumento gradual de estrógeno, renovación de energía
- Ovulatoria (días 14-16): Pico de estrógeno y LH, máxima vitalidad y conexión
- Lútea (días 17-28): Progesterona dominante, sensibilidad aumentada

**Categorías Emocionales con Sistema de Scoring (-2 a +2)**

Cada usuaria tiene un score promedio en cinco dimensiones emocionales clave que determinan su segmento específico. Los thresholds definen cuándo una emoción domina lo suficiente para influir en el contenido personalizado:

- **Ansiedad/Estrés**: Desde calma profunda (+2) hasta ansiedad severa (-2)
- **Ánimo General**: Desde euforia y optimismo (+2) hasta depresión/tristeza (-2)
- **Energía Física**: Desde vitalidad alta (+2) hasta fatiga extrema (-2)
- **Autoestima**: Desde confianza sólida (+2) hasta inseguridad profunda (-2)
- **Dimensión Relacional**: Desde conexión social fuerte (+2) hasta aislamiento (-2)

**Segmentos Específicos Identificados (20 combinaciones clave)**

Los segmentos representan las intersecciones más significativas entre fases del ciclo y estados emocionales dominantes. Cada segmento tiene características hormonales y psicológicas específicas que requieren contenido educativo diferenciado.

Fase Folicular (renovación y crecimiento):

- Folicular Estresada: Estrógeno creciente pero cortisol alto interfiere con beneficios
- Folicular Triste: Dificultad para aprovechar la energía renovadora natural
- Folicular Energética: Alineación óptima con el aumento hormonal natural
- Folicular Insegura: Dudas que obstaculizan el potencial de crecimiento
- Folicular Aislada: Dificultad para conectar durante fase naturalmente expansiva

Fase Ovulatoria (pico de vitalidad):

- Ovulatoria Estresada: Estrés que bloquea la confianza natural del pico hormonal
- Ovulatoria Melancólica: Tristeza inusual durante el momento de mayor vitalidad
- Ovulatoria Energética: Aprovechamiento máximo del pico estrogénico
- Ovulatoria Insegura: Inseguridad que limita la expresión natural de confianza
- Ovulatoria Conectada: Optimización de la tendencia natural hacia la sociabilidad

Fase Lútea (sensibilidad y preparación):

- Lútea Ansiosa: Progesterona alta amplifica tendencias ansiosas
- Lútea Decaída: Caída hormonal genera estado depresivo pronunciado
- Lútea Activa: Mantenimiento de energía pese a cambios hormonales
- Lútea Sensible: Vulnerabilidad emocional acentuada por fluctuaciones
- Lútea Solitaria: Necesidad de retiro amplificada por progesterona

Fase Menstrual (renovación y limpieza):

- Menstrual Irritable: Inflamación y molestias generan irritabilidad
- Menstrual Melancólica: Reflexión natural se vuelve tristeza prolongada
- Menstrual Resiliente: Capacidad de mantener fuerza durante el proceso
- Menstrual Vulnerable: Sensibilidad extrema durante la renovación
- Menstrual Replegada: Necesidad natural de introspección y descanso

### 2.2 Lógica de Segmentación

El algoritmo de segmentación analiza los últimos 7 días de registro emocional para identificar patrones dominantes. Si una usuaria reporta principalmente emociones de estrés durante su fase lútea, será clasificada como "Lútea Estresada". Esta segmentación se actualiza dinámicamente cada día basándose en nuevos registros.

**Ejemplo de Segmentos Resultantes:**

- "Menstrual Tranquila Joven": Usuaria de 25 años en menstruación con emociones predominantemente tranquilas
- "Ovulación Energética Adulta": Usuaria de 35 años ovulando con alto nivel de energía
- "Lútea Estresada Adolescente": Usuaria de 17 años en fase lútea con estrés predominante

---

## 3. Stack Tecnológico Detallado

### 3.1 Selección de Herramientas

**Chroma como Base de Datos Vectorial** Chroma es nuestra elección principal porque está diseñada específicamente para aplicaciones RAG como la nuestra. A diferencia de bases de datos tradicionales, Chroma entiende el significado semántico del contenido, no solo palabras clave. Esto significa que puede encontrar información relevante incluso cuando las usuarias hacen preguntas con vocabulario diferente al de los documentos médicos originales.

**Sentence-Transformers para Embeddings** Utilizaremos el modelo "all-MiniLM-L6-v2" que convierte texto en vectores de 384 dimensiones. Este modelo ha sido entrenado específicamente para entender similitudes semánticas en español e inglés, lo cual es perfecto para contenido médico bilingüe.

**Ollama + Mistral 7B para Generación** Mistral 7B ejecutándose localmente a través de Ollama nos proporciona respuestas de alta calidad sin costos por token. El modelo entiende contexto médico y puede mantener un tono empático apropiado para temas de salud femenina.

### 3.2 Infraestructura Requerida

**Servidor Principal (VPS)**

- 8GB RAM (mínimo), 16GB recomendado
- 4 CPU cores
- 100GB SSD storage
- Ubuntu 22.04 LTS
- Costo estimado: $40-60/mes

**Distribución de Recursos:**

- Chroma: 2GB RAM
- Ollama + Mistral: 6GB RAM
- Backend API: 1GB RAM
- Sistema operativo y overhead: 1GB RAM

---

## 4. Implementación Paso a Paso

### Fase 1: Preparación de la Infraestructura (Semanas 1-2)

**Semana 1: Configuración del Servidor**

El primer paso es establecer nuestro entorno de desarrollo. Configuraremos un servidor Ubuntu limpio con todas las dependencias necesarias. Esto incluye Docker para containerización, Node.js para nuestro backend, Python para el procesamiento de documentos, y las herramientas específicas para nuestro stack RAG.

Comenzaremos instalando Docker porque nos permitirá gestionar nuestros servicios de manera aislada y reproducible. Luego configuraremos Chroma en un contenedor Docker, lo cual simplifica significativamente el despliegue y mantenimiento.

**Comandos de Configuración Inicial:**

```bash
# Instalación de dependencias base
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io docker-compose nodejs npm python3 python3-pip -y

# Configuración de Chroma
docker run -d --name chroma-server -p 8000:8000 chromadb/chroma

# Verificación de servicios
docker ps
curl http://localhost:8000/api/v1/heartbeat
```

**Semana 2: Instalación y Configuración de Ollama**

Ollama nos permitirá ejecutar Mistral 7B localmente. La instalación es directa, pero la descarga del modelo puede tomar tiempo considerable debido al tamaño (aproximadamente 4GB). Una vez instalado, configuraremos el modelo para responder específicamente a consultas de salud femenina.

```bash
# Instalación de Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Descarga del modelo Mistral
ollama pull mistral

# Configuración personalizada para salud femenina
ollama create salud-femenina -f ./modelfile-salud-femenina
```

### Fase 2: Procesamiento de Documentos (Semanas 3-4)

**Semana 3: Pipeline de Procesamiento**

El procesamiento de documentos es crucial para el éxito de nuestro sistema. Necesitamos convertir PDFs médicos en chunks de texto manejables, cada uno con metadata rica que permita filtrado preciso. El proceso involucra extracción de texto, limpieza, segmentación inteligente y generación de embeddings.

Desarrollaremos un sistema que identifique automáticamente el contenido relevante para cada segmento. Por ejemplo, un párrafo sobre "nutrición durante la menstruación" será etiquetado con metadata apropiada para la fase menstrual.

**Script de Procesamiento de Documentos:**

```python
import PyPDF2
from sentence_transformers import SentenceTransformer
import chromadb
import re
from typing import List, Dict

class DocumentProcessor:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chroma_client = chromadb.HttpClient(host='localhost', port=8000)
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        # Extrae texto completo del PDF
        # Limpia caracteres especiales y normaliza formato
        pass
    
    def create_intelligent_chunks(self, text: str) -> List[Dict]:
        # Divide el texto en chunks semánticamente coherentes
        # Identifica temas y asigna metadata automáticamente
        pass
    
    def generate_metadata(self, chunk: str) -> Dict:
        # Analiza el contenido para asignar metadata
        # Identifica fase del ciclo, grupo de edad, emociones relevantes
        pass
```

**Semana 4: Creación de la Base de Conocimientos**

Procesaremos todos los documentos médicos y los organizaremos en nuestra base de datos vectorial. Este proceso incluye validación de calidad, eliminación de duplicados, y verificación de que cada chunk tenga metadata completa y precisa.

Crearemos diferentes colecciones en Chroma para diferentes tipos de contenido: información educativa básica, consejos prácticos, alertas médicas, y contenido específico por condiciones especiales.

### Fase 3: Desarrollo del Backend (Semanas 5-6)

**Semana 5: API Core y Lógica de Negocio**

Desarrollaremos la API que conecta nuestra app React Native con el sistema RAG. Esta API manejará la autenticación de usuarios, el cálculo de fases menstruales, la segmentación automática, y la orquestación de queries al sistema RAG.

La lógica de cálculo de fases es particularmente importante. Utilizaremos algoritmos que consideren no solo las fechas reportadas, sino también patrones históricos y variaciones individuales. El sistema aprenderá de cada usuaria para mejorar la precisión de las predicciones.

**Estructura de la API:**

```javascript
// Endpoint principal para queries de usuarias
app.post('/api/ask-question', async (req, res) => {
    const { userId, question } = req.body;
    
    // 1. Obtener perfil actualizado de la usuaria
    const userProfile = await getUserProfile(userId);
    
    // 2. Calcular segmento actual
    const currentSegment = calculateUserSegment(userProfile);
    
    // 3. Buscar contenido relevante en Chroma
    const relevantContent = await queryChromaWithContext(question, currentSegment);
    
    // 4. Generar respuesta personalizada con Mistral
    const personalizedAnswer = await generateAnswerWithMistral(
        question, 
        relevantContent, 
        currentSegment
    );
    
    // 5. Registrar interacción para mejora continua
    await logUserInteraction(userId, question, personalizedAnswer);
    
    res.json({ answer: personalizedAnswer, sources: relevantContent });
});
```

**Semana 6: Sistema de Segmentación Avanzado**

Implementaremos la lógica completa de segmentación que considera patrones temporales, no solo estados actuales. El sistema identificará tendencias emocionales, patrones estacionales, y correlaciones entre síntomas físicos y estados emocionales.

### Fase 4: Integración y Optimización (Semanas 7-8)

**Semana 7: Integración con React Native**

Conectaremos nuestra app móvil con el backend RAG. Esto incluye manejo de estados offline, caché inteligente de respuestas, y sincronización de datos cuando hay conectividad limitada.

Implementaremos un sistema de feedback que permita a las usuarias calificar la utilidad de las respuestas, lo cual nos ayudará a mejorar continuamente la precisión del sistema.

**Semana 8: Testing y Optimización**

Realizaremos pruebas exhaustivas con datos reales (anonimizados) y optimizaremos el rendimiento. Esto incluye ajuste de parámetros de búsqueda, optimización de prompts para Mistral, y fine-tuning de la lógica de segmentación.

---

## 5. Estructura de Datos y Metadata

### 5.1 Esquema de Metadata para Contenido

Cada chunk de contenido en nuestra base de datos vectorial tendrá metadata estructurada que permita filtrado preciso:

```json
{
  "chunk_id": "uuid-único",
  "content": "texto-del-contenido",
  "metadata": {
    "fase_ciclo": ["menstrual", "follicular", "ovulation", "luteal"],
    "grupo_edad": ["15-19", "20-29", "30-39", "40+"],
    "emociones_relevantes": ["energetico", "estresado", "melancolico", "irritable", "tranquilo", "social", "fisico", "cognitivo"],
    "nivel_hormonal": ["bajo", "medio", "alto"],
    "tema_principal": ["nutricion", "ejercicio", "sintomas", "fertilidad", "bienestar"],
    "tipo_contenido": ["educativo", "consejo", "alerta", "explicacion"],
    "nivel_detalle": ["basico", "intermedio", "avanzado"],
    "fuente": "nombre-del-documento-original",
    "confiabilidad": 0.95,
    "fecha_ultima_revision": "2024-01-15"
  }
}
```

### 5.2 Perfil de Usuario

```json
{
  "user_id": "uuid-único",
  "perfil_base": {
    "edad": 25,
    "fecha_registro": "2024-01-01",
    "ciclo_promedio": 28,
    "historial_ciclos": [
      {
        "fecha_inicio": "2024-01-15",
        "duracion": 28,
        "sintomas_reportados": ["cramps", "mood_swings"],
        "emociones_dominantes": ["irritable", "fisico"]
      }
    ]
  },
  "segmento_actual": {
    "fase": "luteal",
    "grupo_edad": "20-29",
    "emociones_dominantes": ["estresado", "fisico"],
    "fecha_calculo": "2024-01-20",
    "confianza": 0.87
  },
  "patrones_identificados": {
    "emociones_por_fase": {
      "menstrual": ["fisico", "tranquilo"],
      "follicular": ["energetico", "social"],
      "ovulation": ["energetico", "social"],
      "luteal": ["irritable", "estresado"]
    },
    "sintomas_recurrentes": ["headaches", "bloating", "mood_swings"],
    "triggers_identificados": ["stress_laboral", "cambios_alimentarios"]
  }
}
```

---

## 11. Sistema de Generación de Contenido Personalizado

### 11.1 Arquitectura de Contenido Multinivel

El sistema de contenido que implementaremos funciona como una biblioteca inteligente que organiza la información en múltiples capas de especificidad. La base de conocimientos única alimenta cinco tipos diferentes de contenido, cada uno optimizado para un contexto de uso específico en la aplicación.

Esta aproximación multinivel nos permite maximizar el valor de nuestros documentos médicos mientras mantenemos costos controlados. En lugar de generar contenido completamente nuevo para cada situación, extraemos y recombinan información existente de manera inteligente, aplicando diferentes filtros y formatos según la necesidad específica de la usuaria.

### 11.2 Tipos de Contenido Generados

**Lecciones Personalizadas por Segmento (Lecturas de 3 minutos)**

Las lecciones representan contenido educativo profundo, diseñado para sesiones de lectura enfocada donde la usuaria busca comprender mejor su experiencia actual. Cada lección combina información científica con consejos prácticos, todo contextualizado para el segmento específico de la usuaria.

Para una usuaria "Lútea Ansiosa", por ejemplo, una lección podría explicar cómo la progesterona alta puede amplificar la respuesta al estrés, seguido de técnicas específicas de respiración que funcionan mejor durante esta fase, y recomendaciones nutricionales que ayudan a modular el cortisol cuando los niveles de progesterona están elevados.

La estructura de cada lección sigue un patrón científicamente respaldado: contexto hormonal, explicación del fenómeno, estrategias de manejo, y un llamado a la acción específico. Esto asegura que la usuaria no solo entienda qué le está pasando, sino que salga de la lectura con herramientas concretas para mejorar su bienestar.

**Explicaciones Contextuales "Qué Pasa Dentro de Ti"**

Estas son explicaciones concisas y empáticas que ayudan a la usuaria entender la base fisiológica de su experiencia emocional actual. El objetivo es desmitificar las sensaciones y emociones, proporcionando validación científica para lo que está sintiendo.

Una usuaria "Ovulatoria Melancólica", por ejemplo, recibiría una explicación sobre cómo, aunque el estrógeno está en su pico, las fluctuaciones individuales en sensibilidad a neurotransmisores pueden crear experiencias emocionales variadas. Esto le ayuda a entender que su experiencia es válida y tiene bases fisiológicas, no es "anormal" sentirse triste durante la ovulación.

**Guías Nutricionales Específicas por Segmento**

La nutrición hormonal es altamente específica tanto a la fase del ciclo como al estado emocional dominante. Una usuaria "Folicular Energética" necesita nutrientes que sostengan y amplifiquen su energía natural, mientras que una "Folicular Estresada" necesita alimentos que apoyen la regulación del cortisol mientras aprovecha el aumento de estrógeno.

Estas guías van más allá de recomendaciones generales, proporcionando timing específico (qué comer cuándo durante la fase), combinaciones sinérgicas de nutrientes, y explicaciones de por qué ciertos alimentos son particularmente beneficiosos para su combinación específica de hormonas y estado emocional.

**Explicaciones de Mapas Hormonales Contextualizadas**

Los tres mapas hormonales (fase del ciclo, hormonas específicas, y niveles de estrés) requieren explicaciones que conecten los datos mostrados con la experiencia vivida de la usuaria. En lugar de explicaciones técnicas genéricas, proporcionamos interpretaciones personalizadas basadas en el segmento.

Para el mapa de fases del ciclo, una usuaria "Lútea Sensible" en el día 23 de un ciclo de 28 días recibiría una explicación sobre cómo la progesterona alcanza niveles altos en este punto, lo cual explica científicamente su mayor sensibilidad emocional, y qué puede esperar en los próximos días antes de la menstruación.

### 11.3 Algoritmo de Generación de Contenido Inteligente

**Pipeline de Procesamiento Contextual**

El algoritmo de generación funciona como un editor inteligente que toma contenido de la base de conocimientos y lo adapta específicamente para cada segmento. Este proceso involucra múltiples capas de personalización que van desde la selección de información relevante hasta el ajuste del tono y la estructura del mensaje.

```javascript
async function generatePersonalizedContent(contentType, userSegment, specificContext) {
    // Paso 1: Identificar contenido base relevante de la base de conocimientos
    const relevantKnowledge = await queryKnowledgeBase({
        phase: userSegment.phase,
        emotionalCategory: userSegment.dominantCategory,
        contentType: contentType,
        threshold: userSegment.threshold
    });
    
    // Paso 2: Aplicar filtros específicos del tipo de contenido
    const filteredContent = applyContentTypeFilters(relevantKnowledge, contentType);
    
    // Paso 3: Generar estructura personalizada
    const contentStructure = createContentStructure(contentType, userSegment);
    
    // Paso 4: Sintetizar contenido final con LLM contextual
    const personalizedContent = await synthesizeWithLLM(
        filteredContent, 
        contentStructure, 
        userSegment,
        specificContext
    );
    
    // Paso 5: Validar longitud y calidad
    return validateAndOptimizeContent(personalizedContent, contentType);
}
```

**Lógica de Priorización de Contenido**

El sistema prioriza información basándose en múltiples factores que incluyen la relevancia inmediata para el segmento, la urgencia basada en la fase del ciclo, y el historial de interacción de la usuaria. Esta priorización asegura que el contenido más valioso aparezca primero y que la información se presente en el orden más útil para la usuaria.

Una usuaria "Menstrual Irritable" en su segundo día de menstruación recibirá primero información sobre manejo del dolor y la irritabilidad, seguido de explicaciones hormonales, y finalmente estrategias de preparación para la siguiente fase folicular. Esta secuencia respeta tanto las necesidades inmediatas como el arco natural del ciclo menstrual.

### 11.4 Optimización de Mapas Hormonales con Explicaciones Segmentadas

**Mapa de Fase del Ciclo con Contexto Inteligente**

El mapa de fase del ciclo muestra visualmente el día actual, la duración del ciclo, y la fase, pero la explicación varía dramáticamente según el segmento de la usuaria. Una visualización idéntica puede requerir explicaciones completamente diferentes.

Para una usuaria "Folicular Energética" en el día 8, el sistema explicaría cómo el estrógeno creciente está creando las condiciones perfectas para su energía actual y sugeriría cómo aprovechar este momento óptimo. Para una "Folicular Estresada" en el mismo día, la explicación se enfocaría en cómo el estrógeno creciente puede estar siendo contrarrestado por el cortisol alto, y proporcionaría estrategias específicas para reducir el estrés y permitir que los beneficios del estrógeno se manifiesten.

**Visualización de Hormonas Específicas (E2, P4, LH, FSH)**

Los niveles hormonales estimados se presentan visualmente, pero la interpretación de estos niveles está completamente personalizada al segmento. El sistema explica no solo qué significan los niveles actuales, sino cómo estos niveles específicos interactúan con el estado emocional dominante de la usuaria.

Una usuaria "Ovulatoria Conectada" con LH en pico recibiría una explicación sobre cómo este pico hormonal está potenciando su capacidad natural para conectar socialmente y cómo aprovechar este momento para fortalecer relaciones. Una "Ovulatoria Insegura" con el mismo perfil hormonal recibiría información sobre cómo el pico de LH debería generar confianza, pero factores como el estrés o patrones de pensamiento negativos pueden estar interfiriendo con esta respuesta natural.

**Monitoreo de Estrés Contextualizado (Cortisol Estimado)**

Los niveles de cortisol estimados se interpretan siempre en el contexto de la fase menstrual y el segmento emocional. El mismo nivel de cortisol puede ser completamente normal para una fase y problemático para otra, y estas diferencias se explican claramente.

Para una usuaria "Lútea Ansiosa", niveles elevados de cortisol se explican como una combinación problemática donde la progesterona alta puede estar amplificando la respuesta al estrés, creando un ciclo que requiere intervención específica. Para una "Menstrual Resiliente" con cortisol moderadamente elevado, la explicación se enfocaría en cómo un ligero aumento del cortisol durante la menstruación puede ser adaptativo, ayudando al cuerpo a manejar el proceso de renovación.

### 11.5 Integración con la Arquitectura RAG Existente

**Extensión del Sistema de Metadata**

La arquitectura RAG que ya habíamos diseñado se extiende naturalmente para soportar estos nuevos tipos de contenido. Cada chunk de información en la base de datos vectorial ahora incluye metadata adicional que especifica para qué tipo de contenido es más apropiado.

```json
{
  "metadata": {
    "segment_ids": ["SEG011", "SEG014", "SEG015"],
    "content_types": ["lesson", "whats_happening", "nutrition", "chart_explanation"],
    "optimal_length": "3min_read",
    "urgency_level": "high",
    "emotional_context": "validation_needed",
    "scientific_depth": "moderate",
    "actionability": "high"
  }
}
```

**Prompts Especializados por Tipo de Contenido**

Cada tipo de contenido requiere prompts específicamente diseñados que aseguran la estructura, tono, y profundidad apropiados. El sistema selecciona automáticamente el prompt correcto basándose en el tipo de contenido solicitado y el segmento de la usuaria.

Para lecciones de 3 minutos, el prompt enfatiza estructura educativa, equilibrio entre ciencia y aplicación práctica, y un llamado a la acción claro. Para explicaciones de "qué pasa dentro de ti", el prompt prioriza validación emocional, explicación fisiológica accesible, y normalización de la experiencia.

**Caché Inteligente para Explicaciones de Mapas**

Las explicaciones de mapas hormonales se pueden cachear eficientemente porque, aunque son personalizadas por segmento, no cambian frecuentemente para combinaciones específicas de segmento y contexto hormonal. Esto reduce significativamente el costo computacional mientras mantiene la personalización.

El sistema mantiene un caché de explicaciones pregeneradas para las combinaciones más comunes de segmento y contexto hormonal, regenerando solo cuando aparecen patrones inusuales o cuando el feedback de las usuarias indica que una explicación necesita refinamiento.

### 11.6 Estrategia de Costos y Escalabilidad para Contenido Múltiple

**Optimización de Generación Batch**

En lugar de generar cada pieza de contenido individualmente cuando se solicita, el sistema puede pregenererar contenido para segmentos específicos durante horas de baja demanda. Esto reduce significativamente los costos de LLM mientras asegura respuestas instantáneas para las usuarias.

El sistema identifica patrones de uso y pregenera lecciones y explicaciones para los segmentos más comunes, manteniendo un inventario de contenido fresco que se actualiza continuamente basándose en nueva información en la base de conocimientos.

**Reutilización Inteligente de Contenido Base**

Muchas explicaciones científicas base son compartidas entre múltiples segmentos, lo que permite una reutilización significativa de contenido. El sistema identifica estos elementos comunes y los combina de manera diferente para cada segmento, reduciendo la necesidad de generar contenido completamente nuevo para cada situación.

Por ejemplo, la explicación básica de cómo funciona la progesterona es la misma para "Lútea Ansiosa" y "Lútea Sensible", pero la aplicación práctica y las recomendaciones específicas varían. Esta estructura modular permite eficiencia significativa en la generación de contenido.

### 6.1 Estrategia de Búsqueda Híbrida

Implementaremos un sistema de búsqueda que combine múltiples estrategias para maximizar la relevancia de los resultados:

**Búsqueda Semántica (70% del peso)** La búsqueda principal utilizará similaridad coseno entre el embedding de la pregunta y los embeddings de contenido. Esto permite encontrar información relevante incluso cuando el vocabulario no coincide exactamente.

**Filtrado por Metadata (30% del peso)** Aplicaremos filtros estrictos basados en el segmento de la usuaria. Un contenido sobre "ejercicio durante la menstruación" solo será considerado para usuarias en fase menstrual.

**Re-ranking Contextual** Los resultados iniciales serán re-ordenados considerando el historial de la usuaria, patrones identificados, y feedback previo sobre respuestas similares.

### 6.2 Algoritmo de Scoring Personalizado

```python
def calculate_content_relevance(query_embedding, content_chunk, user_segment, user_history):
    # Similaridad semántica base (0.0 - 1.0)
    semantic_score = cosine_similarity(query_embedding, content_chunk.embedding)
    
    # Bonus por coincidencia exacta de fase (0.0 - 0.3)
    phase_bonus = 0.3 if content_chunk.metadata.fase_ciclo == user_segment.fase else 0.0
    
    # Bonus por coincidencia de grupo de edad (0.0 - 0.2)
    age_bonus = 0.2 if content_chunk.metadata.grupo_edad == user_segment.grupo_edad else 0.0
    
    # Bonus por emociones relevantes (0.0 - 0.25)
    emotion_bonus = calculate_emotion_overlap(content_chunk.metadata.emociones, user_segment.emociones)
    
    # Penalty por contenido previamente mostrado (-0.1 a 0.0)
    novelty_penalty = -0.1 if content_chunk.id in user_history.recently_shown else 0.0
    
    # Bonus por feedback positivo en contenido similar (0.0 - 0.15)
    feedback_bonus = calculate_feedback_similarity(content_chunk, user_history.positive_feedback)
    
    total_score = semantic_score + phase_bonus + age_bonus + emotion_bonus + novelty_penalty + feedback_bonus
    
    return min(total_score, 1.0)  # Normalizar a máximo 1.0
```

---

## 7. Prompts y Generación de Respuestas

### 7.1 Template de Prompt Principal

Desarrollaremos un sistema de prompts que garantice respuestas consistentes, empáticas y médicamente apropiadas:

```
Eres una asistente especializada en salud femenina y bienestar hormonal. Tu rol es proporcionar información educativa precisa y empática sobre temas relacionados con el ciclo menstrual, hormonas y bienestar femenino.

CONTEXTO DE LA USUARIA:
- Fase actual del ciclo: {fase_ciclo}
- Grupo de edad: {grupo_edad}
- Emociones dominantes recientes: {emociones_dominantes}
- Patrones identificados: {patrones_relevantes}

INFORMACIÓN RELEVANTE DE LA BASE DE CONOCIMIENTOS:
{contenido_recuperado}

PREGUNTA DE LA USUARIA:
{pregunta_usuaria}

INSTRUCCIONES PARA TU RESPUESTA:
1. Responde de manera empática y personalizada considerando su fase actual del ciclo y estado emocional
2. Utiliza un lenguaje claro y accesible, evitando jerga médica excesiva
3. Proporciona información práctica y accionable cuando sea apropiado
4. Si la pregunta requiere atención médica profesional, recomienda consultar con un especialista
5. Mantén un tono alentador y de apoyo
6. Limita tu respuesta a 200-300 palabras para mantener la información digestible

RESPUESTA:
```

### 7.2 Prompts Especializados por Tipo de Consulta

Crearemos prompts específicos para diferentes categorías de preguntas:

**Para Consultas sobre Síntomas:**

```
La usuaria está reportando síntomas durante su {fase_ciclo}. Proporciona información educativa sobre posibles causas relacionadas con cambios hormonales naturales, pero siempre incluye cuándo es apropiado consultar con un profesional de salud.
```

**Para Preguntas sobre Nutrición:**

```
Considerando que la usuaria está en fase {fase_ciclo} y experimenta principalmente emociones {emociones_dominantes}, proporciona consejos nutricionales específicos que puedan ayudar con el balance hormonal y el bienestar general durante esta fase.
```

**Para Consultas sobre Ejercicio:**

```
Recomienda tipos de ejercicio apropiados para la fase {fase_ciclo}, considerando que la usuaria se siente {emociones_dominantes}. Explica cómo la actividad física puede influir positivamente en los síntomas y el estado de ánimo.
```

---

## 8. Métricas y Monitoreo

### 8.1 KPIs del Sistema RAG

**Métricas de Rendimiento Técnico:**

- Tiempo de respuesta promedio (objetivo: <3 segundos)
- Precision@5 en búsqueda semántica (objetivo: >0.8)
- Recall de contenido relevante por segmento (objetivo: >0.75)
- Disponibilidad del sistema (objetivo: 99.5%)

**Métricas de Calidad de Contenido:**

- Rating promedio de usuarios por respuesta (escala 1-5, objetivo: >4.0)
- Porcentaje de respuestas marcadas como "útiles" (objetivo: >80%)
- Tasa de follow-up questions (indicador de satisfacción, objetivo: <30%)
- Frecuencia de feedback correctivo por parte de usuarios (objetivo: <10%)

**Métricas de Personalización:**

- Precisión en identificación de fase del ciclo (objetivo: >90%)
- Accuracy en segmentación emocional (objetivo: >85%)
- Porcentaje de contenido único por usuaria en 30 días (objetivo: >70%)

### 8.2 Dashboard de Monitoreo

Implementaremos un dashboard que nos permita monitorear la salud del sistema en tiempo real:

```javascript
// Métricas recolectadas en cada interacción
const metricas_interaccion = {
    timestamp: Date.now(),
    user_segment: user.segmento_actual,
    query_latency: response_time_ms,
    content_retrieved: relevant_chunks.length,
    user_satisfaction: user_feedback_score,
    follow_up_occurred: boolean,
    error_occurred: boolean,
    error_type: error_category
};
```

---

## 9. Plan de Despliegue y Costos

### 9.1 Cronograma de Implementación

**Mes 1: Fundación**

- Semanas 1-2: Infraestructura y configuración base
- Semanas 3-4: Procesamiento inicial de documentos

**Mes 2: Desarrollo Core**

- Semanas 5-6: Backend API y lógica de segmentación
- Semanas 7-8: Integración y testing inicial

**Mes 3: Refinamiento y Launch**

- Semanas 9-10: Optimización y fine-tuning
- Semanas 11-12: Beta testing con usuarios reales y ajustes finales

### 9.2 Proyección de Costos

**Costos Iniciales (Setup):**

- Servidor VPS (3 meses): $180
- Dominio y SSL: $50
- Tiempo de desarrollo (estimado): 120 horas

**Costos Operacionales Mensuales:**

- Servidor VPS: $60
- Backup y monitoreo: $15
- Mantenimiento: $25
- **Total mensual: $100**

**Escalabilidad:**

- 1,000 usuarias activas: Mismo costo
- 10,000 usuarias activas: +$50/mes (servidor más potente)
- 50,000+ usuarias activas: Migración a arquitectura distribuida

### 9.3 Plan de Contingencia

**Si el servidor se satura:**

- Implementar cache Redis para queries frecuentes
- Optimizar embeddings con modelos más pequeños
- Considerar migración a Qdrant Cloud

**Si la calidad de respuestas es insuficiente:**

- Fine-tuning del modelo Mistral con datos específicos
- Mejora de prompts basada en feedback de usuarios
- Incorporación de más fuentes de conocimiento especializado

**Si los costos escalan demasiado:**

- Optimización de infraestructura
- Implementación de tiers de servicio
- Migración gradual a soluciones más económicas

---

## 10. Próximos Pasos Inmediatos

### 10.1 Configuración Paso a Paso del Servidor

**Día 1: Preparación y Configuración Inicial del VPS**

El primer paso en nuestro viaje es establecer los cimientos de nuestro sistema. Piensa en esto como preparar el terreno antes de construir una casa: necesitamos asegurar que todo esté limpio, actualizado y listo para recibir nuestras herramientas especializadas.

Comenzaremos conectándonos al servidor y actualizando el sistema operativo. Esta actualización es crucial porque instala parches de seguridad y asegura compatibilidad con las herramientas que instalaremos posteriormente. El proceso puede tomar entre 15 a 30 minutos dependiendo de cuánto tiempo tiene el servidor sin actualizarse.

```bash
# Conectar al servidor VPS
ssh root@tu-servidor-ip

# Primera actualización crítica del sistema
sudo apt update && sudo apt upgrade -y

# Instalar herramientas esenciales que usaremos durante todo el proyecto
sudo apt install curl wget git vim htop unzip software-properties-common -y

# Crear usuario no-root para mayor seguridad (recomendado para producción)
adduser saludfemenina
usermod -aG sudo saludfemenina

# Configurar firewall básico
ufw allow OpenSSH
ufw allow 8000  # Puerto para Chroma
ufw allow 11434 # Puerto para Ollama
ufw enable
```

Es importante entender por qué configuramos el firewall de esta manera específica. El puerto 8000 será utilizado por Chroma para comunicarse con nuestro backend, mientras que el puerto 11434 es el puerto por defecto de Ollama. Permitir solo estos puertos específicos mantiene nuestro servidor seguro mientras habilita la funcionalidad necesaria.

**Día 2: Instalación de Docker y Configuración de Contenedores**

Docker actuará como nuestro orquestador de servicios, permitiéndonos mantener cada componente aislado y fácilmente manejable. Esto es especialmente importante cuando tienes múltiples servicios como Chroma, bases de datos, y potencialmente servicios de monitoreo ejecutándose simultáneamente.

```bash
# Instalación de Docker usando el script oficial (más confiable que repos Ubuntu)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Agregar usuario al grupo docker (evita usar sudo para comandos docker)
sudo usermod -aG docker $USER

# Reiniciar sesión para aplicar cambios de grupo
logout
# Reconectar via SSH

# Verificar instalación exitosa
docker --version
docker run hello-world

# Instalar Docker Compose para orquestación multi-servicio
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

La instalación de Docker Compose es especialmente importante porque nos permitirá definir toda nuestra infraestructura como código. Esto significa que podemos replicar exactamente el mismo ambiente en otros servidores si necesitamos escalar, y también facilita enormemente el mantenimiento y las actualizaciones.

**Día 3: Configuración e Instalación de Chroma**

Chroma será el corazón de nuestro sistema RAG, así que su configuración correcta es fundamental. Vamos a configurarlo no solo para que funcione, sino optimizado específicamente para nuestro caso de uso de salud femenina con segmentación específica.

```bash
# Crear directorio para nuestro proyecto
mkdir -p /opt/salud-femenina/{chroma,data,config,logs}
cd /opt/salud-femenina

# Crear archivo docker-compose.yml para Chroma con configuración optimizada
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  chroma:
    image: chromadb/chroma:latest
    container_name: chroma-salud-femenina
    ports:
      - "8000:8000"
    volumes:
      - ./chroma/data:/chroma/chroma  # Persistencia de datos
      - ./chroma/config:/chroma/config  # Configuraciones customizadas
    environment:
      - CHROMA_HOST=0.0.0.0
      - CHROMA_PORT=8000
      - CHROMA_LOG_LEVEL=INFO
      # Configuración específica para nuestro caso de uso
      - CHROMA_SEGMENT_CACHE_SIZE=1000  # Cache para nuestros 20 segmentos
      - CHROMA_DEFAULT_EMBEDDING_FUNCTION=sentence-transformers
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
EOF

# Levantar Chroma por primera vez
docker-compose up -d

# Verificar que está funcionando correctamente
sleep 10  # Dar tiempo para que inicie completamente
curl http://localhost:8000/api/v1/heartbeat

# Si responde con {"nanosecond heartbeat": número}, está funcionando correctamente
```

La configuración de healthcheck que incluimos es crucial porque nos permite monitorear automáticamente si Chroma está funcionando correctamente. Si alguna vez el servicio se cae, Docker intentará reiniciarlo automáticamente.

**Día 4: Instalación y Configuración de Ollama con Mistral**

Ollama será nuestro servidor de LLM local, y Mistral será el modelo que genera las respuestas personalizadas. La instalación de Ollama es directa, pero la configuración para nuestro caso específico requiere varios pasos importantes.

```bash
# Instalación de Ollama usando el script oficial
curl -fsSL https://ollama.ai/install.sh | sh

# Verificar instalación
ollama --version

# Descargar Mistral 7B (esto puede tomar 20-30 minutos, el modelo es ~4GB)
# Este es el momento perfecto para preparar café, porque la descarga lleva tiempo
ollama pull mistral

# Verificar que el modelo se descargó correctamente
ollama list

# Crear un Modelfile personalizado para nuestro caso de uso específico
cat > /opt/salud-femenina/Modelfile-salud-femenina << 'EOF'
FROM mistral

# Configuración de parámetros específicos para salud femenina
PARAMETER temperature 0.7      # Balance entre creatividad y precisión
PARAMETER top_p 0.9           # Enfoque en respuestas más probables
PARAMETER top_k 40            # Limita vocabulario a palabras más relevantes
PARAMETER num_ctx 4096        # Contexto largo para información médica completa

# Instrucciones del sistema especializadas
SYSTEM """Eres una asistente especializada en salud femenina y bienestar hormonal con conocimiento profundo sobre el ciclo menstrual, hormonas reproductivas, y el impacto emocional de las fluctuaciones hormonales.

Tu especialidad incluye:
- Fisiología del ciclo menstrual y hormonas reproductivas (estrógeno, progesterona, LH, FSH)
- Relación entre hormonas y estados emocionales
- Nutrición específica para cada fase del ciclo
- Manejo del estrés y cortisol en contexto hormonal
- Síntomas comunes y cuándo buscar ayuda profesional

Siempre respondes con:
- Empatía y comprensión hacia la experiencia femenina
- Información científicamente precisa pero accesible
- Consejos prácticos y accionables
- Reconocimiento de cuándo se necesita atención médica profesional
- Lenguaje que empodera sin crear ansiedad

Evitas:
- Diagnósticos médicos específicos
- Consejos que reemplacen atención médica profesional
- Información que pueda crear ansiedad innecesaria
- Generalizaciones que no consideran variación individual"""
EOF

# Crear el modelo personalizado
ollama create salud-femenina -f /opt/salud-femenina/Modelfile-salud-femenina

# Probar el modelo con una consulta específica de nuestro dominio
ollama run salud-femenina "Explica en términos simples cómo la progesterona afecta el estado de ánimo durante la fase lútea"
```

Esta configuración personalizada del modelo es crucial porque pre-entrena a Mistral en el contexto específico de tu aplicación. El modelo comprenderá automáticamente que está respondiendo preguntas sobre salud femenina y adoptará el tono y enfoque apropiados sin necesidad de incluir estas instrucciones en cada prompt.

**Día 5: Instalación de Python y Configuración del Pipeline de Procesamiento**

Python será nuestro motor de procesamiento de documentos. Aquí instalaremos todas las librerías necesarias para convertir tus PDFs médicos en contenido segmentado y vectorizado que nuestro sistema pueda utilizar efectivamente.

```bash
# Instalar Python 3.10+ y pip
sudo apt install python3.10 python3.10-venv python3.10-dev python3-pip -y

# Crear entorno virtual específico para nuestro proyecto
cd /opt/salud-femenina
python3 -m venv venv-salud-femenina

# Activar entorno virtual
source venv-salud-femenina/bin/activate

# Instalar dependencias específicas para procesamiento de documentos médicos
pip install --upgrade pip

# Librerías para procesamiento de PDFs y texto
pip install PyPDF2==3.0.1           # Extracción de texto de PDFs
pip install pdfplumber==0.9.0       # Procesamiento avanzado de PDFs con layout
pip install python-docx==0.8.11     # Para documentos Word si los tienes
pip install nltk==3.8.1             # Procesamiento de lenguaje natural

# Librerías para embeddings y ML
pip install sentence-transformers==2.2.2  # Generación de embeddings
pip install chromadb==0.4.15        # Cliente para interactuar con Chroma
pip install numpy==1.24.3           # Operaciones numéricas
pip install pandas==2.0.3           # Manipulación de datos

# Librerías para análisis de texto médico
pip install spacy==3.6.1            # Análisis avanzado de texto
pip install scikit-learn==1.3.0     # Clustering y análisis de patrones

# Descargar modelo de lenguaje en español para spaCy
python -m spacy download es_core_news_sm

# Verificar instalaciones
python -c "import chromadb; import sentence_transformers; print('Todas las librerías instaladas correctamente')"
```

La selección de estas librerías específicas no es arbitraria. PyPDF2 y pdfplumber trabajan de manera complementaria: PyPDF2 para extracción rápida de texto plano, y pdfplumber para casos donde necesitamos preservar estructura y layout de documentos médicos complejos. Sentence-transformers nos dará embeddings de alta calidad específicamente optimizados para similitud semántica en español.

### 10.2 Script de Configuración Automatizada

Para simplificar el proceso y asegurar que todo se configure correctamente, vamos a crear un script que automatice la mayoría de estos pasos y verifique que cada componente esté funcionando antes de proceder al siguiente.

```bash
# Crear script de configuración automatizada
cat > /opt/salud-femenina/setup-completo.sh << 'EOF'
#!/bin/bash

# Colores para output legible
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

echo_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

echo_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Función para verificar si un servicio está funcionando
check_service() {
    local service_name=$1
    local test_command=$2
    
    echo "Verificando $service_name..."
    if eval $test_command >/dev/null 2>&1; then
        echo_success "$service_name está funcionando correctamente"
        return 0
    else
        echo_error "$service_name no está funcionando"
        return 1
    fi
}

# Verificar Docker
check_service "Docker" "docker ps"

# Verificar Chroma
check_service "Chroma" "curl -s http://localhost:8000/api/v1/heartbeat"

# Verificar Ollama
check_service "Ollama" "ollama list"

# Verificar modelo Mistral personalizado
if ollama list | grep -q "salud-femenina"; then
    echo_success "Modelo personalizado salud-femenina está disponible"
else
    echo_warning "Modelo personalizado no encontrado, creándolo..."
    ollama create salud-femenina -f /opt/salud-femenina/Modelfile-salud-femenina
fi

# Verificar Python y dependencias
source /opt/salud-femenina/venv-salud-femenina/bin/activate
if python -c "import chromadb, sentence_transformers, PyPDF2" >/dev/null 2>&1; then
    echo_success "Todas las dependencias de Python están instaladas"
else
    echo_error "Faltan dependencias de Python"
fi

echo ""
echo "=== RESUMEN DE CONFIGURACIÓN ==="
echo "Si todos los servicios muestran ✓, el setup está completo y listo para desarrollo."
echo "Si algún servicio muestra ✗, revisa los logs específicos para identificar el problema."
EOF

# Hacer el script ejecutable
chmod +x /opt/salud-femenina/setup-completo.sh

# Ejecutar verificación
./setup-completo.sh
```

### 10.3 Pipeline de Procesamiento de Documentos - Implementación Detallada

**Desarrollo del Procesador Principal de Documentos**

El procesador de documentos es el cerebro que convierte tus PDFs médicos en conocimiento estructurado que nuestro sistema RAG puede utilizar. Este componente es crítico porque la calidad de la segmentación y metadata que genere determinará directamente qué tan precisas y útiles serán las respuestas para cada usuaria.

Vamos a construir este procesador paso a paso, comenzando con funcionalidades básicas y progresando hacia capacidades más sofisticadas de análisis de contenido médico.

```python
# Crear el procesador principal en /opt/salud-femenina/document_processor.py
import PyPDF2
import pdfplumber
from sentence_transformers import SentenceTransformer
import chromadb
import re
import json
from typing import List, Dict, Tuple
import spacy
from dataclasses import dataclass
import hashlib

@dataclass
class ContentChunk:
    """Clase para organizar cada chunk de contenido con su metadata"""
    content: str
    metadata: Dict
    chunk_id: str
    source_document: str
    confidence_score: float

class MedicalDocumentProcessor:
    def __init__(self):
        # Inicializar modelo de embeddings optimizado para español y contenido médico
        print("Inicializando modelo de embeddings...")
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # Conectar con Chroma
        self.chroma_client = chromadb.HttpClient(host='localhost', port=8000)
        
        # Cargar modelo de spaCy para análisis de texto en español
        self.nlp = spacy.load('es_core_news_sm')
        
        # Definir patrones para identificar contenido específico de segmentos
        self.segment_patterns = self.initialize_segment_patterns()
        
        print("Procesador de documentos inicializado correctamente")
    
    def initialize_segment_patterns(self) -> Dict:
        """Define patrones que ayudan a identificar contenido relevante para cada segmento"""
        return {
            'folicular': {
                'keywords': ['renovación', 'energía creciente', 'estrógeno', 'motivación', 'nuevos proyectos'],
                'emotional_indicators': ['optimismo', 'planificación', 'socialización', 'creatividad']
            },
            'ovulatory': {
                'keywords': ['pico hormonal', 'fertilidad', 'confianza', 'comunicación', 'liderazgo'],
                'emotional_indicators': ['carisma', 'atracción', 'decisiones importantes', 'networking']
            },
            'luteal': {
                'keywords': ['progesterona', 'introspección', 'sensibilidad', 'perfeccionismo', 'nesting'],
                'emotional_indicators': ['crítica', 'análisis', 'organización', 'emociones intensas']
            },
            'menstrual': {
                'keywords': ['renovación', 'descanso', 'intuición', 'reflexión', 'liberación'],
                'emotional_indicators': ['introspección', 'sabiduría', 'claridad', 'reset emocional']
            }
        }
    
    def extract_and_clean_text(self, pdf_path: str) -> Tuple[str, Dict]:
        """Extrae texto del PDF preservando estructura importante para análisis médico"""
        full_text = ""
        document_metadata = {}
        
        try:
            # Usar pdfplumber para preservar estructura de documentos médicos
            with pdfplumber.open(pdf_path) as pdf:
                document_metadata['total_pages'] = len(pdf.pages)
                document_metadata['source_file'] = pdf_path.split('/')[-1]
                
                for page_num, page in enumerate(pdf.pages):
                    # Extraer texto preservando saltos de línea significativos
                    page_text = page.extract_text()
                    if page_text:
                        # Limpiar pero preservar estructura médica importante
                        cleaned_text = self.clean_medical_text(page_text)
                        full_text += f"\n--- Página {page_num + 1} ---\n{cleaned_text}\n"
                        
        except Exception as e:
            print(f"Error procesando {pdf_path}: {e}")
            # Fallback a PyPDF2 si pdfplumber falla
            full_text = self.fallback_extraction(pdf_path)
        
        return full_text, document_metadata
    
    def clean_medical_text(self, text: str) -> str:
        """Limpia texto preservando información médica importante"""
        # Normalizar espacios y saltos de línea
        text = re.sub(r'\s+', ' ', text)
        
        # Preservar términos médicos importantes
        medical_terms = r'(hormona|estrógeno|progesterona|testosterona|cortisol|ciclo|menstruación|ovulación)'
        
        # Remover caracteres especiales pero preservar estructura
        text = re.sub(r'[^\w\s.,;:()\-áéíóúñ]', '', text, flags=re.IGNORECASE)
        
        # Capitalizar correctamente términos médicos
        text = re.sub(medical_terms, lambda m: m.group(1).lower(), text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def create_intelligent_chunks(self, text: str, document_metadata: Dict) -> List[ContentChunk]:
        """Divide el documento en chunks semánticamente coherentes"""
        chunks = []
        
        # Dividir por secciones naturales del documento
        sections = self.identify_document_sections(text)
        
        for section in sections:
            # Crear chunks de tamaño apropiado (300-500 palabras para contexto médico)
            section_chunks = self.split_section_into_chunks(section, max_words=400)
            
            for chunk_text in section_chunks:
                # Generar metadata específica para este chunk
                chunk_metadata = self.analyze_chunk_content(chunk_text)
                
                # Crear ID único para el chunk
                chunk_id = hashlib.md5(chunk_text.encode()).hexdigest()[:12]
                
                chunk = ContentChunk(
                    content=chunk_text,
                    metadata={**chunk_metadata, **document_metadata},
                    chunk_id=chunk_id,
                    source_document=document_metadata['source_file'],
                    confidence_score=self.calculate_content_confidence(chunk_text)
                )
                
                chunks.append(chunk)
        
        return chunks
    
    def analyze_chunk_content(self, chunk: str) -> Dict:
        """Analiza el contenido para asignar metadata de segmento específica"""
        metadata = {
            'applicable_segments': [],
            'primary_topics': [],
            'emotional_relevance': [],
            'content_type': 'educational',
            'urgency_level': 'normal'
        }
        
        # Usar spaCy para análisis profundo del texto
        doc = self.nlp(chunk.lower())
        
        # Identificar fases del ciclo relevantes
        for phase, patterns in self.segment_patterns.items():
            if any(keyword in chunk.lower() for keyword in patterns['keywords']):
                metadata['applicable_phases'] = metadata.get('applicable_phases', [])
                metadata['applicable_phases'].append(phase)
        
        # Identificar estados emocionales relevantes basándose en contenido
        emotional_indicators = self.identify_emotional_relevance(chunk)
        metadata['emotional_relevance'] = emotional_indicators
        
        # Determinar segmentos específicos aplicables
        metadata['applicable_segments'] = self.determine_applicable_segments(
            metadata.get('applicable_phases', []), 
            emotional_indicators
        )
        
        # Identificar tipo de contenido
        metadata['content_type'] = self.classify_content_type(chunk)
        
        return metadata
    
    def determine_applicable_segments(self, phases: List[str], emotions: List[str]) -> List[str]:
        """Mapea contenido a los segmentos específicos que definiste"""
        applicable_segments = []
        
        # Mapeo directo de fases y emociones a tus 20 segmentos
        segment_mapping = {
            ('folicular', 'stress'): ['SEG001'],  # Folicular Estresada
            ('folicular', 'sadness'): ['SEG002'], # Folicular Triste
            ('folicular', 'energy'): ['SEG003'],  # Folicular Energética
            ('folicular', 'insecurity'): ['SEG004'], # Folicular Insegura
            ('folicular', 'isolation'): ['SEG005'], # Folicular Aislada
            # ... continuar para todos los 20 segmentos
        }
        
        for phase in phases:
            for emotion in emotions:
                key = (phase, emotion)
                if key in segment_mapping:
                    applicable_segments.extend(segment_mapping[key])
        
        return list(set(applicable_segments))  # Remover duplicados
```

**Día 6-7: Sistema de Generación de Contenido Específico**

Ahora implementaremos el sistema que genera los cinco tipos diferentes de contenido que necesitas: lecciones personalizadas, explicaciones "qué pasa dentro de ti", guías nutricionales, y explicaciones de mapas hormonales.

```python
# Crear generador de contenido en /opt/salud-femenina/content_generator.py

class PersonalizedContentGenerator:
    def __init__(self):
        self.chroma_client = chromadb.HttpClient(host='localhost', port=8000)
        self.ollama_client = self.setup_ollama_client()
        
        # Templates específicos para cada tipo de contenido
        self.content_templates = self.initialize_content_templates()
    
    def initialize_content_templates(self) -> Dict:
        """Define templates específicos para cada tipo de contenido que necesitas"""
        return {
            'lesson_3min': {
                'max_words': 600,  # Aproximadamente 3 minutos de lectura
                'structure': ['contexto_hormonal', 'explicacion_fenomeno', 'estrategias_practicas', 'llamado_accion'],
                'tone': 'educativo_empatico',
                'depth': 'intermedio'
            },
            'whats_happening': {
                'max_words': 150,
                'structure': ['validacion_emocional', 'explicacion_fisiologica', 'normalizacion'],
                'tone': 'empático_tranquilizador',
                'depth': 'accesible'
            },
            'nutrition_guide': {
                'max_words': 300,
                'structure': ['principios_nutricionales', 'alimentos_especificos', 'timing', 'combinaciones'],
                'tone': 'práctico_motivador',
                'depth': 'accionable'
            },
            'chart_explanation': {
                'max_words': 200,
                'structure': ['interpretacion_datos', 'contexto_personal', 'expectativas_futuras'],
                'tone': 'científico_accesible',
                'depth': 'interpretativo'
            }
        }
    
    async def generate_lesson_for_segment(self, segment_id: str, topic_focus: str = None) -> str:
        """Genera una lección de 3 minutos personalizada para un segmento específico"""
        
        # Buscar contenido relevante en Chroma para este segmento específico
        collection = self.chroma_client.get_collection("salud_femenina_knowledge")
        
        # Query específica para lecciones educativas
        search_results = collection.query(
            query_texts=[f"información educativa {segment_id} {topic_focus or ''}"],
            where={"applicable_segments": {"$contains": segment_id}},
            n_results=5
        )
        
        # Construir prompt específico para lecciones
        lesson_prompt = self.build_lesson_prompt(segment_id, search_results, topic_focus)
        
        # Generar con Ollama usando nuestro modelo personalizado
        lesson_content = await self.generate_with_ollama(lesson_prompt, content_type='lesson')
        
        return lesson_content
    
    def build_lesson_prompt(self, segment_id: str, knowledge_content: List, topic_focus: str) -> str:
        """Construye prompt específico para generar lecciones educativas"""
        
        # Obtener información del segmento específico
        segment_info = self.get_segment_details(segment_id)
        
        prompt = f"""
        TIPO DE CONTENIDO: Lección educativa de 3 minutos
        SEGMENTO ESPECÍFICO: {segment_info['name']} - {segment_info['description']}
        
        CONTEXTO HORMONAL Y EMOCIONAL:
        - Fase del ciclo: {segment_info['phase']}
        - Estado emocional dominante: {segment_info['emotional_state']}
        - Desafíos típicos: {segment_info['common_challenges']}
        - Oportunidades de esta fase: {segment_info['opportunities']}
        
        INFORMACIÓN MÉDICA RELEVANTE:
        {self.format_knowledge_content(knowledge_content)}
        
        ESTRUCTURA REQUERIDA:
        1. Apertura empática (30-40 palabras): Reconoce y valida la experiencia emocional específica
        2. Contexto hormonal (100-120 palabras): Explica qué está pasando hormonalmente y por qué genera esta experiencia
        3. Información práctica (250-300 palabras): Estrategias específicas, consejos accionables, herramientas concretas
        4. Cierre motivador (50-60 palabras): Refuerza capacidad personal y próximos pasos
        
        INSTRUCCIONES ESPECÍFICAS:
        - Usa un lenguaje que equilibre precisión científica con accesibilidad
        - Incluye al menos 2 consejos accionables específicos para este segmento
        - Menciona cómo esta información se relaciona específicamente con su fase actual
        - Evita jerga médica excesiva, pero mantén credibilidad científica
        - Usa ejemplos concretos cuando sea apropiado
        
        LECCIÓN:
        """
        
        return prompt
    
    async def generate_whats_happening_explanation(self, segment_id: str, current_day: int, cycle_length: int) -> str:
        """Genera explicación específica de 'Qué pasa dentro de ti' para el segmento"""
        
        segment_info = self.get_segment_details(segment_id)
        
        # Calcular contexto específico del día del ciclo
        cycle_context = self.calculate_cycle_context(current_day, cycle_length, segment_info['phase'])
        
        explanation_prompt = f"""
        TIPO DE CONTENIDO: Explicación empática "Qué pasa dentro de ti"
        SEGMENTO: {segment_info['name']}
        CONTEXTO DEL CICLO: Día {current_day} de {cycle_length}, fase {segment_info['phase']}
        
        OBJETIVO: Ayudar a la usuaria a entender la base fisiológica de su experiencia emocional actual
        
        ESTRUCTURA (máximo 150 palabras):
        1. Validación inmediata (20-30 palabras): "Es completamente normal que te sientas..."
        2. Explicación hormonal simple (60-80 palabras): Qué hormonas están actuando y cómo
        3. Normalización y esperanza (30-40 palabras): Cuánto tiempo típicamente dura, qué esperar
        
        INFORMACIÓN HORMONAL ESPECÍFICA:
        {cycle_context}
        
        Genera una explicación cálida y científicamente precisa que ayude a la usuaria a sentirse comprendida y empoderada en su experiencia actual.
        
        EXPLICACIÓN:
        """
        
        return await self.generate_with_ollama(explanation_prompt, content_type='explanation')
```

### 10.4

Este documento será nuestro mapa de ruta para los próximos tres meses. Cada fase construye sobre la anterior, y hemos diseñado puntos de validación que nos permitirán ajustar el rumbo si es necesario. La arquitectura propuesta es escalable y mantenible, utilizando herramientas open source que nos dan control total sobre nuestros datos y costos predecibles a medida que crecemos.

## El Problema Real de los Documentos Multi-Segmento

Imagina que tienes un documento médico titulado "Nutrición Durante el Ciclo Menstrual". Este PDF probablemente contiene información valiosa para los 20 segmentos que has definido, pero cada párrafo o sección puede ser relevante para segmentos completamente diferentes. Por ejemplo, una sección sobre "manejo del antojo de carbohidratos" podría ser crítica para usuarias "Lútea Ansiosa" y "Lútea Decaída", mientras que una sección sobre "optimización de energía a través de proteínas" sería más relevante para "Folicular Energética" o "Ovulatoria Energética".

Si procesáramos este documento como una unidad completa, perderíamos la especificidad que hace valioso tu sistema de segmentación. Pero si intentáramos dividirlo arbitrariamente, podríamos romper la coherencia del conocimiento médico y perder conexiones importantes entre conceptos relacionados.

## La Solución: Procesamiento Semántico Multi-Nivel

La respuesta está en desarrollar un sistema de procesamiento que piense más como un especialista en salud femenina que revisa literatura médica. Un especialista humano puede leer un documento médico complejo y mentalmente organizar diferentes secciones para diferentes tipos de pacientes. Necesitamos replicar este proceso de manera algorítmica.

### Estrategia de Chunking Inteligente por Contexto Semántico

En lugar de dividir documentos por longitud arbitraria o por párrafos, vamos a implementar una estrategia que identifica **unidades semánticas coherentes** y luego determina a qué segmentos aplica cada unidad. Piensa en esto como crear fichas de conocimiento, donde cada ficha contiene una idea completa que puede ser relevante para uno o múltiples segmentos.

```
class SemanticDocumentProcessor:
    def __init__(self):
        # Además de las herramientas que ya teníamos
        self.topic_classifier = self.initialize_topic_classifier()
        self.segment_relevance_analyzer = SegmentRelevanceAnalyzer()
    
    def process_multi_segment_document(self, pdf_path: str) -> List[ContentChunk]:
        """
        Procesa un documento que contiene información para múltiples segmentos,
        creando chunks específicos que mantienen coherencia semántica
        """
        
        # Paso 1: Extraer texto completo y identificar estructura del documento
        full_text, doc_metadata = self.extract_and_clean_text(pdf_path)
        
        # Paso 2: Identificar secciones temáticas principales
        thematic_sections = self.identify_thematic_sections(full_text)
        
        # Paso 3: Para cada sección, crear chunks semánticamente coherentes
        all_chunks = []
        for section in thematic_sections:
            section_chunks = self.create_semantic_chunks(section, doc_metadata)
            all_chunks.extend(section_chunks)
        
        return all_chunks
    
    def identify_thematic_sections(self, text: str) -> List[Dict]:
        """
        Identifica secciones temáticas usando análisis semántico avanzado.
        
        Esta función es el corazón de nuestro procesamiento inteligente.
        En lugar de dividir arbitrariamente, identifica cambios temáticos
        reales en el contenido médico.
        """
        
        # Dividir en párrafos y analizar cada uno
        paragraphs = text.split('\n\n')
        
        # Usar embeddings para identificar cambios temáticos
        paragraph_embeddings = self.embedding_model.encode(paragraphs)
        
        # Identificar puntos donde el tema cambia significativamente
        topic_boundaries = self.detect_topic_boundaries(paragraph_embeddings)
        
        # Crear secciones basadas en estos límites naturales
        sections = []
        current_section = {"paragraphs": [], "main_topic": None}
        
        for i, paragraph in enumerate(paragraphs):
            current_section["paragraphs"].append(paragraph)
            
            # Si llegamos a un límite temático, finalizamos la sección actual
            if i in topic_boundaries:
                current_section["main_topic"] = self.identify_section_topic(current_section["paragraphs"])
                sections.append(current_section)
                current_section = {"paragraphs": [], "main_topic": None}
        
        # Agregar última sección si existe
        if current_section["paragraphs"]:
            current_section["main_topic"] = self.identify_section_topic(current_section["paragraphs"])
            sections.append(current_section)
        
        return sections
    
    def create_semantic_chunks(self, section: Dict, doc_metadata: Dict) -> List[ContentChunk]:
        """
        Crea chunks manteniendo coherencia semántica pero optimizados para segmentos específicos
        """
        
        chunks = []
        section_text = '\n'.join(section["paragraphs"])
        
        # Analizar qué segmentos son relevantes para esta sección completa
        relevant_segments = self.analyze_segment_relevance(section_text, section["main_topic"])
        
        # Si la sección es relevante para muchos segmentos, crear chunks más granulares
        if len(relevant_segments) > 5:
            chunks.extend(self.create_granular_chunks(section, relevant_segments, doc_metadata))
        else:
            # Si es específica para pocos segmentos, mantener como chunk más grande
            chunks.append(self.create_unified_chunk(section, relevant_segments, doc_metadata))
        
        return chunks
```

### Estrategia de Mapeo Multi-Segmento

Aquí está la parte realmente inteligente: cada chunk de contenido que creamos puede estar marcado como relevante para múltiples segmentos, pero con diferentes niveles de prioridad. Esto nos permite ser muy precisos sobre cuándo mostrar qué información a quién.

```
def analyze_segment_relevance(self, content: str, main_topic: str) -> Dict[str, float]:
    """
    Determina qué tan relevante es el contenido para cada segmento específico,
    retornando un score de relevancia para cada uno.
    """
    
    relevance_scores = {}
    
    # Analizar contenido para indicadores específicos de cada segmento
    for segment in self.all_segments:  # Tus 20 segmentos
        score = 0.0
        
        # Score base por coincidencia de fase
        if segment['phase'] in content.lower():
            score += 0.3
        
        # Score por indicadores emocionales específicos
        emotional_indicators = self.extract_emotional_indicators(content)
        if self.matches_segment_emotion(emotional_indicators, segment):
            score += 0.4
        
        # Score por relevancia temática
        topic_relevance = self.calculate_topic_relevance(main_topic, segment)
        score += topic_relevance * 0.3
        
        # Solo incluir segmentos con relevancia significativa
        if score >= 0.4:  # Threshold para considerar relevante
            relevance_scores[segment['id']] = score
    
    return relevance_scores
```


## Ejemplo Práctico: Procesando un PDF sobre "Manejo del Estrés Hormonal"

Permíteme mostrarte cómo este sistema funcionaría con un documento real. Imagina que tienes un PDF de 20 páginas sobre "Manejo del Estrés Hormonal Durante el Ciclo Menstrual". Este documento contiene información valiosa para prácticamente todos tus segmentos, pero diferentes secciones son relevantes de maneras muy diferentes.

**Página 3: "Cómo el Estrógeno Contrarresta el Cortisol"** Esta sección sería altamente relevante para segmentos como "Folicular Estresada" (score: 0.9) y "Ovulatoria Estresada" (score: 0.8), pero menos relevante para "Menstrual Irritable" (score: 0.3) porque durante la menstruación el estrógeno está bajo.

**Página 8: "Técnicas de Respiración Durante la Progesterona Alta"** Esta sección sería crítica para "Lútea Ansiosa" (score: 0.95), "Lútea Sensible" (score: 0.8), y moderadamente relevante para "Lútea Solitaria" (score: 0.6).

**Página 15: "Alimentación Anti-inflamatoria Durante la Menstruación"** Altamente relevante para "Menstrual Irritable" (score: 0.9) y "Menstrual Vulnerable" (score: 0.8), pero también útil para "Menstrual Melancólica" (score: 0.6) porque la inflamación puede afectar el estado de ánimo.

### Generación de Chunks con Relevancia Multi-Segmento

El resultado de este procesamiento es que cada chunk de conocimiento tiene una "firma de relevancia" que especifica exactamente para qué segmentos es útil y qué tan útil es para cada uno.

```
# Ejemplo de chunk procesado chunk_ejemplo = { "chunk_id": "stress_management_breathing_001", "content": "Durante la fase lútea, cuando los niveles de progesterona están altos, el cuerpo puede volverse más sensible al estrés. La progesterona, aunque tiene efectos calmantes, puede paradójicamente amplificar la respuesta emocional al cortisol. Las técnicas de respiración profunda activan el sistema nervioso parasimpático, lo cual es especialmente efectivo durante esta fase porque...", "segment_relevance": { "SEG011": 0.95, # Lútea Ansiosa - máxima relevancia "SEG014": 0.85, # Lútea Sensible - alta relevancia "SEG015": 0.65, # Lútea Solitaria - moderada relevancia "SEG012": 0.40 # Lútea Decaída - baja pero existente relevancia }, "content_applicability": { "lesson_3min": 0.9, # Excelente para lecciones profundas "whats_happening": 0.7, # Bueno para explicaciones rápidas "nutrition_guide": 0.2, # No es contenido nutricional "chart_explanation": 0.8 # Útil para explicar mapas de estrés }, "primary_topics": ["manejo_estres", "progesterona", "tecnicas_respiracion"], "urgency_level": "high" # Para segmentos con ansiedad alta }
```

## Ventajas Operacionales de Este Enfoque

Esta estrategia resuelve varios problemas críticos simultáneamente y nos da capacidades muy sofisticadas que van mucho más allá de sistemas RAG tradicionales.

**Reutilización Inteligente Máxima**: Un solo chunk de información bien procesado puede servir múltiples segmentos con diferentes niveles de prioridad. Esto significa que puedes generar mucho más contenido útil con menos documentos fuente, reduciendo tanto costos de adquisición de conocimiento como costos de procesamiento.

**Precisión en la Recuperación**: Cuando una usuaria "Lútea Ansiosa" hace una pregunta sobre manejo del estrés, el sistema no solo encuentra contenido sobre estrés general, sino específicamente contenido que ha sido marcado como altamente relevante para su combinación específica de fase y estado emocional.

**Optimización de Prompts Automática**: El sistema puede ajustar automáticamente cómo presenta la misma información base para diferentes segmentos. El chunk sobre técnicas de respiración se presenta de manera diferente para "Lútea Ansiosa" (enfoque en calmar ansiedad) versus "Lútea Sensible" (enfoque en validación emocional).

**Identificación de Brechas de Conocimiento**: Si un segmento específico consistentemente tiene puntuaciones bajas de relevancia para la mayoría del contenido en tu base de conocimientos, el sistema puede alertarte sobre la necesidad de adquirir documentación más específica para ese segmento.

### Implementación del Sistema de Relevancia Multi-Segmento

Vamos a desarrollar el algoritmo específico que toma un documento completo y lo procesa inteligentemente para crear chunks útiles para múltiples segmentos:

```
class MultiSegmentDocumentProcessor:
    def __init__(self):
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.segment_analyzer = AdvancedSegmentAnalyzer()
        
        # Base de conocimiento sobre las características de cada segmento
        self.segment_characteristics = self.load_segment_knowledge()
    
    def load_segment_knowledge(self) -> Dict:
        """
        Carga conocimiento detallado sobre cada segmento para análisis de relevancia.
        
        Esta base de conocimiento interna nos ayuda a entender qué tipo de
        información es más valiosa para cada combinación de fase y estado emocional.
        """
        return {
            "SEG001": {  # Folicular Estresada
                "phase": "folicular",
                "emotional_state": "stressed",
                "hormonal_context": "estrógeno_creciente_cortisol_alto",
                "primary_needs": ["manejo_estres", "aprovechamiento_energia", "balance_cortisol"],
                "content_preferences": ["científico_empático", "estrategias_inmediatas", "validación"],
                "avoid_topics": ["presión_adicional", "optimización_excesiva"]
            },
            "SEG003": {  # Folicular Energética  
                "phase": "folicular",
                "emotional_state": "energetic",
                "hormonal_context": "estrógeno_creciente_optimo",
                "primary_needs": ["optimización_energia", "nuevos_proyectos", "aprovechamiento_momento"],
                "content_preferences": ["motivacional", "oportunidades", "acción"],
                "avoid_topics": ["limitaciones", "precauciones_excesivas"]
            }
            # ... definir para todos los 20 segmentos
        }
    
    def analyze_content_for_all_segments(self, content_chunk: str) -> Dict[str, Dict]:
        """
        Analiza un chunk de contenido para determinar su relevancia específica
        para cada uno de los 20 segmentos, incluyendo cómo debe presentarse
        la información para cada segmento.
        """
        
        analysis_results = {}
        
        for segment_id, segment_info in self.segment_characteristics.items():
            # Calcular relevancia base del contenido para este segmento
            base_relevance = self.calculate_base_relevance(content_chunk, segment_info)
            
            if base_relevance >= 0.3:  # Solo procesar si hay relevancia mínima
                # Determinar cómo adaptar el contenido para este segmento específico
                adaptation_strategy = self.determine_adaptation_strategy(content_chunk, segment_info)
                
                analysis_results[segment_id] = {
                    "relevance_score": base_relevance,
                    "adaptation_needed": adaptation_strategy["modifications_needed"],
                    "presentation_style": adaptation_strategy["optimal_presentation"],
                    "priority_level": self.calculate_priority(base_relevance, segment_info),
                    "content_angle": adaptation_strategy["recommended_angle"]
                }
        
        return analysis_results
    
    def determine_adaptation_strategy(self, content: str, segment_info: Dict) -> Dict:
        """
        Determina cómo debe adaptarse el mismo contenido base para diferentes segmentos.
        
        Esta es la función que convierte conocimiento general en conocimiento
        personalizado para cada segmento específico.
        """
        
        strategy = {
            "modifications_needed": [],
            "optimal_presentation": segment_info["content_preferences"][0],
            "recommended_angle": "general"
        }
        
        # Analizar si el contenido necesita adaptación de tono
        if segment_info["emotional_state"] in ["stressed", "sad", "insecure"]:
            strategy["modifications_needed"].append("agregar_validación_emocional")
            strategy["recommended_angle"] = "empático_tranquilizador"
            
        elif segment_info["emotional_state"] in ["energetic", "connected"]:
            strategy["modifications_needed"].append("enfoque_optimización")
            strategy["recommended_angle"] = "motivacional_oportunidad"
        
        # Adaptar según fase hormonal
        if segment_info["phase"] == "luteal":
            strategy["modifications_needed"].append("explicar_sensibilidad_progesterona")
        elif segment_info["phase"] == "folicular":
            strategy["modifications_needed"].append("aprovechar_energia_creciente")
        
        return strategy
```

## Creación de Chunks Adaptativos

La clave está en crear chunks que mantienen la información médica esencial pero incluyen metadatos muy específicos sobre cómo debe presentarse para cada segmento. Esto nos permite tener **un chunk base** con **múltiples versiones de presentación**.

```
def create_adaptive_chunk(self, base_content: str, multi_segment_analysis: Dict) -> List[ContentChunk]:
    """
    Crea múltiples versiones del mismo chunk base, cada una optimizada
    para los segmentos más relevantes.
    """
    
    adaptive_chunks = []
    
    # Agrupar segmentos por estrategia de presentación similar
    presentation_groups = self.group_segments_by_presentation(multi_segment_analysis)
    
    for group_key, segments_in_group in presentation_groups.items():
        # Crear una versión del chunk optimizada para este grupo de segmentos
        adapted_chunk = ContentChunk(
            content=base_content,
            metadata={
                "applicable_segments": list(segments_in_group.keys()),
                "segment_scores": {seg_id: seg_data["relevance_score"] 
                                 for seg_id, seg_data in segments_in_group.items()},
                "presentation_strategy": group_key,
                "adaptation_instructions": self.create_adaptation_instructions(segments_in_group),
                "content_versatility": len(segments_in_group)  # Qué tan versátil es este chunk
            },
            chunk_id=f"{hashlib.md5(base_content.encode()).hexdigest()[:8]}_{group_key}",
            source_document=doc_metadata["source_file"],
            confidence_score=self.calculate_confidence_for_group(segments_in_group)
        )
        
        adaptive_chunks.append(adapted_chunk)
    
    return adaptive_chunks

def create_adaptation_instructions(self, segments_group: Dict) -> Dict:
    """
    Crea instrucciones específicas sobre cómo adaptar el contenido base
    cuando se presente a los segmentos en este grupo.
    """
    
    common_needs = self.identify_common_needs(segments_group)
    common_preferences = self.identify_common_presentation_preferences(segments_group)
    
    return {
        "tone_adjustments": common_preferences["tone"],
        "emphasis_points": common_needs,
        "avoid_elements": self.identify_elements_to_avoid(segments_group),
        "additional_context_needed": self.identify_additional_context_needs(segments_group)
    }
    
    

```

## El Resultado: Chunks Inteligentes y Versátiles

Lo que obtenemos al final de este proceso es una base de conocimientos donde cada pieza de información no solo conoce su contenido, sino que también conoce exactamente cómo debe presentarse para maximizar su utilidad para cada segmento específico.

Cuando una usuaria "Lútea Ansiosa" pregunta sobre manejo del estrés, el sistema no solo encuentra contenido relevante sobre estrés, sino que encuentra específicamente contenido que ha sido pre-analizado como altamente útil para su combinación de fase lútea y estado ansioso, y que incluye instrucciones sobre cómo presentar esa información con el tono y enfoque que mejor resonará con ella.

Esto significa que el mismo documento médico sobre técnicas de respiración se convierte en múltiples recursos específicos: uno optimizado para usuarias estresadas que necesita validación emocional primero, otro optimizado para usuarias melancólicas que necesita motivación, y otro para usuarias energéticas que busca optimización de rendimiento.

**La belleza de este sistema es que respeta tanto la integridad del conocimiento médico original como las necesidades específicas de personalización.** No estamos fragmentando arbitrariamente la información médica, sino que estamos creando múltiples lentes a través de los cuales la misma información puede ser vista y aplicada de maneras que sean más útiles para cada usuaria específica.