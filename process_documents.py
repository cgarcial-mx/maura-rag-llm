# python-scripts/process_documents.py

import os
import sys
from pathlib import Path
import logging
from typing import List

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent))

from document_processor.pdf_processor import MedicalDocumentProcessor
from config.settings import CHROMA_HOST, CHROMA_PORT, MISTRAL_API_KEY

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def process_pdfs_in_folder(pdf_folder: str):
    """
    Procesa todos los PDFs en una carpeta y los sube a Chroma DB
    """
    try:
        # Inicializar procesador
        processor = MedicalDocumentProcessor(
            chroma_host=CHROMA_HOST,
            chroma_port=CHROMA_PORT,
            mistral_api_key=MISTRAL_API_KEY
        )
        
        # Obtener lista de PDFs
        pdf_path = Path(pdf_folder)
        pdf_files = list(pdf_path.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning(f"No se encontraron PDFs en {pdf_folder}")
            return
        
        logger.info(f"Procesando {len(pdf_files)} PDFs...")
        
        for pdf_file in pdf_files:
            try:
                logger.info(f"Procesando: {pdf_file.name}")
                
                # Procesar documento
                chunks = processor.process_document(str(pdf_file))
                
                logger.info(f"✓ {pdf_file.name}: {len(chunks)} chunks procesados")
                
                # Mover a carpeta de procesados
                processed_path = Path("data/processed") / pdf_file.name
                pdf_file.rename(processed_path)
                
            except Exception as e:
                logger.error(f"Error procesando {pdf_file.name}: {e}")
                continue
        
        logger.info("✓ Procesamiento completado")
        
    except Exception as e:
        logger.error(f"Error en procesamiento: {e}")
        raise

if __name__ == "__main__":
    # Procesar PDFs en la carpeta data/pdfs
    pdf_folder = "data/pdfs"
    
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
        logger.info(f"Carpeta creada: {pdf_folder}")
        logger.info("Coloca tus PDFs en esta carpeta y ejecuta el script nuevamente")
    else:
        process_pdfs_in_folder(pdf_folder)