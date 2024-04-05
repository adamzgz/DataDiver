import uuid
from database import connect_to_database
import logging

# Inicializa el logging
logger = logging.getLogger(__name__)


# Función para generar un ID único para cada dataset
def generate_data_id() -> str:
    return str(uuid.uuid4())


# Función para obtener la ruta de un dataset a partir de su ID
def get_file_path(data_id):
    db = connect_to_database()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT file_path FROM data_files WHERE data_id = %s", (data_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise FileNotFoundError(f"Fichero no encontrado en el data id: {data_id}")
    finally:
        cursor.close()
        db.close()


# Función para insertar un nuevo dataset en la base de datos
def insert_file_mapping(user_id, data_id, file_path):
    db = connect_to_database()
    cursor = db.cursor()
   # Inserta el nuevo dataset en data_files
    cursor.execute(
        "INSERT INTO data_files (data_id, file_path) VALUES (%s, %s)",
        (data_id, file_path)
    )
    db.commit()
    # Ahora, asocia este dataset con el user_id en la tabla user_datasets
    cursor.execute(
        "INSERT INTO user_datasets (user_id, data_id) VALUES (%s, %s)",
        (user_id, data_id)
    )
    db.commit()
    cursor.close()
    db.close()
    logger.info(f"Dataset insertado en la base de datos con ID: {data_id}")

# Funcion para comprobar si existe la version cleaned del dataset

def check_cleaned_dataset(file_name):
    db = connect_to_database()
    cursor = db.cursor()
    # Obtiene el nombre base del archivo sin la extensión para buscar cualquier archivo _cleaned correspondiente
    base_file_name = file_name.rsplit('.', 1)[0] + "_cleaned"
    try:
        query = """
        SELECT data_id, file_path 
        FROM data_files 
        WHERE file_path LIKE %s
        """
        cursor.execute(query, (f"%{base_file_name}%",))
        result = cursor.fetchone()
        if result:
            # Devuelve el data_id y la ruta del dataset limpio si existe
            return result
        else:
            return None, None
    finally:
        cursor.close()
        db.close()

    
# Funcion para obtener el data-id de un dataset a partir del path del archivo

def get_data_id(file_path):
    db = connect_to_database()
    cursor = db.cursor()
    try:
        # Obtiene el data_id del dataset a partir de su file_path
        cursor.execute("SELECT data_id FROM data_files WHERE file_path = %s", (file_path,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise FileNotFoundError(f"Fichero no encontrado en el path: {file_path}")
    finally:
        cursor.close()
        db.close()