# Importar librerias
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler 
import logging



# Inicializa el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#----------------------------------------------
# Funcion para guardar las modificaciones
#----------------------------------------------

def save_dataset_cleaned(df, file_path):
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

def estandarizacion(df):
    for col in df.columns:
        df[col] = (df[col] - df[col].mean()) / df[col].std()
    return df

# ----------------------------------------------
# Funciones dependientes de opciones
# ----------------------------------------------

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

# ----------------------------------------------
# Funcion CORE
# ----------------------------------------------
        

# Funcion para comprobar la opcion de limpieza seleccionada en el frontend
def data_cleaning(df, options, file_path):

    # Guardar el estado anterior del DataFrame para deshacer
    estado_anterior = df.copy()

    '''Funcion general para limpiar un DataFrame de acuerdo a las opciones seleccionadas.
    
    Parámetros:
    - df: DataFrame de pandas.
    - options: Diccionario con las opciones de limpieza seleccionadas.
    - file_path: Ruta del archivo original.

    Retorna según la opción seleccionada:
    - Para opciones de identificación devuelve la respuesta.
    - Para opciones de tratatamiento, devuelve la ruta del archivo CSV con el DataFrame limpio.
    
    '''

    # Identificar valores duplicados si check_duplicates es True

    if options.get('check_duplicates'):
        logger.info("Inicio de la funcion check_duplicates")
        
        try:
            duplicates = df.duplicated().sum()

        except Exception as error:
            return str(f'Error identificando datos duplicados: {error}')
        
        message = f"Se han encontrado {duplicates} filas duplicadas"

        return file_path, message


    # Eliminar valores duplicados, si remove_duplicates es True
        
    if options.get('remove_duplicates'):

        logger.info("Inicio de la funcion remove_duplicates")
        try:
            df, message = remove_duplicates(df)

        except Exception as error:
            return str(f'Error eliminando datos duplicados: {error}')
        
        logger.info("Datos duplicados eliminados")

        try:
            cleaned_dataset_path = save_dataset_cleaned(df, file_path)

        except Exception as error:
            return str(f'Error guardando el archivo limpio: {error}')

        return cleaned_dataset_path, message
    
    
    # Contar valores nulos

    if options.get('count_missing_values'):
        
        logger.info("Inicio de la funcion count_missing_values")

        # Contamos los valores nulos
        try:
            missing_values = df.isnull().sum()
        
        except Exception as error:
            return str(f'Error contando valores nulos: {error}')
        

        # Como los valores nulos son un objeto de pandas, lo convertimos a un diccionario para poder devolverlo como mensaje.
        try:
            message = missing_values.to_dict()
        
        except Exception as error:
            return str(f'Error convirtiendo valores nulos a diccionario: {error}')

        return file_path, message
    

    # Tratamiento de valores nulos

    if options.get('treat_missing_values'):
        logger.info("Inicio de la funcion treat_missing_values")

        # Comprobamos que metodo se ha seleccionado
        method = options['treat_missing_values']

        # lanzamos la funcion de tratamiento de valores nulos
        logger.info("Tratando valores nulos")
        try:
            df,message = treat_missing_values(df, method)
        
        except Exception as error:
            return str(f'Error tratando valores nulos: {error}')
        
        logger.info("Valores nulos tratados")

        logger.info("Guardando el archivo limpio en la nueva ruta")
        try:
            cleaned_dataset_path = save_dataset_cleaned(df, file_path)
        
        except Exception as error:
            return str(f'Error guardando el archivo limpio: {error}')

        return cleaned_dataset_path, message
        
    # Eliminar datos atipicos
    if options.get('outliers') == 'remove':

        logger.info("Inicio de la funcion outliers")

        try:
            logger.info("Eliminando valores atipicos con la funcion remove")
            df = outliers(df, 'remove')
        
        except Exception as error:
            return str(f'Error eliminando valores atipicos: {error}')
        
        try:
            logger.info("Guardando el archivo limpio en la nueva ruta")
            cleaned_dataset_path = save_dataset_cleaned(df, file_path)
        
        except Exception as error:
            return str(f'Error guardando el archivo limpio: {error}')
        
        message = "Valores atípicos eliminados"
        
        return cleaned_dataset_path, message


    # Reemplazar datos atipicos con valores maximos/minimos
    elif options.get('outliers') == 'clip':

        logger.info("Inicio de la funcion outliers")
        try:
            logger.info("Reemplazando valores atipicos con valores maximos/minimos")
            df = outliers(df, 'clip')

        except Exception as error:
            return str(f'Error reemplazando valores atipicos: {error}')
        
        try:
            logger.info("Guardando el archivo limpio en la nueva ruta")
            cleaned_dataset_path = save_dataset_cleaned(df, file_path)
        
        except Exception as error:
            return str(f'Error guardando el archivo limpio: {error}')
        
        message = "Valores atípicos reemplazados"

        return cleaned_dataset_path, message

# Normalización de datos
            
    # Normalizacion entre 0 y 1 (KNN, Redes Neuronales)
    if options.get('normalization') == 'min_max':

        logger.info("Inicio de la normalizacion MinMaxScaler")
        try:
            df = normalize_min_max(df,file_path)

        except Exception as error:
            return str(f'Error normalizando con MinMaxScaler: {error}')
    
        try:
            logger.info("Guardando el archivo limpio en la nueva ruta")
            cleaned_dataset_path = save_dataset_cleaned(df, file_path)
        
        except Exception as error:
            return str(f'Error guardando el archivo limpio: {error}')
        
        return cleaned_dataset_path, message

    
    # Estandarizacion (Distribucion normal con media 0 y desviacion estandar 1, SVM, Regresion Lineal)
    elif options.get('normalization') == 'estandarizacion':

        logger.info("Inicio de la estandarizacion")
        try:
            df = estandarizacion(df)

        except Exception as error:
            return str(f'Error estandarizando: {error}')
        
        try:
            logger.info("Guardando el archivo limpio en la nueva ruta")
            cleaned_dataset_path = save_dataset_cleaned(df, file_path)
        
        except Exception as error:
            return str(f'Error guardando el archivo limpio: {error}')
        
        message = "Datos estandarizados"
        
        return cleaned_dataset_path, message


# Codificación de variables categóricas
    
    # Codificacion binaria
    if options.get('encoding') == 'one_hot':

        try:
            logger.info("Inicio de la codificacion one_hot")
            df = pd.get_dummies(df,file_path)

        except Exception as error:
            return str(f'Error codificando variables categoricas: {error}')
        
        try:
            logger.info("Guardando el archivo limpio en la nueva ruta")
            cleaned_dataset_path = save_dataset_cleaned(df, file_path)
        
        except Exception as error:
            return str(f'Error guardando el archivo limpio: {error}')
        
        message = "Variables categoricas codificadas"
        
        return cleaned_dataset_path, message


    # Codificacion ordinal
    if options.get('encoding') == 'ordinal':

        try:

            label_encoder = LabelEncoder()
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = label_encoder.fit_transform(df[col])

        except Exception as error:
            return str(f'Error codificando variables categoricas: {error}')
        
        try:
            logger.info("Guardando el archivo limpio en la nueva ruta")
            cleaned_dataset_path = save_dataset_cleaned(df, file_path)
        
        except Exception as error:
            return str(f'Error guardando el archivo limpio: {error}')
        
        message = "Variables categoricas codificadas"
        
        return cleaned_dataset_path, message

    # Eliminar columnas
    if options.get('drop_columns'):
        logger.info("Inicio de la eliminacion de columnas")

        try:

            df = df.drop(columns=options['drop_columns'])
        
        except Exception as error:
            return str(f'Error eliminando columnas: {error}')
        
        try:
            logger.info("Guardando el archivo limpio en la nueva ruta")
            cleaned_dataset_path = save_dataset_cleaned(df, file_path)
        
        except Exception as error:
            return str(f'Error guardando el archivo limpio: {error}')
        
        return cleaned_dataset_path, message
    
    # Mostrar informacion del dataset
    if options.get('show_info'):
        logger.info("Mostrando informacion del dataset")

        message = df.info()
        return file_path, message
    
    
    # Conversión de tipos de datos de una columna (por ejemplo, de string a float, de int a datetime, etc.).

    if options.get('change_data_type'):

        # Cambiar el tipo de datos de las columnas seleccionadas
        try:
            logger.info("Cambiando el tipo de datos de las columnas seleccionadas")

            for col, dtype in options['change_data_type'].items():
                df[col] = df[col].astype(dtype)
        
        except Exception as error:
            return str(f'Error cambiando el tipo de datos de las columnas: {error}')
        
        try:
            logger.info("Guardando el archivo limpio en la nueva ruta")
            cleaned_dataset_path = save_dataset_cleaned(df, file_path)

        except Exception as error:
            return str(f'Error guardando el archivo limpio: {error}')
        
        message = "Tipo de datos de las columnas cambiado"

        return cleaned_dataset_path, message
        
        
# Manejo de strings: Operaciones específicas para datos de tipo string, como:
        
    # Convertir a mayúsculas 
    if options.get('string_operations') == 'upper':
        logger
        try:
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].str.upper()
        except Exception as error:
            return str(f'Error convirtiendo a mayusculas: {error}')
        
        try:
            logger.info("Guardando el archivo limpio en la nueva ruta")
            cleaned_dataset_path = save_dataset_cleaned(df, file_path)
        
        except Exception as error:
            return str(f'Error guardando el archivo limpio: {error}')
        
        message = "Datos convertidos a mayúsculas"

        return cleaned_dataset_path, message
    
    # Convertir a minusculas
    if options.get('string_operations') == 'lower':

        try:
            logger.info("Convirtiendo a minusculas")

            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].str.lower()

        except Exception as error:
            return str(f'Error convirtiendo a minusculas: {error}')
        
        try:
            logger.info("Guardando el archivo limpio en la nueva ruta")
            cleaned_dataset_path = save_dataset_cleaned(df, file_path)
        
        except Exception as error:
            return str(f'Error guardando el archivo limpio: {error}')
        
        message = "Datos convertidos a minúsculas"

        return cleaned_dataset_path, message
    
    # Eliminar espacios en blanco.
    if options.get('string_operations') == 'strip':
        logger.info("Eliminando espacios en blanco")

        try:
            logger.info("Eliminando espacios en blanco")
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].str.strip()
        
        except Exception as error:
            return str(f'Error eliminando espacios en blanco: {error}')
        
        try:
            logger.info("Guardando el archivo limpio en la nueva ruta")
            cleaned_dataset_path = save_dataset_cleaned(df, file_path)

        except Exception as error:
            return str(f'Error guardando el archivo limpio: {error}')
        
        message = "Espacios en blanco eliminados"

        return cleaned_dataset_path, message
    
    # Aplicar expresiones regulares para limpieza o extracción de datos.
    if options.get('string_operations') == 'regex':
        

        try:
            logger.info("Aplicando expresiones regulares")
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].str.replace(options['regex_pattern'], options['regex_replacement'])

        except Exception as error:
            return str(f'Error aplicando expresiones regulares: {error}')
        
        try:
            logger.info("Guardando el archivo limpio en la nueva ruta")
            cleaned_dataset_path = save_dataset_cleaned(df, file_path)
        
        except Exception as error:
            return str(f'Error guardando el archivo limpio: {error}')
        
        message = "Expresiones regulares aplicadas"
        
        return cleaned_dataset_path, message