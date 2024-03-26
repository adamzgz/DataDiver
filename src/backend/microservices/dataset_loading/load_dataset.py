import pandas as pd
from fastapi import UploadFile
import asyncio
import logging

# Inicializa el logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Inicio de carga de archivo")


# Realiza la carga de forma asincrona
async def load_data(file: UploadFile):
    loop = asyncio.get_running_loop()

    try:

        # Segun el tipo de archivo, se carga de una forma u otra

        if file.content_type == "text/csv":
            df = await loop.run_in_executor(None, pd.read_csv, file.file._file)
            logger.info("Archivo csv cargado exitosamente")

        elif file.content_type in ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
            df = await loop.run_in_executor(None, pd.read_excel, file.file._file)
            logger.info("Archivo excel cargado exitosamente")

        elif file.content_type == "application/json":
            df = await loop.run_in_executor(None, pd.read_json, file.file._file)
            logger.info("Archivo json cargado exitosamente")

        else:
            raise Exception("Formato de archivo no soportado.")
        
    # Captura cualquier excepcion, la guarda y la lanza la lanza
    except Exception as error:
        logger.error(f"Error al cargar el archivo: {error}")
        raise Exception(f"Error al cargar el archivo: {error}")


    return df