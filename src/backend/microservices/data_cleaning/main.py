from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os
import load_dataset as ld
import data_cleaning_functions as dcf
from typing import Optional, List, Dict
import numpy as np
import logging
import pandas as pd
import uuid
import mysql.connector
from dotenv import load_dotenv


# Inicializa el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CleaningRequest(BaseModel):
    file_name: str
    check_duplicates: Optional[bool] = False
    remove_duplicates: Optional[bool] = False
    count_missing_values: Optional[bool] = False
    treat_missing_values: Optional[str] = None
    constant_value: Optional[float] = None
    outliers: Optional[str] = None
    normalization: Optional[str] = None
    encoding: Optional[str] = None
    drop_columns: Optional[List[str]] = None
    show_info: Optional[bool] = False
    change_data_type: Optional[Dict[str, str]] = None
    string_operations: Optional[str] = None
    regex_pattern: Optional[str] = None
    regex_replacement: Optional[str] = None
    deshacer: Optional[bool] = False

# Inicializa la aplicación FastAPI
app = FastAPI()

# Carga las variables de entorno desde `.env`
load_dotenv()

# Accede a las variables de entorno
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

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

# Endpoints

@app.post("/apply_cleaning")
async def apply_cleaning_operation(request: CleaningRequest):
    global ultimo_estado # Accede al estado global

    options = request.dict(exclude={'file_name', 'deshacer'})

    logger.info(f"Recibida petición para aplicar operaciones de limpieza de datos al dataset {request.file_name}")
    logger.info(f"Obteniendo dataset con ID: {request.file_name}")

    try:
        file_location = get_file_path(request.file_name)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    try:
        df = await ld.load_data(file_location)
        file_path, message = dcf.data_cleaning(df, options)
        logger.info(f"Funcion Datacleaning completa, enviando resultado fuera de la API, Dataset ID: {request.file_name}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

    # Si el resultado es int64 o float64 se transforma a tipo nativo de Python (No deberia dar el caso: DEBUG)
    if isinstance(message, np.int64) or isinstance(message, np.float64):
        try:
            logger.info("Número Numpy detectado, convirtiendo a tipo nativo python")
            # Convierte np.int64 o np.float64 a tipos nativos de Python

            message = message.item()
            logger.info("Número Numpy convertido a tipo nativo")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # Si el file_path recibido es *_cleaned.csv, se inserta en la base de datos
        
    if file_path.endswith("_cleaned.csv"):
        try:

            data_id = generate_data_id()
            insert_file_mapping(data_id, file_path)
            logger.info(f"Dataset limpio insertado en la base de datos con ID: {data_id}")
            return {"message": message, "data_id": data_id}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return {data_id, message}
    
 