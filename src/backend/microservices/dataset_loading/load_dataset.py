import pandas as pd
from fastapi import UploadFile
import io
import logging

# Inicializa el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def load_data(file: UploadFile):
    logger.info("Inicio de carga de archivo")
    try:
        # Utiliza la API de UploadFile para leer el contenido del archivo
        contents = await file.read()
        # Dependiendo del tipo de archivo, decide cómo cargarlo en un DataFrame
        if file.content_type == "text/csv":
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
            logger.info("Archivo csv cargado exitosamente")

        elif file.content_type in ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
            df = pd.read_excel(io.BytesIO(contents))
            logger.info("Archivo excel cargado exitosamente")

        elif file.content_type == "application/json":
            df = pd.read_json(io.StringIO(contents.decode('utf-8')))
            logger.info("Archivo json cargado exitosamente")

        else:
            raise Exception("Formato de archivo no soportado.")
        
    except Exception as error:
        logger.error(f"Error al cargar el archivo: {error}")
        raise

    finally:
        # cierra el archivo subido después de usarlo
        await file.close()
    
    return df