# Importar librerias
import numpy as np
from logging_config import setup_logging

# Inicializa el logging
logger = setup_logging()


# Funcion para tratar valores nulos en un DataFrame

def treat_missing_values(df, method):
    
        '''Función para tratar valores nulos en un DataFrame.
        Parámetros:
        - df: DataFrame de pandas.
        - method: Método para tratar valores nulos. Opciones: 'mean', 'median', 'mode', 'drop_rows', 'drop_columns'.
        Retorna:
        - DataFrame con valores nulos tratados.'''

        logger.info("Inicio de tratamiento de valores nulos")

        # Selecciona solo columnas numéricas
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        # Trata valores nulos según el método seleccionado
        
        # Imputa la media, si el método es 'mean'
        if method == 'mean':
            logger.info("Imputando valores nulos con la media")
            logger.info("Numeric Cols: {}". format(numeric_cols) )
            try:
                
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            
            except Exception as error:
                return df, str(f'Error imputando valores nulos con la media: {error}')
            
            logger.info("Media Imputada")
            return df, str(f'Valores nulos imputados con la media')
    
        # Imputa la mediana, si el método es 'median'
        elif method == 'median':
            logger.info("Imputando valores nulos con la mediana")
            logger.info("Numeric Cols: {}". format(numeric_cols) )

            try:
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

            except Exception as error:
                return str(f'Error imputando valores nulos con la mediana: {error}')
            
            logger.info("Mediana Imputada")
            return df
        
        # Imputa la moda, si el método es 'mode'
        elif method == 'mode':
            logger.info("Imputando valores nulos con la moda")
            logger.info("Numeric Cols: {}". format(numeric_cols) )

            try:
                df = df.fillna(df.mode().iloc[0])

            except Exception as error:
                return str(f'Error imputando valores nulos con la moda: {error}')
            
            logger.info("Moda Imputada")
            return df
        
        # Elimina filas con valores nulos, si el método es 'drop_rows'
        elif method == 'drop_rows':
            logger.info("Eliminando filas con valores nulos")

            try:
                df = df.dropna()

            except Exception as error:
                return str(f'Error eliminando filas con valores nulos: {error}')
            
            logger.info("Filas con valores nulos eliminadas")
            return df
    
        # Elimina columnas con valores nulos, si el método es 'drop_columns'
        elif method == 'drop_columns':
            logger.info("Eliminando columnas con valores nulos")
            try:
                df = df.dropna(axis=1)
            
            except Exception as error:
                return str(f'Error eliminando columnas con valores nulos: {error}')
            
            logger.info("Columnas con valores nulos eliminadas")
            return df
    
        else:
            return "Método no válido. Por favor, seleccione un método de tratamiento de valores nulos."