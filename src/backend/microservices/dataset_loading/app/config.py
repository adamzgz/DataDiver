import os
from dotenv import load_dotenv

# Carga las variables de entorno al inicio del programa
load_dotenv('token.env')

# Accede a las variables de entorno y las asigna
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")


# Configuración de la aplicación
# --------------------------------
# configuracion de la ruta base para el almacenamiento de archivos
FILE_STORAGE_PATH = "/files"  # Ruta base para el almacenamiento de archivos

# configuracion de los tipos de archivos permitidos
ALLOWED_FILE_TYPES = ["text/csv", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/json"]  # Tipos de archivos permitidos
