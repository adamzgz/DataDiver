import pandas as pd
from logging_config import setup_logging

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

def save_dataset_cleaned(df, file_path, cleaned_existe):
    '''Funcion para guardar un DataFrame limpio en un nuevo archivo CSV
    
    Parámetros:
    - df: DataFrame de pandas.
    - file_path: Ruta del archivo original.

    Retorna:
    - Ruta del archivo CSV con el DataFrame limpio.
    
    '''
    # Crear una nueva ruta para el archivo limpio
    logger.info("Sustituyendo la extension del archivo original por _cleaned.csv")
    try:

    # comprueba si el archivo es _cleaned.csv
        if cleaned_existe:
            logger.info("El archivo ya es un archivo limpio")
            cleaned_file_path = file_path
        else:
            logger.info("El archivo no es un archivo limpio")
            cleaned_file_path = file_path.replace(".csv", "_cleaned.csv")
            
    except Exception as error:
        return str(f'Error cambiando la ruta del archivo: {error}')
    
    # Guardar el dataframe limpio en un nuevo archivo
    logger.info("Guardando el archivo limpio en la nueva ruta")
    try:
        df.to_csv(cleaned_file_path, index=False)
    except Exception as error:         
            return str(f'Error guardando el archivo limpio: {error}')

    # Devuelve la ruta del archivo limpio
    return cleaned_file_path

#----------------------------------------------
# Funcion para deshacer cambios
#----------------------------------------------

# Esta funcion está por terminar (DEBUG)
def deshacer(df, estado_anterior):
    '''Funcion para deshacer los cambios realizados en un DataFrame'''
    df = estado_anterior
    
    return df