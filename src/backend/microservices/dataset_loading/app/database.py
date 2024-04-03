import logging
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASS, DB_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Función para conectar a la base de datos
def connect_to_database():

    logger.info("Conectando a la base de datos...")
    logger.info(f"Host: {DB_HOST}, User: {DB_USER}, Database: {DB_NAME}")

    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )