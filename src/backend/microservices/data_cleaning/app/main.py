from fastapi import FastAPI, HTTPException

import backend.microservices.data_cleaning.app.utils.dataset_utils as ld
import utils.data_cleaning_functions as dcf
import numpy as np
import utils.database_utils as du
from logging_config import setup_logging
from pydantic import BaseModel
from typing import Optional, List, Dict
from utils.undo_functions import detect_differences, store_differences
from datetime import datetime


class CleaningRequest(BaseModel):
    user_id: int  
    data_id: int
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


# Inicializa el logging
logger = setup_logging()

# Inicializa la aplicación FastAPI
app = FastAPI()


# Endpoints

@app.post("/apply_cleaning/")
async def apply_cleaning_operation(request: CleaningRequest):
    # Paso 1: Obtener la ruta del dataset y cargarlo
    try:
        file_location = du.get_file_path(request.data_id)
        df = await ld.load_data(file_location)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail="Dataset no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Paso 2: Aplicar operaciones de limpieza
    try:
        options = request.dict(exclude_unset=True)
        df_original = df.copy()
        df_cleaned, message = dcf.data_cleaning(df, options)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Paso 3: Detectar diferencias y almacenar el backup
    differences = detect_differences(df_original, df_cleaned)
    if differences:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Formato de fecha y hora
        differences_file_name = f"backups/{request.user_id}/differences_{request.data_id}_{timestamp}.json"
        store_differences(differences, differences_file_name)
    

    # Paso 4: Guardar el dataset limpiado en el sistema de archivos
    cleaned_file_path = ld.save_dataset_cleaned(df_cleaned, file_location, cleaned_existe=False)
    
    # Paso 5: Insertar el registro del dataset limpiado en la base de datos
    try:
        # Suponiendo que `insert_dataset` devuelve el nuevo `data_id` para el dataset limpiado
        new_data_id = du.insert_dataset(request.user_id, cleaned_file_path)
        return {"message": "Limpieza aplicada correctamente", "new_data_id": new_data_id}
    except Exception as e:
        logger.error(f"Error al almacenar el dataset limpiado: {e}")
        raise HTTPException(status_code=500, detail="Error al almacenar el dataset limpiado")