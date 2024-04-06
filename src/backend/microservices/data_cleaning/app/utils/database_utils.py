from database import connect_to_database
import logging

# Inicializa el logging
logger = logging.getLogger(__name__)


# Función para obtener la ruta de un dataset a partir de su ID
def get_file_path(data_id):
    db = connect_to_database()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT file_path FROM datasets WHERE data_id = %s", (data_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise FileNotFoundError(f"Fichero no encontrado en el data id: {data_id}")
    finally:
        cursor.close()
        db.close()


def insert_dataset(user_id, file_path):
    db = connect_to_database()
    cursor = db.cursor()
    try:
        # Inserta el nuevo dataset en la tabla datasets
        cursor.execute(
            "INSERT INTO datasets (user_id, file_path) VALUES (%s, %s)",
            (user_id, file_path)
        )
        db.commit()
        data_id = cursor.lastrowid  # Obtiene el data_id generado automáticamente por MySQL
        logger.info(f"Dataset insertado en la base de datos con ID: {data_id}")
        return data_id
    finally:
        cursor.close()
        db.close()

# Funcion para comprobar si existe la version cleaned del dataset

def check_cleaned_dataset(file_name):
    db = connect_to_database()
    cursor = db.cursor()
    # Obtiene el nombre base del archivo sin la extensión para buscar cualquier archivo _cleaned correspondiente
    base_file_name = file_name.rsplit('.', 1)[0] + "_cleaned"
    try:
        query = """
        SELECT data_id, file_path 
        FROM datasets 
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
        cursor.execute("SELECT data_id FROM datasets WHERE file_path = %s", (file_path,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise FileNotFoundError(f"Fichero no encontrado en el path: {file_path}")
    finally:
        cursor.close()
        db.close()

