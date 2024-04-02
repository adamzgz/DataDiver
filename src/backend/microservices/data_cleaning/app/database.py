import mysql.connector
from config import DB_HOST, DB_USER, DB_PASS, DB_NAME

# Función para conectar a la base de datos
def connect_to_database():

    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )