import pandas as pd
import logging

# Inicializa el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def load_data(file_location: str):
    logger.info("Inicio de carga de archivo")
    try:
        # Identifica el tipo de archivo por su extensión y carga el DataFrame correspondiente
        if file_location.endswith('.csv'):
            df = pd.read_csv(file_location)
            logger.info("Archivo CSV cargado exitosamente")

        elif file_location.endswith('.xlsx') or file_location.endswith('.xls'):
            df = pd.read_excel(file_location)
            logger.info("Archivo Excel cargado exitosamente")

        elif file_location.endswith('.json'):
            df = pd.read_json(file_location)
            logger.info("Archivo JSON cargado exitosamente")

        else:
            raise Exception("Formato de archivo no soportado")
        
    except Exception as error:
        logger.error(f"Error al cargar el archivo: {error}")
        raise
    
    return df