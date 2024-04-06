import pandas as pd
from logging_config import setup_logging
import json
from undo_functions import apply_differences

# Inicializa el logging
logger = setup_logging()

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


#----------------------------------------------
# Funcion para deshacer cambios
#----------------------------------------------

def undo_changes(df: pd.DataFrame, changes_file: str) -> pd.DataFrame:
    # Cargar diferencias desde el archivo
    try:
        with open(changes_file, 'r') as file:
            differences = json.load(file)
    except Exception as error:
        logger.error(f"Error al cargar las diferencias: {error}")
        raise error

    # Aplicar diferencias inversas (Este paso necesita implementación detallada basada en tu estructura de diferencias)

    df = apply_differences(df, differences)

    logger.info("Cambios deshechos exitosamente.")
    return df  # Devuelve el DataFrame con los cambios deshechos