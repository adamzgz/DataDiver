import uuid
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASS, DB_NAME

# -----------------------------#
# Funciones auxiliares
# -----------------------------#

# Función para generar un ID único para cada dataset
def generate_data_id() -> str:
    return str(uuid.uuid4())

# Función para conectar a la base de datos
def connect_to_database():

    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

# Función para insertar un nuevo dataset en la base de datos
def insert_file_mapping(data_id, file_path):
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO data_files (data_id, file_path) VALUES (%s, %s)",
        (data_id, file_path)
    )
    db.commit()
    cursor.close()
    db.close()

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