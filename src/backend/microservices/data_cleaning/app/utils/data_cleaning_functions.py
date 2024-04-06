# Importar librerias
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from logging_config import setup_logging
from dataset_utils import save_dataset_cleaned, deshacer
from cleaning_utils import remove_duplicates
from normalization_utils import normalize_min_max, estandarizacion
from outliers_utils import outliers
from missing_values_utils import treat_missing_values


# Inicializa el logging
logger = setup_logging()

# ----------------------------------------------
# Funcion CORE
# ----------------------------------------------

# Funcion para comprobar la opcion de limpieza seleccionada en el frontend
def data_cleaning(df, options, file_path, cleaned_existe):

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
            cleaned_dataset_path = save_dataset_cleaned(df, file_path,cleaned_existe)

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
            cleaned_dataset_path = save_dataset_cleaned(df, file_path,cleaned_existe)
        
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
            cleaned_dataset_path = save_dataset_cleaned(df, file_path,cleaned_existe)
        
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
            cleaned_dataset_path = save_dataset_cleaned(df, file_path,cleaned_existe)
        
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
            cleaned_dataset_path = save_dataset_cleaned(df, file_path,cleaned_existe)
        
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
            cleaned_dataset_path = save_dataset_cleaned(df, file_path,cleaned_existe)
        
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
            cleaned_dataset_path = save_dataset_cleaned(df, file_path,cleaned_existe)
        
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
            cleaned_dataset_path = save_dataset_cleaned(df, file_path,cleaned_existe)
        
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
            cleaned_dataset_path = save_dataset_cleaned(df, file_path,cleaned_existe)
        
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
            cleaned_dataset_path = save_dataset_cleaned(df, file_path,cleaned_existe)

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
            cleaned_dataset_path = save_dataset_cleaned(df, file_path,cleaned_existe)
        
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
            cleaned_dataset_path = save_dataset_cleaned(df, file_path,cleaned_existe)
        
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
            cleaned_dataset_path = save_dataset_cleaned(df, file_path,cleaned_existe)

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
            cleaned_dataset_path = save_dataset_cleaned(df, file_path,cleaned_existe)
        
        except Exception as error:
            return str(f'Error guardando el archivo limpio: {error}')
        
        message = "Expresiones regulares aplicadas"
        
        return cleaned_dataset_path, message