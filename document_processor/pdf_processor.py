# document_processor/pdf_processor.py
import os
import json
import hashlib
import requests
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import logging
from dataclasses import dataclass

# Librerías de procesamiento de documentos
import PyPDF2
import pdfplumber
from sentence_transformers import SentenceTransformer

# Librerías de análisis de texto
import spacy
import re

# Cliente de Chroma
import chromadb

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ContentChunk:
    """Representa un chunk de contenido procesado"""
    chunk_id: str
    content: str
    metadata: Dict
    source_document: str
    confidence_score: float
    processing_method: str
    embedding: Optional[List[float]] = None

class MedicalDocumentProcessor:
    def __init__(self, chroma_host: str = "localhost", chroma_port: int = 8000, mistral_api_key: str = None):
        """
        Inicializa el procesador de documentos médicos
        """
        logger.info("Inicializando MedicalDocumentProcessor...")
        
        try:
            # Inicializar modelo de embeddings
            logger.info("Cargando modelo de embeddings...")
            self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2', device='cpu')
            logger.info("✓ Modelo de embeddings cargado correctamente (usando CPU)")
            
            # Conectar con Chroma
            logger.info("Conectando con Chroma DB...")
            self.chroma_client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
            logger.info("✓ Conectado a Chroma DB")
            
            # Cargar modelo de spaCy para español
            logger.info("Cargando modelo de spaCy...")
            self.nlp = spacy.load('es_core_news_sm')
            logger.info("✓ Modelo de spaCy cargado")
            
            # Definir patrones de segmentación
            self.segment_patterns = self._initialize_segment_patterns()
            
            # Crear colección en Chroma si no existe
            self._setup_chroma_collection()
            
            logger.info("✓ MedicalDocumentProcessor inicializado completamente")
            
        except Exception as e:
            logger.error(f"Error durante la inicialización: {e}")
            raise
    
    def _initialize_segment_patterns(self) -> Dict:
        """
        Define los patrones para identificar contenido relevante para cada segmento
        """
        return {
            'folicular': {
                'keywords': {
                    'es': ['renovación', 'energía creciente', 'estrógeno', 'motivación', 'nuevos proyectos', 'crecimiento'],
                    'en': ['renewal', 'growing energy', 'estrogen', 'motivation', 'new projects', 'growth']
                },
                'emotional_indicators': {
                    'es': ['optimismo', 'planificación', 'socialización', 'creatividad', 'confianza'],
                    'en': ['optimism', 'planning', 'socialization', 'creativity', 'confidence']
                }
            },
            'ovulatoria': {
                'keywords': {
                    'es': ['pico hormonal', 'fertilidad', 'confianza', 'comunicación', 'liderazgo', 'atracción'],
                    'en': ['hormonal peak', 'fertility', 'confidence', 'communication', 'leadership', 'attraction']
                },
                'emotional_indicators': {
                    'es': ['carisma', 'decisión', 'networking', 'expresividad', 'liderazgo'],
                    'en': ['charisma', 'decision', 'networking', 'expressiveness', 'leadership']
                }
            },
            'lutea': {
                'keywords': {
                    'es': ['progesterona', 'introspección', 'sensibilidad', 'perfeccionismo', 'nesting', 'preparación'],
                    'en': ['progesterone', 'introspection', 'sensitivity', 'perfectionism', 'nesting', 'preparation']
                },
                'emotional_indicators': {
                    'es': ['crítica', 'análisis', 'organización', 'emociones intensas', 'reflexión'],
                    'en': ['criticism', 'analysis', 'organization', 'intense emotions', 'reflection']
                }
            },
            'menstrual': {
                'keywords': {
                    'es': ['renovación', 'descanso', 'intuición', 'reflexión', 'liberación', 'limpieza'],
                    'en': ['renewal', 'rest', 'intuition', 'reflection', 'liberation', 'cleaning']
                },
                'emotional_indicators': {
                    'es': ['introspección', 'sabiduría', 'claridad', 'reset emocional', 'descanso'],
                    'en': ['introspection', 'wisdom', 'clarity', 'emotional reset', 'rest']
                }
            }
        }
    
    def _setup_chroma_collection(self):
        """
        Configura la colección en Chroma para almacenar el conocimiento médico
        """
        try:
            # Intentar obtener la colección existente
            self.collection = self.chroma_client.get_collection("salud_femenina_knowledge")
            logger.info("✓ Colección existente recuperada")
        except:
            # Crear nueva colección si no existe
            self.collection = self.chroma_client.create_collection(
                name="salud_femenina_knowledge",
                metadata={"description": "Base de conocimientos sobre salud femenina y ciclo menstrual"}
            )
            logger.info("✓ Nueva colección creada")
    
    def process_document(self, pdf_path: str) -> List[ContentChunk]:
        """
        Procesa un documento PDF completo
        """
        logger.info(f"Procesando documento: {pdf_path}")
        
        try:
            # Extraer texto del PDF
            full_text, doc_metadata = self._extract_text_from_pdf(pdf_path)
            logger.info(f"Texto extraído: {len(full_text)} caracteres")
            
            # Crear chunks inteligentes
            chunks = self._create_intelligent_chunks(full_text, doc_metadata)
            logger.info(f"Chunks creados: {len(chunks)}")
            
            # Generar embeddings para cada chunk
            for chunk in chunks:
                chunk.embedding = self._generate_embedding(chunk.content)
            
            # Guardar en Chroma
            self._save_chunks_to_chroma(chunks)
            
            logger.info(f"✓ Documento procesado exitosamente: {len(chunks)} chunks guardados")
            return chunks
            
        except Exception as e:
            logger.error(f"Error procesando documento {pdf_path}: {e}")
            raise
    
    def _extract_text_from_pdf(self, pdf_path: str) -> Tuple[str, Dict]:
        """
        Extrae texto del PDF preservando estructura importante
        """
        full_text = ""
        document_metadata = {
            'source_file': Path(pdf_path).name,
            'file_size': os.path.getsize(pdf_path),
            'extraction_method': 'pdfplumber'
        }
        
        try:
            # Usar pdfplumber para mejor preservación de estructura
            with pdfplumber.open(pdf_path) as pdf:
                document_metadata['total_pages'] = len(pdf.pages)
                
                for page_num, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        # Limpiar pero preservar estructura médica
                        cleaned_text = self._clean_medical_text(page_text)
                        full_text += f"\n--- Página {page_num + 1} ---\n{cleaned_text}\n"
                        
        except Exception as e:
            logger.warning(f"pdfplumber falló, usando PyPDF2 como fallback: {e}")
            # Fallback a PyPDF2
            full_text = self._fallback_pdf_extraction(pdf_path)
            document_metadata['extraction_method'] = 'PyPDF2_fallback'
        
        return full_text, document_metadata
    
    def _clean_medical_text(self, text: str) -> str:
        """
        Limpia el texto preservando información médica importante
        """
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text)
        
        # Preservar términos médicos importantes
        medical_terms = [
            'hormona', 'estrógeno', 'progesterona', 'testosterona', 'cortisol',
            'ciclo', 'menstruación', 'ovulación', 'folicular', 'lútea',
            'FSH', 'LH', 'endometrio', 'folículo', 'cuerpo lúteo'
        ]
        
        # Remover caracteres especiales pero preservar estructura
        text = re.sub(r'[^\w\s.,;:()\-áéíóúñ]', '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def _fallback_pdf_extraction(self, pdf_path: str) -> str:
        """
        Extracción de texto usando PyPDF2 como fallback
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            logger.error(f"Error en extracción fallback: {e}")
            raise
    
    def _create_intelligent_chunks(self, text: str, doc_metadata: Dict) -> List[ContentChunk]:
        """
        Divide el texto en chunks semánticamente coherentes
        """
        chunks = []
        
        # Dividir por secciones naturales
        sections = self._identify_document_sections(text)
        
        for section in sections:
            # Crear chunks de tamaño apropiado
            section_chunks = self._split_section_into_chunks(section, max_words=400)
            
            for chunk_text in section_chunks:
                # Generar metadata específica
                chunk_metadata = self._analyze_chunk_content(chunk_text)
                
                # Crear ID único
                chunk_id = hashlib.md5(chunk_text.encode()).hexdigest()[:12]
                
                chunk = ContentChunk(
                    chunk_id=chunk_id,
                    content=chunk_text,
                    metadata={**chunk_metadata, **doc_metadata},
                    source_document=doc_metadata['source_file'],
                    confidence_score=self._calculate_content_confidence(chunk_text),
                    processing_method="local_extraction"
                )
                
                chunks.append(chunk)
        
        return chunks
    
    def _identify_document_sections(self, text: str) -> List[str]:
        """
        Identifica secciones temáticas en el documento
        """
        # Dividir por párrafos
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # Agrupar párrafos relacionados
        sections = []
        current_section = []
        
        for paragraph in paragraphs:
            if len(current_section) == 0 or self._paragraphs_are_related(current_section[-1], paragraph):
                current_section.append(paragraph)
            else:
                if current_section:
                    sections.append('\n\n'.join(current_section))
                current_section = [paragraph]
        
        # Agregar última sección
        if current_section:
            sections.append('\n\n'.join(current_section))
        
        return sections
    
    def _paragraphs_are_related(self, para1: str, para2: str) -> bool:
        """
        Determina si dos párrafos están temáticamente relacionados
        """
        # Usar embeddings para calcular similitud
        try:
            emb1 = self.embedding_model.encode([para1])[0]
            emb2 = self.embedding_model.encode([para2])[0]
            
            # Calcular similitud coseno
            similarity = self._cosine_similarity(emb1, emb2)
            return similarity > 0.7  # Threshold de similitud
        except:
            # Fallback simple: verificar palabras clave comunes
            words1 = set(para1.lower().split())
            words2 = set(para2.lower().split())
            common_words = words1.intersection(words2)
            return len(common_words) > 3
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calcula similitud coseno entre dos vectores
        """
        import numpy as np
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _split_section_into_chunks(self, section: str, max_words: int = 400) -> List[str]:
        """
        Divide una sección en chunks de tamaño apropiado
        """
        words = section.split()
        chunks = []
        
        for i in range(0, len(words), max_words):
            chunk_words = words[i:i + max_words]
            chunk_text = ' '.join(chunk_words)
            if chunk_text.strip():
                chunks.append(chunk_text)
        
        return chunks
    
    def _analyze_chunk_content(self, chunk: str) -> Dict:
        """
        Analiza el contenido para asignar metadata específica
        """
        metadata = {
            'applicable_segments': [],
            'primary_topics': [],
            'emotional_relevance': [],
            'content_type': 'educational',
            'urgency_level': 'normal',
            'applicable_phases': []
        }
        
        # Usar spaCy para análisis profundo
        doc = self.nlp(chunk.lower())
        
        # Identificar fases del ciclo relevantes
        for phase, patterns in self.segment_patterns.items():
            if any(keyword in chunk.lower() for keyword in patterns['keywords']['en']): # Changed to English keywords
                metadata['applicable_phases'].append(phase)
        
        # Identificar estados emocionales relevantes
        emotional_indicators = self._identify_emotional_relevance(chunk)
        metadata['emotional_relevance'] = emotional_indicators
        
        # Determinar segmentos específicos aplicables
        metadata['applicable_segments'] = self._determine_applicable_segments(
            metadata['applicable_phases'], 
            emotional_indicators
        )
        
        # Identificar tipo de contenido
        metadata['content_type'] = self._classify_content_type(chunk)
        
        return metadata
    
    def _identify_emotional_relevance(self, chunk: str) -> List[str]:
        """
        Identifica indicadores emocionales en el contenido
        """
        emotional_keywords = {
            'ansiedad': ['ansiedad', 'estrés', 'preocupación', 'nerviosismo'],
            'tristeza': ['tristeza', 'melancolía', 'depresión', 'desánimo'],
            'energía': ['energía', 'vitalidad', 'motivación', 'entusiasmo'],
            'confianza': ['confianza', 'seguridad', 'autoestima', 'empoderamiento'],
            'conexión': ['conexión', 'socialización', 'empatía', 'comunicación']
        }
        
        relevant_emotions = []
        for emotion, keywords in emotional_keywords.items():
            if any(keyword in chunk.lower() for keyword in keywords):
                relevant_emotions.append(emotion)
        
        return relevant_emotions
    
    def _determine_applicable_segments(self, phases: List[str], emotions: List[str]) -> List[str]:
        """
        Mapea contenido a los segmentos específicos
        """
        # Mapeo simplificado - puedes expandir esto según tus 20 segmentos
        segment_mapping = {
            ('folicular', 'ansiedad'): ['SEG001'],  # Folicular Estresada
            ('folicular', 'energía'): ['SEG003'],   # Folicular Energética
            ('lutea', 'ansiedad'): ['SEG011'],      # Lútea Ansiosa
            ('menstrual', 'tristeza'): ['SEG017'],  # Menstrual Melancólica
        }
        
        applicable_segments = []
        for phase in phases:
            for emotion in emotions:
                key = (phase, emotion)
                if key in segment_mapping:
                    applicable_segments.extend(segment_mapping[key])
        
        return list(set(applicable_segments))
    
    def _classify_content_type(self, chunk: str) -> str:
        """
        Clasifica el tipo de contenido del chunk
        """
        content_indicators = {
            'lesson': ['explicación', 'información', 'educativo', 'aprender'],
            'nutrition': ['nutrición', 'alimentación', 'dieta', 'vitaminas'],
            'exercise': ['ejercicio', 'actividad física', 'deporte', 'movimiento'],
            'symptoms': ['síntomas', 'signos', 'molestias', 'dolor'],
            'wellness': ['bienestar', 'cuidado', 'autocuidado', 'equilibrio']
        }
        
        chunk_lower = chunk.lower()
        for content_type, indicators in content_indicators.items():
            if any(indicator in chunk_lower for indicator in indicators):
                return content_type
        
        return 'educational'
    
    def _calculate_content_confidence(self, chunk: str) -> float:
        """
        Calcula un score de confianza para el chunk
        """
        # Score base
        confidence = 0.5
        
        # Bonus por longitud apropiada
        word_count = len(chunk.split())
        if 100 <= word_count <= 500:
            confidence += 0.2
        
        # Bonus por términos médicos
        medical_terms = ['hormona', 'ciclo', 'menstruación', 'estrógeno', 'progesterona']
        medical_term_count = sum(1 for term in medical_terms if term in chunk.lower())
        confidence += min(medical_term_count * 0.1, 0.3)
        
        # Bonus por estructura clara
        if any(marker in chunk for marker in ['•', '-', '1.', '2.', 'Primero', 'Segundo']):
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _generate_embedding(self, text: str) -> List[float]:
        """
        Genera embedding para el texto
        """
        try:
            embedding = self.embedding_model.encode([text])[0]
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generando embedding: {e}")
            return []
    
    def _save_chunks_to_chroma(self, chunks: List[ContentChunk]):
        """
        Guarda los chunks en Chroma DB
        """
        try:
            # Preparar datos para Chroma
            documents = [chunk.content for chunk in chunks]
            metadatas = [chunk.metadata for chunk in chunks]
            ids = [chunk.chunk_id for chunk in chunks]
            embeddings = [chunk.embedding for chunk in chunks if chunk.embedding]
            
            # Solo incluir chunks con embeddings válidos
            valid_chunks = [(doc, meta, chunk_id, emb) 
                           for doc, meta, chunk_id, emb in zip(documents, metadatas, ids, embeddings)
                           if emb]
            
            if valid_chunks:
                docs, metas, ids, embs = zip(*valid_chunks)
                
                # Limpiar metadata para Chroma (convertir listas vacías a strings vacíos)
                cleaned_metas = []
                for meta in metas:
                    cleaned_meta = {}
                    for key, value in meta.items():
                        if isinstance(value, list):
                            if value:  # Si la lista tiene elementos, convertir a string
                                cleaned_meta[key] = ', '.join(str(item) for item in value)
                            else:  # Si la lista está vacía, usar string vacío
                                cleaned_meta[key] = ""
                        else:
                            cleaned_meta[key] = value
                    cleaned_metas.append(cleaned_meta)
                
                # Agregar a Chroma
                self.collection.add(
                    documents=list(docs),
                    metadatas=cleaned_metas,  # Usar cleaned_metas en lugar de list(metadatas)
                    ids=list(ids),
                    embeddings=list(embs)
                )
                
                logger.info(f"✓ {len(valid_chunks)} chunks guardados en Chroma")
            else:
                logger.warning("No hay chunks válidos para guardar")
                
        except Exception as e:
            logger.error(f"Error guardando chunks en Chroma: {e}")
            raise