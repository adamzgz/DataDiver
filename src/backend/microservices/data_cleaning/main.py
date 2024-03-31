from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os
import load_dataset as ld
import data_cleaning_functions as dcf
from typing import Optional, List, Dict
import numpy as np
import logging
import pandas as pd

# Inicializa el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Estructura para mantener el estado de los datasets en memoria
datasets_state = {}

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

app = FastAPI()


@app.post("/apply_cleaning")
async def apply_cleaning_operation(request: CleaningRequest):
    global ultimo_estado # Accede al estado global

    options = request.dict(exclude={'file_name', 'deshacer'})

    # Definir la ruta de almacenamiento y comprobar si el archivo existe
    storage_path = "/files"
    file_location = os.path.join(storage_path, request.file_name)

    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    try:
        df = await ld.load_data(file_location)
        result = dcf.data_cleaning(df, options)
        logger.info(f"Funcion Datacleaning completa, enviando resultado fuera de la API, Dataset ID: {request.file_name}")

        # Maneja diferentes tipos de resultados
        if isinstance(result, pd.DataFrame):
            # Si el resultado es un DataFrame, se convierte a un formato específico (por ejemplo, JSON)
            result = result.to_json(orient="records")
            logger.info("DataFrame convertido a JSON")

        elif isinstance(result, np.int64) or isinstance(result, np.float64):
            # Convierte np.int64 o np.float64 a tipos nativos de Python

            result = result.item()  # Otra opción es result = int(result) si sabes que es siempre entero
            logger.info("Número Numpy convertido a tipo nativo")
            # Puedes agregar más condiciones según sea necesario para otros tipos de datos

        return {"message": "Operaciones aplicadas con éxito", "result": result}

   
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
 