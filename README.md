# python-scripts/README.md
# Scripts de Python para RAG de Salud Femenina

## Descripción
Scripts para procesar documentos médicos y generar contenido personalizado por segmentos.

## Estructura
- `document_processor/`: Procesamiento de PDFs y carga a Chroma DB
- `content_generator/`: Generación de contenido por segmentos
- `config/`: Configuración del sistema
- `data/`: Datos de entrada y salida
- `logs/`: Logs de procesamiento

## Uso

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
python -m spacy download es_core_news_sm
```

### 2. Configurar variables de entorno
```bash
export CHROMA_HOST="localhost"
export CHROMA_PORT="8000"
export MISTRAL_API_KEY="tu_api_key"  # Opcional
```

### 3. Procesar PDFs
```bash
python process_documents.py
```

### 4. Generar contenido por segmentos
```bash
python generate_content.py
```

## Archivos de entrada/salida
- **Entrada**: PDFs en `data/pdfs/`
- **Salida**: 
  - Chunks en Chroma DB
  - Contenido generado en `data/exports/`
  - Logs en `logs/`