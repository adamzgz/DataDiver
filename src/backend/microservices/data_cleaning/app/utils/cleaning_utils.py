from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler 
from logging_config import setup_logging
from dataset_utils import save_dataset_cleaned, deshacer


# Inicializa el logging
logger = setup_logging()

#----------------------------------------------
# Funciones de operaciones de limpieza
#----------------------------------------------

# Funcion para identificar y eliminar valores duplicados en un DataFrame
def remove_duplicates(df):

    '''Función para identificar y eliminar valores duplicados en un DataFrame.

    Parámetros:
    - df: DataFrame de pandas.

    Retorna:    
    - df: DataFrame sin valores duplicados.
    - message: Mensaje indicando si se han eliminado filas duplicadas o no y cuantas se han eliminado.'''

    logger.info("Inicio de la funcion remove_duplicates") 
    try:
        duplicates = df.duplicated().sum()

        if duplicates > 0:
            df = df.drop_duplicates()           
            message = f"Se han eliminado {duplicates} filas duplicadas"

            return df, message
        else: 
            return df, "No se han encontrado filas duplicadas"
    except Exception as error:
        return df, str(f'Error eliminando datos duplicados{error}') 
    
