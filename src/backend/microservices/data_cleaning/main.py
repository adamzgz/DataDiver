from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os
import load_dataset as ld
import data_cleaning_functions as dcf
from typing import Optional, List, Dict
import numpy as np
import logging
import pandas as pd

from dotenv import load_dotenv
import aux_functions as af


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


# Endpoints

@app.post("/apply_cleaning")
async def apply_cleaning_operation(request: CleaningRequest):
    global ultimo_estado # Accede al estado global

    options = request.dict(exclude={'file_name', 'deshacer'})

    logger.info(f"Recibida petición para aplicar operaciones de limpieza de datos al dataset {request.file_name}")
    logger.info(f"Obteniendo dataset con ID: {request.file_name}")

    try:
        file_location = af.get_file_path(request.file_name)
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

            data_id = af.generate_data_id()
            af.insert_file_mapping(data_id, file_path)
            logger.info(f"Dataset limpio insertado en la base de datos con ID: {data_id}")
            return {"message": message, "data_id": data_id}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return {data_id, message}
    
 