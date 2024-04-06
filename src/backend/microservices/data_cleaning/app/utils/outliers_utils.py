from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler 
from logging_config import setup_logging


# Inicializa el logging
logger = setup_logging()

# Funcion para eliminar valores atípicos en un DataFrame usando la regla del rango intercuartílico

def outliers_remove(df, constant_value=1.5):
    '''Función para eliminar valores atípicos en un DataFrame.
    Parámetros:
    - df: DataFrame de pandas.
    Retorna:
    - DataFrame sin valores atípicos.'''

    logger.info("Inicio de eliminacion de valores atipicos")

    try:
        for col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df = df[(df[col] >= Q1 - constant_value * IQR) & (df[col] <= Q3 + constant_value * IQR)]

    except Exception as error:
        return str(f'Error eliminando valores atipicos: {error}')
    
    return df


def outliers_clip(df, constant_value=1.5):
    '''Función para reemplazar valores atípicos con valores máximos/mínimos en un DataFrame.
    Parámetros:
    - df: DataFrame de pandas.
    Retorna:
    - DataFrame con valores atípicos reemplazados.'''


    logger.info("Inicio de reemplazo de valores atipicos")
    try:
        for col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df[col] = df[col].clip(lower=Q1 - constant_value * IQR, upper=Q3 + constant_value * IQR)
    except Exception as error:
        return str(f'Error reemplazando valores atipicos: {error}')
    return df


# Funcion para tratar los outliers dependiendo del metodo seleccionado
def outliers(df, method):
        '''Función para tratar valores atípicos en un DataFrame.
        Parámetros:
        - df: DataFrame de pandas.
        - method: Método para tratar valores atípicos. Opciones: 'remove', 'clip'.
        Retorna:
        - DataFrame con valores atípicos tratados.'''

        logger.info("Inicio de tratamiento de valores atipicos")

        # Trata valores atípicos según el método seleccionado
        
        # Elimina valores atípicos, si el método es 'remove'
        if method == 'remove':
            logger.info("Eliminando valores atipicos con metodo remove")
            
            try:
                df = outliers_remove(df)

            except Exception as error:
                return str(f'Error eliminando valores atipicos: {error}')
            
            logger.info("Valores atipicos eliminados")
            return df
        
        # Reemplaza valores atípicos con valores máximos/mínimos, si el método es 'clip'
        elif method == 'clip':
            logger.info("Reemplazando valores atipicos con valores maximos/minimos")
            try:
                df = outliers_clip(df)
                
            except Exception as error:
                return str(f'Error reemplazando valores atipicos con valores maximos/minimos: {error}')
            
            logger.info("Valores atipicos reemplazados")
            return df
        
        else:
            return "Método no válido. Por favor, seleccione un método de tratamiento de valores atípicos."