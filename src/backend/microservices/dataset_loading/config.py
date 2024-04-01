import os
from dotenv import load_dotenv

# Carga las variables de entorno al inicio del programa
load_dotenv()

# Accede a las variables de entorno y las asigna
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")