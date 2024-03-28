from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os
import load_dataset as ld
import data_cleaning_functions as dcf
from typing import Optional, List, Dict
import numpy as np

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

app = FastAPI()

@app.post("/apply_cleaning")
async def apply_cleaning_operation(request: CleaningRequest):
    options = request.dict(exclude={'file_name'})

    # Definir la ruta de almacenamiento y comprobar si el archivo existe
    storage_path = "/files"
    file_location = os.path.join(storage_path, request.file_name)

    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    try:
        df = await ld.load_data(file_location)
        result = dcf.data_cleaning(df, options)
        if isinstance(result, np.int64):
            result = int(result)  # Convierte np.int64 a int nativo de Python
        return {"message": "Operaciones aplicadas con éxito", "result": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
