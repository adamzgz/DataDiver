import numpy as np
from sklearn.preprocessing import  MinMaxScaler
from logging_config import setup_logging


# Inicializa el logging
logger = setup_logging()

# Funcion para normalizar un DataFrame utilizando MinMaxScaler
def normalize_min_max(df):

    '''Función para normalizar un DataFrame utilizando MinMaxScaler.
    
    Parámetros:
    - df: DataFrame de pandas.

    Retorna:
    - DataFrame normalizado.
    '''
    logger.info("Inicio de la normalizacion MinMaxScaler")
    # Selecciona solo columnas numéricas
    try:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
    
        # Aplica MinMaxScaler solo a las columnas numéricas
        scaler = MinMaxScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    except Exception as error:
        return str(f'Error normalizando con MinMaxScaler: {error}')
    
    return df

def estandarizacion(df):
    for col in df.columns:
        df[col] = (df[col] - df[col].mean()) / df[col].std()
    return df