from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
import shutil
import os
import redis
from io import BytesIO
import pandas as pd
import load_dataset as ld
import pyarrow as pa

# Lanza la api 
app = FastAPI()

# Conectar a Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

#Endpoint para subir un archivo y almacenarlo en el servidor

@app.post("/upload-dataset/{session_id}")
async def upload_dataset(session_id: str, file: UploadFile = File(...)):
   
    # Definir la ruta de almacenamiento
    storage_path = f"/files/{session_id}"
    file_location = f"{storage_path}/{file.filename}"
    
    # Verificar que el archivo sea un CSV o un Excel o un JSON
    if file.content_type in ["text/csv",
                            "application/vnd.ms-excel",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            "application/json"]:
        try:
        
            # Guardar archivo en el almacenamiento
            with open(file_location, "wb+") as file_object:
                shutil.copyfileobj(file.file, file_object)
            
            # Carga de un DataFrame desde un archivo
            df = ld(file)

            # Serializar el DataFrame para almacenamiento en Redis
            context = pa.default_serialization_context()

            r.set("key", context.serialize(df).to_buffer().to_pybytes())
            context.deserialize(r.get("key"))

           # Lugar para la lógica de notificación al servicio de destino
            
            # Por ahora, solo devolvemos la ruta del archivo
            return {"location": file_location}
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Formato de archivo no soportado.")




        



    


