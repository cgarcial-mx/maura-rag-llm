# config/database.py
# Este archivo no es necesario para tu caso actual, pero lo creo por si lo necesitas después
import os
from config.settings import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD

def get_postgres_connection():
    """
    Obtiene conexión a PostgreSQL (para uso futuro)
    """
    try:
        import psycopg2
        return psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
    except ImportError:
        print("psycopg2 no está instalado. Para usar PostgreSQL, instala: pip install psycopg2-binary")
        return None