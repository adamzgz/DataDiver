# Importar librerias
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder 

# Funcion para comprobar la opcion de limpieza seleccionada en el frontend

def remove_duplicates(df):

    '''Función para identificar y remover valores duplicados en un DataFrame.
    Parámetros:
    - df: DataFrame de pandas.
    Retorna:
    - Mensaje indicando si se encontraron y eliminaron filas duplicadas, o si no se encontraron.'''

    duplicates = df.duplicated().sum()
    try:
        if duplicates > 0:
            df = df.drop_duplicates()
            return "Se han eliminado {} filas duplicadas".format(duplicates)
        else:
            return "No se han encontrado filas duplicadas"
    except Exception as error:
        return str(error)    


def data_cleaning(df, options):

    # Identificar valores duplicados

    if options.get('check_duplicates'):
        duplicates = df.duplicated().sum()
        
        return duplicates


    # Eliminar valores duplicados
        
    if options.get('remove_duplicates'):
        return remove_duplicates(df)
    
    # Contar valores nulos

    if options.get('count_missing_values'):
        missing_values = df.isnull().sum()
        missing_values = missing_values.to_dict()
        return missing_values
    
    # Tratamiento valores nulos

    # Imputar la media
    if options.get('treat_missing_values') == 'mean':
        df = df.fillna(df.mean())
        return df

    # Imputar la mediana

    elif options.get('treat_missing_values') == 'median':
        df = df.fillna(df.median())
        return df

    # Imputar la moda
    elif options.get('treat_missing_values') == 'mode':
        df = df.fillna(df.mode().iloc[0])
        return df

    # Eliminar filas con valores nulos
    elif options.get('treat_missing_values') == 'drop_rows':
        df = df.dropna()
        return df
    
    # Eliminar columnas con valores nulos
    elif options.get('treat_missing_values') == 'drop_columns':
        df = df.dropna(axis=1)
        return df

    # Rellenar con un valor constante
    elif options.get('treat_missing_values') == 'constant':
        df = df.fillna(options['constant_value'])
        return df


    # Tratamiento de datos atipicos
        
    # Eliminar datos atipicos
    if options.get('outliers') == 'remove':
        for col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]
        return df


    # Reemplazar datos atipicos con valores maximos/minimos
    elif options.get('outliers') == 'clip':
        for col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df[col] = df[col].clip(lower=Q1 - 1.5 * IQR, upper=Q3 + 1.5 * IQR)
        return df

# Normalización de datos
            
    # Normalizacion entre 0 y 1 (KNN, Redes Neuronales)
    if options.get('normalization') == 'min_max':
        for col in df.columns:
            df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
        return df

    
    # Estandarizacion (Distribucion normal con media 0 y desviacion estandar 1, SVM, Regresion Lineal)
    elif options.get('normalization') == 'estandarizacion':
        for col in df.columns:
            df[col] = (df[col] - df[col].mean()) / df[col].std()
        return df


# Codificación de variables categóricas
    
    # Codificacion binaria
    if options.get('encoding') == 'one_hot':
        df = pd.get_dummies(df)
        return df


    # Codificacion ordinal
    if options.get('encoding') == 'ordinal':
        label_encoder = LabelEncoder()
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = label_encoder.fit_transform(df[col])
        return df

    # Eliminar columnas
    if options.get('drop_columns'):
        df = df.drop(columns=options['drop_columns'])
        return df
    
    # Mostrar informacion del dataset
    if options.get('show_info'):
        return df.info()
    
    # Conversión de tipos de datos de una columna (por ejemplo, de string a float, de int a datetime, etc.).

    if options.get('change_data_type'):
        for col, dtype in options['change_data_type'].items():
            df[col] = df[col].astype(dtype)
            return df
    
# Manejo de strings: Operaciones específicas para datos de tipo string, como:
        
    # Convertir a mayúsculas 
    if options.get('string_operations') == 'upper':
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.upper()
        return df
    
    # Convertir a minusculas
    if options.get('string_operations') == 'lower':
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.lower()
        return df
    
    # Eliminar espacios en blanco.
    if options.get('string_operations') == 'strip':
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()
        return df
    
    # Aplicar expresiones regulares para limpieza o extracción de datos.
    if options.get('string_operations') == 'regex':
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.replace(options['regex_pattern'], options['regex_replacement'])
        return df
    
    

    
