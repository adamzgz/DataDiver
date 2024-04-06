from database import connect_to_database
import logging

# Inicializa el logging
logger = logging.getLogger(__name__)

def execute_query(query, params=None, fetchone=False, commit=False):
    """
    Función de utilidad para ejecutar consultas SQL con manejo de contextos para la conexión y el cursor.
    """
    with connect_to_database() as db:
        with db.cursor() as cursor:
            cursor.execute(query, params)
            if commit:
                db.commit()
                return cursor.lastrowid
            if fetchone:
                return cursor.fetchone()
            return None

def get_file_path(data_id):
    """
    Función para obtener la ruta de un dataset a partir de su ID.
    """
    result = execute_query(
        "SELECT file_path FROM datasets WHERE data_id = %s",
        (data_id,),
        fetchone=True
    )
    if result:
        return result[0]
    else:
        raise FileNotFoundError(f"Fichero no encontrado en el data id: {data_id}")

def insert_dataset(user_id, file_path):
    """
    Función para insertar un nuevo dataset en la base de datos y devolver su data_id.
    """
    data_id = execute_query(
        "INSERT INTO datasets (user_id, file_path) VALUES (%s, %s)",
        (user_id, file_path),
        commit=True
    )
    logger.info(f"Dataset insertado en la base de datos con ID: {data_id}")
    return data_id

def check_cleaned_dataset(file_name):
    """
    Función para comprobar si existe la versión 'cleaned' de un dataset.
    """
    base_file_name = file_name.rsplit('.', 1)[0] + "_cleaned%"
    result = execute_query(
        "SELECT data_id, file_path FROM datasets WHERE file_path LIKE %s",
        (base_file_name,),
        fetchone=True
    )
    if result:
        return result
    else:
        return None, None

def get_data_id(file_path):
    """
    Función para obtener el data_id de un dataset a partir del path del archivo.
    """
    result = execute_query(
        "SELECT data_id FROM datasets WHERE file_path = %s",
        (file_path,),
        fetchone=True
    )
    if result:
        return result[0]
    else:
        raise FileNotFoundError(f"Fichero no encontrado en el path: {file_path}")
