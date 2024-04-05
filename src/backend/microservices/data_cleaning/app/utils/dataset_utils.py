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
